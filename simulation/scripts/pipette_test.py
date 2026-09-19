#!/usr/bin/env python3
"""Draw from every flask on the bench and deliver it into the beaker.

Run from simulation/ after scripts/generate_rail_scene.py:
    python scripts/pipette_test.py
    python scripts/pipette_test.py --draw 0.6 --only SMP-0084

The whole cycle runs with physics: the arm is driven through its position
actuators, `mj_step` runs throughout, and the tip has to be down the bore and
under the surface before any liquid moves. A transfer that reports a miss is a
real geometric miss, not a scripted failure --- which is the reason to simulate
it rather than animate it.

This is the pipetting counterpart of scripts/grasp_test.py and reports the same
shape of thing: where each attempt got to, and by how much it missed.
"""
import argparse
import sys
from pathlib import Path

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import grasp_test as gt
import pipetting as pip
import rail_kinematics as rk

CLEARANCE = 0.06        # tip height over the rim on the way in and out
# How far down the liquid column to aim, as a fraction of its height. A real
# pipette dips 2 to 3 mm to keep the outside of the tip dry; here the servos
# land within a few millimetres of the target, so aiming just under the surface
# left the tip above it on four flasks out of twelve. Aiming a quarter of the
# way down costs nothing and removes the whole failure mode.
IMMERSION = 0.25


def target_depth(vessel: pip.Container, data: mujoco.MjData) -> float:
    """World height to put the tip at to draw from a vessel."""
    base = float(data.body(vessel.body).xpos[2])
    column = vessel.height()
    return base + vessel.floor + max(column * (1 - IMMERSION), 0.003)


def run(model: mujoco.MjModel, data: mujoco.MjData, vessel: pip.Container,
        beaker: pip.Container, pipette: pip.Pipette, draw: float
        ) -> dict[str, object]:
    """One full transfer: into the flask, draw, over the beaker, deliver.

    Args:
        model: Compiled scene.
        data: Data to run in; reset before use.
        vessel: Flask to draw from.
        beaker: Container to deliver into.
        pipette: Tool state.
        draw: Millilitres to attempt.

    Returns:
        A record of what happened and the volumes either side.
    """
    ids = gt.actuators(model)
    before = vessel.volume
    axis = data.body(vessel.body).xpos

    over = np.array([float(axis[0]), float(axis[1]),
                     float(data.site(vessel.mouth).xpos[2]) + CLEARANCE])
    station = rk.reach(model, data, over)
    if station is None:
        return {'sample': vessel.name, 'stage': 'no IK over the mouth',
                'moved': 0.0, 'miss': float('nan')}
    q_over = data.qpos[rk.arm_qpos(model)].copy()
    rk.set_rail(model, data, station)
    down = over.copy()
    down[2] = target_depth(vessel, data)
    if not rk.solve_any(model, data, down):
        return {'sample': vessel.name, 'stage': 'no IK in the bore',
                'moved': 0.0, 'miss': float('nan')}
    q_down = data.qpos[rk.arm_qpos(model)].copy()

    mujoco.mj_resetData(model, data)
    rk.set_rail(model, data, station)
    data.qpos[rk.arm_qpos(model)] = q_over
    mujoco.mj_forward(model, data)
    for i, value in zip(ids, np.concatenate(
            [[station - model.body('rail_carriage').pos[0]], q_over])):
        data.ctrl[i] = value

    gt.hold(model, data, ids, station, q_over, None, 0.5)
    gt.hold(model, data, ids, station, q_down, None, 1.2)
    miss, depth = pip.entry(model, data, vessel)
    drew = pip.aspirate(model, data, vessel, pipette, draw)
    gt.hold(model, data, ids, station, q_over, None, 1.0)

    record = {'sample': vessel.name, 'miss': miss, 'depth': depth,
              'before': before, 'moved': 0.0}
    if not drew:
        record['stage'] = 'aspiration refused'
        return record

    # Over the beaker and deliver.
    mouth = data.site(beaker.mouth).xpos
    above = np.array([float(mouth[0]), float(mouth[1]),
                      float(mouth[2]) - 0.01])
    station = rk.reach(model, data, above)
    if station is None:
        record['stage'] = 'drew but cannot reach the beaker'
        return record
    q_beaker = data.qpos[rk.arm_qpos(model)].copy()
    data.qpos[rk.arm_qpos(model)] = q_over
    mujoco.mj_forward(model, data)
    gt.hold(model, data, ids, station, q_beaker, None, 2.0)
    gave = pip.dispense(model, data, beaker, pipette)
    record['moved'] = before - vessel.volume
    record['stage'] = 'TRANSFERRED' if gave else 'drew but could not deliver'
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--draw', type=float, default=0.5,
                        help='millilitres to take from each flask')
    parser.add_argument('--only', nargs='*', help='sample ids to try')
    args = parser.parse_args()

    model, data = rk.load()
    mujoco.mj_forward(model, data)
    vessels = pip.containers(model, data)
    beaker = vessels['beaker']
    pipette = pip.Pipette()
    flasks = [v for k, v in sorted(vessels.items()) if k != 'beaker']
    if args.only:
        flasks = [v for v in flasks if v.name in args.only]

    print(f'{len(flasks)} open flasks holding '
          f'{sum(v.volume for v in flasks):.1f} ml between them; '
          f'tip radius {pip.tip_radius(model) * 1000:.1f} mm\n')
    print(f'  {"sample":10s} {"outcome":26s} {"moved":>8s} {"miss":>8s} {"depth":>9s}')
    results = []
    for flask in flasks:
        record = run(model, data, flask, beaker, pipette, args.draw)
        results.append(record)
        print(f'  {record["sample"]:10s} {record["stage"]:26s} '
              f'{record["moved"]:6.2f} ml '
              f'{record.get("miss", float("nan")) * 1000:6.1f} mm '
              f'{record.get("depth", float("nan")) * 1000:+7.1f} mm')

    won = sum(r['stage'] == 'TRANSFERRED' for r in results)
    print(f'\ntransferred: {won}/{len(results)}')
    print(f'beaker now holds {beaker.volume:.2f} ml = {beaker.mass:.2f} g '
          f'at {pip.DENSITY} g/ml')
    print(f'pipette still holds {pipette.volume:.2f} ml')
    misses = [r['miss'] for r in results if not np.isnan(r.get('miss', np.nan))]
    if misses:
        print(f'tip alignment: {np.mean(misses) * 1000:.1f} mm mean, '
              f'{max(misses) * 1000:.1f} mm worst')


if __name__ == '__main__':
    main()
