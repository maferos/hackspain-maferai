#!/usr/bin/env python3
"""Try to pick up every dynamic vessel on the bench, with physics running.

Run from simulation/ after scripts/generate_rail_scene.py:
    python scripts/grasp_test.py
    python scripts/grasp_test.py --lift 0.25 --verbose

This is the check that the scene is actually good for manipulation, which the
reachability report is not: `rail_reach.py` only asks whether the arm can hold a
pose, with no contact, no gravity and nothing to hold. Here the arm is driven
through its position actuators, `mj_step` runs the whole way, and a vessel counts
as picked up only if it is still off the bench at the end.

Every stage is reported per vessel, because the interesting failures are not
"it did not work" but *where* it stopped: no IK solution means the geometry is
wrong, a vessel that never leaves the bench means the grip slipped, and one that
leaves and comes back means the lift was too fast for the friction available.
"""
import argparse
import sys
from pathlib import Path

import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rail_kinematics as rk

OPEN, SHUT = 0.0, 255.0     # the 2F-85's ctrlrange
GRASP_FRACTION = 0.35      # up the vessel wall, below the shoulder where it tapers
APPROACH = 0.12             # how far above the grasp the approach starts


def actuators(model: mujoco.MjModel) -> list[int]:
    """Actuator ids for the rail and the six arm joints, in trajectory order."""
    return [model.actuator(rk.RAIL_JOINT).id] + [
        model.actuator(name.replace('_joint', '')).id for name in rk.ARM_JOINTS]


def hold(model: mujoco.MjModel, data: mujoco.MjData, ids: list[int],
         station: float, pose: np.ndarray, grip: float | None, seconds: float,
         settle: float = 0.5) -> None:
    """Ramp the servo targets to a pose, then sit on the target while it catches up.

    The settle is not padding. Ramping the target and reading the tool straight
    after leaves the arm mid-motion: measured that way the tool looked 20 to
    47 mm off, which is wider than a flask, and the gripper closed on nothing.
    With a settle it converges to a few millimetres.

    Args:
        model: Compiled scene.
        data: Data to step.
        ids: Actuator ids for the rail and the arm joints.
        station: World X for the carriage.
        pose: Target arm joint angles.
        grip: Gripper actuator target, or None when no gripper is fitted.
        seconds: Length of the ramp.
        settle: Extra time held at the final target.
    """
    home = model.body('rail_carriage').pos[0]
    start = np.array([data.ctrl[i] for i in ids])
    goal = np.concatenate([[station - home], pose])
    # Give a long move long enough to arrive. A fixed ramp is fine for the
    # short hops and leaves the arm still flying after a 4 m run down the rail,
    # which reads downstream as a miss that is really just lateness.
    move = np.abs(goal - start)
    seconds = max(seconds, float(move[0]) / 0.6, float(move[1:].max()) / 0.9)
    ramp = max(int(seconds / model.opt.timestep), 1)
    for step in range(ramp + int(settle / model.opt.timestep)):
        alpha = 0.5 - 0.5 * np.cos(np.pi * min(step + 1, ramp) / ramp)
        for i, value in zip(ids, start + alpha * (goal - start)):
            data.ctrl[i] = value
        if grip is not None and model.nu > len(ids):
            # Only when a gripper is fitted; the pipetting scene has no fingers.
            data.ctrl[model.actuator('arm_grip_fingers_actuator').id] = grip
        mujoco.mj_step(model, data)


def close_on_object(model: mujoco.MjModel, data: mujoco.MjData, ids: list[int],
                    station: float, pose: np.ndarray, *, seconds: float = 1.2
                    ) -> rk.Grip:
    """Close the gripper until its own sensors say it is holding something.

    This is how the real 2F-85 is driven: it is told to close and it reports
    back whether it stopped on an object or ran to the stop. Commanding a fixed
    full-close and assuming the best cannot tell those apart --- and squeezes
    thin glass at whatever the servo can manage.

    Args:
        model: Compiled scene.
        data: Data to step.
        ids: Actuator ids for the rail and arm joints.
        station: World X for the carriage.
        pose: Arm pose to hold while closing.
        seconds: How long to keep closing before giving up.

    Returns:
        The gripper state when it stopped.
    """
    home = model.body('rail_carriage').pos[0]
    grip_id = model.actuator('arm_grip_fingers_actuator').id
    steps = max(int(seconds / model.opt.timestep), 1)
    for step in range(steps):
        data.ctrl[grip_id] = SHUT * min((step + 1) / (steps * 0.6), 1.0)
        for i, value in zip(ids, np.concatenate([[station - home], pose])):
            data.ctrl[i] = value
        mujoco.mj_step(model, data)
        grip = rk.read_grip(model, data)
        if grip.holding and step > steps * 0.3:
            # Stop advancing, hold what the pads have already got.
            data.ctrl[grip_id] = data.ctrl[grip_id]
            break
    return rk.read_grip(model, data)


def attempt(model: mujoco.MjModel, data: mujoco.MjData, bottle: rk.Bottle,
            lift: float) -> dict[str, object]:
    """Approach, close, lift, and report what happened.

    Args:
        model: Compiled scene.
        data: Data to run in; reset before use.
        bottle: The vessel to pick up.
        lift: How far to raise the tool after closing, in metres.

    Returns:
        A record with the stage reached and the vessel's height gain.
    """
    body = f'dyn_{bottle.sample_id}'
    grasp = rk.BENCH_TOP + (bottle.top - rk.BENCH_TOP) * GRASP_FRACTION
    above = np.array([bottle.x, bottle.y, grasp + APPROACH])
    on = np.array([bottle.x, bottle.y, grasp])

    station = rk.reach(model, data, above)
    if station is None:
        return {'sample': bottle.sample_id, 'stage': 'no IK above the vessel',
                'gain': 0.0}
    q_above = data.qpos[rk.arm_qpos(model)].copy()
    rk.set_rail(model, data, station)
    if not rk.solve_any(model, data, on):
        return {'sample': bottle.sample_id, 'stage': 'no IK at the grasp',
                'gain': 0.0}
    q_on = data.qpos[rk.arm_qpos(model)].copy()

    # Start already at the approach pose: getting there is a motion-planning
    # problem through 300 vessels, and not what this test is about.
    mujoco.mj_resetData(model, data)
    rk.set_rail(model, data, station)
    data.qpos[rk.arm_qpos(model)] = q_above
    mujoco.mj_forward(model, data)
    ids = actuators(model)
    home = model.body('rail_carriage').pos[0]
    for i, value in zip(ids, np.concatenate([[station - home], q_above])):
        data.ctrl[i] = value
    data.ctrl[model.actuator('arm_grip_fingers_actuator').id] = OPEN

    base = float(data.body(body).xpos[2])
    hold(model, data, ids, station, q_above, OPEN, 0.4)
    hold(model, data, ids, station, q_on, OPEN, 1.0)          # descend
    closed = close_on_object(model, data, ids, station, q_on)  # close on it
    grip = data.ctrl[model.actuator('arm_grip_fingers_actuator').id]
    hold(model, data, ids, station, q_above, grip, 1.2)       # lift clear
    lifted = float(data.body(body).xpos[2])
    hold(model, data, ids, station, q_above, grip, 1.0)       # and hold it
    held = float(data.body(body).xpos[2])
    final = rk.read_grip(model, data)

    gain = held - base
    if not closed.holding:
        stage = ('closed on air' if closed.closure > rk.FINGERS_SHUT
                 else 'jammed before closing')
    elif gain > 0.02:
        stage = 'PICKED UP'
    elif lifted - base > 0.02:
        stage = 'lifted then dropped'
    else:
        stage = 'held but not lifted'
    return {'sample': bottle.sample_id, 'stage': stage, 'gain': gain,
            'peak': lifted - base, 'grip': closed, 'final': final}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lift', type=float, default=APPROACH,
                        help='how far to raise the tool, m')
    parser.add_argument('--only', nargs='*', help='sample ids to try')
    args = parser.parse_args()

    model, data = rk.load()
    mujoco.mj_forward(model, data)
    vessels = [b for b in rk.bottles(model, data) if b.dynamic]
    if args.only:
        vessels = [b for b in vessels if b.sample_id in args.only]
    print(f'{len(vessels)} dynamic vessels; the other '
          f'{sum(1 for b in rk.bottles(model, data) if not b.dynamic)} are scenery\n')

    results = [attempt(model, data, b, args.lift) for b in vessels]
    print(f'  {"sample":10s} {"outcome":22s} {"rose":>9s} '
          f'{"squeeze":>8s} {"closure":>8s} {"detected":>9s}')
    for r in results:
        g = r.get('grip')
        print(f'  {r["sample"]:10s} {r["stage"]:22s} {r["gain"] * 1000:+6.1f} mm '
              f'{"" if g is None else f"{g.squeeze:6.1f} N"} '
              f'{"" if g is None else f"{g.closure:7.3f}"} '
              f'{"" if g is None else ("   yes" if g.holding else "    no")}')
    won = sum(r['stage'] == 'PICKED UP' for r in results)
    sensed = sum(1 for r in results if r.get('grip') and r['grip'].holding)
    print(f'\ngripper reported an object: {sensed}/{len(results)}')
    print(f'picked up and still held:   {won}/{len(results)}')
    agree = sum(1 for r in results
                if bool(r.get('grip') and r['grip'].holding)
                == (r['stage'] == 'PICKED UP'))
    print(f'sensor agreed with reality: {agree}/{len(results)}')


if __name__ == '__main__':
    main()
