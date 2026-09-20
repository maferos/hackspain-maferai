"""Cartesian positioning for the double-rail vertical-hand prototype.

Targets refer to the hand's pinch site in world metres. This module positions
joints; it does not plan obstacle-free paths or identify vessels.
"""
import mujoco
import numpy as np

JOINTS = ('gantry_x', 'gantry_y', 'gantry_z')
SITE = 'arm_grip_pinch'


def move_to(model, data, target):
    """Set an attainable XYZ target, rejecting travel limits before mutation."""
    target = np.asarray(target, dtype=float)
    if target.shape != (3,) or not np.isfinite(target).all():
        raise ValueError('Target must contain three finite world coordinates')
    mujoco.mj_forward(model, data)
    joints = [model.joint(name) for name in JOINTS]
    indices = np.array([joint.qposadr[0] for joint in joints])
    values = data.qpos[indices] + target - data.site(SITE).xpos
    if any(not joint.range[0] <= value <= joint.range[1]
           for joint, value in zip(joints, values)):
        raise ValueError('Target is outside the gantry travel')
    data.qpos[indices] = values
    for name, value in zip(JOINTS, values):
        data.ctrl[model.actuator(name).id] = value
    mujoco.mj_forward(model, data)
