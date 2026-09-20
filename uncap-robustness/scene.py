"""The MuJoCo model of one trial: the uncap-and-pipette hand on a 6-DoF
carriage, one amber bottle standing free on the floor, its cap on a thread.

Everything physical that the shipped scene (simulation/models/
iris_pipette_scene.xml) does with welds is done here by contact:

* the bottle is a free body held only by the 2F-85's pads (friction);
* the cap is a free body welded to a thread follower on the bottle, a slide
  and a hinge coupled by a joint equality lift = pitch/2pi * spin (the iris
  clamp kit's own recipe, mujoco/bottle_cap.xml); the blades, given the kit's
  collision boxes, grip it by friction and turn it; after `turns` turns the
  thread lets go (trial.py switches the weld and the equality off);
* the pipette meets the bottle's hollow collision, the clamp's envelope and
  the floor; the rig meets the floor, so a hand driven into the table shows.

The rig is simulation/assets/ur10e_iris_pipette/ur10e_iris_pipette.xml,
read as it is; only this copy in memory is changed (blade boxes, gravity
compensation, the hand frame slid to the bottle's diameter, contact masks).

Frames: the carriage's origin is the hand frame's (iris_pipette_rig.py): on
the bottle's axis, at the height where the reference bottle's base would be.
Joints, outermost first: slides x, y, z; yaw about z through that origin;
pitch about the jaw axis (hand Y) through the pads' centre, (0, 0, PADS_Z).

Version 2 of the hand (README.md, "v2"), also in memory only:

* the gripper's axis sits 20 mm under the cap seat instead of 34 mm, so its
  base clears the table 14 mm sooner (the clamp's housing, 2.5 mm under the
  seat, still clears the fingers under it);
* L fingertips: each pad is moved 15 mm down, on the same face plane, so the
  pads grip the bottle where they did (43.1 mm up the hand frame, was 44.1);
* the iris closes to 80 degrees instead of 76, for the PP18 and PP20 caps;
* the housing may turn past its zero turn, so the recap can seat the cap.
"""
import json
import math
import os
import sys
from functools import lru_cache
from pathlib import Path

import mujoco
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SIM = ROOT / 'simulation'
sys.path.insert(0, str(SIM / 'scripts'))
sys.path.insert(0, str(HERE))
import iris_pipette_rig as rig  # noqa: E402
import gripper  # noqa: E402
from bottles import LIQUID_DENSITY, bottle  # noqa: E402

RIG_XML = SIM / 'assets/ur10e_iris_pipette/ur10e_iris_pipette.xml'
# Which hand to build: 'v2' is the shipped 2F-85 with L fingertips and a raised
# axis; 'v3' replaces it with the compact V-groove gripper of gripper.py.
HAND = os.environ.get('HAND', 'v3')
V2 = {'axis_below_cap': 0.020, 'finger_drop': 0.015, 'blade_max': math.radians(80)}
V3 = {'axis_below_cap': 0.021, 'finger_drop': 0.0, 'blade_max': math.radians(80)}
# The clamp gets a short axis of its own (v3.1): once the thread lets go, the cap is
# still 12 mm inside the neck, and swinging it out on the hinge's arc drags it against
# the neck and tips the bottle out of the hand. With CLAMP_LIFT the clamp pulls the cap
# straight up first, clear of the neck, and only then swings.
CLAMP_LIFT = {'stroke': 0.020, 'kp': 8000.0, 'kv': 200.0, 'force': 120.0}
# 'v4' is v2 without the L fingertips: the axis raise and the 80 deg blades, on
# the stock 2F-85 pads. It exists to test whether v2's 51 rig_clear failures --
# the pipette's body against the finger links the L tips pushed into its
# corridor -- were the price of the gain or just a side effect of the tips.
V4 = {'axis_below_cap': 0.020, 'finger_drop': 0.0, 'blade_max': math.radians(80)}
VER = {'v3': V3, 'v4': V4}.get(HAND, V2)
GRIP_Z = rig.IRIS['bottle_h'] - VER['axis_below_cap']     # the tool axis in the hand frame
PADS_Z = GRIP_Z - VER['finger_drop']                      # where the bottle is held
PAD_GEOMS = (gripper.PAD_GEOMS if HAND == 'v3'
             else tuple(f'L_{s}_pad{i}' for s in ('left', 'right') for i in (1, 2)))
GRIP_JOINTS = gripper.JOINTS if HAND == 'v3' else ('right_driver_joint',)
PAD_FIT = HERE / 'cache/pad_fit.json'

# Frozen by the calibration on the nominal trial (README.md, "Calibration").
PHYSICS = {
    'timestep': 0.0005,
    'thread_solref': (0.002, 1.0),
    'blade_friction': 1.5,
    'noslip_iterations': 10,
    # MuJoCo's default contact and limit stiffness (solref 0.02) lets the
    # 86 g bottle sink ~4 mm into the floor and the cap sag 1.8 mm past the
    # thread's end stop; the bottle, the cap, the floor and the stop get this.
    'solid_solref': (0.002, 1.0),
}

# Contact classes: (contype, conaffinity). Two geoms touch when either one's
# contype shares a bit with the other's conaffinity.
FLOOR, BOTTLE, CAP, PADS, BLADES, PIPETTE, CLAMP, RIG, CAP_BORE = (1 << k for k in range(9))
MASKS = {
    'floor': (FLOOR, BOTTLE | CAP | PADS | PIPETTE | RIG),
    'bottle': (BOTTLE, FLOOR | PADS | PIPETTE | RIG),
    'cap': (CAP, FLOOR | BLADES),
    'pads': (PADS, FLOOR | BOTTLE),
    'blades': (BLADES, CAP),
    'pipette': (PIPETTE, FLOOR | BOTTLE | CLAMP),
    'clamp': (CLAMP, PIPETTE | RIG | PADS),   # the gripper under the clamp, now 14 mm closer
    'rig': (RIG, FLOOR | BOTTLE | PIPETTE),
    'cap_bore': (CAP_BORE, BOTTLE),   # the inside of the cap: the neck guides and seats it
}
# The clamp kit's blade box, in the blade frame (mujoco/iris_clamp.xml).
BLADE_BOX = {'size': (0.006, 0.031, 0.00125), 'pos': (0.006, 0.031, 0.00125)}
CARRIAGE = {   # joint: (kp, kv, force)
    'cx': (40000, 2000, 800), 'cy': (40000, 2000, 800), 'cz': (40000, 2000, 800),
    'cyaw': (4000, 200, 300), 'cpitch': (4000, 200, 300),
}


def pad_fit() -> np.ndarray:
    """The pads' reach ahead of the flange against the aperture (the shipped
    generator's cubic), cached: it needs the finger linkage solve."""
    if PAD_FIT.exists():
        return np.array(json.loads(PAD_FIT.read_text()))
    from generate_iris_pipette_viewer import pad_fit as fit
    from hand_linkage import GRIPPER, linkage
    _, _, fits = linkage()
    coef = fit(mujoco.MjModel.from_xml_path(str(GRIPPER)), fits)
    PAD_FIT.parent.mkdir(exist_ok=True)
    PAD_FIT.write_text(json.dumps(coef.tolist()))
    return coef


def flange_x(bottle_r: float) -> float:
    if HAND == 'v3':
        return gripper.FLANGE_X          # the compact gripper's own reach, the same for every bottle
    return -float(np.polynomial.polynomial.polyval(2 * bottle_r, pad_fit()))


def hand_z0(d: dict) -> float:
    """Where the hand frame's origin has to be, above the floor, for the
    clamp to meet this bottle's cap: the rig is built around the cap seat
    at IRIS['bottle_h']."""
    return d['cap_z'] - rig.IRIS['bottle_h']


def _v(x) -> str:
    return ' '.join(f'{float(a):.6g}' for a in np.atleast_1d(x))


def _ring(n, r_out, r_in, z0, z1) -> list[tuple]:
    """A tube as n boxes: (pos, quat, half size)."""
    r_mid, t, half_w = (r_out + r_in) / 2, r_out - r_in, r_in * math.tan(math.pi / n)
    return [((r_mid * math.cos(a), r_mid * math.sin(a), (z0 + z1) / 2), rig.zrot(a), (t / 2, half_w, (z1 - z0) / 2))
            for a in (k * 2 * math.pi / n for k in range(n))]


def bottle_xml(d: dict) -> str:
    """The bottle body: glass mesh (visual, gives the mass), hollow collision,
    a liquid body whose mass trial.py sets, the thread follower."""
    ct, ca = MASKS['bottle']
    col = [((0, 0, d['floor'] / 2), (1, 0, 0, 0), (d['r'] - d['wall'], d['floor'] / 2), 'cylinder')]
    col += [(*b, 'box') for b in _ring(16, d['r'], d['r'] - d['wall'], d['floor'], d['shoulder'])]
    # The neck collides at its thread's root, not its crest: the crest is a helix
    # with gaps between its turns, and the thread's grip is the joint equality's
    # job, not contact's. A smooth tube at the crest leaves the cap 0.35 mm and
    # jams it on the way out; at the root it has 1.35 mm, as the real pair does.
    col += [(*b, 'box') for b in _ring(24, d['neck_root'], d['bore'], d['neck'], d['h'])]
    ss = ' '.join(map(str, PHYSICS['solid_solref']))
    geoms = ''.join(f'      <geom type="{k}" pos="{_v(p)}" quat="{_v(q)}" size="{_v(s)}" contype="{ct}" conaffinity="{ca}"'
                    f' mass="0" friction="1 0.005 0.0001" solref="{ss}" group="3"/>\n' for p, q, s, k in col)
    ri = d['r'] - d['wall'] - 0.0005
    k = d['pitch'] / (2 * math.pi)
    # the cap's inside: a thin ring around the neck and a ceiling 0.2 mm over the lip when closed
    ct2, ca2 = MASKS['cap_bore']
    ceiling = d['cap_h'] - d['cap_top'] + 0.0002
    inner = [(*b, 'box') for b in _ring(24, d['cap_bore'] + 0.001, d['cap_bore'], 0.0, ceiling)]
    inner.append(((0, 0, ceiling + 0.0005), (1, 0, 0, 0), (d['cap_bore'], 0.0005), 'cylinder'))
    cap_bore = ''.join(f'      <geom type="{k_}" pos="{_v(p)}" quat="{_v(q)}" size="{_v(s)}" contype="{ct2}" conaffinity="{ca2}"'
                       f' mass="0" friction="0.3 0.005 0.0001" solref="{ss}" group="3"/>\n' for p, q, s, k_ in inner)
    return f'''    <body name="bottle">
      <freejoint name="bottle"/>
      <geom name="glass" type="mesh" mesh="glass" material="amber" density="{rig.AMBER["glass_density"]}" contype="0" conaffinity="0" group="2"/>
{geoms}      <body name="liquid" pos="0 0 {d["floor"]}">
        <geom name="liquid" type="cylinder" size="{ri:.6g} 0.001" pos="0 0 0.001" material="liquid" mass="1e-4" contype="0" conaffinity="0" group="2"/>
      </body>
      <body name="thread_follower" pos="0 0 {d["cap_z"]:.6g}">
        <joint name="cap_lift" type="slide" axis="0 0 1" range="-0.001 0.05" damping="0.5" solreflimit="{ss}"/>
        <joint name="cap_spin" type="hinge" axis="0 0 1" frictionloss="0.04" damping="0.002"/>
        <inertial pos="0 0 0" mass="0.001" diaginertia="1e-7 1e-7 1e-7"/>
      </body>
    </body>
    <body name="cap" pos="0 0 {d["cap_z"]:.6g}">
      <freejoint name="cap"/>
      <geom name="cap_visual" type="mesh" mesh="cap" material="cap" density="{rig.AMBER["cap_density"]}" contype="0" conaffinity="0" group="2"/>
      <geom name="cap_collision" type="cylinder" size="{d["cap_r"]:.6g} {d["cap_h"] / 2:.6g}" pos="0 0 {d["cap_h"] / 2:.6g}"
            contype="{MASKS["cap"][0]}" conaffinity="{MASKS["cap"][1]}" mass="0" friction="1.5 0.01 0.001" condim="4" solref="{ss}" group="3"/>
{cap_bore}    </body>
''', k


def scene_xml(d: dict) -> str:
    body, k = bottle_xml(d)
    sr = ' '.join(map(str, PHYSICS['thread_solref']))
    fx = flange_x(d['r'])
    joints = ''.join(f'<joint name="{n}" type="{t}" axis="{a}" damping="1" armature="0.1"/>'
                     for n, t, a in (('cx', 'slide', '1 0 0'), ('cy', 'slide', '0 1 0'), ('cz', 'slide', '0 0 1')))
    acts = ''.join(f'    <position name="{n}" joint="{n}" kp="{kp}" kv="{kv}" forcerange="{-f} {f}"/>\n'
                   for n, (kp, kv, f) in CARRIAGE.items())
    return f'''<mujoco model="uncap_{d["ml"]}ml">
  <compiler angle="radian" autolimits="true"/>
  <option integrator="implicitfast" timestep="{PHYSICS["timestep"]}" cone="elliptic" impratio="10"
          noslip_iterations="{PHYSICS["noslip_iterations"]}"/>
  <visual><global offwidth="1280" offheight="720"/><quality shadowsize="4096"/></visual>
  <asset>
    <model name="rig" file="{RIG_XML}"/>
    <mesh name="glass" file="{d["glass_stl"]}" inertia="exact"/>
    <mesh name="cap" file="{d["cap_stl"]}" inertia="exact"/>
    <material name="amber" rgba="0.62 0.28 0.05 0.5"/>
    <material name="cap" rgba="0.93 0.93 0.91 1"/>
    <material name="liquid" rgba="0.31 0.61 0.85 0.6"/>
    <texture name="grid" type="2d" builtin="checker" rgb1="0.86 0.87 0.88" rgb2="0.8 0.81 0.82" width="512" height="512"/>
    <material name="floor" texture="grid" texrepeat="8 8"/>
  </asset>
  <worldbody>
    <light pos="0.4 -0.6 1.2" dir="-0.3 0.5 -1" diffuse="0.7 0.7 0.7" castshadow="true"/>
    <geom name="floor" type="plane" size="1 1 0.05" material="floor" contype="{MASKS["floor"][0]}" conaffinity="{MASKS["floor"][1]}"
          solref="{' '.join(map(str, PHYSICS['solid_solref']))}"/>
    <body name="carriage" gravcomp="1">
      <inertial pos="0 0 0" mass="1" diaginertia="0.01 0.01 0.01"/>
      {joints}
      <body name="yaw_link" gravcomp="1">
        <inertial pos="0 0 0" mass="0.5" diaginertia="0.005 0.005 0.005"/>
        <joint name="cyaw" type="hinge" axis="0 0 1" damping="1" armature="0.1"/>
        <body name="pitch_link" pos="0 0 {PADS_Z:.6g}" gravcomp="1">
          <inertial pos="0 0 0" mass="0.5" diaginertia="0.005 0.005 0.005"/>
          <joint name="cpitch" type="hinge" axis="0 1 0" damping="1" armature="0.1"/>
          <frame pos="{fx:.6g} 0 {VER['finger_drop']:.6g}" quat="{_v(rig.TOOL_QUAT)}">
            <attach model="rig" body="ur10e_iris_pipette" prefix=""/>
          </frame>
        </body>
      </body>
    </body>
{body}  </worldbody>
  <equality>
    <joint name="thread_screw" joint1="cap_lift" joint2="cap_spin" polycoef="0 {k:.8g} 0 0 0" solref="{sr}"/>
    <weld name="thread_weld" body1="cap" body2="thread_follower" solref="{sr}" torquescale="1"/>
  </equality>
  <actuator>
{acts}  </actuator>
</mujoco>
'''


def _mask_of(model: mujoco.MjModel, g: int) -> str | None:
    """Which contact class a colliding geom of the rig belongs to."""
    name = model.geom(g).name
    body = model.body(model.geom_bodyid[g]).name
    if name.endswith(('_pad1', '_pad2')) or name in gripper.PAD_GEOMS:
        return 'pads'
    if name in ('clamp_envelope', 'motor_envelope'):
        return 'clamp'
    if name.startswith(('pipette_col_', 'plunger_col_')):
        return 'pipette'
    if name.endswith('_col') and body.startswith('blade_'):
        return 'blades'
    return 'rig'


@lru_cache(maxsize=None)
def build(ml: int) -> mujoco.MjModel:
    """The compiled model for one bottle size."""
    d = bottle(ml)
    spec = mujoco.MjSpec.from_string(scene_xml(d))
    for k in range(rig.IRIS['n_blades']):
        spec.body(f'blade_{k}').add_geom(
            name=f'blade_{k}_col', type=mujoco.mjtGeom.mjGEOM_BOX, size=BLADE_BOX['size'], pos=BLADE_BOX['pos'],
            friction=[PHYSICS['blade_friction'], 0.01, 0.001], condim=4, mass=0, group=3,
            solref=PHYSICS['solid_solref'])
    # the mount plate slides so the pads stay on the axis for this diameter, and
    # the tool axis sits at GRIP_Z_V2 (the tool's pose in the hand frame, inverted)
    pos, quat = rig.inverse_pose((flange_x(d['r']), 0.0, GRIP_Z), rig.TOOL_QUAT)
    spec.body('hand_frame').pos = pos
    spec.body('hand_frame').quat = quat
    rig_bodies = {'bottle', 'cap', 'liquid', 'thread_follower', 'world'}
    for b in spec.bodies:
        if b.name not in rig_bodies:
            b.gravcomp = 1
    if HAND == 'v3':
        spec.delete(spec.body('base_mount'))           # the 2F-85, its actuator and its tendons
        gripper.add(spec, 'wrist_3_link', MASKS['pads'], MASKS['rig'], d['r'])
    else:
        _l_fingertips(spec)
    # the clamp's own lift, along its axis (its mount's +Z), between the hinge and the housing
    mount = spec.body('clamp_mount')
    mount.add_joint(name='clamp_lift', type=mujoco.mjtJoint.mjJNT_SLIDE, axis=[0, 0, 1],
                    range=[0.0, CLAMP_LIFT['stroke']], damping=20.0, armature=0.01)
    spec.add_actuator(name='clamp_lift', target='clamp_lift', trntype=mujoco.mjtTrn.mjTRN_JOINT,
                      gainprm=[CLAMP_LIFT['kp']] + [0] * 9, biastype=mujoco.mjtBias.mjBIAS_AFFINE,
                      biasprm=[0, -CLAMP_LIFT['kp'], -CLAMP_LIFT['kv']] + [0] * 7,
                      ctrlrange=[0.0, CLAMP_LIFT['stroke']], forcerange=[-CLAMP_LIFT['force'], CLAMP_LIFT['force']])
    model = spec.compile()
    for g in range(model.ngeom):
        in_rig = model.body(model.geom_bodyid[g]).name not in rig_bodies
        if in_rig and (model.geom_contype[g] or model.geom_conaffinity[g]):
            model.geom_contype[g], model.geom_conaffinity[g] = MASKS[_mask_of(model, g)]
    # the iris to 80 degrees; the housing may turn back past zero to seat the cap
    for k in range(rig.IRIS['n_blades']):
        model.jnt_range[model.joint(f'blade_{k}').id] = (0.0, VER['blade_max'])
    model.jnt_range[model.joint('cam').id] = (-VER['blade_max'], 0.0)
    model.actuator_ctrlrange[model.actuator('cam').id] = (-VER['blade_max'], 0.0)
    yaw_j, yaw_a = model.joint('body_yaw').id, model.actuator('body_yaw').id
    model.jnt_range[yaw_j] = (-2 * math.pi, model.jnt_range[yaw_j][1])
    model.actuator_ctrlrange[yaw_a] = (-2 * math.pi, model.actuator_ctrlrange[yaw_a][1])
    return model


def _l_fingertips(spec: mujoco.MjSpec) -> None:
    """Move each pad box V2['finger_drop'] down (hand -Z), on the same face
    plane: the 2F-85 is parallel, so each pad keeps its orientation in the
    hand, and the offset is fixed in the pad's frame. The original boxes stop
    colliding; a bracket joins old and new (drawn only)."""
    probe = spec.compile()
    data = mujoco.MjData(probe)
    mujoco.mj_kinematics(probe, data)
    down = data.xmat[probe.body('hand_frame').id].reshape(3, 3) @ np.array([0.0, 0.0, -1.0])
    for side in ('left', 'right'):
        pad = probe.body(f'{side}_pad').id
        offset = data.xmat[pad].reshape(3, 3).T @ down * V2['finger_drop']
        body = spec.body(f'{side}_pad')
        for i in (1, 2):
            g = probe.geom(f'{side}_pad{i}').id
            old = spec.geom(f'{side}_pad{i}')
            old.contype, old.conaffinity = 0, 0
            new = body.add_geom(name=f'L_{side}_pad{i}', type=mujoco.mjtGeom.mjGEOM_BOX, size=probe.geom_size[g],
                                pos=probe.geom_pos[g] + offset, quat=probe.geom_quat[g], friction=probe.geom_friction[g],
                                condim=int(probe.geom_condim[g]), solref=probe.geom_solref[g], solimp=probe.geom_solimp[g],
                                mass=0, group=3, contype=1, conaffinity=1)
            # the 2F-85's pads carry priority 1 so that their own friction and solref rule the
            # contact; without it the pair takes the bottle's, and the grip loses the cap's
            # seating torque. Carry the rest of the contact parameters too.
            new.priority = int(probe.geom_priority[g])
            new.solmix, new.margin, new.gap = float(probe.geom_solmix[g]), float(probe.geom_margin[g]), float(probe.geom_gap[g])
            body.add_geom(type=mujoco.mjtGeom.mjGEOM_BOX, size=probe.geom_size[g], pos=probe.geom_pos[g] + offset,
                          quat=probe.geom_quat[g], rgba=[0.12, 0.12, 0.13, 1], contype=0, conaffinity=0, mass=0, group=2)
        centre = np.mean([probe.geom_pos[probe.geom(f'{side}_pad{i}').id] for i in (1, 2)], axis=0)
        body.add_geom(type=mujoco.mjtGeom.mjGEOM_CAPSULE, fromto=[*centre, *(centre + offset)], size=[0.004, 0, 0],
                      rgba=[0.3, 0.32, 0.35, 1], contype=0, conaffinity=0, mass=0, group=2)


def set_fill(model: mujoco.MjModel, data: mujoco.MjData, d: dict, height: float) -> float:
    """Give the liquid body the mass and the shape of `height` metres of
    water; returns the mass."""
    ri = float(model.geom('liquid').size[0])
    mass = LIQUID_DENSITY * math.pi * ri * ri * height
    b, g = model.body('liquid').id, model.geom('liquid').id
    model.body_mass[b] = max(mass, 1e-4)
    model.body_ipos[b] = (0, 0, height / 2)
    model.body_inertia[b] = (mass * (3 * ri * ri + height * height) / 12,) * 2 + (mass * ri * ri / 2,)
    model.geom_size[g][1] = max(height / 2, 1e-4)
    model.geom_pos[g] = (0, 0, height / 2)
    mujoco.mj_setConst(model, data)
    return mass


if __name__ == '__main__':
    for ml in (10, 60, 100):
        m = build(ml)
        print(f'{ml} ml: {m.nbody} bodies, {m.njnt} joints, {m.ngeom} geoms, {m.neq} equalities, '
              f'flange_x {flange_x(bottle(ml)["r"]) * 1000:.1f} mm, hand at {hand_z0(bottle(ml)) * 1000:+.1f} mm')
