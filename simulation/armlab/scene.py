"""Load the rail scene and name what is in it.

The vessel inventory comes from `scripts/rail_kinematics.bottles()` rather than
being re-derived here: it already recovers each vessel's extent from the compiled
geom AABBs and flags the free bodies as `dynamic`, and it is the same list
`rail_reach.py` and `grasp_test.py` are scored against. Re-implementing it would
mean armlab disagreeing with the team's own numbers.

Balances keep the `balance_<n>_balance` naming that
`dashboard/bridge/labbridge/mujoco_adapter.py` also reads.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np

SIM = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SIM / 'scripts'))
import rail_kinematics as rk  # noqa: E402  (needs the path above)

DEFAULT_SCENE = rk.SCENE

_BALANCE = re.compile(r'^(balance_\d+)_balance$')


@dataclass(frozen=True)
class Sample:
    """A vessel on the bench that the arm can pick up."""

    sample_id: str
    body: str
    body_id: int
    bottle: rk.Bottle

    @property
    def diameter(self) -> float:
        """Not measured here: the scene's vessels are all well inside the
        2F-85's 85 mm span, and `grasp_test.py` closes on contact rather than to
        a width, so nothing needs a number."""
        return 0.0

    def position(self, data: mujoco.MjData) -> np.ndarray:
        return data.xpos[self.body_id].copy()


@dataclass(frozen=True)
class Target:
    """A fixed place to put something."""

    target_id: str
    body_id: int
    top: float

    def position(self, data: mujoco.MjData) -> np.ndarray:
        return data.xpos[self.body_id].copy()

    def surface(self, data: mujoco.MjData) -> np.ndarray:
        return self.position(data) + (0.0, 0.0, self.top)


class Scene:
    """A compiled model plus the lookup tables the skills and planner need."""

    def __init__(self, path: str | Path = DEFAULT_SCENE):
        self.path = Path(path)
        self.model, self.data = rk.load(self.path)
        self.samples = self._samples()
        self.targets = self._targets()
        self.reset()

    # -- construction ------------------------------------------------------
    def _bodies(self) -> list[tuple[int, str]]:
        return [(i, mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_BODY, i) or '')
                for i in range(self.model.nbody)]

    def _samples(self) -> dict[str, Sample]:
        """The liftable vessels, keyed by catalogue id.

        `bottles()` also reports welded scenery; only the `dynamic` ones have a
        free joint to move. `grasp_test.py` scores exactly this set.
        """
        bodies = {name: i for i, name in self._bodies()}
        out = {}
        for bottle in rk.bottles(self.model, self.data):
            if not bottle.dynamic:
                continue
            body = f'dyn_{bottle.sample_id}'
            if body in bodies:
                out[bottle.sample_id] = Sample(bottle.sample_id, body, bodies[body], bottle)
        return out

    def _targets(self) -> dict[str, Target]:
        return {m.group(1): Target(m.group(1), body_id, self._top_surface(m.group(1)))
                for body_id, name in self._bodies() if (m := _BALANCE.match(name))}

    def _top_surface(self, target_id: str) -> float:
        """Height of an instrument's top face above its body origin."""
        tops = [float(self.data.geom_xpos[i, 2] + self.model.geom_size[i, 2])
                for i in range(self.model.ngeom)
                if (mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, i) or ''
                    ).startswith(f'{target_id}_') and self.model.geom_contype[i]]
        body = next(i for i, n in self._bodies() if n == f'{target_id}_balance')
        return max(tops, default=0.05) - float(self.data.xpos[body, 2])

    # -- state -------------------------------------------------------------
    def reset(self) -> None:
        """Return to the scene's own `scan` keyframe."""
        mujoco.mj_resetData(self.model, self.data)
        key = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_KEY, 'scan')
        if key >= 0:
            mujoco.mj_resetDataKeyframe(self.model, self.data, key)
        mujoco.mj_forward(self.model, self.data)

    def inventory(self) -> dict:
        """What the planner is allowed to refer to."""
        return {
            'samples': sorted(self.samples),
            'targets': sorted(self.targets),
            'cameras': [mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_CAMERA, i)
                        for i in range(self.model.ncam)],
        }
