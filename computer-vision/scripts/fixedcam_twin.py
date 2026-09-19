"""Render MuJoCo twins of Isaac frames of the populated open bench, and score both

Eloi's Isaac datasets (``simulation/renders/isaac/dataset_v1``, ``_v2``) render
the open MiniHannover desk as populated in commit 284a545: 407 containers on the
worktop, 187 of them catalogue samples and 220 ``reserve`` amber vials with blank
labels. Isaac tags only meshes whose path holds a sample id, so its COCO boxes
cover the 187 and leave the 220 unlabelled: scored naively, every box a detector
puts on a reserve vial would count as false.

This script builds the same scene in MuJoCo, from the scene files of that
commit, with the ``general`` camera set to Isaac's image size and field of
view, and:

``render``
    Renders the bench as built (nothing moved) under random light, like Isaac's
    v1/v2, with exact truth for all 407 containers. Output: the ``twin_mujoco``
    split for ``fixedcam_bench.py``.
``isaac``
    Converts Isaac's COCO for the ``general`` camera into the same truth format
    (``twin_isaac`` split): a labelled bottle keeps Isaac's tight box and
    ``visible_frac = 1 - occlusion``; every reserve vial is added from the MuJoCo
    twin as a bottle that is not required, so a box on it is ignored rather
    than false. The camera pose and field of view are the twin's.

Isaac's USD camera took MuJoCo's ``fovy`` as its horizontal field of view, so
the Isaac view is narrower than the MuJoCo scene's own camera; ``--fovy`` sets
the vertical field of view used here (the default is what that conversion
gives at 16:9, checked by overlaying the two renders).

    python scripts/fixedcam_twin.py render --scene-root <extracted simulation/>
    python scripts/fixedcam_twin.py isaac --coco <lab_dataset_v2> --twin twin_mujoco
"""

import argparse
import json
import math
import re
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import cv2
import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fixedcam_dataset as fd  # noqa: E402
import render_perfumery as rp  # noqa: E402

from labvision import registry  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "simulation" / "out" / "fixedcam"
WIDTH, HEIGHT = 1600, 900
MUJOCO_FOVY = 60.44
ISAAC_FOVY = math.degrees(
    2 * math.atan(math.tan(math.radians(MUJOCO_FOVY) / 2) * HEIGHT / WIDTH)
)
"""Vertical field of view of Isaac's ``general`` camera: MuJoCo's 60.44 degrees
read as horizontal, at 1600 x 900."""

STOCK_GEOM = re.compile(
    r"^room_stock_((?:SMP|PWD)-\d{4}|reserve_\d+)_(body|glass|cap|label|label_back)_0$"
)
"""A worktop container of the populated open desk: catalogue or reserve."""

OPEN_BENCH = fd.Scene(
    path=Path("models") / "minihannover_open_scene.xml",
    centre=(-1.5, -0.4),
    half=(3.0, 1.0),
    x_range=(-4.4, 1.4),
    y_ranges=((-1.35, 0.55, 1.0),),
)


def reserve_rows(scene_root: Path) -> list:
    """Registry-like rows for the reserve vials, sized from the population file"""
    population = json.loads(
        (scene_root / "assets" / "minihannover_open" / "population.json").read_text()
    )
    rows = []
    for c in population["containers"]:
        if c["sample_id"] is None:
            sample = SimpleNamespace(
                sample_id=f"reserve_{c['extra_id']:03d}",
                phase=c["phase"],
                container_ml=float(c["container_ml"]),
            )
            rows.append(SimpleNamespace(sample=sample))
    return rows


def load_twin_lab(scene_root: Path, fovy: float) -> rp.Lab:
    """Build ``render_perfumery.Lab`` on the populated open scene, stock included

    ``Lab`` finds gantry bottles by geom name and looks sample ids up in the
    registry; both are pointed, for the length of the build, at the open desk's
    ``stock_`` geoms and at a registry that also knows the reserve vials.
    """
    scene = fd.Scene(scene_root / OPEN_BENCH.path, OPEN_BENCH.centre, OPEN_BENCH.half,
                     OPEN_BENCH.x_range, OPEN_BENCH.y_ranges)  # fmt: skip
    rows = registry.build_registry(registry.default_samples()) + reserve_rows(
        scene_root
    )
    saved = (rp.SHELF_GEOM, rp.registry.build_registry)
    rp.SHELF_GEOM = STOCK_GEOM
    rp.registry.build_registry = lambda _samples: rows
    try:
        rp.SCENE = scene.path
        rp.EXTRA_SAMPLES = ()

        def where_is(position: np.ndarray) -> str:
            x, y, z = position
            dx, dy = x - scene.centre[0], y - scene.centre[1]
            inside = abs(dx) <= scene.half[0] and abs(dy) <= scene.half[1]
            return "bench" if inside and abs(z - rp.WORKTOP_Z) < 0.03 else "room"

        rp.where_is = where_is
        lab = rp.Lab(WIDTH, HEIGHT)
    finally:
        rp.SHELF_GEOM, rp.registry.build_registry = saved
    camera = lab.cameras["general"]
    lab.model.cam_fovy[camera] = fovy
    mujoco.mj_kinematics(lab.model, lab.data)
    return lab


def render(args: argparse.Namespace) -> None:
    """Render the twin split: the bench as built, light drawn per frame"""
    lab = load_twin_lab(args.scene_root, args.fovy)
    m = lab.model
    camera = lab.cameras["general"]
    split = fd.Split("open", args.seed, light=0.45)
    randomiser = fd.Randomiser(lab, camera)
    out = DATA / args.split
    out.mkdir(parents=True, exist_ok=True)
    stock = sum(1 for s in lab.samples if s["anchor_geom"] is not None)
    print(f"{len(lab.samples)} samples, {stock} worktop stock; fovy {args.fovy:.2f}")
    records = []
    started = time.perf_counter()
    for k in range(args.frames):
        rng = np.random.default_rng(args.seed + k)
        drawn = randomiser.draw(rng, split) if k else {}
        lab.reset()
        rgb, bottles, categories = lab.render(camera, WIDTH, HEIGHT)
        stem = f"{args.split}_{k:04d}"
        cv2.imwrite(str(out / f"{stem}.png"), rgb[:, :, ::-1])
        cv2.imwrite(str(out / f"{stem}_cat.png"), categories)
        records.append({
            "file": f"{stem}.png", "categories": f"{stem}_cat.png",
            "set": args.split, "split": args.split, "scene": "open_populated",
            "seed": args.seed + k, "camera": "general", "width": WIDTH,
            "height": HEIGHT, "fovy_deg": round(float(m.cam_fovy[camera]), 3),
            "cam_pos": [round(float(v), 4) for v in lab.data.cam_xpos[camera]],
            "cam_xmat": [round(float(v), 6) for v in lab.data.cam_xmat[camera]],
            "randomisation": drawn, "bottles": bottles,
        })  # fmt: skip
        required = sum(
            b["where"] == "bench" and b["visible_frac"] >= 0.5 and not b["clipped"]
            for b in bottles
        )
        elapsed = time.perf_counter() - started
        print(f"{stem}: {len(bottles)} bottles in view, {required} required, "
              f"{elapsed / (k + 1):.1f} s/frame", flush=True)  # fmt: skip
    randomiser.reset()
    gt = {
        "scene": f"{args.scene_root.as_posix()}/{OPEN_BENCH.path.as_posix()}",
        "split": args.split,
        "camera": "general",
        "bench_centre": list(OPEN_BENCH.centre),
        "bench_half": list(OPEN_BENCH.half),
        "worktop_z": rp.WORKTOP_Z,
        "frames": records,
    }
    (out / "gt.json").write_text(json.dumps(gt, indent=1), encoding="utf-8")


def isaac(args: argparse.Namespace) -> None:
    """Convert Isaac's COCO for the general camera into the twin_isaac split

    Without ``annotations/instances.json`` the split is written with the frames
    and no truth, so the detectors can run while the annotations are fetched;
    running this again once they are there fills the truth in, and the cached
    boxes stay valid because the frame files are not rewritten.
    """
    annotations = args.coco / "annotations" / "instances.json"
    if annotations.exists():
        coco = json.loads(annotations.read_text())
    else:
        print(f"no {annotations}: writing the frames with no truth")
        images = sorted((args.coco / "images" / "general").glob("rgb_*.png"))
        coco = {
            "categories": [],
            "annotations": [],
            "images": [
                {"id": k, "file_name": f"images/general/{path.name}",
                 "width": WIDTH, "height": HEIGHT}
                for k, path in enumerate(images)
            ],
        }  # fmt: skip
    names = {c["id"]: c["name"].replace("_", "-") for c in coco["categories"]}
    rows = registry.build_registry(registry.default_samples())
    samples = {r.sample.sample_id: r.sample for r in rows}
    twin = json.loads((DATA / args.twin / "gt.json").read_text())
    reference = twin["frames"][0]
    twin_by_id = {b["sample_id"]: b for b in reference["bottles"]}
    reserves = [b for b in reference["bottles"]
                if str(b["sample_id"]).startswith("reserve_")]  # fmt: skip
    by_image: dict[int, list] = {}
    for a in coco["annotations"]:
        by_image.setdefault(a["image_id"], []).append(a)
    out = DATA / args.split
    out.mkdir(parents=True, exist_ok=True)
    frames = []
    for image in sorted(coco["images"], key=lambda i: i["file_name"]):
        if not image["file_name"].startswith("images/general/"):
            continue
        source = args.coco / image["file_name"]
        if not source.exists():
            continue
        name = f"{args.split}_{Path(image['file_name']).stem}.png"
        target = out / name
        if not target.exists():
            target.write_bytes(source.read_bytes())
        bottles = []
        for a in by_image.get(image["id"], []):
            sample_id = names[a["category_id"]]
            sample = samples.get(sample_id)
            if sample is None:
                continue
            x, y, w, h = a["bbox"]
            box = [x, y, x + w, y + h]
            partner = twin_by_id.get(sample_id)
            bottles.append({
                "sample_id": sample_id, "phase": sample.phase,
                "container_ml": sample.container_ml,
                "where": partner["where"] if partner else "bench",
                "xyxy": box, "full_xyxy": box,
                "pixels": int(w * h * (1 - a.get("occlusion", 0.0))),
                "visible_frac": round(1.0 - float(a.get("occlusion", 0.0)), 3),
                "clipped": bool(x <= 0 or y <= 0 or x + w >= image["width"] - 1
                                or y + h >= image["height"] - 1),
                "source": "isaac",
            })  # fmt: skip
        for r in reserves:
            # Unlabelled in Isaac: a box on one is neither a hit nor a miss.
            bottles.append({**r, "where": "unlabelled", "source": "mujoco_twin"})
        frames.append({
            "file": name, "set": args.split, "split": args.split,
            "scene": "open_populated", "camera": "general",
            "width": image["width"], "height": image["height"],
            "fovy_deg": reference["fovy_deg"], "cam_pos": reference["cam_pos"],
            "cam_xmat": reference["cam_xmat"], "bottles": bottles,
        })  # fmt: skip
    gt = {k: v for k, v in twin.items() if k != "frames"}
    gt.update(scene=f"isaac:{args.coco.name}", split=args.split, frames=frames)
    (out / "gt.json").write_text(json.dumps(gt, indent=1), encoding="utf-8")
    labelled = sum(len(f["bottles"]) - len(reserves) for f in frames)
    print(
        f"{len(frames)} Isaac frames, {labelled} labelled boxes, "
        f"{len(reserves)} reserve vials ignored per frame -> {out}"
    )


def main() -> None:
    """Parse the command line"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p_render = sub.add_parser("render")
    p_render.add_argument(
        "--scene-root",
        type=Path,
        required=True,
        help="a simulation/ folder holding models/ and assets/",
    )
    p_render.add_argument("--frames", type=int, default=20)
    p_render.add_argument("--fovy", type=float, default=ISAAC_FOVY)
    p_render.add_argument("--seed", type=int, default=600_000)
    p_render.add_argument("--split", default="twin_mujoco")
    p_isaac = sub.add_parser("isaac")
    p_isaac.add_argument("--coco", type=Path, required=True)
    p_isaac.add_argument("--twin", default="twin_mujoco")
    p_isaac.add_argument("--split", default="twin_isaac")
    args = parser.parse_args()
    render(args) if args.command == "render" else isaac(args)


if __name__ == "__main__":
    main()
