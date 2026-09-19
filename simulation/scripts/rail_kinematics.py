#!/usr/bin/env python3
"""Kinematics helpers for the rail scene: bottle targets and top-down IK.

Shared by scripts/rail_demo.py and scripts/rail_reach.py. Nothing here steps
physics --- it all runs on mj_forward, so poses are exact rather than settled.

The gripper's approach axis is the +Z of the ``arm_grip_pinch`` site, which is
Robotiq's own pinch point 145 mm beyond the coupling. A top-down grasp therefore
wants that axis pointing at world -Z, with the yaw about it left free: the
vessels are round, so one rotational degree of freedom is genuinely redundant
and the solver is better off spending it on reach.
"""
import re
from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np

SIM = Path(__file__).resolve().parents[1]
SCENE = SIM / 'models/minihannover_rail_scene.xml'

ARM_JOINTS = (
    'arm_shoulder_pan_joint', 'arm_shoulder_lift_joint', 'arm_elbow_joint',
    'arm_wrist_1_joint', 'arm_wrist_2_joint', 'arm_wrist_3_joint',
)
RAIL_JOINT = 'rail_x'
TCP_SITE = 'arm_grip_pinch'
EIH_SITE = 'arm_eih_site'
BENCH_TOP = 0.90
# What computer-vision/scripts/wrist_scan.py found the ArUco rings need: about
# 0.30 m of standoff, and near level. The bars are rings round the bottle, so
# from above a ring is an arc --- at 25 degrees it bends too far to rectify,
# at 8 it still reads.
LABEL_STANDOFF = 0.30
LABEL_ELEVATION = 8.0
# Approach bearings to try, starting on the rail side and alternating outwards.
# The arm is on the far side of the bench, so those are the cheap ones to hold.
BEARINGS = tuple(
    (float(np.cos(a)), float(np.sin(a)))
    for a in np.radians([90, 60, 120, 30, 150, 0, 180, -30, -150, -60, -120, -90])
)
# Hand down, leaning over the bench. Damped least squares is a local method, so
# solve_any retries from each of these rather than trusting one basin.
SEED_POSES = (
    (-1.5708, -1.2, 1.9, -2.2708, -1.5708, 0.0),
    (-1.5708, -1.0, 1.6, -2.2000, -1.5708, 0.0),
    (-1.5708, -2.0, 2.2, -1.8000, -1.5708, 0.0),
    (-1.5708, -0.8, 2.4, -3.1000, -1.5708, 0.0),
)
SEED_POSE = SEED_POSES[0]


@dataclass(frozen=True)
class Bottle:
    """A vessel standing on the bench.

    Attributes:
        sample_id: Catalogue id, or a ``reserve_*`` tag for unbarcoded stock.
        x: World X of the vessel axis, in metres.
        y: World Y of the vessel axis, in metres.
        top: World Z of the highest point of the vessel, in metres.
        label_z: World Z of the middle of the label, in metres. Measured from
            the label geometry, not guessed, so it follows each vessel's size.
        dynamic: Whether the vessel is a free body that can be picked up, as
            opposed to scenery that only collides.
    """

    sample_id: str
    x: float
    y: float
    top: float
    label_z: float
    dynamic: bool = False

    @property
    def cap(self) -> np.ndarray:
        """Point at the centre of the vessel's cap."""
        return np.array([self.x, self.y, self.top])

    @property
    def label(self) -> np.ndarray:
        """Point on the vessel axis level with the middle of the label."""
        return np.array([self.x, self.y, self.label_z])


def load(path: Path = SCENE) -> tuple[mujoco.MjModel, mujoco.MjData]:
    """Compile the rail scene.

    Args:
        path: Scene MJCF to load.

    Returns:
        Freshly compiled model and its data, already forward-evaluated.
    """
    model = mujoco.MjModel.from_xml_path(str(path))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    return model, data


def arm_dofs(model: mujoco.MjModel) -> np.ndarray:
    """Indices of the six arm DoFs in the model's velocity vector."""
    return np.array([model.joint(name).dofadr[0] for name in ARM_JOINTS])


def arm_qpos(model: mujoco.MjModel) -> np.ndarray:
    """Indices of the six arm joints in the model's position vector."""
    return np.array([model.joint(name).qposadr[0] for name in ARM_JOINTS])


def bottles(model: mujoco.MjModel, data: mujoco.MjData) -> list[Bottle]:
    """Every vessel of the bench population, from the scene's geometry.

    Most of the population is baked into the lab-room model as static
    ``room_stock_*`` geoms, so the vessels are recovered by name and their
    extent measured from the compiled geom AABBs. The ones the scene owns as
    free bodies appear instead as ``dyn_*`` and are flagged ``dynamic``.

    Sample ids contain underscores (``reserve_000``), so the pattern has to
    anchor on the part suffix rather than assume the id has none.

    Args:
        model: Compiled scene.
        data: Forward-evaluated data for that scene.

    Returns:
        One Bottle per sample, sorted along the bench.
    """
    pattern = re.compile(
        r'^(?:room_stock|dyn)_(.+?)_(body|glass|cap|label|label_back)(?:_\d+)?$')
    groups: dict[str, list[int]] = {}
    labels: dict[str, list[int]] = {}
    free: set[str] = set()
    for i in range(model.ngeom):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i) or ''
        match = pattern.match(name)
        if not match:
            continue
        groups.setdefault(match.group(1), []).append(i)
        if match.group(2) == 'label':
            labels.setdefault(match.group(1), []).append(i)
        if name.startswith('dyn_'):
            free.add(match.group(1))

    out = []
    for sample_id, geoms in groups.items():
        pts = np.vstack([_corners(model, data, i) for i in geoms])
        top = float(pts[:, 2].max())
        marked = labels.get(sample_id)
        if marked:
            band = np.vstack([_corners(model, data, i) for i in marked])[:, 2]
            label_z = float((band.min() + band.max()) / 2)
        else:
            # No label geometry: aim at mid-wall, which is where one would go.
            label_z = (BENCH_TOP + top) / 2
        out.append(Bottle(sample_id=sample_id,
                          x=float(pts[:, 0].mean()), y=float(pts[:, 1].mean()),
                          top=top, label_z=label_z,
                          dynamic=sample_id in free))
    return sorted(out, key=lambda b: b.x)


def _corners(model: mujoco.MjModel, data: mujoco.MjData, geom: int) -> np.ndarray:
    """World-space corners of a geom's axis-aligned bounding box."""
    centre, half = model.geom_aabb[geom][:3], model.geom_aabb[geom][3:]
    signs = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1)
                      for sz in (-1, 1)])
    local = signs * half + centre
    return local @ data.geom_xmat[geom].reshape(3, 3).T + data.geom_xpos[geom]


def set_rail(model: mujoco.MjModel, data: mujoco.MjData, x: float) -> float:
    """Put the carriage at a world X, clamped to the rail's travel.

    Args:
        model: Compiled scene.
        data: Data to write into.
        x: Desired world X of the carriage centre, in metres.

    Returns:
        The world X actually reached after clamping.
    """
    joint = model.joint(RAIL_JOINT)
    home = model.body('rail_carriage').pos[0]
    lo, hi = joint.range
    q = float(np.clip(x - home, lo, hi))
    data.qpos[joint.qposadr[0]] = q
    if model.nu:
        data.ctrl[model.actuator(RAIL_JOINT).id] = q
    return float(home + q)


def solve_ik(model: mujoco.MjModel, data: mujoco.MjData, target: np.ndarray,
             *, approach: tuple[float, float, float] = (0.0, 0.0, -1.0),
             site_name: str = TCP_SITE, image_up: tuple[float, float, float] | None = None,
             seed: np.ndarray | None = None, iterations: int = 400,
             tol: float = 1.5e-3, damping: float = 0.12) -> bool:
    """Drive the tool centre point onto a target with a fixed approach axis.

    Damped least squares over the six arm joints only; the rail is left wherever
    the caller put it, so a failure here means "unreachable from this station",
    not "unreachable".

    Args:
        model: Compiled scene.
        data: Data to solve in; its arm joints are overwritten.
        target: World position for the driven site, shape (3,).
        approach: World direction the site's +Z should point along.
        site_name: Site to drive --- TCP_SITE for a grasp, EIH_SITE to aim the
            eye-in-hand camera.
        image_up: World direction that should end up at the top of the camera
            image. Omit to leave the roll about the approach axis free, which
            is right for a grasp on a round vessel and wrong for a camera.
        seed: Starting arm configuration; SEED_POSE when omitted.
        iterations: Maximum Gauss-Newton steps.
        tol: Position tolerance in metres; orientation is held to 10x tol.
        damping: Levenberg-Marquardt damping, in joint-space units.

    Returns:
        True when both tolerances are met.
    """
    dofs, qadr = arm_dofs(model), arm_qpos(model)
    site = model.site(site_name).id
    lo = np.array([model.jnt_range[model.joint(n).id][0] for n in ARM_JOINTS])
    hi = np.array([model.jnt_range[model.joint(n).id][1] for n in ARM_JOINTS])
    data.qpos[qadr] = SEED_POSE if seed is None else seed
    goal_axis = np.asarray(approach, dtype=float)
    goal_axis /= np.linalg.norm(goal_axis)
    # The camera's image-up is the site's -Y, by how eih_site is built.
    goal_up = None
    if image_up is not None:
        goal_up = np.asarray(image_up, dtype=float)
        goal_up = goal_up - goal_up.dot(goal_axis) * goal_axis
        norm = np.linalg.norm(goal_up)
        if norm < 1e-6:
            raise ValueError('image_up is parallel to the approach axis')
        goal_up = -goal_up / norm

    jacp, jacr = np.zeros((3, model.nv)), np.zeros((3, model.nv))
    for _ in range(iterations):
        mujoco.mj_kinematics(model, data)
        mujoco.mj_comPos(model, data)
        pos_err = target - data.site_xpos[site]
        frame = data.site_xmat[site].reshape(3, 3)
        rot_err = np.cross(frame[:, 2], goal_axis)
        if goal_up is not None:
            rot_err = rot_err + np.cross(frame[:, 1], goal_up)
        if np.linalg.norm(pos_err) < tol and np.linalg.norm(rot_err) < tol * 10:
            return True

        mujoco.mj_jacSite(model, data, jacp, jacr, site)
        jac = np.vstack([jacp[:, dofs], jacr[:, dofs]])
        err = np.concatenate([pos_err, rot_err])
        step = jac.T @ np.linalg.solve(jac @ jac.T + damping**2 * np.eye(6), err)
        q = np.clip(data.qpos[qadr] + np.clip(step, -0.3, 0.3), lo, hi)
        # Five of the six joints turn +-360 degrees, so a solution that drifts
        # towards +-2pi is the same pose one turn away from a hard stop. Folding
        # it back keeps the solver off the limit, where the Jacobian stalls.
        free = (hi - lo) > 2 * np.pi - 1e-6
        q[free] = (q[free] + np.pi) % (2 * np.pi) - np.pi
        data.qpos[qadr] = q

    mujoco.mj_kinematics(model, data)
    mujoco.mj_comPos(model, data)
    frame = data.site_xmat[site].reshape(3, 3)
    residual = np.cross(frame[:, 2], goal_axis)
    if goal_up is not None:
        residual = residual + np.cross(frame[:, 1], goal_up)
    return bool(np.linalg.norm(target - data.site_xpos[site]) < tol
                and np.linalg.norm(residual) < tol * 10)


# The UR10e's own envelope, measured from the base flange: 1.30 m of reach plus
# the gripper's 145 mm pinch offset, and nothing closer than the shoulder can
# fold. Cheap to check, and it skips the expensive solve for most targets.
ENVELOPE = (0.22, 1.40)


def solve_any(model: mujoco.MjModel, data: mujoco.MjData, target: np.ndarray,
              **kwargs) -> bool:
    """Try :func:`solve_ik` from every seed in SEED_POSES until one lands.

    Args:
        model: Compiled scene.
        data: Data to solve in; its arm joints are overwritten.
        target: World position for the driven site, shape (3,).
        **kwargs: Forwarded to :func:`solve_ik`, minus ``seed``.

    Returns:
        True when any seed converged; the data holds that solution.
    """
    mujoco.mj_kinematics(model, data)
    distance = float(np.linalg.norm(target - data.body('arm_base').xpos))
    if not ENVELOPE[0] <= distance <= ENVELOPE[1]:
        return False
    for seed in SEED_POSES:
        if solve_ik(model, data, target, seed=np.array(seed), **kwargs):
            return True
    return False


# The UR10e cannot fold onto a point right under its own shoulder, so a vessel
# directly beneath the carriage is a dead-zone miss rather than a reach miss.
# Standing off along the rail is exactly the freedom the rail exists to give.
STANDOFFS = (0.0, 0.30, -0.30, 0.50, -0.50, 0.70, -0.70)


def reach(model: mujoco.MjModel, data: mujoco.MjData, target: np.ndarray,
          *, standoffs: tuple[float, ...] = STANDOFFS,
          **kwargs) -> float | None:
    """Find a rail station the target can be reached from, and pose the arm.

    Args:
        model: Compiled scene.
        data: Data to solve in; the rail and arm joints are overwritten.
        target: World position for the driven site, shape (3,).
        standoffs: Offsets along the rail to try, in metres, in order.
        **kwargs: Forwarded to :func:`solve_ik`.

    Returns:
        World X of the carriage for the solution found, or None if every
        station failed.
    """
    for offset in standoffs:
        station = set_rail(model, data, float(target[0]) + offset)
        if solve_any(model, data, target, **kwargs):
            return station
    return None


def label_view(bottle: Bottle, *, standoff: float = LABEL_STANDOFF,
               elevation: float = LABEL_ELEVATION,
               bearing: tuple[float, float] = (0.0, 1.0)
               ) -> tuple[np.ndarray, np.ndarray]:
    """Where to put the eye-in-hand camera to read one vessel's label.

    The arm comes at the vessel from the rail side, so the default bearing is
    +Y. Elevation is measured up from level.

    Args:
        bottle: Vessel to read.
        standoff: Distance from the vessel axis to the camera, in metres.
        elevation: Degrees above level to look down from.
        bearing: Horizontal direction the camera stands in, from the vessel.

    Returns:
        The camera position, and the unit direction it must look along.
    """
    heading = np.array([bearing[0], bearing[1], 0.0], dtype=float)
    heading /= np.linalg.norm(heading)
    rise = np.radians(elevation)
    offset = standoff * (np.cos(rise) * heading + np.sin(rise) * np.array([0, 0, 1.0]))
    return bottle.label + offset, -offset / np.linalg.norm(offset)


def read_label(model: mujoco.MjModel, data: mujoco.MjData, bottle: Bottle, *,
               standoff: float = LABEL_STANDOFF,
               elevation: float = LABEL_ELEVATION,
               bearings: tuple[tuple[float, float], ...] | None = None
               ) -> tuple[float, tuple[float, float]] | None:
    """Pose the arm so the eye-in-hand camera is square on a vessel's label.

    Tries each approach bearing in turn, skipping the ones where a neighbouring
    vessel is in the way, and takes the first the arm can actually hold. Coming
    at a vessel from the right side matters more than the angle: at 8 degrees of
    elevation, approaching every vessel from the rail side sees 60% of the
    labels, while picking the bearing per vessel sees all of them.

    Args:
        model: Compiled scene.
        data: Data to solve in; the rail and arm joints are overwritten.
        bottle: Vessel to read.
        standoff: Distance from the vessel axis to the camera, in metres.
        elevation: Degrees above level to look down from.
        bearings: Horizontal directions to try, in order. BEARINGS by default,
            which starts on the rail side and works outwards.

    Returns:
        The carriage X and the bearing used, or None if no combination worked.
    """
    for bearing in bearings or BEARINGS:
        eye, direction = label_view(bottle, standoff=standoff,
                                    elevation=elevation, bearing=bearing)
        if not line_of_sight(model, data, eye, bottle):
            continue
        station = reach(model, data, eye, approach=tuple(direction),
                        site_name=EIH_SITE, image_up=(0.0, 0.0, 1.0))
        if station is not None:
            return station, bearing
    return None


def line_of_sight(model: mujoco.MjModel, data: mujoco.MjData, eye: np.ndarray,
                  bottle: Bottle) -> bool:
    """Whether a vessel's label is actually visible from a camera position.

    Casts a ray at the label and checks what it hits first. The bench holds 93
    vessels packed about 9 mm apart, so a neighbour blocking the view is the
    normal case rather than the exception, and no amount of arm cleverness
    fixes it.

    Args:
        model: Compiled scene.
        data: Forward-evaluated data for that scene.
        eye: World position of the camera, shape (3,).
        bottle: Vessel whose label is being looked at.

    Returns:
        True when the first thing the ray meets belongs to that vessel.
    """
    direction = bottle.label - eye
    distance = float(np.linalg.norm(direction))
    geomid = np.zeros(1, dtype=np.int32)
    hit = mujoco.mj_ray(model, data, eye, direction / distance, None, 1, -1,
                        geomid)
    if hit < 0 or geomid[0] < 0:
        return False
    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, int(geomid[0])) or ''
    return name.startswith((f'room_stock_{bottle.sample_id}_',
                            f'dyn_{bottle.sample_id}_'))


# The gripper's own senses, as the sensors compile in the scene. The real 2F-85
# reports the same three things over Modbus: how hard it is pressing, how far
# the fingers got, and whether it stopped on something.
GRIP_SENSORS = ('arm_grip_right_pad_force', 'arm_grip_left_pad_force',
                'arm_grip_finger_drive', 'arm_grip_right_finger',
                'arm_grip_left_finger')
# rad; the driver joints run 0 to 0.8. The threshold is well short of the stop
# because the pads press on each other at full close and register a few newtons
# of their own: at 0.78 the gripper reported holding two vessels it had closed
# straight past.
FINGERS_SHUT = 0.74
GRIP_FORCE = 2.0        # N on a pad before the gripper is taken to be holding


@dataclass(frozen=True)
class Grip:
    """What the gripper can tell about what it is holding.

    Attributes:
        right: Normal force on the right pad, in newtons.
        left: Normal force on the left pad, in newtons.
        drive: Force the finger servo is putting out.
        closure: How far the fingers have closed, 0 open to about 0.8 shut.
        holding: Fingers stalled short of shut with force on both pads --- the
            2F-85's own "object detected" condition.
    """

    right: float
    left: float
    drive: float
    closure: float
    holding: bool

    @property
    def squeeze(self) -> float:
        """The smaller of the two pad forces: what is actually pinched."""
        return min(self.right, self.left)


def read_grip(model: mujoco.MjModel, data: mujoco.MjData) -> Grip:
    """Read the gripper's sensors.

    Args:
        model: Compiled scene.
        data: Data with sensors evaluated.

    Returns:
        The current gripper state.
    """
    values = {name: float(data.sensor(name).data[0]) for name in GRIP_SENSORS}
    right = values['arm_grip_right_pad_force']
    left = values['arm_grip_left_pad_force']
    closure = (values['arm_grip_right_finger'] + values['arm_grip_left_finger']) / 2
    return Grip(right=right, left=left,
                drive=values['arm_grip_finger_drive'], closure=closure,
                holding=closure < FINGERS_SHUT and min(right, left) > GRIP_FORCE)
