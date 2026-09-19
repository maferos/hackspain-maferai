"""Render labelled frames from the fixed room camera, for training and benchmarking

The fixed camera is the scene's ``general`` GoPro (Linear, 1920 x 1080, fovy
60.44), on the aisle wall 3 m up, looking down at the bench. From there a
10 ml amber bottle is about 8 x 15 px and a 2 L HDPE bottle about 43 x 71 px,
and the gantry above the bench holds 187 more sample bottles that look the
same. This script renders that view with the exact box of every sample bottle,
using :class:`render_perfumery.Lab` for the scene, the extra bottles and the
segmentation truth. The scene files are loaded as committed and never written;
everything below happens in memory.

Two scenes can be loaded:

``gantry``
    ``simulation/models/minihannover_scene.xml``: the 6 x 1.5 m bench under the
    shelving gantry, the main scene.
``open``
    ``simulation/models/minihannover_open_scene.xml``: the shelf-free variant
    with a 6 x 2 m desk centred at (-1.5, -0.4), same ``general`` camera. Used
    as the out-of-distribution test: a detector never sees it in training.

Splits, each rendered from its own seeds so no layout is shared:

``train`` / ``val``
    Gantry scene with domain randomisation: light intensity and colour, a
    worktop tint, and the camera moved by a few centimetres and degrees, as a
    real mount or an Isaac port of the scene would move it.
``test``
    Gantry scene as built: nominal light, nominal camera. The main benchmark.
``test_open``
    Open scene as built. Measures what survives a change of scene.
``test_shift``
    Gantry scene, nominal camera, strong light randomisation, and the frame
    degraded as a real camera would (blur, noise, JPEG, gamma). A proxy for
    the step to Isaac's renderer and to a real GoPro.

Bottles are laid out on free worktop by ray casts, sometimes spread out and
sometimes in a cluster where they hide each other. Every sample bottle in view
is truth, wherever it stands (bench, gantry shelf, room); each record says
``where``, and the benchmark scores the bench alone.

    python scripts/fixedcam_dataset.py --splits test --frames 150
    python scripts/fixedcam_dataset.py --splits train,val --frames 600,60

Output: ``<out>/<split>/<split>_0000.png``, ``..._cat.png`` (per-pixel
category map) and ``<out>/<split>/gt.json``, in the format of
``render_perfumery.py`` plus ``scene``, ``split``, ``seed`` and the
randomisation drawn for each frame.
"""

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import cv2
import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import render_perfumery as rp  # noqa: E402

from labvision import registry  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO / "simulation" / "out" / "fixedcam"
CAMERA = "general"
WIDTH, HEIGHT = 1920, 1080

EXTRA_PER_SIZE = 3
"""Extra bottles of every size of both kits added to the scene, on top of its
own 7 loose ones, so a layout can hold up to 37 bottles of any mix."""


@dataclass(frozen=True)
class Scene:
    """A scene file and where bottles may stand on its worktop

    Attributes:
        path: The MJCF scene, as committed.
        centre: Worktop centre (x, y) in metres.
        half: Worktop half length and half depth, metres.
        x_range: Worktop x a bottle may be placed at; clipped to what the
            fixed camera sees, so no render is wasted on bottles out of frame.
        y_ranges: Bands of worktop y a bottle may stand in, each with a weight.
    """

    path: Path
    centre: tuple[float, float]
    half: tuple[float, float]
    x_range: tuple[float, float]
    y_ranges: tuple[tuple[float, float, float], ...]


SCENES: dict[str, Scene] = {
    "gantry": Scene(
        REPO / "simulation" / "models" / "minihannover_scene.xml",
        centre=(0.0, 0.0),
        half=(3.0, 0.75),
        x_range=(-2.9, 2.3),
        # The aisle half (y < 0) is the working side the camera sees; the far
        # half is mostly behind the gantry, kept for occluded examples.
        y_ranges=((-0.72, -0.08, 0.75), (0.08, 0.72, 0.25)),
    ),
    "open": Scene(
        REPO / "simulation" / "models" / "minihannover_open_scene.xml",
        centre=(-1.5, -0.4),
        half=(3.0, 1.0),
        x_range=(-4.4, 1.4),
        y_ranges=((-1.35, 0.55, 1.0),),
    ),
}


@dataclass(frozen=True)
class Split:
    """How the frames of one split are drawn

    Attributes:
        scene: Key in :data:`SCENES`.
        seed: First seed; frame ``k`` uses ``seed + k``.
        light: Largest relative change of light intensity, 0 for nominal.
        tint: Chance of tinting the worktop.
        camera_jitter: Whether to move the camera off its mount.
        degrade: Whether to degrade the frame as a real camera would.
        frames: Default number of frames.
    """

    scene: str
    seed: int
    light: float = 0.0
    tint: float = 0.0
    camera_jitter: bool = False
    degrade: bool = False
    frames: int = 100


SPLITS: dict[str, Split] = {
    "train": Split("gantry", 100_000, light=0.45, tint=0.5, camera_jitter=True,
                   frames=600),
    "val": Split("gantry", 200_000, light=0.45, tint=0.5, camera_jitter=True,
                 frames=60),
    "test": Split("gantry", 300_000, frames=150),
    "test_open": Split("open", 400_000, frames=100),
    "test_shift": Split("gantry", 500_000, light=0.6, tint=0.7, degrade=True,
                        frames=100),
}  # fmt: skip


def extra_samples() -> tuple[str, ...]:
    """Pick :data:`EXTRA_PER_SIZE` sample ids of every bottle size of both kits

    Sample ids repeat ones already in the room; identity is the barcode's job.
    """
    rows = registry.build_registry(registry.default_samples())
    by_size: dict[tuple[str, float], list[str]] = {}
    for row in rows:
        key = (row.sample.phase, row.sample.container_ml)
        by_size.setdefault(key, []).append(row.sample.sample_id)
    picked = []
    for key in sorted(by_size):
        # Skip the first ids: the scene already places some of them by hand.
        picked.extend(sorted(by_size[key])[-EXTRA_PER_SIZE:])
    return tuple(picked)


def load_lab(scene: Scene) -> rp.Lab:
    """Build :class:`render_perfumery.Lab` on another scene file

    ``Lab`` reads the scene path, the extra bottles and the bench bounds from
    module globals of ``render_perfumery``; they are pointed at ``scene`` here
    rather than editing that shared script.
    """
    rp.SCENE = scene.path
    rp.EXTRA_SAMPLES = extra_samples()

    def where_is(position: np.ndarray) -> str:
        x, y, z = position
        dx, dy = x - scene.centre[0], y - scene.centre[1]
        if abs(dx) <= scene.half[0] and abs(dy) <= scene.half[1]:
            if abs(z - rp.WORKTOP_Z) < 0.02:
                return "bench"
            if z > rp.WORKTOP_Z + 0.2:
                return "shelf"
        return "room"

    rp.where_is = where_is
    return rp.Lab(WIDTH, HEIGHT)


class Randomiser:
    """Draw and undo the per-frame changes to lights, worktop and camera"""

    def __init__(self, lab: rp.Lab, camera: int) -> None:
        """Remember the nominal values so every frame starts from them"""
        m = lab.model
        self.lab = lab
        self.camera = camera
        self.light_diffuse = m.light_diffuse.copy()
        self.head_diffuse = m.vis.headlight.diffuse.copy()
        self.head_ambient = m.vis.headlight.ambient.copy()
        names = [
            mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_GEOM, g) or ""
            for g in range(m.ngeom)
        ]
        worktop = [g for g, n in enumerate(names) if n.startswith("room_worktop")]
        self.worktop_mats = sorted({int(m.geom_matid[g]) for g in worktop} - {-1})
        self.worktop_geoms = [g for g in worktop if m.geom_matid[g] < 0]
        self.mat_rgba = m.mat_rgba.copy()
        self.geom_rgba = m.geom_rgba.copy()
        self.cam_pos = m.cam_pos[camera].copy()
        self.cam_quat = m.cam_quat[camera].copy()

    def reset(self) -> None:
        """Put lights, worktop and camera back to the scene file's values"""
        m = self.lab.model
        m.light_diffuse[:] = self.light_diffuse
        m.vis.headlight.diffuse[:] = self.head_diffuse
        m.vis.headlight.ambient[:] = self.head_ambient
        m.mat_rgba[:] = self.mat_rgba
        m.geom_rgba[:] = self.geom_rgba
        m.cam_pos[self.camera] = self.cam_pos
        m.cam_quat[self.camera] = self.cam_quat

    def draw(self, rng: np.random.Generator, split: Split) -> dict:
        """Apply one random draw for ``split`` and return what was drawn"""
        self.reset()
        m = self.lab.model
        drawn: dict = {}
        if split.light > 0:
            scale = rng.uniform(1 - split.light, 1 + split.light)
            colour = np.clip(1 + rng.normal(0, 0.035, 3), 0.9, 1.1)
            m.light_diffuse[:] = np.clip(self.light_diffuse * scale * colour, 0, 1)
            head = rng.uniform(1 - split.light, 1 + split.light, 2)
            m.vis.headlight.diffuse[:] = np.clip(self.head_diffuse * head[0], 0, 1)
            m.vis.headlight.ambient[:] = np.clip(self.head_ambient * head[1], 0, 1)
            drawn["light"] = [round(float(scale), 3), *np.round(colour, 3).tolist()]
            drawn["headlight"] = np.round(head, 3).tolist()
        if split.tint > 0 and rng.random() < split.tint:
            hue = np.clip(1 + rng.normal(0, 0.02, 3), 0.95, 1.05)
            shade = rng.uniform(0.78, 1.0) * hue
            for mat in self.worktop_mats:
                m.mat_rgba[mat, :3] = np.clip(self.mat_rgba[mat, :3] * shade, 0, 1)
            for g in self.worktop_geoms:
                m.geom_rgba[g, :3] = np.clip(self.geom_rgba[g, :3] * shade, 0, 1)
            drawn["worktop_tint"] = np.round(shade, 3).tolist()
        if split.camera_jitter:
            shift = np.clip(rng.normal(0, 0.07, 3), -0.15, 0.15)
            axis = rng.normal(size=3)
            axis /= np.linalg.norm(axis)
            angle = math.radians(float(np.clip(rng.normal(0, 2.0), -5, 5)))
            turn = np.array([math.cos(angle / 2), *(math.sin(angle / 2) * axis)])
            m.cam_pos[self.camera] = self.cam_pos + shift
            m.cam_quat[self.camera] = rp.quat_mul(turn, self.cam_quat)
            drawn["camera_shift_m"] = np.round(shift, 3).tolist()
            drawn["camera_turn_deg"] = round(math.degrees(angle), 2)
        return drawn


def lay_out(
    lab: rp.Lab, rng: np.random.Generator, scene: Scene, count: int
) -> tuple[int, bool]:
    """Park every movable bottle, then stand ``count`` of them on free worktop

    With some chance the layout is a cluster: most bottles within about 15 cm
    of one point, so they hide each other the way a working area does.

    Returns:
        How many bottles were placed, and whether the layout is a cluster.
    """
    lab.park_all()
    movable = [s for s in lab.samples if s["movable"]]
    cluster = bool(rng.random() < 0.35)
    bands = np.array([b[2] for b in scene.y_ranges])
    band = scene.y_ranges[int(rng.choice(len(bands), p=bands / bands.sum()))]
    hub = (rng.uniform(*scene.x_range), rng.uniform(band[0], band[1]))
    placed = 0
    for index in rng.permutation(len(movable))[:count]:
        sample = movable[index]
        for _ in range(100):
            if cluster and rng.random() < 0.75:
                x, y = hub[0] + rng.normal(0, 0.15), hub[1] + rng.normal(0, 0.12)
            else:
                lo, hi, _ = scene.y_ranges[
                    int(rng.choice(len(bands), p=bands / bands.sum()))
                ]
                x, y = rng.uniform(*scene.x_range), rng.uniform(lo, hi)
            inside = scene.x_range[0] <= x <= scene.x_range[1] and any(
                lo <= y <= hi for lo, hi, _ in scene.y_ranges
            )
            if inside and lab.is_free(x, y, sample["radius"]):
                lab.place(sample, x, y, rp.WORKTOP_Z, rng.uniform(-np.pi, np.pi))
                placed += 1
                break
    return placed, cluster


def degrade(image: np.ndarray, rng: np.random.Generator) -> tuple[np.ndarray, dict]:
    """Degrade a clean render the way a real camera and its encoder would

    Gamma and contrast, a slight defocus blur, sensor noise and JPEG
    compression, each drawn at random. Works on uint8 images of any channel
    order.

    Returns:
        The degraded image and the parameters drawn.
    """
    drawn: dict = {}
    out = image.astype(np.float32) / 255.0
    gamma = rng.uniform(0.8, 1.25)
    contrast = rng.uniform(0.85, 1.1)
    out = np.clip((out**gamma - 0.5) * contrast + 0.5, 0, 1)
    drawn["gamma"] = round(float(gamma), 3)
    drawn["contrast"] = round(float(contrast), 3)
    out = (out * 255.0).astype(np.float32)
    if rng.random() < 0.7:
        sigma = rng.uniform(0.3, 1.2)
        out = cv2.GaussianBlur(out, (0, 0), sigma)
        drawn["blur_sigma"] = round(float(sigma), 2)
    if rng.random() < 0.8:
        noise = rng.uniform(1.0, 6.0)
        out = out + rng.normal(0, noise, out.shape).astype(np.float32)
        drawn["noise_sigma"] = round(float(noise), 2)
    out = np.clip(out, 0, 255).astype(np.uint8)
    if rng.random() < 0.8:
        quality = int(rng.integers(55, 96))
        ok, buffer = cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, quality])
        if ok:
            out = cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED)
            drawn["jpeg_quality"] = quality
    return out, drawn


def render_split(name: str, frames: int, out_root: Path) -> None:
    """Render ``frames`` frames of one split and write them with ``gt.json``"""
    split = SPLITS[name]
    scene = SCENES[split.scene]
    out = out_root / name
    out.mkdir(parents=True, exist_ok=True)
    lab = load_lab(scene)
    m = lab.model
    camera = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_CAMERA, CAMERA)
    randomiser = Randomiser(lab, camera)
    movable = sum(s["movable"] for s in lab.samples)
    print(f"[{name}] {scene.path.name}: {len(lab.samples)} samples, "
          f"{movable} movable", flush=True)  # fmt: skip
    records: list[dict] = []
    gt_path = out / "gt.json"
    started = time.perf_counter()
    for k in range(frames):
        seed = split.seed + k
        rng = np.random.default_rng(seed)
        drawn = randomiser.draw(rng, split)
        placed, cluster = lay_out(lab, rng, scene, int(rng.integers(8, 29)))
        mujoco.mj_kinematics(m, lab.data)
        rgb, bottles, categories = lab.render(camera, WIDTH, HEIGHT)
        bgr = rgb[:, :, ::-1]
        if split.degrade:
            bgr, drawn["degrade"] = degrade(np.ascontiguousarray(bgr), rng)
        stem = f"{name}_{k:04d}"
        cv2.imwrite(str(out / f"{stem}.png"), bgr)
        cv2.imwrite(str(out / f"{stem}_cat.png"), categories)
        records.append(
            {
                "file": f"{stem}.png",
                "categories": f"{stem}_cat.png",
                "set": name,
                "split": name,
                "scene": split.scene,
                "seed": seed,
                "camera": CAMERA,
                "width": WIDTH,
                "height": HEIGHT,
                "fovy_deg": round(float(m.cam_fovy[camera]), 3),
                "cam_pos": [round(float(v), 4) for v in lab.data.cam_xpos[camera]],
                "cam_xmat": [round(float(v), 6) for v in lab.data.cam_xmat[camera]],
                "placed": placed,
                "cluster": cluster,
                "randomisation": drawn,
                "bottles": bottles,
            }
        )
        bench = sum(b["where"] == "bench" for b in bottles)
        elapsed = time.perf_counter() - started
        print(
            f"[{name}] {k + 1}/{frames} {stem}: {placed} placed, {bench} on the "
            f"bench in view, {elapsed / (k + 1):.1f} s/frame",
            flush=True,
        )
        if (k + 1) % 25 == 0 or k + 1 == frames:
            write_gt(gt_path, scene, name, records)
    randomiser.reset()


def write_gt(path: Path, scene: Scene, split: str, records: list[dict]) -> None:
    """Write the split's ground truth, replacing any earlier partial file"""
    gt = {
        "scene": str(scene.path.relative_to(REPO)).replace("\\", "/"),
        "split": split,
        "camera": CAMERA,
        "bench_centre": list(scene.centre),
        "bench_half": list(scene.half),
        "worktop_z": rp.WORKTOP_Z,
        "frames": records,
    }
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(gt, indent=1), encoding="utf-8")
    tmp.replace(path)


def main() -> None:
    """Render the requested splits"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--splits", default="test", help=f"comma-separated, from {list(SPLITS)}"
    )
    parser.add_argument(
        "--frames",
        default=None,
        help="comma-separated frame counts, one per split; default per split",
    )
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    names = [s.strip() for s in args.splits.split(",") if s.strip()]
    unknown = [n for n in names if n not in SPLITS]
    if unknown:
        parser.error(f"unknown split(s) {unknown}; choose from {list(SPLITS)}")
    counts = (
        [int(c) for c in args.frames.split(",")]
        if args.frames
        else [SPLITS[n].frames for n in names]
    )
    if len(counts) != len(names):
        parser.error("--frames needs one count per split")
    for name, count in zip(names, counts, strict=True):
        render_split(name, count, args.out)


if __name__ == "__main__":
    main()
