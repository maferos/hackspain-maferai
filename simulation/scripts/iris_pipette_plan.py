"""The uncap-and-pipette sequence, for the page, the .blend and both simulators.

Plain Python (numpy only, through iris_pipette_rig): iris_pipette_play.py
(MuJoCo), iris_pipette_isaac.py (Isaac Lab) and generate_iris_pipette_blend.py
(Blender) all import it, and the viewer generator writes STEPS and START into
the page, so the four play the same 19 steps.

The sequence is in the state of iris_pipette_rig.STATE plus ``fill`` (how full
the tip is, page and .blend only). Two values depend on the bottle the page has
set, so STEPS carries them as sentinels: ``'closed'`` is the jaws closed on the
bottle (its diameter) and ``'dive'`` the tip at its dive height. ``keys()``
resolves them; the simulators use the reference bottle.

The bottle rides with the hand while the jaws are closed on it and the cap
rides in the clamp once the housing has turned: ``attachments()`` says which,
the same rule the page uses to re-parent them and the simulators use to switch
their welds.
"""
import math

import numpy as np

from iris_pipette_rig import (ACTUATED, ALPHA_CONTACT, BOTTLE_R, FOLLOW,
                              HINGE_UP, IRIS, IRIS_OPEN, OPEN_APERTURE,
                              PLUNGER_STROKE, STATE, STOW, TIP_READY, Z_LIFT,
                              dive_z, joint_values)

DRIVER_CLOSED = 0.8     # the 2F-85's right_driver_joint, fully closed

START = {'lift_z': Z_LIFT, 'grip_aperture': OPEN_APERTURE, 'hinge_angle': HINGE_UP,
         'iris_angle': IRIS_OPEN, 'housing_turns': 0.0, 'pipette_tip': TIP_READY,
         'swing_angle': STOW, 'plunger': 0.0, 'fill': 0.0}

# (name, seconds, what changes); every value eases from the previous key.
STEPS = [
    ('Lower the hand over the bottle', 1.6, {'lift_z': 0.0}),
    ('Close the gripper on it', 0.9, {'grip_aperture': 'closed'}),
    ('Lift the bottle', 1.2, {'lift_z': Z_LIFT}),
    ('Swing the iris clamp down onto the cap', 1.6, {'hinge_angle': 0.0}),
    ('Close the iris on the cap', 0.9, {'iris_angle': ALPHA_CONTACT}),
    ('Unscrew: housing turns 2×, the hinge follows the cap up', 3.0,
     {'housing_turns': IRIS['turns'], 'hinge_angle': FOLLOW}),
    ('Swing the clamp up with the cap', 1.6, {'hinge_angle': HINGE_UP}),
    ('Swing the pipette in over the neck: the cone seats', 1.4, {'swing_angle': 0.0}),
    ('Press the plunger', 0.6, {'plunger': PLUNGER_STROKE}),
    ('Lower the pipette into the liquid', 1.4, {'pipette_tip': 'dive'}),
    ('Aspirate: release the plunger', 1.2, {'plunger': 0.0, 'fill': 1.0}),
    ('Withdraw the pipette', 1.2, {'pipette_tip': TIP_READY}),
    ("Swing the pipette out to the arm's side", 1.4, {'swing_angle': STOW}),
    ('Swing the clamp back down onto the neck', 1.6, {'hinge_angle': FOLLOW}),
    ('Screw the cap back', 3.0, {'housing_turns': 0.0, 'hinge_angle': 0.0}),
    ('Open the iris', 0.9, {'iris_angle': IRIS_OPEN}),
    ('Stow the clamp', 1.6, {'hinge_angle': HINGE_UP}),
    ('Put the bottle down', 1.2, {'lift_z': 0.0}),
    ('Open the gripper and lift the hand clear', 1.6, {'grip_aperture': OPEN_APERTURE, 'lift_z': Z_LIFT}),
]
TAIL = 0.8              # rest at the end before the page loops


def keys(bottle_r: float = BOTTLE_R, dive: float | None = None) -> list[tuple[float, dict]]:
    """The keyframes: (time, full state) at the start and after every step."""
    closed, tip = 2 * bottle_r, dive_z() if dive is None else dive
    out = [(0.0, dict(START))]
    for _, seconds, delta in STEPS:
        t, last = out[-1]
        state = dict(last)
        for k, v in delta.items():
            state[k] = closed if v == 'closed' else tip if v == 'dive' else v
        out.append((t + seconds, state))
    return out


KEYS = keys()
DURATION = KEYS[-1][0]


def step_end(n: int) -> float:
    """When step n (1-based) is complete."""
    return KEYS[n][0]


# For the checks: the moments by which each thing should have happened.
GRIPPED_AT = step_end(2)
LIFTED_AT = step_end(3)
UNSCREWED_AT = step_end(6)
CAP_AWAY_AT = step_end(7)
DIVED_AT = step_end(10)
RECAPPED_AT = step_end(15)
RELEASED_AT = step_end(19)


def ease(x: float) -> float:
    """The page's easing: a half cosine, so nothing starts or stops with a jerk."""
    return 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, x)))


def state_at(t: float, frames: list[tuple[float, dict]] = KEYS) -> tuple[dict, int]:
    """The state at time t and the step (0-based) it is in, -1 once over.

    The last step opens the gripper first and lifts the hand after, as the
    page does.
    """
    for i in range(1, len(frames)):
        (t0, a), (t1, b) = frames[i - 1], frames[i]
        if t < t1:
            f = ease((t - t0) / (t1 - t0))
            state = {k: a[k] + (b[k] - a[k]) * f for k in a}
            if i == len(frames) - 1:
                state['grip_aperture'] = a['grip_aperture'] + (b['grip_aperture'] - a['grip_aperture']) * ease(2 * (t - t0) / (t1 - t0))
                state['lift_z'] = a['lift_z'] + (b['lift_z'] - a['lift_z']) * ease(2 * (t - t0) / (t1 - t0) - 1)
            return state, i - 1
    return dict(frames[-1][1]), -1


def attachments(state: dict, bottle_r: float = BOTTLE_R) -> dict:
    """Who carries the bottle and the cap at a state: the page's rule."""
    return {'bottle': 'hand' if state['grip_aperture'] <= 2 * bottle_r + 0.0005 else 'world',
            'cap': 'clamp' if state['housing_turns'] > 1e-4 else 'bottle'}


def driver_target(aperture: float, bottle_r: float = BOTTLE_R) -> float:
    """The 2F-85's driver joint for an aperture: it closes fully on the bottle,
    so the pads squeeze while the weld carries it (the page stops at the
    diameter)."""
    s = (OPEN_APERTURE - aperture) / (OPEN_APERTURE - 2 * bottle_r)
    return DRIVER_CLOSED * min(1.0, max(0.0, s))


def targets(t: float) -> dict:
    """The actuated joints' targets at time t, by joint name."""
    state, _ = state_at(t)
    joints = joint_values(state)
    out = {name: joints[name] for name in ACTUATED if name in joints}
    out['right_driver_joint'] = driver_target(state['grip_aperture'])
    return out


def to_json() -> dict:
    """START and STEPS for the page, sentinels kept."""
    return {'start': {k: START[k] for k in (*STATE, 'fill')},
            'steps': [[name, seconds, delta] for name, seconds, delta in STEPS]}


if __name__ == '__main__':
    for n, (name, _, _) in enumerate(STEPS, 1):
        t = step_end(n)
        s, _ = state_at(t - 1e-6)
        print(f'{t:5.1f} s  {n:2d}. {name}: ' + ', '.join(
            f'{k}={v:.3f}' for k, v in s.items() if k in STEPS[n - 1][2]))
    print(f'{DURATION:.1f} s in all; targets at 8 s: {np.round(list(targets(8.0).values()), 3)}')
