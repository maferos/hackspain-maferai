"""Load the actuated scene and name what is in it.

The naming conventions (``balance_<n>_balance``, ``loose_<i>`` wrapping
``loose_<i>_<SAMPLE-ID>``) are the same ones
``dashboard/bridge/labbridge/mujoco_adapter.py`` already reads, so the regexes
below are deliberately identical -- both sides must keep agreeing about what a
sample is called. What is *not* copied is that module's ``BENCH`` constant: it
hardcodes the original 6.0 x 1.5 m desk and is wrong for the open variant.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import mujoco
import numpy as np

SIM = Path(__file__).resolve().parents[1]
DEFAULT_SCENE = SIM / 'models' / 'minihannover_open_aloha_scene.xml'

_BALANCE = re.compile(r'^(balance_\d+)_balance$')
_PLACE = re.compile(r'^place_(\w+)$')
_LOOSE = re.compile(r'^loose_(\d+)$')
_LOOSE_CHILD = re.compile(r'^loose_(\d+)_((?:SMP|PWD)-\d{4})$')


@dataclass(frozen=True)
class Sample:
    """A free-floating labelled container the arm can pick up."""

    sample_id: str          # e.g. SMP-0009
    body: str               # the freejoint wrapper, e.g. loose_1
    body_id: int
    qpos_adr: int
    #: Widest collidable cross-section, in metres -- what the gripper must span.
    diameter: float
    #: Height of that widest section above the body origin. Containers taper, so
    #: closing the fingers anywhere else just nudges the neck.
    grasp_height: float

    def position(self, data: mujoco.MjData) -> np.ndarray:
        return data.xpos[self.body_id].copy()


@dataclass(frozen=True)
class Target:
    """A fixed place to put something -- today, a balance."""

    target_id: str
    body_id: int
    #: Height of the instrument's top surface above its body origin. A balance is
    #: a tall thing whose origin is at bench level, and `assets/balance/balance.xml`
    #: is visual meshes plus a single collision box covering the whole instrument
    #: -- there is no exposed pan to aim at, so this is the surface you can set
    #: something down on. (Weighing is likewise not simulated: no joint, no sensor.)
    top: float

    def position(self, data: mujoco.MjData) -> np.ndarray:
        return data.xpos[self.body_id].copy()

    def surface(self, data: mujoco.MjData) -> np.ndarray:
        return self.position(data) + (0.0, 0.0, self.top)


class Scene:
    """A compiled model plus the lookup tables the skills and planner need."""

    def __init__(self, path: str | Path = DEFAULT_SCENE):
        self.path = Path(path)
        self.model = mujoco.MjModel.from_xml_path(str(self.path))
        self.data = mujoco.MjData(self.model)
        # Populate xpos/geom_xpos before measuring anything: the grasp geometry
        # below is read off world positions, which are all zero until this runs.
        mujoco.mj_forward(self.model, self.data)
        self.samples = self._samples()
        self.targets = self._targets()
        self.reset()

    # -- construction ------------------------------------------------------
    def _names(self, objtype) -> list[tuple[int, str]]:
        count = {mujoco.mjtObj.mjOBJ_BODY: self.model.nbody}[objtype]
        return [(i, mujoco.mj_id2name(self.model, objtype, i) or '') for i in range(count)]

    def _samples(self) -> dict[str, Sample]:
        wrappers, ids = {}, {}
        for body_id, name in self._names(mujoco.mjtObj.mjOBJ_BODY):
            if m := _LOOSE.match(name):
                wrappers[m.group(1)] = (body_id, name)
            elif m := _LOOSE_CHILD.match(name):
                ids[m.group(1)] = m.group(2)
        out = {}
        for index, (body_id, name) in wrappers.items():
            sample_id = ids.get(index)
            if sample_id is None:
                continue
            adr = self.model.jnt_qposadr[self.model.body_jntadr[body_id]]
            out[sample_id] = Sample(sample_id, name, body_id, int(adr),
                                    *self._grasp_geometry(name, body_id))
        return out

    def _grasp_geometry(self, wrapper: str, body_id: int) -> tuple[float, float]:
        """Width and height of a container's widest collidable section.

        The label geoms are visual only (contype 0) and slightly wider than the
        glass, so counting them would make every grasp too loose. The height
        matters just as much as the width: a flask's widest point is its belly,
        and closing the fingers up at the neck leaves one pad touching nothing.
        """
        candidates = []
        for i in range(self.model.ngeom):
            name = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, i) or ''
            if not name.startswith(f'{wrapper}_') or not self.model.geom_contype[i]:
                continue
            offset = float(self.data.geom_xpos[i, 2] - self.data.xpos[body_id, 2])
            candidates.append(self._widest_slice(i, offset))
        if not candidates:
            return 0.04, 0.05
        return max(candidates)

    def _widest_slice(self, geom_id: int, offset: float) -> tuple[float, float]:
        """Width and mid-height of a geom's straight, grippable section.

        Bounding boxes are not enough here. These containers are meshes with a
        tapering shoulder and a narrow neck, so the box half-width describes the
        body while the geom origin sits well above it -- grasping at the origin
        closes the fingers around the neck and only one pad ever touches.

        Nor is it enough to take the single widest ring of vertices: the bodies
        are revolved surfaces with vertices only where the profile changes, so the
        widest ring is the shoulder, a millimetre from where the taper begins.
        What we want is the *middle* of the full-width section, and its narrowest
        radius, so the fingers close on a straight wall rather than a slope.
        """
        model = self.model
        if model.geom_type[geom_id] != mujoco.mjtGeom.mjGEOM_MESH:
            size = model.geom_size[geom_id]
            return 2 * float(size[:2].max()), offset
        mesh = model.geom_dataid[geom_id]
        start = model.mesh_vertadr[mesh]
        vertices = model.mesh_vert[start:start + model.mesh_vertnum[mesh]]
        radius = np.linalg.norm(vertices[:, :2], axis=1)
        bands = np.round(vertices[:, 2] / 0.002).astype(int)
        rings = {b: float(radius[bands == b].mean()) for b in set(bands.tolist())}
        full_width = max(rings.values())
        grippable = [b for b, r in rings.items() if r >= 0.95 * full_width]
        low, high = min(grippable) * 0.002, max(grippable) * 0.002
        narrowest = min(rings[b] for b in grippable)
        return 2 * narrowest, offset + (low + high) / 2

    def _targets(self) -> dict[str, Target]:
        out = {}
        for body_id, name in self._names(mujoco.mjtObj.mjOBJ_BODY):
            for pattern, prefix in ((_BALANCE, None), (_PLACE, 'place_')):
                if m := pattern.match(name):
                    key = m.group(1)
                    out[key] = Target(key, body_id,
                                      self._top_surface(prefix or f'{key}_', body_id))
        return out

    def _top_surface(self, geom_prefix: str, body_id: int) -> float:
        tops = [float(self.data.geom_xpos[i, 2] + self.model.geom_size[i, 2]
                      - self.data.xpos[body_id, 2])
                for i in range(self.model.ngeom)
                if (mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_GEOM, i) or ''
                    ).startswith(geom_prefix) and self.model.geom_contype[i]]
        return max(tops, default=0.05)

    # -- state -------------------------------------------------------------
    def reset(self) -> None:
        """Return to the keyframed start pose of every attached arm.

        Each arm contributes its own keyframe (``l/neutral_pose``,
        ``r/neutral_pose``) covering only its own joints, so they are merged by
        applying each one's non-zero entries in turn rather than by resetting to
        a single key.
        """
        mujoco.mj_resetData(self.model, self.data)
        for k in range(self.model.nkey):
            qpos, ctrl = self.model.key_qpos[k], self.model.key_ctrl[k]
            self.data.qpos[np.nonzero(qpos)] = qpos[np.nonzero(qpos)]
            self.data.ctrl[np.nonzero(ctrl)] = ctrl[np.nonzero(ctrl)]
        mujoco.mj_forward(self.model, self.data)

    def inventory(self) -> dict:
        """What the planner is allowed to refer to."""
        return {
            'samples': sorted(self.samples),
            'targets': sorted(self.targets),
            'cameras': [mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_CAMERA, i)
                        for i in range(self.model.ncam)],
        }
