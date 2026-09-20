#!/usr/bin/env python3
"""Open the double rail in MuJoCo's native viewer with XYZ actuator controls.

macOS: simulation/.venv/bin/mjpython simulation/scripts/view_gantry.py
Other platforms: use the environment's python instead of mjpython.
"""
import argparse
import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer

from generate_gantry_scene import build_scene


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pattern', default='p01', choices=('p01', 'p02', 'p03', 'p04'))
    args = parser.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'view/backend'))
    from scene_patterns import build_pattern
    model, _ = build_pattern(build_scene(), args.pattern)
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    with mujoco.viewer.launch_passive(model, data) as viewer:
        viewer.cam.type = mujoco.mjtCamera.mjCAMERA_FIXED
        viewer.cam.fixedcamid = model.camera('general').id
        print('Use the Control panel: gantry_x, gantry_y, gantry_z and hand fingers.')
        while viewer.is_running():
            began = time.monotonic()
            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(max(0, model.opt.timestep-(time.monotonic()-began)))


if __name__ == '__main__':
    main()
