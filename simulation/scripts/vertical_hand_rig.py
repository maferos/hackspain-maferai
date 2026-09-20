"""The vertical uncap-and-pipette hand of gripper-design/vertical_hand.html, as numbers.

One description for four outputs: ``vertical_hand.blend`` (+ ``.glb``, ``.usd``)
by generate_vertical_hand_blend.py, which also writes the MJCF
(``assets/vertical_hand/vertical_hand.xml`` and ``_scene.xml``) and the URDF
(``vertical_hand.urdf``) from the same tree, and vertical_hand_play.py, which
plays the 23 steps in MuJoCo. Every number is the page's: the parameter block
of ``gripper-design/vertical_hand.html`` in millimetres and degrees, kept here
verbatim so the two can be diffed; ``STATE``, the joints and ``fk`` are in
metres and radians.

Hand frame: +X from the arm to the bottle, Y across, Z up; the bottle's axis
at x = y = 0; the reference (60 ml) bottle's base at z = 0 when the hand is
lowered (``lift_z`` = 0). The hand's own origin rides ``lift_z`` up the world
Z axis; the table is the world's z = 0.
"""
import math

import numpy as np

MM = 0.001
DEG = math.pi / 180
TAU = 2 * math.pi

# ============================== PARAMETERS (mm, degrees), the page's ==============================
REF_CAP_Z = 78.1                         # the reference cap seat; everything on the hand is placed off it
AXIS_BELOW_CAP = 21
GRIP_Z = REF_CAP_Z - AXIS_BELOW_CAP      # 57.1: the tool axis
JAW = dict(p=8, half_width=22.5, clearance=0.2, liner=3, half_height=16, plate=6, open_clear=6)
BODY = dict(length=52, half_width=32, half_height=16)
FRONT_CLEAR, FLANGE_X = 30, -118
HUB_HALF, COMB_X, COMB_GAP = 14, 12, 1
BEAM = dict(x0=-31, x1=-25, half_z=8, half_y=96)
CARRIAGE = dict(x0=-30, x1=-24, width=14, half_z=12)
ARM = dict(x0=-24, x1=-2, width=12, half_z=11)
FLANGE = dict(r=45, face_r=31.5, pcd=25, bolt_r=3.3, ring_h=12, stub_r=45, stub_len=150)
SPINE = dict(x0=-150, x1=-75, half_y=60, z0=44, z1=430)     # the harness
FLANGE_Z, FLANGE_C = SPINE['z1'], (SPINE['x0'] + SPINE['x1']) / 2
STRUT_Y = 92
RAIL = dict(x=-45, z=230, y0=36, y1=264, park=160, col_y=80)   # the clamp's rail, along Y
IRIS = dict(r_pivot=55, n_blades=6, blade_len=62, blade_w=12, blade_t=2.5, blade_max=80, housing_r=69, housing_ri=59,
            z_cam=18, cam_t=6, z_gears=30, gear_t=8, z_carrier=42, carrier_t=6, z_top=60, r_ring=36, r_sun=12, planet_r=24,
            open_r=35, cap_dz=-1.5)
Z_IRIS = REF_CAP_Z - IRIS['cap_dz']      # 79.6: iris plane when the blades meet the cap
CLAMP_LIFT, PITCH, TURNS = 25, 2.75, 2
CAP_LIFT = PITCH * TURNS                 # the thread walks the cap up 5.5 mm
LIFT_HI = CAP_LIFT + CLAMP_LIFT          # 30.5: the clamp travels in and out this high
PIP = dict(tip_len=12, tip_r0=2.4, tip_r1=3.6, shaft_len=78, shaft_r1=5.8, collar_len=26, collar_r1=11.2,
           body_z0=116, body_len=105, body_w0=24, body_w1=30, body_d0=20, body_d1=24,
           plunger_x=3, plunger_r=4, plunger_len=30, button_r=8.5, button_h=8.5,
           ejector_x=16.5, ejector_r=2.8, ejector_btn_r=7.5, ejector_btn_h=6, ejector_btn_z=232,
           ejector_sleeve_r=6.8, ejector_sleeve_z0=66, ejector_sleeve_z1=94,
           hook_z=213, hook_reach=24, grip_z=168.5, stroke=14)
PIVOT = dict(x=30, y=-90)
STOW = 80                                # degrees, the pipette parked out beside the harness
YOKE_Y = PIVOT['y'] - 28
NECK_H = 95 - REF_CAP_Z                  # 16.9: cap seat to lip on the reference bottle
TIP_READY = REF_CAP_Z + NECK_H + 15      # 110: tip just over the neck
CLIPS = [125, PIP['grip_z']]
CAR = [PIP['grip_z'] - 20, PIP['grip_z'] + 60]
RAIL_TOP = TIP_READY + CAR[1]
MAST_BOTTOM = 70
TIP_DIVE, LIFT_Z = 20, 100
BTN_TOP = PIP['body_z0'] + PIP['body_len'] + PIP['plunger_len'] + PIP['button_h']   # 259.5

# bottles.py catalogue (mm): radius, height, shoulder, neck start, neck radius, cap seat, cap height, cap radius
CATALOGUE = {
    10: dict(r=11.01, h=52.28, shoulder=32.98, neck=39.58, neck_r=8.95, cap_z=39.72, cap_h=14.16, cap_r=10.9),
    20: dict(r=13.87, h=65.87, shoulder=44.85, neck=53.17, neck_r=8.95, cap_z=53.31, cap_h=14.16, cap_r=10.9),
    30: dict(r=15.87, h=75.40, shoulder=51.88, neck=61.40, neck_r=9.95, cap_z=61.60, cap_h=15.40, cap_r=11.9),
    50: dict(r=18.82, h=89.40, shoulder=60.86, neck=72.15, neck_r=12.45, cap_z=72.50, cap_h=18.50, cap_r=14.4),
    60: dict(r=20.00, h=95.00, shoulder=65.75, neck=77.75, neck_r=12.45, cap_z=78.10, cap_h=18.50, cap_r=14.4),
    100: dict(r=23.71, h=112.63, shoulder=79.21, neck=93.43, neck_r=13.95, cap_z=93.87, cap_h=20.36, cap_r=15.9),
}
REF_ML = 60
BOTTLE = dict(CATALOGUE[REF_ML], ml=REF_ML, level=0.5 * CATALOGUE[REF_ML]['shoulder'])


# gripper.py's closed forms (mm)
def vertex(r: float) -> float:
    """Each jaw's offset from the axis when its cradle is closed on a bottle of radius r."""
    return (r * r + JAW['p'] ** 2) / (2 * JAW['p']) + JAW['clearance']


EDGE = JAW['half_width'] ** 2 / (2 * JAW['p'])


def stroke(r: float) -> float:
    """Each jaw's offset when open clear of a bottle of radius r."""
    return EDGE + r + JAW['open_clear']


def parab(x: float) -> float:
    return -x * x / (2 * JAW['p'])


IRIS_OPEN = math.acos(IRIS['open_r'] / IRIS['r_pivot'])      # blades inside the housing, Ø70 open


def iris_contact(b: dict = BOTTLE) -> float:
    """Blade angle with the blades on the cap of bottle b."""
    return math.acos(b['cap_r'] / IRIS['r_pivot'])


def base_z(b: dict = BOTTLE) -> float:
    """The bottle's base in the hand frame (mm): its cap seat is put on the reference one's."""
    return REF_CAP_Z - b['cap_z']


# ============================== STATE (SI) ==============================
# The degrees of freedom, the custom properties of the .blend and the actuators of the MJCF.
STATE = ['lift_z', 'grip_aperture', 'clamp_y', 'clamp_lift', 'iris_angle', 'housing_turns',
         'pipette_tip', 'swing_angle', 'plunger']
# (default, min, max, subtype, description) for the Blender properties
PROPS = {
    'lift_z': (LIFT_Z * MM, 0.0, 0.3, 'DISTANCE', 'Hand height: the bottle base above the table once held (m)'),
    'grip_aperture': (2 * stroke(BOTTLE['r']) * MM, 2 * vertex(CATALOGUE[10]['r']) * MM, 2 * stroke(CATALOGUE[100]['r']) * MM,
                      'DISTANCE', 'Opening between the two cradle vertices (m)'),
    'clamp_y': (RAIL['park'] * MM, 0.0, RAIL['park'] * MM + 0.02, 'DISTANCE', 'Clamp carriage along its Y rail: 0 centred on the cap (m)'),
    'clamp_lift': (LIFT_HI * MM, 0.0, LIFT_HI * MM + 0.005, 'DISTANCE', 'Clamp lift column: 0 with the iris plane on the cap seat (m)'),
    'iris_angle': (IRIS_OPEN, 0.0, IRIS['blade_max'] * DEG, 'ANGLE', 'Blade angle: aperture = 2 r_pivot cos(angle)'),
    'housing_turns': (0.0, 0.0, TURNS + 0.5, 'NONE', 'Turns of the clamp housing (unscrewing the cap)'),
    'pipette_tip': (TIP_READY * MM, 0.01, 0.15, 'DISTANCE', 'Pipette tip height in the hand frame (m)'),
    'swing_angle': (STOW * DEG, 0.0, STOW * DEG, 'ANGLE', 'Pipette frame swing: 0 in over the neck, positive out beside the harness'),
    'plunger': (0.0, 0.0, PIP['stroke'] * MM, 'DISTANCE', 'Plunger pressed (m)'),
}


def start(b: dict = BOTTLE) -> dict:
    return dict(lift_z=LIFT_Z * MM, grip_aperture=2 * stroke(b['r']) * MM, clamp_y=RAIL['park'] * MM, clamp_lift=LIFT_HI * MM,
                iris_angle=IRIS_OPEN, housing_turns=0.0, pipette_tip=TIP_READY * MM, swing_angle=STOW * DEG, plunger=0.0, fill=0.0)


# (name, seconds, changes): the page's STEPS, in page units; keys() converts.
STEPS = [
    ('Lower the hand over the bottle', 1.6, dict(lift_z=0)),
    ('Close the gripper: the cradles centre the bottle', 0.9, dict(grip='closed')),
    ('Lift the bottle', 1.2, dict(lift_z=LIFT_Z)),
    ('Slide the iris clamp in, high over the cap', 1.6, dict(clamp_y=0)),
    ('Lower the clamp onto the cap', 0.9, dict(clift=0)),
    ('Close the iris on the cap', 0.9, dict(iris='contact')),
    ('Unscrew: the housing turns 2x, the clamp follows the cap up', 3.0, dict(turns=TURNS, clift=CAP_LIFT)),
    ('Lift the cap straight off the neck', 0.9, dict(clift=LIFT_HI)),
    ('Slide the clamp out with the cap', 1.6, dict(clamp_y=RAIL['park'])),
    ('Swing the pipette onto the axis: the cone seats', 1.4, dict(swing=0)),
    ('Press the plunger', 0.6, dict(plunger=PIP['stroke'])),
    ('Lower the pipette into the liquid', 1.4, dict(tip='dive')),
    ('Aspirate: release the plunger', 1.2, dict(plunger=0, fill=1)),
    ('Withdraw the pipette', 1.2, dict(tip=TIP_READY)),
    ('Swing the pipette out beside the harness', 1.4, dict(swing=STOW)),
    ('Slide the clamp back in, the cap high over the neck', 1.6, dict(clamp_y=0)),
    ('Lower the cap onto the thread', 0.9, dict(clift=CAP_LIFT)),
    ('Screw the cap back', 3.0, dict(turns=0, clift=0)),
    ('Open the iris', 0.9, dict(iris=IRIS_OPEN)),
    ('Lift the clamp clear of the cap', 0.9, dict(clift=LIFT_HI)),
    ('Slide the clamp out', 1.6, dict(clamp_y=RAIL['park'])),
    ('Put the bottle down', 1.2, dict(lift_z=0)),
    ('Open the gripper and lift the hand clear', 1.6, dict(grip='open', lift_z=LIFT_Z)),
]
TAIL = 0.8
_PAGE_TO_STATE = dict(lift_z='lift_z', grip='grip_aperture', clamp_y='clamp_y', clift='clamp_lift', iris='iris_angle',
                      turns='housing_turns', tip='pipette_tip', swing='swing_angle', plunger='plunger', fill='fill')


def _convert(key: str, v, b: dict):
    if key == 'grip':
        return 2 * (vertex(b['r']) if v == 'closed' else stroke(b['r'])) * MM
    if key == 'iris':
        return iris_contact(b) if v == 'contact' else v
    if key == 'tip':
        return (base_z(b) + TIP_DIVE) * MM if v == 'dive' else v * MM
    if key in ('lift_z', 'clamp_y', 'clift', 'plunger'):
        return v * MM
    if key == 'swing':
        return v * DEG
    return v


def keys(b: dict = BOTTLE) -> list[tuple[float, dict]]:
    """(time, state) at the start and after every step, for bottle b."""
    out = [(0.0, start(b))]
    for _, dur, delta in STEPS:
        t, last = out[-1]
        s = dict(last)
        for k, v in delta.items():
            s[_PAGE_TO_STATE[k]] = _convert(k, v, b)
        out.append((t + dur, s))
    return out


KEYS = keys()
DURATION = KEYS[-1][0]


def step_end(n: int, frames=KEYS) -> float:
    """The time step n (1-based) ends."""
    return frames[n][0]


def ease(x: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, x)))


def state_at(t: float, frames=KEYS) -> tuple[dict, int]:
    """The state at time t (the page's easing) and the step under way (0-based, -1 after the end).

    The last step opens the jaws first and lifts after, as the page does.
    """
    for i in range(1, len(frames)):
        if t < frames[i][0]:
            (ta, a), (tb, b) = frames[i - 1], frames[i]
            f = ease((t - ta) / (tb - ta))
            s = {k: a[k] + (b[k] - a[k]) * f for k in a}
            if i == len(frames) - 1:
                g, m = ease(2 * (t - ta) / (tb - ta)), ease(2 * (t - ta) / (tb - ta) - 1)
                s['grip_aperture'] = a['grip_aperture'] + (b['grip_aperture'] - a['grip_aperture']) * g
                s['lift_z'] = a['lift_z'] + (b['lift_z'] - a['lift_z']) * m
            return s, i - 1
    return dict(frames[-1][1]), -1


def attachments(state: dict, b: dict = BOTTLE) -> tuple[bool, bool]:
    """(bottle held in the hand, cap held in the clamp): the page's parenting rule."""
    held = state['grip_aperture'] <= 2 * vertex(b['r']) * MM + 0.3 * MM
    in_clamp = state['housing_turns'] > 1e-4
    return held, in_clamp


# ============================== JOINT TREE (SI) ==============================
# Every joint is linear in one property: q = coef * state[prop], about/along `axis` of the
# link frame. The mount pose (pos, yaw) is relative to the parent link's joint frame.
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
_X, _Y, _Z = (-1, 0, 0), (0, -1, 0), (0, 0, -1)
IRIS_MAX = IRIS['blade_max'] * DEG


def _links() -> list[dict]:
    def link(name, parent, pos, joint, yaw=0.0, mass=0.05):
        typ, axis, prop, coef, rng = joint
        return dict(name=name, parent=parent, pos=tuple(p * MM for p in pos), yaw=yaw, mass=mass,
                    joint=dict(name=name, type=typ, axis=axis, prop=prop, coef=coef, range=rng))

    jaw_lo, jaw_hi = PROPS['grip_aperture'][1] / 2, PROPS['grip_aperture'][2] / 2
    links = [
        link('hand', None, (0, 0, 0), ('slide', Z, 'lift_z', 1.0, (0.0, 0.3)), mass=3.0),
        link('jaw_l', 'hand', (0, 0, GRIP_Z), ('slide', Y, 'grip_aperture', 0.5, (jaw_lo, jaw_hi)), mass=0.12),
        link('jaw_r', 'hand', (0, 0, GRIP_Z), ('slide', _Y, 'grip_aperture', 0.5, (jaw_lo, jaw_hi)), mass=0.12),
        link('clamp_slide', 'hand', (0, 0, 0), ('slide', Y, 'clamp_y', 1.0, (0.0, PROPS['clamp_y'][2])), mass=0.3),
        link('clamp_lift', 'clamp_slide', (0, 0, Z_IRIS), ('slide', Z, 'clamp_lift', 1.0, (0.0, PROPS['clamp_lift'][2])), mass=0.35),
        link('housing', 'clamp_lift', (0, 0, 0), ('hinge', Z, 'housing_turns', TAU, (0.0, (TURNS + 0.5) * TAU)), mass=0.3),
        link('cam', 'housing', (0, 0, 0), ('hinge', _Z, 'iris_angle', 1.0, (0.0, IRIS_MAX)), mass=0.05),
        link('sun', 'housing', (0, 0, 0), ('hinge', Z, 'iris_angle', 3.0, (0.0, 3 * IRIS_MAX)), mass=0.01),
    ]
    for k in range(3):
        a = k * TAU / 3
        links.append(link(f'planet_{k}', 'housing', (IRIS['planet_r'] * math.cos(a), IRIS['planet_r'] * math.sin(a), 0),
                          ('hinge', _Z, 'iris_angle', 3.0, (0.0, 3 * IRIS_MAX)), mass=0.01))
    for k in range(IRIS['n_blades']):
        phi = k * TAU / IRIS['n_blades']
        links.append(link(f'blade_{k}', 'housing', (IRIS['r_pivot'] * math.cos(phi), IRIS['r_pivot'] * math.sin(phi), k * IRIS['blade_t']),
                          ('hinge', Z, 'iris_angle', 1.0, (0.0, IRIS_MAX)), yaw=phi, mass=0.005))
    links += [
        link('pip_slide', 'hand', (0, 0, 0), ('slide', Z, 'pipette_tip', 1.0, (PROPS['pipette_tip'][1], PROPS['pipette_tip'][2])), mass=0.25),
        link('pip_swing', 'pip_slide', (PIVOT['x'], PIVOT['y'], 0), ('hinge', Z, 'swing_angle', 1.0, (0.0, STOW * DEG)), mass=0.2),
        link('plunger', 'pip_swing', (-PIVOT['x'], -PIVOT['y'], 0), ('slide', _Z, 'plunger', 1.0, (0.0, PIP['stroke'] * MM)), mass=0.01),
    ]
    return links


LINKS = _links()
LINK = {b['name']: b for b in LINKS}
# The joints the plan drives; every other joint follows one of these (MJCF equalities, URDF mimics).
ACTUATED = ['lift', 'jaw_l', 'clamp_y', 'clamp_lift', 'body_yaw', 'cam', 'pip_slide', 'pip_swing', 'plunger']
# link -> joint name in the MJCF/URDF (the link and its joint share a name, except these three)
JOINT_NAME = {'hand': 'lift', 'clamp_slide': 'clamp_y', 'housing': 'body_yaw'}
FOLLOWS = {   # follower joint -> (leader joint, multiplier): q_follower = k * q_leader
    'jaw_r': ('jaw_l', 1.0), 'sun': ('cam', 3.0),
    **{f'planet_{k}': ('cam', 3.0) for k in range(3)},
    **{f'blade_{k}': ('cam', 1.0) for k in range(IRIS['n_blades'])},
}
# Points to check the four outputs against each other: (link, position in the link frame, m)
SITES = {
    'jaw_l_vertex': ('jaw_l', (0, 0, 0)),
    'jaw_r_vertex': ('jaw_r', (0, 0, 0)),
    'cap_seat': ('housing', (0, 0, IRIS['cap_dz'] * MM)),
    'blade_0_tip': ('blade_0', (IRIS['blade_w'] / 2 * MM, IRIS['blade_len'] * MM, 0)),
    'tip': ('pip_swing', (-PIVOT['x'] * MM, -PIVOT['y'] * MM, 0)),
    'button': ('plunger', (PIP['plunger_x'] * MM, 0, BTN_TOP * MM)),
}


def joint_name(link: str) -> str:
    return JOINT_NAME.get(link, link)


def joints(state: dict) -> dict[str, float]:
    """Every joint's value (m or rad) for a state."""
    return {joint_name(b['name']): b['joint']['coef'] * state[b['joint']['prop']] for b in LINKS}


def rotz(a: float) -> np.ndarray:
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def _link_pose(name: str, q: dict, cache: dict) -> tuple[np.ndarray, np.ndarray]:
    """(R, p) of a link's joint frame in the world."""
    if name in cache:
        return cache[name]
    b = LINK[name]
    if b['parent'] is None:
        R0, p0 = np.eye(3), np.zeros(3)
    else:
        R0, p0 = _link_pose(b['parent'], q, cache)
    R = R0 @ rotz(b['yaw'])
    p = p0 + R0 @ np.array(b['pos'])
    j, v = b['joint'], q[joint_name(name)]
    axis = np.array(j['axis'], float)
    if j['type'] == 'slide':
        p = p + R @ (axis * v)
    else:
        R = R @ rotz(v * float(np.sign(axis[2])))
    cache[name] = (R, p)
    return cache[name]


def fk(state: dict) -> dict[str, np.ndarray]:
    """World positions of SITES for a state (the hand's base at the world origin)."""
    q, cache = joints(state), {}
    return {k: _link_pose(link, q, cache)[1] + _link_pose(link, q, cache)[0] @ np.array(pos)
            for k, (link, pos) in SITES.items()}


def quat_z(a: float) -> tuple[float, float, float, float]:
    """(w, x, y, z) of a rotation about Z."""
    return (math.cos(a / 2), 0.0, 0.0, math.sin(a / 2))


if __name__ == '__main__':
    s = start()
    print(f'{len(STEPS)} steps, {DURATION:.1f} s; start: ' + ', '.join(f'{k}={v:.4g}' for k, v in s.items()))
    for n in (2, 7, 12):
        st, _ = state_at(step_end(n) - 1e-6)
        pos = fk(st)
        print(f'after step {n}: tip {np.round(pos["tip"], 4)}, cap seat {np.round(pos["cap_seat"], 4)}, '
              f'jaw {np.round(pos["jaw_l_vertex"], 4)}')
