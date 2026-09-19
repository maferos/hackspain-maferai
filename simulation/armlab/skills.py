"""Scripted manipulation primitives for the UR10e on its rail.

Every skill is a generator yielding one action vector per control tick, in the
same layout and units a policy would emit. That is what lets the runtime route a
plan step to either a skill or a Hugging Face checkpoint without caring which:
both are just a source of actions.

The grasp sequence is `scripts/grasp_test.py`'s, which scores 12/12 on the bench
with physics running -- approach above the vessel, descend to a fraction of the
way up its wall, close until the pads report contact, then lift. What is
different here is only the shape: `grasp_test` runs its own `mj_step` loop, while
these yield and let `runtime` step. The gripper still closes on its sensors
rather than to a commanded width, so it stops on the glass instead of crushing
it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

import mujoco
import numpy as np

from armlab.embodiment import BoundEmbodiment
from armlab.scene import Scene, rk

Action = np.ndarray

GRASP_FRACTION = 0.35   # up the vessel wall, below the shoulder where it tapers
APPROACH = 0.12         # m above the grasp where the vertical approach starts
RELEASE = 0.06          # m of bench clearance under the pinch when letting go
OPEN, SHUT = 1.0, 0.0   # normalised: 1 open, 0 shut
# Where to set a vessel down relative to an instrument, tried in order. All of
# them step *towards* the rail rather than towards the aisle: the carriage rides
# at y = 0.14 and the arm reaches 1.30 m, so the far edge of the bench past a
# balance at y = -1.16 is simply outside the envelope -- the first version of
# this reached for y = -1.34 and was told so.
SET_DOWN = ((0.0, 0.18), (0.0, 0.30), (0.22, 0.18), (-0.22, 0.18), (0.0, 0.42))


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

    @property
    def rail_home(self) -> float:
        """World X the carriage's joint coordinate is measured from."""
        return float(self.scene.model.body('rail_carriage').pos[0])


def move(ctx: SkillContext, target: Action, seconds: float) -> Iterator[Action]:
    """Ease the whole command vector from where it is to `target`.

    Raised-cosine rather than linear, and deliberately unhurried: `grasp_test`
    records that reading the tool straight after a ramp leaves it 20-47 mm out,
    wider than a flask, so the servos need time to converge before anything
    closes on anything.
    """
    start = ctx.command.copy()
    steps = ctx.ticks(seconds)
    for i in range(1, steps + 1):
        blend = 0.5 - 0.5 * np.cos(np.pi * i / steps)
        yield start + (target - start) * blend


def hold(ctx: SkillContext, seconds: float) -> Iterator[Action]:
    """Sit on the current target while the arm catches up to it."""
    for _ in range(ctx.ticks(seconds)):
        yield ctx.command.copy()


def close_on_object(ctx: SkillContext, seconds: float = 1.5) -> Iterator[Action]:
    """Close until the gripper's own pads report they are holding something.

    This is how the real 2F-85 is driven: told to close, it reports back whether
    it stopped on an object or ran to its stop. A fixed full-close cannot tell
    those apart, and squeezes thin glass at whatever the servo can manage.
    """
    steps = ctx.ticks(seconds)
    target = ctx.command.copy()
    dim = ctx.binding.spec.gripper_dims[0]
    for step in range(steps):
        # Ramp shut over the first 60%, then dwell -- same schedule as grasp_test.
        target[dim] = OPEN + (SHUT - OPEN) * min((step + 1) / (steps * 0.6), 1.0)
        yield target.copy()
        if step > steps * 0.3 and rk.read_grip(ctx.scene.model, ctx.scene.data).holding:
            return


def home(ctx: SkillContext, seconds: float = 3.0) -> Iterator[Action]:
    yield from move(ctx, ctx.binding.home(), seconds)


def pick(ctx: SkillContext, sample_id: str) -> Iterator[Action]:
    """Grasp a vessel and lift it clear of the bench."""
    sample = ctx.scene.samples.get(sample_id)
    if sample is None:
        raise UnknownObject(f'no sample {sample_id!r} on this bench')
    bottle = sample.bottle
    grasp = rk.BENCH_TOP + (bottle.top - rk.BENCH_TOP) * GRASP_FRACTION
    above = np.array([bottle.x, bottle.y, grasp + APPROACH])
    on = np.array([bottle.x, bottle.y, grasp])

    station, q_above, q_on = _plan_grasp(ctx, above, on)
    yield from move(ctx, _action(ctx, station, q_above, OPEN), 3.0)
    yield from hold(ctx, 0.4)
    yield from move(ctx, _action(ctx, station, q_on, OPEN), 1.5)
    yield from hold(ctx, 0.4)
    yield from close_on_object(ctx)
    grip = float(ctx.command[ctx.binding.spec.gripper_dims[0]])
    yield from move(ctx, _action(ctx, station, q_above, grip), 1.5)
    yield from hold(ctx, 0.6)


def place(ctx: SkillContext, target_id: str) -> Iterator[Action]:
    """Set whatever is held down on the bench beside a named instrument.

    Not *on* the instrument: `assets/balance/balance.xml` is an analytical
    balance with a closed glass draft shield, modelled as one collision box over
    the whole 0.311 m of it, so it has no pan a vessel could stand on. Until that
    asset gains one, the honest motion is to bring the vessel to the balance and
    set it on the bench in front of it, which is what a technician would do
    before opening the shield.
    """
    target = ctx.scene.targets.get(target_id)
    if target is None:
        raise UnknownObject(f'no target {target_id!r} in this scene')
    origin = target.position(ctx.scene.data)

    plan, spot = None, None
    for dx, dy in SET_DOWN:
        spot = np.array([origin[0] + dx, origin[1] + dy, rk.BENCH_TOP + RELEASE])
        try:
            plan = _plan_grasp(ctx, spot + (0, 0, APPROACH), spot)
            break
        except Unreachable:
            continue
    if plan is None:
        raise Unreachable(f'no spot beside {target_id} is within the arm\'s reach')

    station, q_above, q_down = plan
    grip = float(ctx.command[ctx.binding.spec.gripper_dims[0]])
    yield from move(ctx, _action(ctx, station, q_above, grip), 3.0)
    yield from move(ctx, _action(ctx, station, q_down, grip), 1.5)
    yield from hold(ctx, 0.4)
    yield from move(ctx, _action(ctx, station, q_down, OPEN), 0.8)
    yield from hold(ctx, 0.3)
    yield from move(ctx, _action(ctx, station, q_above, OPEN), 1.5)


def stow(ctx: SkillContext) -> Iterator[Action]:
    yield from home(ctx)


# -- helpers ---------------------------------------------------------------

class SkillError(RuntimeError):
    """A skill could not be carried out. Reported, never fatal."""


class Unreachable(SkillError):
    pass


class UnknownObject(SkillError):
    pass


def _plan_grasp(ctx: SkillContext, above: np.ndarray, on: np.ndarray):
    """Solve the carriage station and the two arm poses, without disturbing the sim.

    `rail_kinematics` solves on `mj_kinematics` alone and writes straight into
    qpos, so it runs on a scratch copy here -- the live data belongs to the
    physics loop.
    """
    model = ctx.scene.model
    scratch = mujoco.MjData(model)
    scratch.qpos[:] = ctx.scene.data.qpos
    mujoco.mj_forward(model, scratch)

    station = rk.reach(model, scratch, above)
    if station is None:
        raise Unreachable(f'the arm cannot reach {np.round(above, 3).tolist()} '
                          f'from anywhere on the rail')
    q_above = scratch.qpos[rk.arm_qpos(model)].copy()
    rk.set_rail(model, scratch, station)
    if not rk.solve_any(model, scratch, on):
        raise Unreachable(f'the arm reaches above {np.round(on, 3).tolist()} '
                          f'but not down onto it')
    return station, q_above, scratch.qpos[rk.arm_qpos(model)].copy()


def _action(ctx: SkillContext, station: float, arm: np.ndarray, grip: float) -> Action:
    """Assemble an action vector: [rail, six arm joints, gripper].

    The rail actuator is commanded in joint coordinates, measured from the
    carriage's home X -- the same conversion `rk.set_rail` makes.
    """
    return np.concatenate([[station - ctx.rail_home], arm, [grip]])


SKILLS = {'pick': pick, 'place': place, 'home': home, 'stow': stow}
