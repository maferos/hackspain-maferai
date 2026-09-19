"""The robot side of the swap seam.

An `Embodiment` says how a 1-D action vector maps onto MuJoCo actuators, and how
to read the matching proprioceptive vector back. It knows nothing about which
policy produces that vector, which is what lets the same scene be driven by a
Hugging Face checkpoint, a scripted skill, or anything else.

Only `ur10e_rail` exists today -- the arm `scripts/generate_rail_scene.py` puts
on the open bench. Adding another robot is a new Embodiment here plus an
`embodiment = ...` line in config/policies.toml.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import mujoco
import numpy as np


@dataclass(frozen=True)
class Embodiment:
    """A named actuator layout, in the order a policy's action vector uses."""

    name: str
    actuators: tuple[str, ...]
    #: Indices into `actuators` carrying a normalised [0, 1] gripper command,
    #: 0 closed and 1 open. That is the convention every ALOHA-lineage checkpoint
    #: on the Hub emits, so it is what the seam converts to and from.
    gripper_dims: tuple[int, ...]
    #: Actuator values for a fully open and a fully shut gripper, in the
    #: actuator's own units. Robotiq counts run 0 = open, 255 = shut, i.e. the
    #: opposite direction to the normalised form -- hence a pair rather than a
    #: scale factor.
    gripper_open: float
    gripper_shut: float
    #: Logical camera name -> MuJoCo camera name.
    cameras: dict[str, str]
    #: Per-arm IK end-effector sites, in actuator order.
    arms: tuple[tuple[str, str], ...]  # (label, site name)
    #: Rest pose, in action-vector layout and units.
    home: tuple[float, ...]
    #: Keyframe to reset to, if the scene ships one.
    home_key: str | None = None

    @property
    def dim(self) -> int:
        return len(self.actuators)


# Read off the compiled scene, not guessed: `rail_x` is declared by the scene
# itself and the arm is attached, yet MuJoCo still orders the parent's own
# actuators first. The `scan` keyframe's eight ctrl values line up with this
# exactly (rail 0, six arm angles, gripper open).
UR10E_RAIL = Embodiment(
    name='ur10e_rail',
    actuators=('rail_x', 'arm_shoulder_pan', 'arm_shoulder_lift', 'arm_elbow',
               'arm_wrist_1', 'arm_wrist_2', 'arm_wrist_3',
               'arm_grip_fingers_actuator'),
    gripper_dims=(7,),
    gripper_open=0.0,
    gripper_shut=255.0,
    cameras={
        'wrist': 'arm_eih',        # eye-in-hand, beside the tool axis
        'carriage': 'carriage',    # rides the rail, looks down the bench
        'overview': 'general',     # the fixed wall camera the CV side uses
    },
    arms=(('arm', 'arm_grip_pinch'),),   # Robotiq's pinch point, approach along +Z
    home=(0.0, -1.5708, -1.9199, 2.0944, -1.7453, -1.5708, 0.0, 1.0),
    home_key='scan',
)

EMBODIMENTS = {e.name: e for e in (UR10E_RAIL,)}


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
        self.ctrl_range = model.actuator_ctrlrange[self.ctrl_ids].copy()

        # Only joint-driven actuators have a qpos behind them. The 2F-85 pulls a
        # tendon, and `actuator_trnid` then holds a tendon id -- indexing
        # jnt_qposadr with it reads an unrelated joint. Those dims report their
        # commanded value instead, which for a position servo is a fair proxy.
        self.qpos_adr = np.full(spec.dim, -1, dtype=int)
        self.dof_ids = np.full(spec.dim, -1, dtype=int)
        for slot, ctrl_id in enumerate(self.ctrl_ids):
            if model.actuator_trntype[ctrl_id] != mujoco.mjtTrn.mjTRN_JOINT:
                continue
            joint = model.actuator_trnid[ctrl_id, 0]
            self.qpos_adr[slot] = model.jnt_qposadr[joint]
            self.dof_ids[slot] = model.jnt_dofadr[joint]
        self.gripper = np.array(spec.gripper_dims, dtype=int)
        self.joint_dims = np.array([i for i in range(spec.dim) if self.qpos_adr[i] >= 0])

    @property
    def dim(self) -> int:
        return self.spec.dim

    # -- gripper units -----------------------------------------------------
    def _denormalise_gripper(self, values: np.ndarray) -> np.ndarray:
        """[0, 1] (1 open) -> the actuator's own units."""
        span = self.spec.gripper_open - self.spec.gripper_shut
        return self.spec.gripper_shut + np.clip(values, 0.0, 1.0) * span

    def _normalise_gripper(self, values: np.ndarray) -> np.ndarray:
        span = self.spec.gripper_open - self.spec.gripper_shut
        return np.clip((values - self.spec.gripper_shut) / span, 0.0, 1.0)

    # -- state and command -------------------------------------------------
    def state(self, data: mujoco.MjData) -> np.ndarray:
        """The proprioceptive vector, in the same layout and units as the action."""
        state = np.zeros(self.dim)
        state[self.joint_dims] = data.qpos[self.qpos_adr[self.joint_dims]]
        tendon = [i for i in range(self.dim) if self.qpos_adr[i] < 0]
        state[tendon] = data.ctrl[self.ctrl_ids[tendon]]
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
        return np.array(self.spec.home, dtype=float)
