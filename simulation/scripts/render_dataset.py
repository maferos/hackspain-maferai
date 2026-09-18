#!/usr/bin/env python3
"""Render a batch of RGB frames from a MuJoCo scene, offscreen.

The point is to unblock the computer-vision team fast: it dumps N PNGs of a
lab scene taken from randomised camera poses (a light domain-randomisation),
plus a `frames.json` recording each pose. Runs on macOS and Linux — plain
MuJoCo offscreen rendering, no cloud and no AutoBio plugin needed.

    python scripts/render_dataset.py                      # 64 frames of the minihannover bench
    python scripts/render_dataset.py -n 200 --width 1024 --height 768
    python scripts/render_dataset.py --scene models/hello.xml --out out/hello

Output goes to `out/<name>/` (git-ignored): frame_0000.png ... plus frames.json.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import mujoco
import numpy as np
from PIL import Image

SIM_DIR = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--scene", default="models/minihannover_scene.xml",
                   help="MJCF scene, relative to simulation/ (default: %(default)s)")
    p.add_argument("--out", default=None,
                   help="Output dir, relative to simulation/ (default: out/<scene stem>)")
    p.add_argument("-n", "--num", type=int, default=64, help="Number of frames (default: %(default)s)")
    p.add_argument("--width", type=int, default=640, help="Frame width (default: %(default)s)")
    p.add_argument("--height", type=int, default=480, help="Frame height (default: %(default)s)")
    p.add_argument("--seed", type=int, default=0, help="RNG seed for reproducible poses (default: %(default)s)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)

    scene_path = (SIM_DIR / args.scene).resolve()
    if not scene_path.exists():
        raise SystemExit(f"scene not found: {scene_path}")
    out_dir = SIM_DIR / (args.out or f"out/{scene_path.stem}")
    out_dir.mkdir(parents=True, exist_ok=True)

    model = mujoco.MjModel.from_xml_path(str(scene_path))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    # Aim the free camera at the scene centre; vary it around a sensible orbit.
    center = model.stat.center.copy()
    extent = float(model.stat.extent)

    renderer = mujoco.Renderer(model, height=args.height, width=args.width)
    cam = mujoco.MjvCamera()
    cam.type = mujoco.mjtCamera.mjCAMERA_FREE

    manifest = []
    for i in range(args.num):
        lookat = center + rng.uniform(-0.15, 0.15, size=3) * extent
        azimuth = float(rng.uniform(0.0, 360.0))
        elevation = float(rng.uniform(-55.0, -10.0))
        distance = float(rng.uniform(0.55, 1.1) * extent)

        cam.lookat[:] = lookat
        cam.azimuth = azimuth
        cam.elevation = elevation
        cam.distance = distance

        renderer.update_scene(data, camera=cam)
        frame = renderer.render()  # (H, W, 3) uint8

        name = f"frame_{i:04d}.png"
        Image.fromarray(frame).save(out_dir / name)
        manifest.append({
            "file": name,
            "azimuth": azimuth,
            "elevation": elevation,
            "distance": distance,
            "lookat": lookat.tolist(),
        })

    (out_dir / "frames.json").write_text(json.dumps({
        "scene": args.scene,
        "width": args.width,
        "height": args.height,
        "seed": args.seed,
        "frames": manifest,
    }, indent=2))

    print(f"Wrote {args.num} frames ({args.width}x{args.height}) to {out_dir}")
    print(f"Camera poses recorded in {out_dir / 'frames.json'}")


if __name__ == "__main__":
    main()
