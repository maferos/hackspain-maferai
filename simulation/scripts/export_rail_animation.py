#!/usr/bin/env python3
"""Bake the existing rail demo into USD for synchronized Isaac Lab rendering.

MuJoCo resolves the source assets and trajectory; all final images are rendered
by Isaac Lab / Isaac Sim RTX. This exports animation, not a PhysX articulation.
"""
import argparse
import json
import math
import re
import sys
from pathlib import Path

import mujoco
import numpy as np
from mujoco.usd import exporter
from pxr import UsdGeom
from rail_usd_table import prepare_table

import rail_demo as demo
import rail_kinematics as rk


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--mode', choices=('sweep', 'visit', 'label'), default='sweep')
    parser.add_argument('--speed', type=float, default=0.6)
    parser.add_argument('--visits', type=int, default=6)
    parser.add_argument('--recording', type=Path, help='Completed record_view_scan.py output')
    parser.add_argument('--pattern', help='Shared viewer layout, p01 through p10')
    parser.add_argument('--fps', type=int, default=30, choices=(10, 15, 30))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    pattern_metadata = {}
    recorded = args.recording is not None
    if recorded:
        pattern_metadata = json.loads((args.recording / 'recording.json').read_text())
        if pattern_metadata['mujoco_version'] != mujoco.__version__:
            raise ValueError('Recording and exporter must use the same MuJoCo version')
        model = mujoco.MjModel.from_binary_path(str(args.recording / 'scene.mjb'))
        data = mujoco.MjData(model)
        rows = np.load(args.recording / 'trajectory.npz')['qpos']
        args.fps = pattern_metadata['fps']
        args.mode = 'scan'
        if rows.shape != (pattern_metadata['frames'], model.nq):
            raise ValueError('Recorded states do not match the saved model')
    else:
        if args.pattern:
            sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'view/backend'))
            from scene_patterns import build_pattern
            model, pattern_metadata = build_pattern(rk.SCENE, args.pattern)
            data = mujoco.MjData(model)
            mujoco.mj_forward(model, data)
        else:
            model, data = rk.load()
        rows = demo.trajectory(model, demo.waypoints(model, data, args.mode, args.visits), args.speed)
        rows = rows[::demo.FPS // args.fps]
        mujoco.mj_resetData(model, data)
    original_name = exporter.USDExporter._get_geom_name
    exporter.USDExporter._get_geom_name = lambda self, geom: re.sub(
        r'[^A-Za-z0-9_]', '_', original_name(self, geom))
    cameras = ['general', demo.resolve_camera(model, 'eih')]
    exp = exporter.USDExporter(
        model, width=1920, height=1080, max_geom=20000,
        output_directory='rail_usd', output_directory_root=str(args.out),
        camera_names=cameras, light_intensity=6000, verbose=False)
    for index, row in enumerate(rows):
        if recorded:
            data.qpos[:] = row
            mujoco.mj_forward(model, data)
        else:
            demo.apply(model, data, row, physics=False)
        exp.update_scene(data)
        if index % 60 == 0:
            print(f'Exported {index + 1}/{len(rows)} animation frames', flush=True)
    exp.stage.SetTimeCodesPerSecond(args.fps)
    exp.stage.SetFramesPerSecond(args.fps)
    exp.stage.SetStartTimeCode(0)
    # MuJoCo's exporter supplies poses but uses a generic lens. Preserve the
    # scene cameras' vertical FOV and our 16:9 output aspect ratio explicitly.
    for name in cameras:
        camera = UsdGeom.Camera(exp.stage.GetPrimAtPath(
            f'/World/Camera_Xform_{name}/Camera_{name}'))
        focal = 20.0
        aperture = 2 * focal * math.tan(math.radians(model.camera(name).fovy[0]) / 2)
        camera.GetFocalLengthAttr().Set(focal)
        camera.GetVerticalApertureAttr().Set(aperture)
        camera.GetHorizontalApertureAttr().Set(aperture * 1920 / 1080)
    exp.save_scene(filetype='usdc')
    # Finalize exporter-owned visibility samples before replacing its visuals.
    prepare_table(exp.stage)
    exp.stage.Export(str(args.out / f'rail_usd/frames/frame_{len(rows)}.usdc'))
    metadata = dict(pattern_metadata, mode=args.mode, fps=args.fps, frames=len(rows),
                    duration_seconds=len(rows)/args.fps, cameras=cameras,
                    animation=pattern_metadata.get('animation', 'Baked source rail trajectory; RTX rendering in Isaac Lab'),
                    usd=f'rail_usd/frames/frame_{len(rows)}.usdc')
    (args.out/'animation.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(json.dumps(metadata), flush=True)


if __name__ == '__main__':
    main()
