"""Scripted manipulation primitives.

Every skill is a generator yielding one action vector per control tick, in the
same layout and units a policy would emit. That is what lets the runtime route a
plan step to either a skill or a Hugging Face checkpoint without caring which:
both are just a source of actions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

import numpy as np

from armlab import ik
from armlab.embodiment import BoundEmbodiment
from armlab.scene import Scene

Action = np.ndarray

APPROACH_HEIGHT = 0.14   # m above the object to line up the vertical approach
GRASP_HEIGHT = 0.05      # m above a container's base to close the fingers
PAN_CLEARANCE = 0.07     # m above a balance body to release
PAN_APPROACH = 0.13      # m above that again -- the balances sit near the edge of
                         # the ALOHA's reach, so the lift over them stays low
GRASP_CLEARANCE = 0.025  # m of extra opening before closing on something
APPROACH_CLEARANCE = 0.008  # m the fingers must spare to descend past an object
OPEN = 1.0


@dataclass
class SkillContext:
    """Everything a skill needs, plus the running command it advances."""

    scene: Scene
    binding: BoundEmbodiment
    control_hz: float
    command: Action = field(default=None)  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.command is None:
            self.command = self.binding.home()

    def ticks(self, seconds: float) -> int:
        return max(1, int(round(seconds * self.control_hz)))


def move(ctx: SkillContext, target: Action, seconds: float) -> Iterator[Action]:
    """Ease the whole command vector from where it is to `target`.

    Raised-cosine rather than linear so the arm neither jerks at the start nor
    overshoots at the end -- the position actuators track a smooth reference far
    better than a step.
    """
    start = ctx.command.copy()
    steps = ctx.ticks(seconds)
    for i in range(1, steps + 1):
        blend = 0.5 - 0.5 * np.cos(np.pi * i / steps)
        yield start + (target - start) * blend


def set_gripper(ctx: SkillContext, arm: str, value: float, seconds: float = 0.5) -> Iterator[Action]:
    target = ctx.command.copy()
    target[_gripper_dim(ctx, arm)] = value
    yield from move(ctx, target, seconds)


def reach(ctx: SkillContext, arm: str, position: np.ndarray, yaw: float = 0.0,
          seconds: float = 1.5) -> Iterator[Action]:
    """Move one arm's gripper to a world position with a top-down approach.

    Falls back to position-only IK when the top-down orientation is what puts the
    pose out of reach. The balances sit near the edge of the ALOHA's envelope, so
    insisting on a vertical hand there fails on targets the arm can plainly touch.
    """
    joints, residual = _solve(ctx, arm, position, yaw)
    if residual > 0.01:
        relaxed, relaxed_residual = _solve(ctx, arm, position, yaw, free_orientation=True)
        if relaxed_residual < residual:
            joints, residual = relaxed, relaxed_residual
    if residual > 0.05:
        raise Unreachable(f'{arm} arm cannot reach {np.round(position, 3).tolist()} '
                          f'(off by {residual * 100:.0f} cm)')
    target = ctx.command.copy()
    target[ctx.binding.arm_slices[arm]] = joints
    yield from move(ctx, target, seconds)


def home(ctx: SkillContext, seconds: float = 2.0) -> Iterator[Action]:
    yield from move(ctx, ctx.binding.home(), seconds)


def pick(ctx: SkillContext, sample_id: str, arm: str | None = None) -> Iterator[Action]:
    """Grasp a labelled container and lift it clear of the bench."""
    sample = ctx.scene.samples.get(sample_id)
    if sample is None:
        raise UnknownObject(f'no sample {sample_id!r} in this scene')
    # The fingers must clear the container on the way down, not merely close on
    # it, so the usable limit is narrower than the gripper's full opening.
    limit = ctx.binding.max_grasp_width - APPROACH_CLEARANCE
    if sample.diameter > limit:
        raise TooWide(f'{sample_id} is {sample.diameter * 1000:.0f} mm across; this '
                      f'gripper can only take {limit * 1000:.0f} mm')
    base = sample.position(ctx.scene.data)
    arm = arm or nearest_arm(ctx, base)
    grip = ctx.binding.grip_for(sample.diameter)
    clear = ctx.binding.grip_for(sample.diameter + GRASP_CLEARANCE)
    yield from set_gripper(ctx, arm, clear, 0.4)
    yield from reach(ctx, arm, base + (0, 0, APPROACH_HEIGHT), seconds=2.0)
    yield from reach(ctx, arm, base + (0, 0, sample.grasp_height), seconds=1.2)
    yield from set_gripper(ctx, arm, grip, 0.8)
    yield from reach(ctx, arm, base + (0, 0, APPROACH_HEIGHT), seconds=1.5)


def place(ctx: SkillContext, target_id: str, arm: str | None = None) -> Iterator[Action]:
    """Set whatever is held down on a balance pan."""
    target = ctx.scene.targets.get(target_id)
    if target is None:
        raise UnknownObject(f'no target {target_id!r} in this scene')
    # Aim at the instrument's top surface, not its body origin -- a balance stands
    # ~0.3 m tall and its origin is down at bench level.
    surface = target.surface(ctx.scene.data)
    arm = arm or _holding_arm(ctx)
    yield from reach(ctx, arm, surface + (0, 0, PAN_APPROACH), seconds=2.0)
    yield from reach(ctx, arm, surface + (0, 0, PAN_CLEARANCE), seconds=1.5)
    yield from set_gripper(ctx, arm, OPEN, 0.6)
    yield from reach(ctx, arm, surface + (0, 0, PAN_APPROACH), seconds=1.2)


def stow(ctx: SkillContext, arm: str | None = None) -> Iterator[Action]:
    yield from home(ctx)


# -- helpers ---------------------------------------------------------------

class SkillError(RuntimeError):
    """A skill could not be carried out. Reported, never fatal."""


class Unreachable(SkillError):
    pass


class UnknownObject(SkillError):
    pass


class TooWide(SkillError):
    pass


def _gripper_dim(ctx: SkillContext, arm: str) -> int:
    index = [label for label, _ in ctx.binding.spec.arms].index(arm)
    return ctx.binding.spec.gripper_dims[index]


def _solve(ctx: SkillContext, arm: str, position: np.ndarray, yaw: float,
           free_orientation: bool = False):
    sl = ctx.binding.arm_slices[arm]
    return ik.solve(
        ctx.scene.model, ctx.scene.data, ctx.binding.site_ids[arm],
        np.asarray(position, dtype=float), None if free_orientation else ik.grasp_frame(yaw),
        qpos_adr=ctx.binding.qpos_adr[sl],
        dof_ids=ctx.binding.dof_ids[sl],
        joint_range=ctx.binding.joint_range[sl],
        seeds=[ctx.binding.home()[sl], ctx.command[sl]])


def nearest_arm(ctx: SkillContext, position: np.ndarray) -> str:
    """Whichever gripper is currently closest -- the cell is symmetric."""
    data = ctx.scene.data
    return min(ctx.binding.site_ids,
               key=lambda arm: float(np.linalg.norm(data.site_xpos[ctx.binding.site_ids[arm]]
                                                    - position)))


def _holding_arm(ctx: SkillContext) -> str:
    """The arm whose gripper is closed, else the one nearest the last command."""
    for label, _ in ctx.binding.spec.arms:
        if ctx.command[_gripper_dim(ctx, label)] < 0.5:
            return label
    return ctx.binding.spec.arms[0][0]


SKILLS = {'pick': pick, 'place': place, 'home': home, 'stow': stow}
