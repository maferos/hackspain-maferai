"""Damped least-squares inverse kinematics for one arm.

Deliberately ~60 lines of `mujoco.mj_jacSite` rather than a dependency. AutoBio
ships an analytical ALOHA solver (`autobio/aloha_analytical_ik.py`), but importing
it would pull in the rest of AutoBio and its MuJoCo 3.3.0 plugin pin, which is the
one thing this package avoids.
"""

from __future__ import annotations

import mujoco
import numpy as np


def _orientation_error(current: np.ndarray, target: np.ndarray) -> np.ndarray:
    """Rotation vector taking the current frame onto the target frame."""
    error_mat = target @ current.T
    quat = np.empty(4)
    mujoco.mju_mat2Quat(quat, error_mat.ravel())
    axis_angle = np.empty(3)
    mujoco.mju_quat2Vel(axis_angle, quat, 1.0)
    return axis_angle


def _descend(
    model: mujoco.MjModel,
    scratch: mujoco.MjData,
    site_id: int,
    target_pos: np.ndarray,
    target_mat: np.ndarray | None,
    qpos_adr: np.ndarray,
    dof_ids: np.ndarray,
    joint_range: np.ndarray,
    rotation_weight: float,
    damping: float,
    step: float,
    iterations: int,
    tolerance: float,
) -> tuple[np.ndarray, float]:
    jac = np.zeros((6, model.nv))
    rows = 3 if target_mat is None else 6
    error = np.zeros(6)
    for _ in range(iterations):
        mujoco.mj_kinematics(model, scratch)
        mujoco.mj_comPos(model, scratch)
        error[:3] = target_pos - scratch.site_xpos[site_id]
        if target_mat is not None:
            current = scratch.site_xmat[site_id].reshape(3, 3)
            error[3:] = rotation_weight * _orientation_error(current, target_mat)
        if np.linalg.norm(error[:rows]) < tolerance:
            break
        mujoco.mj_jacSite(model, scratch, jac[:3], jac[3:], site_id)
        jacobian = jac[:rows][:, dof_ids]
        # (J Jt + lambda^2 I)^-1 -- damping keeps this finite through singularities
        # and near the edge of the workspace, at the cost of a slower approach.
        gain = np.linalg.solve(
            jacobian @ jacobian.T + damping**2 * np.eye(rows), error[:rows])
        scratch.qpos[qpos_adr] = np.clip(
            scratch.qpos[qpos_adr] + step * (jacobian.T @ gain),
            joint_range[:, 0], joint_range[:, 1])
    mujoco.mj_kinematics(model, scratch)
    return (scratch.qpos[qpos_adr].copy(),
            float(np.linalg.norm(target_pos - scratch.site_xpos[site_id])))


def solve(
    model: mujoco.MjModel,
    data: mujoco.MjData,
    site_id: int,
    target_pos: np.ndarray,
    target_mat: np.ndarray | None = None,
    *,
    qpos_adr: np.ndarray,
    dof_ids: np.ndarray,
    joint_range: np.ndarray,
    seeds: list[np.ndarray] | None = None,
    restarts: int = 6,
    rotation_weight: float = 0.4,
    damping: float = 0.08,
    step: float = 0.6,
    iterations: int = 300,
    tolerance: float = 1e-3,
    rng: np.random.Generator | None = None,
) -> tuple[np.ndarray, float]:
    """Solve for joint angles putting `site_id` at `target_pos` (and orientation).

    Runs on a scratch copy of `data`, so the live simulation is never disturbed.
    Returns the best joint vector found and its position error in metres.

    Gradient descent on a 6-DoF arm has local minima, and which one it falls into
    depends entirely on where it started: solving for the same point 2 cm higher
    would converge to 0.1 mm or stall at 200 mm depending on the current pose.
    So each call tries several starting configurations -- the live pose, the
    caller's suggestions, then random ones -- and keeps the best. This is the
    difference between IK that works and IK that works sometimes.
    """
    rng = rng or np.random.default_rng(0)
    scratch = mujoco.MjData(model)
    scratch.qvel[:] = 0.0
    starts = [data.qpos[qpos_adr].copy()] + [np.asarray(s, dtype=float) for s in (seeds or [])]
    span = joint_range[:, 1] - joint_range[:, 0]
    starts += [joint_range[:, 0] + span * rng.random(len(qpos_adr)) for _ in range(restarts)]

    current = starts[0]
    best, best_residual, solutions = current, np.inf, []
    for start in starts:
        scratch.qpos[:] = data.qpos
        scratch.qpos[qpos_adr] = np.clip(start, joint_range[:, 0], joint_range[:, 1])
        joints, residual = _descend(
            model, scratch, site_id, target_pos, target_mat, qpos_adr, dof_ids,
            joint_range, rotation_weight, damping, step, iterations, tolerance)
        if residual < best_residual:
            best, best_residual = joints, residual
        if residual < tolerance:
            solutions.append(joints)
            # Two good solutions are enough to choose a near one from; more just
            # costs time.
            if len(solutions) >= 2:
                break
    if solutions:
        # Among poses that reach the target, take the one needing the least joint
        # travel. A random restart can land on a valid but mirrored elbow-up
        # configuration, and swinging through it mid-carry drops whatever is held.
        best = min(solutions, key=lambda q: float(np.linalg.norm(q - current)))
        best_residual = 0.0 if best_residual < tolerance else best_residual
    return best, best_residual


def grasp_frame(yaw: float = 0.0) -> np.ndarray:
    """A top-down grasp orientation for the ALOHA gripper site.

    The site's local +x points out of the fingers, so pointing it at world -z
    gives a vertical approach; `yaw` spins the hand about that axis.
    """
    forward = np.array([0.0, 0.0, -1.0])
    side = np.array([-np.sin(yaw), np.cos(yaw), 0.0])
    return np.column_stack((forward, side, np.cross(forward, side)))
