#!/usr/bin/env python3
"""Play the UR10e hand's pick-and-place in MuJoCo, and check that it worked.

Run from simulation/ after scripts/generate_hand_scene.py:
    python scripts/hand_pick.py            # headless, prints the check
    python scripts/hand_pick.py --view     # in the viewer, in real time

The hand comes at the amber bottle from the side, nearly level, closes on it,
lifts it LIFT, sets it back down and lets go (hand_pick_plan.py, shared with the Isaac version). Physics
runs the whole way: the bottle is a free body held only by pad friction.

It passes when the pads closed within 5 mm of the planned height, the bottle
was carried at least 90 % of LIFT, the hand never touched the floor, and at
the end it stands upright within 5 degrees, back on the
floor, within 10 mm of where it was picked.
"""
import argparse
import sys
import time
from pathlib import Path

import mujoco
import mujoco.viewer
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hand_pick_plan as plan

SCENE = Path(__file__).resolve().parents[1] / 'models/hand_pick_scene.xml'
GRIP_CTRL = 255.0 / plan.CLOSED    # the 2F-85 takes 0..255 for driver 0..0.8


def run(view: bool) -> bool:
    model = mujoco.MjModel.from_xml_path(str(SCENE))
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, model.key('home').id)
    act = [model.actuator(n).id for n in ('reach', 'lift', 'wrist_3', 'fingers_actuator')]
    bottle = model.body('bottle').id
    start = data.xpos[bottle].copy()
    pads = [g for g in range(model.ngeom) if model.geom_type[g] == mujoco.mjtGeom.mjGEOM_BOX
            and model.body(model.geom_bodyid[g]).name.endswith('_pad')]

    viewer = None
    if view:
        viewer = mujoco.viewer.launch_passive(model, data)
    held, peak, pad_z = None, 0.0, None
    floor_hits = set()
    bottle_tree = {b for b in range(model.nbody) if model.body_rootid[b] == bottle}
    wall = time.time()
    while data.time < plan.DURATION + 1.0:
        reach, lift, wrist, grip = plan.targets(data.time)
        data.ctrl[act] = reach, lift, wrist, grip * GRIP_CTRL
        mujoco.mj_step(model, data)
        rise = data.xpos[bottle][2] - start[2]
        peak = max(peak, rise)
        if held is None and data.time >= plan.HELD_AT:
            held = rise
        for c in data.contact[:data.ncon]:
            bodies = {model.geom_bodyid[c.geom1], model.geom_bodyid[c.geom2]}
            if 0 in bodies and bottle_tree.isdisjoint(bodies):
                floor_hits.add(model.body((bodies - {0}).pop()).name)
        if pad_z is None and data.time >= plan.GRIPPED_AT:
            pad_z = np.mean(data.geom_xpos[pads, 2])
        if viewer is not None:
            if not viewer.is_running():
                return False
            viewer.sync()
            ahead = data.time - (time.time() - wall)
            if ahead > 0:
                time.sleep(ahead)

    end = data.xpos[bottle]
    up = data.xmat[bottle].reshape(3, 3)[:, 2]
    tilt = np.degrees(np.arccos(np.clip(up[2], -1, 1)))
    moved = np.linalg.norm(end[:2] - start[:2])
    landed = pad_z - start[2]
    checks = {
        f'gripped with the pads {landed * 1000:.1f} mm up the bottle (planned {plan.GRASP_Z * 1000:.0f} +- 5)':
            abs(landed - plan.GRASP_Z) <= 0.005,
        f'carried {held * 1000:.1f} mm at t={plan.HELD_AT} s (want >= {0.9 * plan.LIFT * 1000:.0f})':
            held >= 0.9 * plan.LIFT,
        'hand clear of the floor' + (f': hit by {sorted(floor_hits)}' if floor_hits else ''):
            not floor_hits,
        f'set down {moved * 1000:.1f} mm from where it was picked (want <= 10)': moved <= 0.01,
        f'standing {tilt:.1f} deg off vertical (want <= 5)': tilt <= 5,
        f'back on the floor: z {end[2] * 1000:+.1f} mm': abs(end[2] - start[2]) <= 0.003,
    }
    print(f'peak lift {peak * 1000:.1f} mm')
    for label, ok in checks.items():
        print(f'  {"ok  " if ok else "FAIL"} {label}')
    if viewer is not None:
        while viewer.is_running():
            time.sleep(0.05)
    return all(checks.values())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--view', action='store_true', help='show it in the MuJoCo viewer')
    ok = run(parser.parse_args().view)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
