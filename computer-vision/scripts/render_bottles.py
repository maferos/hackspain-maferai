"""Render random bottle layouts on the bench, seen by the scene camera, with exact boxes

Builds a MuJoCo scene in the room of :mod:`labvision.scene` --- bench top at
z = 0.95 centred on (7, 2.5), the GoPro at (7, 0, 3) aimed at the bench --- with
the agrochemical bottle kit from ``assets/agrochemical-bottles`` standing on
it, and renders N frames of random layouts. Every frame comes with the exact
pixel box of each bottle, read off a segmentation render, its base position,
and the camera pose, so the detector and the size classifier can be scored
against the truth rather than against eyeballed labels.

The GLBs are converted once to binary STL (MuJoCo reads no glTF), rotated
from the kit's Y-up to MuJoCo's Z-up, and cached next to the output.

    python scripts/render_bottles.py                         # 40 frames, 1080p Linear
    python scripts/render_bottles.py --frames 100 --width 3840 --height 2160
    python scripts/render_bottles.py --lens narrow --seed 7

Output: ``<out>/frame_0000.png`` ... and ``<out>/gt.json``.
"""

import argparse
import json
import sys
from pathlib import Path

import cv2
import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision.scene import (  # noqa: E402
    CAMERA_POSITION,
    CAMERA_TARGET,
    TABLE_CENTRE,
    TABLE_TOP_Z,
    VESSELS,
    gopro_intrinsics,
)

REPO = Path(__file__).resolve().parents[2]
KIT = REPO / "assets" / "agrochemical-bottles" / "glb"
GLB_NAMES = {
    "bottle_100ml": ("bottle_100ml_hdpe_white", "cap_100ml_pp_white"),
    "bottle_250ml": ("bottle_250ml_hdpe_white", "cap_250ml_pp_white"),
    "bottle_500ml": ("bottle_500ml_hdpe_white", "cap_500ml_pp_white"),
    "bottle_1000ml": ("bottle_1l_hdpe_white", "cap_1l_pp_white"),
    "bottle_1000ml_wide": ("bottle_1l_wide_hdpe_white", "cap_1l_wide_pp_white"),
    "bottle_2000ml": ("bottle_2l_hdpe_white", "cap_2l_pp_white"),
}
TABLE_SIZE_M = (6.0, 1.5)
"""Bench top, the minihannover worktop from ``simulation/assets``. Its far ends
are 4.4 m from the camera against 3.2 m at the centre, which is the point."""
INSTANCES_PER_SIZE = 4
PARKED = (0.0, 0.0, -5.0)
"""Where unused bottle instances wait, under the floor and out of every view."""


def convert_meshes(mesh_dir: Path) -> dict[str, dict[str, float]]:
    """Convert the kit's GLBs to Z-up binary STL, once, and return their sizes"""
    import trimesh

    mesh_dir.mkdir(parents=True, exist_ok=True)
    y_up_to_z_up = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])
    info: dict[str, dict[str, float]] = {}
    for vessel, (bottle, cap) in GLB_NAMES.items():
        sizes = {}
        for part, name in (("bottle", bottle), ("cap", cap)):
            stl = mesh_dir / f"{name}.stl"
            scene = trimesh.load(KIT / f"{name}.glb", force="scene")
            mesh = (
                scene.to_geometry()
                if hasattr(scene, "to_geometry")
                else scene.dump(True)
            )
            mesh.apply_transform(y_up_to_z_up)
            lo, hi = mesh.bounds
            mesh.apply_translation([-(lo[0] + hi[0]) / 2, -(lo[1] + hi[1]) / 2, -lo[2]])
            if not stl.exists():
                mesh.export(stl)
            lo, hi = mesh.bounds
            sizes[f"{part}_height"] = float(hi[2] - lo[2])
            sizes[f"{part}_diameter"] = float(max(hi[0] - lo[0], hi[1] - lo[1]))
        info[vessel] = sizes
    return info


def look_at_xyaxes(position, target) -> str:
    """MuJoCo ``xyaxes`` for a camera at position looking at target, Z up"""
    forward = np.asarray(target, float) - np.asarray(position, float)
    forward /= np.linalg.norm(forward)
    right = np.cross(forward, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)
    return " ".join(f"{v:.6f}" for v in (*right, *up))


def build_xml(mesh_dir: Path, sizes: dict, width: int, height: int, fovy: float) -> str:
    """Return the MJCF of the room, the bench, the camera and parked bottle instances"""
    assets = [
        '<texture type="skybox" builtin="gradient" rgb1="0.78 0.80 0.84" '
        'rgb2="0.55 0.58 0.64" width="256" height="256"/>',
        '<texture name="checker" type="2d" builtin="checker" rgb1="0.82 0.82 0.80" '
        'rgb2="0.68 0.68 0.66" width="256" height="256"/>',
        '<material name="floor" texture="checker" texrepeat="24 24" '
        'reflectance="0.05"/>',
        '<material name="bench" rgba="0.52 0.42 0.33 1" specular="0.2" '
        'shininess="0.3"/>',
        '<material name="hdpe" rgba="0.93 0.93 0.90 1" specular="0.35" '
        'shininess="0.5"/>',
        '<material name="pp" rgba="0.96 0.96 0.94 1" specular="0.25" shininess="0.4"/>',
    ]
    bodies = []
    parked = " ".join(str(v) for v in PARKED)
    for vessel, (bottle, cap) in GLB_NAMES.items():
        assets.append(f'<mesh name="{vessel}" file="{bottle}.stl"/>')
        assets.append(f'<mesh name="{vessel}_cap" file="{cap}.stl"/>')
        cap_z = sizes[vessel]["bottle_height"] - sizes[vessel]["cap_height"] + 0.001
        for i in range(INSTANCES_PER_SIZE):
            bodies.append(
                f'<body name="{vessel}#{i}" mocap="true" pos="{parked}">'
                f'<geom type="mesh" mesh="{vessel}" material="hdpe"/>'
                f'<geom type="mesh" mesh="{vessel}_cap" material="pp" '
                f'pos="0 0 {cap_z:.4f}"/>'
                "</body>"
            )
    bx, by = TABLE_CENTRE
    hx, hy = TABLE_SIZE_M[0] / 2, TABLE_SIZE_M[1] / 2
    leg_h = (TABLE_TOP_Z - 0.04) / 2
    cam_pos = " ".join(str(v) for v in CAMERA_POSITION)
    cam_axes = look_at_xyaxes(CAMERA_POSITION, CAMERA_TARGET)
    world = [
        f'<light pos="{bx} {by} 2.9" dir="0 0 -1" diffuse="0.7 0.7 0.7" '
        'castshadow="true"/>',
        f'<light pos="{bx - 2} 0.5 2.8" dir="0.4 0.5 -1" diffuse="0.45 0.45 0.45" '
        'castshadow="false"/>',
        '<geom name="floor" type="plane" size="7 2.5 0.1" pos="7 2.5 0" '
        'material="floor"/>',
        f'<geom name="bench_top" type="box" size="{hx} {hy} 0.02" '
        f'pos="{bx} {by} {TABLE_TOP_Z - 0.02}" material="bench"/>',
        f'<geom name="bench_legs" type="box" size="{hx - 0.1} {hy - 0.1} {leg_h}" '
        f'pos="{bx} {by} {leg_h}" rgba="0.35 0.3 0.25 1"/>',
        f'<camera name="gopro" pos="{cam_pos}" xyaxes="{cam_axes}" fovy="{fovy:.4f}"/>',
        *bodies,
    ]
    return (
        '<mujoco model="bottles_on_bench">'
        f'<compiler meshdir="{mesh_dir.as_posix()}"/>'
        "<visual>"
        f'<global offwidth="{width}" offheight="{height}"/>'
        '<headlight ambient="0.35 0.35 0.35" diffuse="0.45 0.45 0.45" '
        'specular="0.1 0.1 0.1"/>'
        '<quality shadowsize="4096"/>'
        "</visual>"
        f"<asset>{''.join(assets)}</asset>"
        f"<worldbody>{''.join(world)}</worldbody>"
        "</mujoco>"
    )


def random_layout(
    rng, vessels: list[str], count: int
) -> list[tuple[str, float, float]]:
    """Place count bottles on the bench without overlaps; returns (vessel, x, y)"""
    bx, by = TABLE_CENTRE
    hx, hy = TABLE_SIZE_M[0] / 2 - 0.08, TABLE_SIZE_M[1] / 2 - 0.08
    placed: list[tuple[str, float, float]] = []
    tries = 0
    while len(placed) < count and tries < 500:
        tries += 1
        vessel = vessels[rng.integers(len(vessels))]
        x, y = bx + rng.uniform(-hx, hx), by + rng.uniform(-hy, hy)
        r = VESSELS[vessel].radius_m
        if all(
            np.hypot(x - px, y - py) > r + VESSELS[pv].radius_m + 0.03
            for pv, px, py in placed
        ):
            placed.append((vessel, x, y))
    return placed


def main() -> None:
    """Render the frames and write the ground truth"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--frames", type=int, default=40)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--lens", default="linear", choices=["linear", "narrow"])
    parser.add_argument("--bottles", default="6,12", help="min,max bottles per frame")
    parser.add_argument("--table", default="6,1.5", help="bench top in metres, x,y")
    parser.add_argument(
        "--include-wide", action="store_true", help="also use bottle_1000ml_wide"
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--out", default=None, help="default ../simulation/out/bottles_<w>x<h>"
    )
    args = parser.parse_args()
    global TABLE_SIZE_M
    TABLE_SIZE_M = tuple(float(v) for v in args.table.split(","))

    out = Path(
        args.out or REPO / "simulation" / "out" / f"bottles_{args.width}x{args.height}"
    )
    out.mkdir(parents=True, exist_ok=True)
    mesh_dir = REPO / "simulation" / "out" / "bottle_meshes"
    sizes = convert_meshes(mesh_dir)
    for vessel, s in sizes.items():
        spec = VESSELS[vessel]
        if (
            abs(s["bottle_height"] - spec.height_m) > 0.004
            or abs(s["bottle_diameter"] - spec.diameter_m) > 0.004
        ):
            print(
                f"warning: {vessel} mesh is {s['bottle_diameter']:.3f} x "
                f"{s['bottle_height']:.3f} m, scene.VESSELS says "
                f"{spec.diameter_m:.3f} x {spec.height_m:.3f}"
            )

    intrinsics = gopro_intrinsics(args.width, args.height, lens=args.lens)
    xml = build_xml(mesh_dir, sizes, args.width, args.height, intrinsics.fovy_deg)
    (out / "scene.xml").write_text(xml, encoding="utf-8")
    model = mujoco.MjModel.from_xml_string(xml)
    data = mujoco.MjData(model)
    cam_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "gopro")
    rgb = mujoco.Renderer(model, height=args.height, width=args.width)
    seg = mujoco.Renderer(model, height=args.height, width=args.width)
    seg.enable_segmentation_rendering()

    vessels = [v for v in VESSELS if args.include_wide or v != "bottle_1000ml_wide"]
    lo, hi = (int(v) for v in args.bottles.split(","))
    rng = np.random.default_rng(args.seed)
    body_of = {
        (v, i): mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, f"{v}#{i}")
        for v in VESSELS
        for i in range(INSTANCES_PER_SIZE)
    }
    frames = []
    for k in range(args.frames):
        data.mocap_pos[:] = PARKED
        layout = random_layout(rng, vessels, int(rng.integers(lo, hi + 1)))
        used: dict[str, int] = {}
        placed_bodies: list[tuple[int, str, float, float]] = []
        for vessel, x, y in layout:
            i = used.get(vessel, 0)
            if i >= INSTANCES_PER_SIZE:
                continue
            used[vessel] = i + 1
            body = body_of[(vessel, i)]
            data.mocap_pos[model.body_mocapid[body]] = (x, y, TABLE_TOP_Z)
            placed_bodies.append((body, vessel, x, y))
        mujoco.mj_forward(model, data)

        rgb.update_scene(data, camera=cam_id)
        image = rgb.render()
        seg.update_scene(data, camera=cam_id)
        labels = seg.render()[:, :, 0]
        geom_body = model.geom_bodyid
        bottles = []
        for body, vessel, x, y in placed_bodies:
            mask = np.zeros(labels.shape, bool)
            for g in np.flatnonzero(geom_body == body):
                mask |= labels == g
            pixels = int(mask.sum())
            if pixels == 0:
                continue
            vs, us = np.nonzero(mask)
            bottles.append(
                {
                    "vessel": vessel,
                    "xyxy": [
                        int(us.min()),
                        int(vs.min()),
                        int(us.max()) + 1,
                        int(vs.max()) + 1,
                    ],
                    "position": [round(x, 4), round(y, 4), TABLE_TOP_Z],
                    "pixels": pixels,
                }
            )
        name = f"frame_{k:04d}.png"
        cv2.imwrite(str(out / name), image[:, :, ::-1])
        frames.append({"file": name, "bottles": bottles})
        print(f"{name}: {len(bottles)} bottles", flush=True)

    gt = {
        "width": args.width,
        "height": args.height,
        "lens": args.lens,
        "fovy_deg": intrinsics.fovy_deg,
        "camera": {
            "pos": [float(v) for v in data.cam_xpos[cam_id]],
            "xmat": [float(v) for v in data.cam_xmat[cam_id]],
        },
        "table_size": TABLE_SIZE_M,
        "frames": frames,
    }
    (out / "gt.json").write_text(json.dumps(gt, indent=1), encoding="utf-8")
    total = sum(len(f["bottles"]) for f in frames)
    print(f"\n{len(frames)} frames, {total} bottles -> {out}")


if __name__ == "__main__":
    main()
