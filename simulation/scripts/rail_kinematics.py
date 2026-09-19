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
BENCH_TOP = 0.90
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
    """

    sample_id: str
    x: float
    y: float
    top: float

    @property
    def cap(self) -> np.ndarray:
        """Point at the centre of the vessel's cap."""
        return np.array([self.x, self.y, self.top])


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

    The population is baked into the lab-room model as static ``room_stock_*``
    geoms rather than as bodies, so the vessels are recovered by name and their
    extent measured from the compiled geom AABBs.

    Args:
        model: Compiled scene.
        data: Forward-evaluated data for that scene.

    Returns:
        One Bottle per sample, sorted along the bench.
    """
    groups: dict[str, list[int]] = {}
    for i in range(model.ngeom):
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_GEOM, i) or ''
        match = re.match(r'room_stock_([A-Za-z0-9-]+)_(?:body|glass|cap|label)', name)
        if match:
            groups.setdefault(match.group(1), []).append(i)

    out = []
    for sample_id, geoms in groups.items():
        pts = np.vstack([_corners(model, data, i) for i in geoms])
        out.append(Bottle(sample_id=sample_id,
                          x=float(pts[:, 0].mean()), y=float(pts[:, 1].mean()),
                          top=float(pts[:, 2].max())))
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
             seed: np.ndarray | None = None, iterations: int = 400,
             tol: float = 1.5e-3, damping: float = 0.12) -> bool:
    """Drive the tool centre point onto a target with a fixed approach axis.

    Damped least squares over the six arm joints only; the rail is left wherever
    the caller put it, so a failure here means "unreachable from this station",
    not "unreachable".

    Args:
        model: Compiled scene.
        data: Data to solve in; its arm joints are overwritten.
        target: World position for the pinch point, shape (3,).
        approach: World direction the gripper should point along.
        seed: Starting arm configuration; SEED_POSE when omitted.
        iterations: Maximum Gauss-Newton steps.
        tol: Position tolerance in metres; orientation is held to 10x tol.
        damping: Levenberg-Marquardt damping, in joint-space units.

    Returns:
        True when both tolerances are met.
    """
    dofs, qadr = arm_dofs(model), arm_qpos(model)
    site = model.site(TCP_SITE).id
    lo = np.array([model.jnt_range[model.joint(n).id][0] for n in ARM_JOINTS])
    hi = np.array([model.jnt_range[model.joint(n).id][1] for n in ARM_JOINTS])
    data.qpos[qadr] = SEED_POSE if seed is None else seed
    goal_axis = np.asarray(approach, dtype=float)
    goal_axis /= np.linalg.norm(goal_axis)

    jacp, jacr = np.zeros((3, model.nv)), np.zeros((3, model.nv))
    for _ in range(iterations):
        mujoco.mj_kinematics(model, data)
        mujoco.mj_comPos(model, data)
        pos_err = target - data.site_xpos[site]
        axis = data.site_xmat[site].reshape(3, 3)[:, 2]
        rot_err = np.cross(axis, goal_axis)
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
    axis = data.site_xmat[site].reshape(3, 3)[:, 2]
    return bool(np.linalg.norm(target - data.site_xpos[site]) < tol
                and np.linalg.norm(np.cross(axis, goal_axis)) < tol * 10)


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
        target: World position for the pinch point, shape (3,).
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
        target: World position for the pinch point, shape (3,).
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
