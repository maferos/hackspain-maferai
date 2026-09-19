"""The uncap-and-pipette hand: one description for the viewer, MuJoCo, Isaac Lab and Blender.

The UR10e's wrist_3 flange with the Robotiq 2F-85 holds a bottle from the
side; an iris clamp on a 90 degree hinge unscrews its cap and swings it clear;
a micropipette in a swing frame on a vertical slide goes down the neck. The
layout constants below, the body tree ``tree()`` and the couplings
``JOINT_MAP`` are read by

* ``generate_iris_pipette_viewer.py`` (the HTML page at the repository root),
* ``generate_iris_pipette_scene.py`` (MJCF for MuJoCo, URDF for Isaac Lab),
* ``generate_iris_pipette_blend.py`` (the .blend, with drivers),
* ``iris_pipette_plan.py`` (the sequence the three of them play),

so the four cannot disagree. Only numpy and the two asset zips are needed:
Isaac's Python and Blender's have no MuJoCo. The 2F-85 itself is not in the
tree: the viewer and the .blend take its finger linkage from hand_linkage.py,
the simulators attach ``assets/robotiq_2f85_sensed``.

Frame: "hand", the frame the arm moves. Origin on the bottle's axis at the
base of the reference bottle (80 mm tall; a taller bottle only reaches further
down), +X from the arm to the bottle, Z up. In it the arm's tool frame sits at
``(flange_x, 0, GRIP_Z)`` with ``TOOL_QUAT``: tool +Z (the fingers) along +X,
the jaws closing along Y. Every joint is at its body's origin and reads zero in
the pose drawn here.
"""
import math
import zipfile
from functools import lru_cache
from pathlib import Path

import numpy as np

SIM = Path(__file__).resolve().parents[1]
ROOT = SIM.parent
IRIS_ZIP = ROOT / 'assets/iris_clamp/iris_clamp_sim_asset.zip'
PIPETTE_ZIP = ROOT / 'assets/micropipette/micropipette_asset.zip'

# Iris clamp, from iris_clamp/params.py.
IRIS = {
    'n_sun': 20, 'n_planet': 20, 'n_ring': 60, 'planet_r': 0.024,
    'n_blades': 6, 'r_pivot': 0.055, 'blade_dz': 0.0025,
    'blade_max': math.radians(76), 'cap_r': 0.014, 'cap_h': 0.018,
    'pitch': 0.0025, 'turns': 2.0, 'bottle_h': 0.08,
    # The cap in the clamp frame at contact, as in mujoco/bottle_cap.xml.
    'cap_z': -0.0015,
}
IRIS_PARTS = ['body', 'cam_ring', 'sun', 'planet', 'blade', 'cap']   # the bottle is drawn to size on the page
# Masses from iris_clamp.xml.
IRIS_MASS = {'sun': 0.02, 'body': 0.35, 'cam_ring': 0.06, 'planet': 0.004, 'blade': 0.006, 'cap': 0.012}

# Micropipette parts by link, with their material (pipette_geometry.py).
PIPETTE_PARTS = {
    'body': {'tip_cone': 'dark', 'shaft': 'blue', 'collar': 'blue',
             'body': 'white', 'finger_hook': 'white', 'display': 'display',
             'label_ridge': 'white', 'ejector_guide': 'white'},
    'plunger': {'plunger_shaft': 'white', 'plunger_button': 'blue'},
    'ejector': {'ejector_rod': 'blue', 'ejector_button': 'blue',
                'ejector_sleeve': 'blue', 'ejector_arm': 'blue'},
}
PIPETTE_MASS = {'body': 0.1, 'plunger': 0.01, 'ejector': 0.005}
PIPETTE_GRIP_Z = 0.1685          # grip site on the handle (micropipette_meta.json)
PLUNGER_STROKE = 0.014
# Collision primitives of micropipette.xml, by link: (type, pos, size). Capsules
# and cylinders run along Z; the ejector never moves here, so it rides the body.
PIPETTE_COLLISION = {
    'body': [('box', (0, 0, 0.1685), (0.0135, 0.011, 0.0525)),
             ('capsule', (0, 0, 0.064), (0.0058, 0.052)),
             ('capsule', (0, 0, 0.00725), (0.0036, 0.00675)),
             ('cylinder', (0, 0, 0.11), (0.0112, 0.006)),
             ('box', (-0.021, 0, 0.213), (0.009, 0.008, 0.012)),
             ('box', (0.0155, 0, 0.154), (0.0035, 0.005, 0.028)),
             ('cylinder', (0.019, 0, 0.235), (0.0075, 0.003)),
             ('cylinder', (0, 0, 0.08), (0.0068, 0.014))],
    'plunger': [('cylinder', (0.003, 0, 0.25925), (0.0085, 0.00425)),
                ('cylinder', (0.003, 0, 0.24), (0.004, 0.021))],
}

# ---- the assembly, in the hand frame ----------------------------------------
Z_IRIS = IRIS['bottle_h'] - IRIS['cap_z']   # iris plane when the blades meet the cap
NECK = {'r': 0.011, 'bore': 0.0085, 'h': 0.018}  # the bottle mesh's neck, under the cap
GRIP_Z = 0.046                   # jaws 34 mm below the shoulder
OPEN_APERTURE = 0.085
# Bottle, as set on the page: default and range. The 2F-85 base (8.5 mm above
# the jaws' bottom) keeps off the table down to 75 mm; the jaws open to 85 mm.
BOTTLE = {'h': (0.08, 0.075, 0.20), 'r': (0.026, 0.020, 0.040), 'level': 0.05}
BOTTLE_R = BOTTLE['r'][0]        # the reference bottle the simulators use
PAD_FIT = (0.03, 0.085)          # apertures the pad-position fit spans
# Hinge on the arm's side of the bottle, over the fingers and just ahead of
# the 2F-85 base, level with the iris plane: the cap starts straight up when
# the arm swings, so while it unscrews (5 mm) the hinge just follows it
# through asin(5/90) = 3.2 deg.
HINGE = (-0.09, Z_IRIS)
SIDE = math.copysign(1, HINGE[0])
IRIS_OPEN = math.acos(0.035 / IRIS['r_pivot'])   # 70 mm open, blades inside the housing
ALPHA_CONTACT = math.acos(IRIS['cap_r'] / IRIS['r_pivot'])   # blades on the cap
CAP_LIFT = IRIS['turns'] * IRIS['pitch']         # the cap rises this much while it unscrews
FOLLOW = math.asin(CAP_LIFT / abs(HINGE[0]))     # hinge angle that keeps the clamp on it
HINGE_UP = math.pi / 2
Z_LIFT = 0.10                    # how high the bottle is carried
# Pipette: a swing frame holds it by two rings on the handle and carries the
# plunger actuator; it turns on a vertical pin in the slide's carriage at
# PIVOT (x, y). Always at TIP_READY (tip just over the neck), it swings by
# STOW (negative: towards the arm) to stand beside the gripper, clear of the
# clamp at every hinge angle, and back in over the bottle once the clamp is up.
# The slide then only runs from the dive to TIP_READY.
PIVOT = (0.03, 0.09)
STOW = math.radians(-80)
YOKE_Y = PIVOT[1] + 0.028        # the mast's plane: the carriage behind the pin
TIP_READY = IRIS['bottle_h'] + NECK['h'] + 0.015
CLIPS = (0.125, PIPETTE_GRIP_Z)  # the frame's rings on the pipette, from the tip
CARRIAGE = (PIPETTE_GRIP_Z - 0.02, PIPETTE_GRIP_Z + 0.06)   # on the rail; the pin's bearings 80 mm apart
FRAME_TOP = 0.30                 # the frame and the actuator over the plunger button, from the tip
# It goes down the neck's bore until the ejector arm is NECK_CLEAR above the
# neck; the page sets the dive within that.
TIP_DIVE = 0.02                  # default dive: tip above the bottle floor
NECK_CLEAR = 0.004
# 2F-85 base: its top face and side faces in the hand frame, where the hinge
# cheeks bolt on.
BASE_TOP = GRIP_Z + 0.0375
BASE_Y = 0.0375
RAIL_TOP = TIP_READY + CARRIAGE[1]
MAST_BOTTOM = 0.07
WEB = math.atan2(-PIVOT[1], -PIVOT[0])   # the frame's web, from the pin towards the bottle axis
WEB_LEN = math.hypot(*PIVOT)

# Tool frame in the hand frame: tool X = hand Y, tool Y = hand Z, tool Z = hand X
# (a 120 degree turn about (1, 1, 1)). MuJoCo order, (w, x, y, z).
TOOL_QUAT = (0.5, 0.5, 0.5, 0.5)

# Colours of the parts drawn here (the 2F-85's are in hand_linkage.MATERIALS).
RIG_MATERIALS = {
    'housing': (0.09, 0.10, 0.11, 1), 'gold': (0.83, 0.65, 0.24, 1),
    'bracket': (0.44, 0.49, 0.55, 1), 'cap': (0.85, 0.20, 0.17, 1),
    'bottle': (0.82, 0.48, 0.11, 0.5), 'liquid': (0.31, 0.61, 0.85, 0.6),
    'white': (0.93, 0.93, 0.92, 1), 'blue': (0.41, 0.58, 0.87, 1),
    'dark': (0.06, 0.06, 0.07, 1), 'display': (0.02, 0.02, 0.02, 1),
}

# ---- the state and the joints ------------------------------------------------
# What the page's sliders, the .blend's properties and the plan's targets share.
STATE = ('lift_z', 'grip_aperture', 'hinge_angle', 'iris_angle', 'housing_turns',
         'pipette_tip', 'swing_angle', 'plunger')
# Joint value = offset + sum(coef * state), linear on purpose: the same map is a
# Blender driver expression, a MuJoCo target and a URDF mimic ratio. The
# planetary train: n_sun q_sun + n_ring q_cam - n_sun q_body = 0, the blades
# follow the cam ring 1:1 and the planets mesh with the sun. grip_aperture is
# not here: the finger linkage is the polynomial fit of hand_linkage.py.
TWO_PI = 2 * math.pi
JOINT_MAP = {
    'lift': (0.0, {'lift_z': 1.0}),
    'clamp_swing': (0.0, {'hinge_angle': 1.0}),
    'sun_input': (0.0, {'iris_angle': IRIS['n_ring'] / IRIS['n_sun'], 'housing_turns': TWO_PI}),
    'body_yaw': (0.0, {'housing_turns': TWO_PI}),
    'cam': (0.0, {'iris_angle': -1.0}),
    **{f'planet_{k}': (0.0, {'iris_angle': -IRIS['n_ring'] / IRIS['n_planet']}) for k in range(3)},
    **{f'blade_{k}': (0.0, {'iris_angle': 1.0}) for k in range(IRIS['n_blades'])},
    'pipette_slide': (-TIP_READY, {'pipette_tip': 1.0}),
    'pipette_swing': (0.0, {'swing_angle': 1.0}),
    'pipette_plunger_slide': (0.0, {'plunger': -1.0}),
}
# The joints the simulators drive; the rest follow through equalities (MJCF) or
# mimics (URDF), except sun_input, which the URDF drives to yaw - 3 cam.
ACTUATED = ['lift', 'right_driver_joint', 'clamp_swing', 'cam', 'body_yaw',
            'pipette_slide', 'pipette_swing', 'pipette_plunger_slide']


def joint_values(state: dict) -> dict:
    """Every joint in JOINT_MAP at a state."""
    return {name: offset + sum(c * state[k] for k, c in coefs.items())
            for name, (offset, coefs) in JOINT_MAP.items()}


# ---- quaternions (w, x, y, z), as MuJoCo has them ---------------------------


def qmul(a, b) -> np.ndarray:
    w1, x1, y1, z1 = a
    w2, x2, y2, z2 = b
    return np.array([w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
                     w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
                     w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
                     w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2])


def qconj(q) -> np.ndarray:
    return np.array([q[0], -q[1], -q[2], -q[3]])


def qrot(q, v) -> np.ndarray:
    """Rotate a vector by a quaternion."""
    return qmul(qmul(q, (0.0, *v)), qconj(q))[1:]


def axis_quat(axis, angle) -> np.ndarray:
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    return np.array([math.cos(angle / 2), *(math.sin(angle / 2) * axis)])


def zrot(angle) -> list:
    return axis_quat((0, 0, 1), angle).tolist()


# Primitives here run along their local Z, as in MuJoCo; these lay them along X or Y.
AXIS_QUAT = {'z': [1.0, 0.0, 0.0, 0.0],
             'x': axis_quat((0, 1, 0), math.pi / 2).tolist(),
             'y': axis_quat((1, 0, 0), -math.pi / 2).tolist()}   # +Z onto +Y


def inverse_pose(pos, quat) -> tuple[list, list]:
    """The pose of the parent frame seen from a child at (pos, quat)."""
    inv = qconj(quat)
    return (-qrot(inv, pos)).tolist(), inv.tolist()


# ---- the meshes in the zips -------------------------------------------------


def zip_member(archive: zipfile.ZipFile, suffix: str) -> bytes:
    (name,) = [n for n in archive.namelist() if n.endswith(suffix)]
    return archive.read(name)


def stl_bytes(raw: bytes, scale: float = 1.0) -> np.ndarray:
    """Triangles of a binary STL held in memory, (n, 3, 3)."""
    count = int(np.frombuffer(raw, np.uint32, 1, 80)[0])
    record = np.dtype([('normal', '<f4', 3), ('v', '<f4', (3, 3)), ('attr', '<u2')])
    return np.frombuffer(raw, record, count, 84)['v'].astype(np.float64) * scale


@lru_cache(maxsize=None)
def pipette_mesh(part: str) -> np.ndarray:
    with zipfile.ZipFile(PIPETTE_ZIP) as archive:
        return stl_bytes(zip_member(archive, f'meshes/{part}.stl'))


@lru_cache(maxsize=None)
def pipette_dims() -> dict:
    """What the frame is built around: the handle's half width, the plunger
    button's top and centre, and how far the tip may go down a neck."""
    body = pipette_mesh('body').reshape(-1, 3)
    button = pipette_mesh('plunger_button').reshape(-1, 3)
    arm_z = float(pipette_mesh('ejector_arm')[..., 2].min())
    return {'half_d': float(body[:, 1].max()), 'btn_top': float(button[:, 2].max()),
            'btn_x': float((button[:, 0].min() + button[:, 0].max()) / 2),
            # the tip's lowest height: the ejector arm NECK_CLEAR above the neck
            'tip_min': IRIS['bottle_h'] + NECK['h'] + NECK_CLEAR - arm_z}


def dive_z(floor: float = 0.0, dive: float = TIP_DIVE) -> float:
    """The tip's height at the dive, in the hand frame: `dive` above the
    bottle's floor, but never below what the ejector arm allows."""
    return max(floor + dive, pipette_dims()['tip_min'])


# ---- the body tree ---------------------------------------------------------------
# Body = {name, parent, pos, quat, joint: None | {name, type, axis, range},
#         geoms: [Geom], sites: [{name, pos}], mass: None | float}
# Geom = {name, type: box|cylinder|capsule|cone|mesh, pos, quat, size, mesh,
#         material, collide: None | class, visible, mass}
# Sizes are half extents (box) or [radius, half length] (cylinder, capsule,
# cone); a cone's apex is at +Z. Collision classes: 'clamp' and 'pipette' meet
# each other, the pipette also meets the bottle and the floor; brackets are
# visual only.


def _geom(name, kind, pos, quat, size, material, mesh=None, collide=None,
          visible=True, mass=None) -> dict:
    return {'name': name, 'type': kind, 'pos': [float(v) for v in pos],
            'quat': [float(v) for v in quat], 'size': [float(v) for v in size],
            'mesh': mesh, 'material': material, 'collide': collide,
            'visible': visible, 'mass': mass}


def box(name, x0, x1, y0, y1, z0, z1, material, **kw) -> dict:
    """A box by its faces, in any order."""
    return _geom(name, 'box', ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), AXIS_QUAT['z'],
                 (abs(x1 - x0) / 2, abs(y1 - y0) / 2, abs(z1 - z0) / 2), material, **kw)


def cyl(name, r, length, axis, pos, material, **kw) -> dict:
    return _geom(name, 'cylinder', pos, AXIS_QUAT[axis], (r, length / 2), material, **kw)


def mesh(name, mesh_key, material, pos=(0, 0, 0), quat=(1, 0, 0, 0), **kw) -> dict:
    return _geom(name, 'mesh', pos, quat, (1.0,), material, mesh=mesh_key, **kw)


def body(name, parent, pos=(0, 0, 0), quat=(1, 0, 0, 0), joint=None, geoms=(),
         sites=(), mass=None) -> dict:
    return {'name': name, 'parent': parent, 'pos': [float(v) for v in pos],
            'quat': [float(v) for v in quat], 'joint': joint, 'geoms': list(geoms),
            'sites': list(sites), 'mass': mass}


def hinge(name, axis, lo=None, hi=None) -> dict:
    return {'name': name, 'type': 'hinge', 'axis': list(axis),
            'range': None if lo is None else [lo, hi]}


def slide(name, axis, lo, hi) -> dict:
    return {'name': name, 'type': 'slide', 'axis': list(axis), 'range': [lo, hi]}


def tool_pose(flange_x: float) -> tuple[list, list]:
    """The arm's tool frame in the hand frame."""
    return [flange_x, 0.0, GRIP_Z], list(TOOL_QUAT)


def tree(flange_x: float, dive: float = TIP_DIVE) -> list[dict]:
    """The bodies on the hand, parents first, for the reference bottle.

    Args:
        flange_x: where the flange sits behind the bottle axis so the pads
            close on it (the pad fit of the 2F-85, negative).
        dive: the tip's depth above the bottle floor; the rail is cut to it.
    """
    HX, HZ = HINGE
    PX, PY = PIVOT
    C0, C1 = CARRIAGE
    YY = YOKE_Y
    dims = pipette_dims()
    HALF_D, BTN_TOP, BTN_X = dims['half_d'], dims['btn_top'], dims['btn_x']
    FTOP, FBOT = BTN_TOP + 0.037, CLIPS[0] - 0.008        # the frame's web, from the tip
    CY0, CY1 = YY - 0.019, YY - 0.007                    # carriage faces
    tip_dive = dive_z(0.0, dive)

    def ax(u):
        """x of a point u from the hinge towards the bottle."""
        return HX - SIDE * u

    bodies = []

    # The hand frame hangs off wrist_3_link, on the gripper body. Two cheeks on
    # the sides of the 2F-85 base carry the hinge axle just ahead of it, over
    # the fingers; an arm out of the +Y cheek carries the pipette's mast.
    frame_geoms = []
    for s in (-1, 1):
        tag = 'p' if s > 0 else 'n'
        frame_geoms += [
            box(f'cheek_{tag}', -0.14, -0.106, s * BASE_Y, s * (BASE_Y + 0.006), 0.035, BASE_TOP, 'bracket'),
            box(f'cheek_arm_{tag}', -0.106, ax(-0.008), s * BASE_Y, s * (BASE_Y + 0.006), HZ - 0.008, BASE_TOP, 'bracket'),
        ]
    frame_geoms += [
        cyl('axle', 0.004, 2 * BASE_Y + 0.016, 'y', (HX, 0, HZ), 'bracket'),
        cyl('hinge_motor', 0.009, 0.022, 'y', (HX, -BASE_Y - 0.017, HZ), 'housing'),
        box('mast_arm', -0.135, -0.112, BASE_Y + 0.006, YY + 0.009, 0.07, 0.082, 'bracket'),   # behind the fingers
        box('mast_arm_out', -0.135, PX + 0.016, YY - 0.003, YY + 0.009, 0.07, 0.082, 'bracket'),   # past them to the mast
        box('mast', PX - 0.016, PX + 0.016, YY - 0.003, YY + 0.009, MAST_BOTTOM, RAIL_TOP + 0.005, 'bracket'),
        box('rail', PX - 0.006, PX + 0.006, YY - 0.007, YY - 0.003, tip_dive + C0, RAIL_TOP, 'housing'),
    ]
    pos, quat = inverse_pose(*tool_pose(flange_x))
    bodies.append(body('hand_frame', 'wrist_3_link', pos, quat, geoms=frame_geoms))

    # Swing arm on the axle; +q swings the clamp up, towards the hinge's side.
    bodies.append(body('clamp_swing', 'hand_frame', (HX, 0, HZ),
                       joint=hinge('clamp_swing', (0, SIDE, 0), 0.0, HINGE_UP), mass=0.02))   # the axle's collar
    # The clamp frame: its iris plane on the bottle axis when the arm is down.
    # The arm leaves the knuckle low and close, so that swung back it lies
    # above the 2F-85 base and the flange.
    bodies.append(body('clamp_mount', 'clamp_swing', (-HX, 0, Z_IRIS - HZ), geoms=[
        cyl('knuckle', 0.008, 2 * BASE_Y - 0.004, 'y', (HX, 0, 0), 'bracket'),
        box('clamp_foot', ax(0), ax(0.017), -0.012, 0.012, -0.005, 0.008, 'bracket'),      # on the knuckle
        box('clamp_post', ax(0.011), ax(0.017), -0.012, 0.012, 0.004, 0.072, 'bracket'),   # 4 mm off the housing
        box('clamp_bridge', ax(0.011), 0, -0.012, 0.012, 0.064, 0.072, 'bracket'),        # to the mount
        cyl('mount_disc', 0.02, 0.004, 'z', (0, 0, 0.062), 'housing'),
        cyl('sun_motor', 0.016, 0.028, 'z', (0, 0, 0.086), 'housing'),
        # the housing and the motor as one envelope, for the pipette to keep off
        cyl('clamp_envelope', 0.069, 0.064, 'z', (0, 0, 0.028), None, collide='clamp', visible=False),
        cyl('motor_envelope', 0.016, 0.04, 'z', (0, 0, 0.08), None, collide='clamp', visible=False),
    ]))
    # Iris clamp rig, as in mujoco/iris_clamp.xml: sun on the mount, the
    # carrier (housing) turns about the axis, the cam ring, planets and blades
    # in it.
    bodies.append(body('sun', 'clamp_mount', joint=hinge('sun_input', (0, 0, 1)),
                       geoms=[mesh('sun', 'iris/sun', 'gold', mass=IRIS_MASS['sun'])]))
    bodies.append(body('carrier', 'clamp_mount', joint=hinge('body_yaw', (0, 0, 1)),
                       geoms=[mesh('housing', 'iris/body', 'housing', mass=IRIS_MASS['body'])],
                       sites=[{'name': 'cap_seat', 'pos': [0, 0, IRIS['cap_z']]}]))
    bodies.append(body('cam_ring', 'carrier', joint=hinge('cam', (0, 0, 1), -IRIS['blade_max'], 0.0),
                       geoms=[mesh('cam_ring', 'iris/cam_ring', 'gold', mass=IRIS_MASS['cam_ring'])]))
    for k in range(3):
        a = k * TWO_PI / 3
        bodies.append(body(f'planet_{k}', 'carrier', (IRIS['planet_r'] * math.cos(a), IRIS['planet_r'] * math.sin(a), 0),
                           joint=hinge(f'planet_{k}', (0, 0, 1)),
                           geoms=[mesh(f'planet_{k}', 'iris/planet', 'housing', mass=IRIS_MASS['planet'])]))
    for k in range(IRIS['n_blades']):
        phi = k * TWO_PI / IRIS['n_blades']
        bodies.append(body(f'blade_{k}', 'carrier',
                           (IRIS['r_pivot'] * math.cos(phi), IRIS['r_pivot'] * math.sin(phi), k * IRIS['blade_dz']),
                           zrot(phi), joint=hinge(f'blade_{k}', (0, 0, 1), 0.0, IRIS['blade_max']),
                           geoms=[mesh(f'blade_{k}', 'iris/blade', 'gold', mass=IRIS_MASS['blade'])]))

    # Pipette: a slide beside the bottle (the mast and rail above are on the
    # hand frame; the carriage rides here) and a swing frame on a vertical pin
    # in the carriage. The frame holds the pipette by two rings and carries the
    # plunger actuator. At a fixed height, tip just over the neck, it swings
    # the pipette out to the arm's side while the clamp works; swung in, a cone
    # seats in a receiver and the self-locking gearmotor holds it, and only
    # then does the slide go down.
    seat_quat = zrot(WEB)
    seat = np.array([PX, PY, 0.0])
    receiver = seat + qrot(seat_quat, (0.021, 0.016, C0 + 0.04))       # cone receiver, ahead of the web
    bodies.append(body('pipette_slide', 'hand_frame', (0, 0, TIP_READY),
                       joint=slide('pipette_slide', (0, 0, 1), dims['tip_min'] - TIP_READY, 0.0), geoms=[
        box('carriage', PX - 0.016, PX + 0.016, CY0, CY1, C0, C1, 'bracket'),
        box('bearing_lug_lo', PX - 0.016, PX + 0.016, PY, CY0, C0, C0 + 0.012, 'bracket'),
        box('bearing_lug_hi', PX - 0.016, PX + 0.016, PY, CY0, C1 - 0.012, C1, 'bracket'),
        box('swing_motor', PX + 0.016, PX + 0.046, CY0, CY1 + 0.006, C1 - 0.034, C1, 'housing'),
        _geom('cone_receiver', 'box', receiver, seat_quat, (0.009, 0.008, 0.01), 'housing'),
    ]))
    held = np.array([-PX, -PY, 0.0])   # the frame's origin is the pin; the pipette is back on the bottle axis
    swing_geoms = [
        cyl('pin', 0.005, C1 - C0 + 0.012, 'z', (0, 0, (C0 + C1) / 2), 'bracket'),
        _geom('web', 'box', qrot(seat_quat, ((0.005 + WEB_LEN - HALF_D - 0.004) / 2, 0, (FBOT + FTOP) / 2)), seat_quat,
              ((WEB_LEN - HALF_D - 0.009) / 2, 0.004, (FTOP - FBOT) / 2), 'bracket'),
        # locator cone, apex towards the receiver (+Y of the web)
        _geom('cone_locator', 'cone', qrot(seat_quat, (0.021, 0.009, C0 + 0.04)),
              qmul(seat_quat, AXIS_QUAT['y']), (0.005, 0.005), 'bracket'),
        box('actuator_arm', *(held[0] + np.array([-0.006, 0.006])), *(held[1] + np.array([-0.006, HALF_D + 0.008])),
            BTN_TOP + 0.025, FTOP, 'bracket'),
        cyl('plunger_actuator', 0.009, 0.036, 'z', held + (BTN_X, 0, BTN_TOP + 0.028), 'housing'),
    ]
    for i, z in enumerate(CLIPS):                                       # two rings on the handle
        for j, (x0, x1, y0, y1) in enumerate([(-0.019, 0.019, HALF_D, HALF_D + 0.005),
                                              (-0.019, -0.0155, -0.004, HALF_D + 0.005),
                                              (0.0155, 0.019, 0.005, HALF_D + 0.005)]):   # clear of the ejector rod
            swing_geoms.append(box(f'ring_{i}_{j}', held[0] + x0, held[0] + x1, held[1] + y0, held[1] + y1,
                                   z - 0.008, z + 0.008, 'bracket'))
    for link in ('body', 'ejector'):
        for part, material in PIPETTE_PARTS[link].items():
            swing_geoms.append(mesh(f'pipette_{part}', f'pipette/{part}', material, held,
                                    mass=PIPETTE_MASS[link] if part in ('body', 'ejector_rod') else 0.0))
    swing_geoms += [_geom(f'pipette_col_{i}', kind, held + p, AXIS_QUAT['z'], size, None,
                          collide='pipette', visible=False)
                    for i, (kind, p, size) in enumerate(PIPETTE_COLLISION['body'])]
    bodies.append(body('pipette_swing', 'pipette_slide', (PX, PY, 0),
                       joint=hinge('pipette_swing', (0, 0, 1), STOW, 0.0), geoms=swing_geoms,
                       sites=[{'name': 'pipette_tip', 'pos': held.tolist()}]))
    plunger_geoms = [mesh(f'pipette_{part}', f'pipette/{part}', material,
                          mass=PIPETTE_MASS['plunger'] if part == 'plunger_shaft' else 0.0)
                     for part, material in PIPETTE_PARTS['plunger'].items()]
    plunger_geoms.append(cyl('pusher', 0.003, 0.012, 'z', (BTN_X, 0, BTN_TOP + 0.006), 'bracket'))
    plunger_geoms += [_geom(f'plunger_col_{i}', kind, p, AXIS_QUAT['z'], size, None,
                            collide='pipette', visible=False)
                      for i, (kind, p, size) in enumerate(PIPETTE_COLLISION['plunger'])]
    bodies.append(body('pipette_plunger', 'pipette_swing', held,
                       joint=slide('pipette_plunger_slide', (0, 0, 1), -PLUNGER_STROKE, 0.0),
                       geoms=plunger_geoms))
    return bodies


def fk(bodies: list[dict], joints: dict, root: dict | None = None) -> dict:
    """World pose (pos, quat) of every body and site, given each joint's value.

    Args:
        bodies: the tree; a body whose parent is not in it hangs off `root`.
        joints: joint name -> value; a joint left out reads zero.
        root: name -> (pos, quat) of the frames the tree hangs from.
    """
    poses = dict(root or {})
    for b in bodies:
        ppos, pquat = poses.get(b['parent'], (np.zeros(3), np.array([1.0, 0, 0, 0])))
        pos = ppos + qrot(pquat, b['pos'])
        quat = qmul(pquat, b['quat'])
        j = b['joint']
        if j is not None:
            q = joints.get(j['name'], 0.0)
            if j['type'] == 'hinge':
                quat = qmul(quat, axis_quat(j['axis'], q))
            else:
                pos = pos + qrot(quat, np.asarray(j['axis'], float) * q)
        poses[b['name']] = (pos, quat)
        for s in b['sites']:
            poses[s['name']] = (pos + qrot(quat, s['pos']), quat)
    return poses


# ---- clearances -----------------------------------------------------------------


def clamp_gap(points: np.ndarray, hinge_angles) -> float:
    """Closest approach of hand-frame points to the clamp, over hinge angles.

    The clamp in its own frame: housing (R 69 mm, 60 mm tall), sun motor on
    top, the cap under the blades, the arm to the hinge. The points are
    brought into the clamp's frame at each hinge angle; the result is the
    smallest distance to those solids, negative inside one.
    """
    rx, rz, y = points[:, 0] - HINGE[0], points[:, 2] - HINGE[1], points[:, 1]
    cylinders = [(0.069, -0.004, 0.06), (0.016, 0.06, 0.10), (IRIS['cap_r'], -0.02, 0.02)]
    boxes = [(min(HINGE[0], 0), max(HINGE[0], 0), -0.012, 0.012, 0.064, 0.072),
             (HINGE[0] - 0.017, HINGE[0] + 0.017, -0.035, 0.035, -0.008, 0.072)]
    gap = np.inf
    for phi in hinge_angles:
        c, s = math.cos(-SIDE * phi), math.sin(-SIDE * phi)
        x = HINGE[0] + rx * c + rz * s
        z = -rx * s + rz * c
        r = np.hypot(x, y)
        for radius, z0, z1 in cylinders:
            d = np.stack([r - radius, np.maximum(z0 - z, z - z1)], 1)
            gap = min(gap, float(outside(d).min()))
        for x0, x1, y0, y1, z0, z1 in boxes:
            d = np.stack([np.maximum(x0 - x, x - x1), np.maximum(y0 - y, y - y1), np.maximum(z0 - z, z - z1)], 1)
            gap = min(gap, float(outside(d).min()))
    return gap


def outside(d: np.ndarray) -> np.ndarray:
    """Distance from per-axis excesses (positive outside a slab): Euclidean outside, depth inside."""
    return np.where((d > 0).any(1), np.linalg.norm(np.maximum(d, 0), axis=1), d.max(1))


def swung(points: np.ndarray, angle: float) -> np.ndarray:
    """Tip-frame points of the pipette and its frame in the hand frame, at TIP_READY, swung by angle."""
    c, s = math.cos(angle), math.sin(angle)
    x, y = points[:, 0] - PIVOT[0], points[:, 1] - PIVOT[1]
    return np.stack([PIVOT[0] + c * x - s * y, PIVOT[1] + s * x + c * y, points[:, 2] + TIP_READY], 1)


def frame_points() -> np.ndarray:
    """The frame's web, from the pipette to the pin, as points (tip frame)."""
    length = math.hypot(*PIVOT)
    toward = np.array(PIVOT) / length
    return np.array([[*(toward * t), z] for t in np.linspace(0.016, length, 15)
                     for z in np.linspace(CLIPS[0] - 0.008, FRAME_TOP, 12)])


def check_clearances() -> tuple[float, float]:
    """The swung-out pipette against the clamp at every hinge angle, and along
    its swing with the clamp swung up.

    Returns:
        The two clearances in metres.

    Raises:
        RuntimeError: If either is under 5 mm.
    """
    parts = [pipette_mesh(part).reshape(-1, 3) for link in PIPETTE_PARTS.values() for part in link]
    pts = np.concatenate([np.unique(np.concatenate(parts).round(3), axis=0), frame_points()])
    out = clamp_gap(swung(pts, STOW), np.radians(np.linspace(0, 90, 46)))
    path = min(clamp_gap(swung(pts, a), [HINGE_UP]) for a in np.linspace(0, STOW, 17))
    centre = swung(np.zeros((1, 3)), STOW)[0]
    print(f'pipette swung {math.degrees(STOW):.0f} deg to ({centre[0] * 1000:.0f}, {centre[1] * 1000:.0f}) mm: '
          f'{out * 1000:.1f} mm clear of the clamp there, {path * 1000:.1f} mm on the way')
    if min(out, path) < 0.005:
        raise RuntimeError('the swinging pipette hits the clamp: move PIVOT or STOW')
    return out, path
