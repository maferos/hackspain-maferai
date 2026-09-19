"""The pick-and-place the UR10e hand plays in hand_pick_scene, for both simulators.

Plain Python on purpose: hand_pick.py (MuJoCo) and hand_pick_isaac.py (Isaac
Lab) both import it, and Isaac's Python has no MuJoCo.

The plan is in the joints both simulators share (see generate_hand_scene.py):

* ``reach``, ``lift`` --- the flange's world X and Z, in metres. The hand
  points along +X, APPROACH_TILT below the horizontal, and its fingers open
  and close along world Y: it takes the bottle from the side.
* ``wrist`` --- ``wrist_3_joint``, radians. Held at 0: with the hand on its
  side, turning the wrist would tip the bottle over.
* ``grip`` --- the 2F-85's driver joint, radians: 0 open, 0.8 closed. Closing
  on the bottle stops at about 0.43; the command stays at 0.8 so the fingers
  keep squeezing, and the actuator's force limit sets how hard.
"""
import numpy as np

OPEN, CLOSED = 0.0, 0.8

# How far the approach dips below the horizontal. A little, so the knuckles
# and the arm stub behind the flange ride clear of the floor.
APPROACH_TILT = np.radians(10.0)
APPROACH = np.array([np.cos(APPROACH_TILT), -np.sin(APPROACH_TILT)])   # (X, Z)

# The bottle: amber_060ml, 40 mm across, straight from 3 to 66 mm up, cap to 97.
BOTTLE_XY = (0.0, 0.0)
# Pad centre height, on the straight wall.
GRASP_Z = 0.040
# Flange to pad centre along the approach, closed on a 40 mm bottle. Measured
# in the MuJoCo scene; hand_pick.py fails if the grasp lands 5 mm off.
FLANGE_TO_PAD = 0.155
LIFT = 0.10               # how high the bottle is carried
PLACE_CLEARANCE = 0.002   # set it down this much above where it was picked
STANDOFF = 0.12           # the straight-in approach starts this far back

# Flange (reach, lift) with the pad centre on the bottle's axis at GRASP_Z.
GRASP = np.array([BOTTLE_XY[0], GRASP_Z]) - FLANGE_TO_PAD * APPROACH
PRE_GRASP = GRASP - STANDOFF * APPROACH
HOME_REACH, HOME_LIFT = GRASP[0] - 0.15, 0.30


def _at(flange, dz=0.0):
    return float(flange[0]), float(flange[1] + dz)


# (time in s, reach, lift, wrist, grip): the targets at each time; between two
# of them every joint eases from one to the next.
WAYPOINTS = [
    (0.0, HOME_REACH, HOME_LIFT, 0.0, OPEN),
    (0.5, HOME_REACH, HOME_LIFT, 0.0, OPEN),
    (2.0, *_at(PRE_GRASP), 0.0, OPEN),                  # line up beside it
    (3.5, *_at(GRASP), 0.0, OPEN),                      # straight in
    (4.0, *_at(GRASP), 0.0, OPEN),
    (5.0, *_at(GRASP), 0.0, CLOSED),                    # grip
    (5.5, *_at(GRASP), 0.0, CLOSED),
    (7.0, *_at(GRASP, LIFT), 0.0, CLOSED),              # pick it up
    (8.0, *_at(GRASP, LIFT), 0.0, CLOSED),              # hold it up
    (9.5, *_at(GRASP, PLACE_CLEARANCE), 0.0, CLOSED),   # set it down
    (10.0, *_at(GRASP, PLACE_CLEARANCE), 0.0, CLOSED),
    (11.0, *_at(GRASP, PLACE_CLEARANCE), 0.0, OPEN),    # let go
    (11.5, *_at(GRASP, PLACE_CLEARANCE), 0.0, OPEN),
    (13.0, *_at(PRE_GRASP, PLACE_CLEARANCE), 0.0, OPEN),  # straight back out
    (14.5, HOME_REACH, HOME_LIFT, 0.0, OPEN),
    (15.0, HOME_REACH, HOME_LIFT, 0.0, OPEN),
]
DURATION = WAYPOINTS[-1][0]
# For the checks: when the bottle should be gripped, and when up.
GRIPPED_AT = 5.4
HELD_AT = 7.5


def targets(t: float) -> np.ndarray:
    """(reach, lift, wrist, grip) targets at time t, eased between waypoints."""
    times = [w[0] for w in WAYPOINTS]
    t = min(max(t, 0.0), DURATION)
    k = max(i for i, w in enumerate(times) if w <= t)
    if k == len(WAYPOINTS) - 1:
        return np.array(WAYPOINTS[-1][1:])
    (t0, *a), (t1, *b) = WAYPOINTS[k], WAYPOINTS[k + 1]
    s = (t - t0) / (t1 - t0)
    s = s * s * (3 - 2 * s)   # smoothstep: start and stop without a jerk
    return np.array(a) + s * (np.array(b) - np.array(a))
