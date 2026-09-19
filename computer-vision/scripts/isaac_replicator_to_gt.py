r"""Turn Isaac Sim Replicator BasicWriter output into the fixed-camera benchmark's truth

The benchmark (``fixedcam_bench.py``) and the crop exporter
(``fixedcam_crops.py``) read one folder per split holding the frames and a
``gt.json`` in the format ``fixedcam_dataset.py`` writes from MuJoCo. This
script makes the same folder from what Replicator's ``BasicWriter`` leaves on
disk, so Isaac renders are scored, and trained on, with no other change:

    writer.initialize(output_dir=..., rgb=True, bounding_box_2d_tight=True,
                      bounding_box_2d_loose=True, camera_params=True)

Per frame ``N`` it reads ``rgb_N.png``, ``bounding_box_2d_tight_N.npy`` with
its ``_labels_N.json`` (and ``_prim_paths_N.json`` when present), the same for
``loose``, and ``camera_params_N.json``. File names are globbed, so any frame
padding works.

- The tight box is what is visible (``xyxy``); the loose box is the whole
  silhouette (``full_xyxy``); ``visible_frac`` is ``1 - occlusionRatio``.
  Tight and loose boxes are paired by prim path, else by order.
- A box is a sample bottle when its semantic class names one: a sample id
  (``SMP-0001``, ``PWD-0042``, looked up in the registry for kit and size),
  or a name holding ``amber`` / ``hdpe`` (or ``liquid`` / ``powder``) and a
  size such as ``50ml``. Every other class (balances, glassware) is dropped.
- ``camera_params`` gives the camera's pose and field of view, which the
  worktop filter needs. Replicator's view transform is world to camera for
  row vectors, in stage units; ``--metres-per-unit`` converts.
- Every bottle is marked ``where: bench`` unless its class or prim path says
  ``shelf``; the Isaac scene is expected to show the bench alone.

    python scripts/isaac_replicator_to_gt.py /path/to/replicator_out \\
        --split isaac_test --bench-centre -1.5 -0.4 --bench-half 3.0 1.0

Output: ``simulation/out/fixedcam/<split>/`` with the frames hard-linked (or
copied) as ``<split>_0000.png`` and ``gt.json``.
"""

import argparse
import json
import math
import os
import re
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision import registry  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "simulation" / "out" / "fixedcam"
SAMPLE_ID = re.compile(r"(SMP|PWD)-\d{4}")
SIZE_ML = re.compile(r"(\d+(?:\.\d+)?)\s*ml", re.IGNORECASE)


def frame_numbers(folder: Path) -> list[str]:
    """Return the frame numbers present, as the strings in the file names"""
    numbers = []
    for path in folder.glob("rgb_*.png"):
        numbers.append(path.stem.removeprefix("rgb_"))
    return sorted(numbers, key=lambda n: int(n) if n.isdigit() else n)


def read_boxes(folder: Path, kind: str, number: str) -> list[dict]:
    """Read one annotator's boxes for a frame, each with its label and prim path

    Args:
        folder: The BasicWriter output folder.
        kind: ``tight`` or ``loose``.
        number: The frame number as written in the file names.

    Returns:
        One dict per box: ``label``, ``prim``, ``box`` (x_min, y_min, x_max,
        y_max) and ``occlusion``.
    """
    stem = f"bounding_box_2d_{kind}"
    path = folder / f"{stem}_{number}.npy"
    if not path.exists():
        return []
    data = np.load(path)
    labels_path = folder / f"{stem}_labels_{number}.json"
    labels = json.loads(labels_path.read_text()) if labels_path.exists() else {}
    prims_path = folder / f"{stem}_prim_paths_{number}.json"
    prims = json.loads(prims_path.read_text()) if prims_path.exists() else []
    out = []
    for k, row in enumerate(data):
        entry = labels.get(str(int(row["semanticId"])), {})
        label = entry.get("class", "") if isinstance(entry, dict) else str(entry)
        names = data.dtype.names
        occlusion = float(row["occlusionRatio"]) if "occlusionRatio" in names else 0.0
        out.append(
            {
                "label": label,
                "prim": prims[k] if k < len(prims) else None,
                "box": [
                    float(row["x_min"]),
                    float(row["y_min"]),
                    float(row["x_max"]),
                    float(row["y_max"]),
                ],
                "occlusion": occlusion if math.isfinite(occlusion) else 0.0,
            }
        )
    return out


def bottle_of(label: str, prim: str | None, samples: dict) -> dict | None:
    """Return the kit and size a semantic label names, or None if not a bottle"""
    text = f"{label} {prim or ''}"
    match = SAMPLE_ID.search(text)
    if match and match.group(0) in samples:
        sample = samples[match.group(0)]
        return {
            "sample_id": sample.sample_id,
            "phase": sample.phase,
            "container_ml": sample.container_ml,
        }
    low = text.lower()
    if "amber" in low or "liquid" in low:
        phase = "liquid"
    elif "hdpe" in low or "powder" in low:
        phase = "powder"
    else:
        return None
    size = SIZE_ML.search(low)
    return {
        "sample_id": None,
        "phase": phase,
        "container_ml": float(size.group(1)) if size else 0.0,
    }


def camera_of(
    params: dict, width: int, height: int, metres_per_unit: float
) -> tuple[list[float], list[float], float]:
    """Return camera position, rotation (row-major, columns right/up/back), fovy

    Replicator's ``cameraViewTransform`` is a flattened 4 x 4 world-to-camera
    matrix for row vectors (USD's convention); its transpose acts on columns.
    The camera looks down its -Z axis with +Y up, as MuJoCo's does.
    """
    view = np.asarray(params["cameraViewTransform"], dtype=float).reshape(4, 4)
    if np.allclose(view[:3, 3], 0.0) and not np.allclose(view[3, :3], 0.0):
        view = view.T  # row-vector form: translation sits in the last row
    to_world = np.linalg.inv(view)
    rotation = to_world[:3, :3]
    position = to_world[:3, 3] * metres_per_unit
    focal = float(params["cameraFocalLength"])
    aperture = params["cameraAperture"]
    vertical = (
        float(aperture[1])
        if float(aperture[1]) > 0
        else float(aperture[0]) * height / width
    )
    fovy = math.degrees(2 * math.atan(vertical / 2 / focal))
    return position.tolist(), rotation.reshape(-1).tolist(), fovy


def link_or_copy(src: Path, dst: Path) -> None:
    """Hard-link a file, or copy it where links are not possible"""
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def convert(
    source: Path, out: Path, split: str, bench_centre: tuple[float, float],
    bench_half: tuple[float, float], worktop_z: float, metres_per_unit: float,
    inclusive_max: bool,
) -> dict:  # fmt: skip
    """Convert one BasicWriter folder and return the ``gt.json`` written"""
    rows = registry.build_registry(registry.default_samples())
    samples = {r.sample.sample_id: r.sample for r in rows}
    out.mkdir(parents=True, exist_ok=True)
    frames = []
    for k, number in enumerate(frame_numbers(source)):
        image_path = source / f"rgb_{number}.png"
        image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        if image is None:
            continue
        height, width = image.shape[:2]
        name = f"{split}_{k:04d}.png"
        if image.ndim == 3 and image.shape[2] == 4:
            cv2.imwrite(str(out / name), image[:, :, :3])  # drop alpha
        else:
            link_or_copy(image_path, out / name)
        tight = read_boxes(source, "tight", number)
        loose = read_boxes(source, "loose", number)
        loose_by_prim = {b["prim"]: b for b in loose if b["prim"]}
        pad = 1.0 if inclusive_max else 0.0
        bottles = []
        for i, t in enumerate(tight):
            kind = bottle_of(t["label"], t["prim"], samples)
            if kind is None:
                continue
            partner = loose_by_prim.get(t["prim"]) if t["prim"] else None
            if partner is None and i < len(loose):
                partner = loose[i]
            full = partner["box"] if partner else t["box"]
            box = [t["box"][0], t["box"][1], t["box"][2] + pad, t["box"][3] + pad]
            full = [full[0], full[1], full[2] + pad, full[3] + pad]
            text = f"{t['label']} {t['prim'] or ''}".lower()
            visible = max(0.0, min(1.0, 1.0 - t["occlusion"]))
            area = max(box[2] - box[0], 0) * max(box[3] - box[1], 0)
            bottles.append(
                {
                    **kind,
                    "where": "shelf" if "shelf" in text else "bench",
                    "xyxy": [round(v, 1) for v in box],
                    "full_xyxy": [round(v, 1) for v in full],
                    "pixels": int(area * visible),
                    "visible_frac": round(visible, 3),
                    "clipped": bool(
                        full[0] <= 0
                        or full[1] <= 0
                        or full[2] >= width
                        or full[3] >= height
                    ),  # fmt: skip
                    "prim": t["prim"],
                }
            )
        record = {
            "file": name,
            "set": split,
            "split": split,
            "scene": "isaac",
            "source": str(image_path),
            "width": width,
            "height": height,
            "bottles": bottles,
        }
        params_path = source / f"camera_params_{number}.json"
        if params_path.exists():
            params = json.loads(params_path.read_text())
            pos, xmat, fovy = camera_of(params, width, height, metres_per_unit)
            record.update(cam_pos=pos, cam_xmat=xmat, fovy_deg=fovy)
        frames.append(record)
    gt = {
        "scene": f"isaac:{source}",
        "split": split,
        "camera": "isaac",
        "bench_centre": list(bench_centre),
        "bench_half": list(bench_half),
        "worktop_z": worktop_z,
        "frames": frames,
    }
    (out / "gt.json").write_text(json.dumps(gt, indent=1), encoding="utf-8")
    return gt


def main() -> None:
    """Parse the command line and convert"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("source", type=Path, help="BasicWriter output folder")
    parser.add_argument("--split", default="isaac_test")
    parser.add_argument("--out", type=Path, default=None, help="default DATA/<split>")
    parser.add_argument("--bench-centre", type=float, nargs=2, default=(0.0, 0.0))
    parser.add_argument("--bench-half", type=float, nargs=2, default=(3.0, 0.75))
    parser.add_argument("--worktop-z", type=float, default=0.90)
    parser.add_argument("--metres-per-unit", type=float, default=1.0)
    parser.add_argument(
        "--exclusive-max",
        action="store_true",
        help="x_max/y_max are already one past the last pixel",
    )
    args = parser.parse_args()
    gt = convert(
        args.source, args.out or DATA / args.split, args.split,
        tuple(args.bench_centre), tuple(args.bench_half), args.worktop_z,
        args.metres_per_unit, not args.exclusive_max,
    )  # fmt: skip
    total = sum(len(f["bottles"]) for f in gt["frames"])
    target = args.out or DATA / args.split
    print(f"{len(gt['frames'])} frames, {total} bottles -> {target}")


if __name__ == "__main__":
    main()
