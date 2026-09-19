"""The robot side of the swap seam.

An `Embodiment` says how a 1-D action vector maps onto MuJoCo actuators, and how
to read the matching proprioceptive vector back. It knows nothing about which
policy produces that vector, which is what lets the same scene be driven by a
Hugging Face checkpoint, a scripted skill, or anything else.

Only `aloha_bimanual` exists today. Adding a `ur5e_2f85` is additive: a new
Embodiment here plus an `embodiment = ...` line in config/policies.toml.
"""

from __future__ import annotations

from dataclasses import dataclass

import mujoco
import numpy as np

# Both arms come from the same AutoBio MJCF (autobio/model/robot/aloha_left.xml),
# attached twice with the prefixes `l/` and `r/`. The inner `left/` is part of the
# source file's own naming and survives the prefix, hence `l/left/...`.
_ARM_JOINTS = ('waist', 'shoulder', 'elbow', 'forearm_roll', 'wrist_angle', 'wrist_rotate')


def _actuators(prefix: str) -> tuple[str, ...]:
    return tuple(f'{prefix}left/{j}' for j in _ARM_JOINTS) + (f'{prefix}left/gripper',)


@dataclass(frozen=True)
class Embodiment:
    """A named actuator layout, in the order a policy's action vector uses."""

    name: str
    actuators: tuple[str, ...]
    #: Indices into `actuators` carrying a normalised [0, 1] gripper command
    #: (0 closed, 1 open) rather than a physical unit. gym-aloha's convention,
    #: and therefore what every ALOHA checkpoint on the Hub emits.
    gripper_dims: tuple[int, ...]
    #: Logical camera name -> MuJoCo camera name.
    cameras: dict[str, str]
    #: Per-arm IK end-effector sites, in actuator order.
    arms: tuple[tuple[str, str], ...]  # (label, site name)
    home_qpos: tuple[float, ...]
    #: Per-arm (finger joints, finger geoms), used to work out what gripper
    #: command actually holds an object of a given width. Both joints are listed
    #: because the MJCF couples them with an <equality>, and equalities are
    #: resolved by the constraint solver -- mj_kinematics alone will not move the
    #: second finger.
    fingers: tuple[tuple[tuple[str, str], tuple[str, str]], ...] = ()
    #: Distance between the two finger geom origins when the fingers meet. Below
    #: this the command is simply crushing. Measured by closing the gripper in
    #: sim and watching where the gap stops shrinking; re-measure if the finger
    #: meshes ever change.
    contact_gap: float = 0.031

    @property
    def dim(self) -> int:
        return len(self.actuators)


# gym-aloha START_ARM_POSE, minus the two finger entries it carries per arm
# (AutoBio drives both fingers from one actuator). This is the pose every ALOHA
# episode begins in, so a policy expects to be handed control from here.
#
# The gripper entry is gym-aloha's start value expressed in *its* normalisation,
# not ours: normalize_puppet_gripper_position(0.02239) over (0.01844, 0.058)
# = 0.10. Handing a policy a fully-open gripper instead would put 2 of the 14
# state dimensions outside anything it saw in training. Scripted skills are
# unaffected -- `pick` opens the fingers as its first action regardless.
_START_ARM_POSE = (0.0, -0.96, 1.16, 0.0, -0.3, 0.0, 0.10)

ALOHA_BIMANUAL = Embodiment(
    name='aloha_bimanual',
    actuators=_actuators('l/') + _actuators('r/'),
    gripper_dims=(6, 13),
    cameras={
        'top': 'top',
        'wrist_left': 'l/wrist_cam_left',
        'wrist_right': 'r/wrist_cam_left',
        'overview': 'general',
    },
    arms=(('left', 'l/left/gripper'), ('right', 'r/left/gripper')),
    home_qpos=_START_ARM_POSE * 2,
    fingers=((('l/left/left_finger', 'l/left/right_finger'), ('l/leftfinger', 'l/rightfinger')),
             (('r/left/left_finger', 'r/left/right_finger'), ('r/leftfinger', 'r/rightfinger'))),
)

EMBODIMENTS = {e.name: e for e in (ALOHA_BIMANUAL,)}


class BoundEmbodiment:
    """An `Embodiment` resolved against a compiled model.

    Holds the ctrl indices, the joint qpos addresses behind them and each
    actuator's ctrlrange, so `state` and `apply` are pure array work.
    """

    def __init__(self, spec: Embodiment, model: mujoco.MjModel):
        self.spec = spec
        missing = [a for a in spec.actuators
                   if mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, a) < 0]
        if missing:
            raise ValueError(
                f'embodiment {spec.name!r} expects actuators not in this model: {missing}')
        self.ctrl_ids = np.array(
            [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, a) for a in spec.actuators])
        joint_ids = np.array([model.actuator_trnid[i, 0] for i in self.ctrl_ids])
        self.qpos_adr = model.jnt_qposadr[joint_ids]
        self.dof_ids = model.jnt_dofadr[joint_ids]
        self.joint_range = model.jnt_range[joint_ids].copy()
        self.ctrl_range = model.actuator_ctrlrange[self.ctrl_ids].copy()
        self.gripper = np.array(spec.gripper_dims, dtype=int)
        self.site_ids = {
            label: mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_SITE, site)
            for label, site in spec.arms}
        # Joints this embodiment may move, per arm -- what IK is allowed to solve
        # over. The 6 revolute joints only; the gripper is commanded directly.
        per_arm = spec.dim // len(spec.arms)
        self.arm_slices = {label: slice(i * per_arm, i * per_arm + per_arm - 1)
                           for i, (label, _) in enumerate(spec.arms)}
        self._grip = self._calibrate_grip(model)

    def _calibrate_grip(self, model: mujoco.MjModel) -> tuple[float, float]:
        """Fit finger gap against rail travel: it is exactly affine.

        Two forward-kinematics evaluations on a scratch MjData are enough, and
        unlike stepping they report the *commanded* geometry rather than where
        the fingers stop when they collide with each other.
        """
        if not self.spec.fingers:
            return (2.0, 0.0)
        joints, geoms = self.spec.fingers[0]
        scratch = mujoco.MjData(model)
        adr = [model.jnt_qposadr[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, j)]
               for j in joints]
        ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_GEOM, g) for g in geoms]

        def gap(rail: float) -> float:
            scratch.qpos[adr] = rail
            mujoco.mj_kinematics(model, scratch)
            return float(np.linalg.norm(scratch.geom_xpos[ids[0]] - scratch.geom_xpos[ids[1]]))

        low, high = self.ctrl_range[self.gripper[0]]
        slope = (gap(high) - gap(low)) / (high - low)
        return (slope, gap(low) - slope * low)

    @property
    def max_grasp_width(self) -> float:
        """Widest object the fingers can open around at all."""
        slope, intercept = self._grip
        return slope * self.ctrl_range[self.gripper[0], 1] + intercept - self.spec.contact_gap

    def grip_for(self, width: float, squeeze: float = 0.004) -> float:
        """Normalised gripper command that closes on an object `width` across.

        Commanding fully closed on a light free object does not grasp it, it
        launches it: the fingers reach the crush point with 2000 kp behind them
        long before they have any load. Aiming a few millimetres inside the
        object's width is what actually holds.
        """
        slope, intercept = self._grip
        rail = (self.spec.contact_gap + width - squeeze - intercept) / slope
        low, high = self.ctrl_range[self.gripper[0]]
        return float(np.clip((rail - low) / (high - low), 0.0, 1.0))

    @property
    def dim(self) -> int:
        return self.spec.dim

    def _denormalise_gripper(self, values: np.ndarray) -> np.ndarray:
        """[0, 1] -> the actuator's own units.

        AutoBio's ALOHA 2 gripper is commanded in metres of finger travel along
        the rail, ctrlrange (0.002, 0.037) -- measured software limits on the real
        arm. gym-aloha's ALOHA 1 used a different origin and range entirely
        (0.01844, 0.058), so its unnormalize_puppet_gripper_position constants do
        NOT transfer. Taking the endpoints from the model keeps this correct for
        whatever gripper an embodiment is bound to.
        """
        low, high = self.ctrl_range[self.gripper, 0], self.ctrl_range[self.gripper, 1]
        return low + np.clip(values, 0.0, 1.0) * (high - low)

    def _normalise_gripper(self, values: np.ndarray) -> np.ndarray:
        low, high = self.ctrl_range[self.gripper, 0], self.ctrl_range[self.gripper, 1]
        return np.clip((values - low) / (high - low), 0.0, 1.0)

    def state(self, data: mujoco.MjData) -> np.ndarray:
        """The proprioceptive vector, in the same layout and units as the action."""
        state = data.qpos[self.qpos_adr].copy()
        state[self.gripper] = self._normalise_gripper(state[self.gripper])
        return state

    def apply(self, data: mujoco.MjData, action: np.ndarray) -> None:
        """Write an action vector to `data.ctrl`."""
        if action.shape != (self.dim,):
            raise ValueError(f'expected an action of shape ({self.dim},), got {action.shape}')
        ctrl = np.asarray(action, dtype=float).copy()
        ctrl[self.gripper] = self._denormalise_gripper(ctrl[self.gripper])
        data.ctrl[self.ctrl_ids] = np.clip(ctrl, self.ctrl_range[:, 0], self.ctrl_range[:, 1])

    def home(self) -> np.ndarray:
        return np.array(self.spec.home_qpos, dtype=float)
