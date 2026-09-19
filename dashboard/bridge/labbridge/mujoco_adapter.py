"""Read the workcell, the free containers and camera images out of a MuJoCo model.

Written against ``simulation/models/minihannover_scene.xml``: balances are
bodies named ``balance_<n>_balance``, the loose containers are free bodies
named ``loose_<i>`` whose child body is ``loose_<i>_<SAMPLE-ID>``, and the
cameras of interest are ``general`` (the fixed GoPro) and ``wrist``.
"""

from __future__ import annotations

import math
import re
import threading
from dataclasses import dataclass

import mujoco
import numpy as np

from labbridge import state as S

BENCH = {"x0": -3.0, "x1": 3.0, "y0": -0.75, "y1": 0.75, "top": 0.90}
"""The minihannover worktop: 6.0 × 1.5 m centred on the origin, top at 0.90 m."""

DEFAULT_CAMERAS = (
    S.camera("overview", "general", "GENERAL", "1920×1080"),
    S.camera("robot", "room_aisle", "AISLE", "1280×720"),
    S.camera("wrist", "wrist", "WRIST", "1280×720"),
)

_BALANCE = re.compile(r"^(balance_\d+)_balance$")
_LOOSE = re.compile(r"^loose_(\d+)$")
_LOOSE_CHILD = re.compile(r"^loose_(\d+)_((?:SMP|PWD)-\d{4})$")


@dataclass
class Vessel:
    """A free container of the scene."""

    index: int
    body: str
    sample_id: str
    body_id: int
    qpos_adr: int
    cls: str

    def position(self, data: mujoco.MjData) -> np.ndarray:
        return data.xpos[self.body_id]


def _body_names(model: mujoco.MjModel) -> list[tuple[int, str]]:
    return [(i, mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i) or "") for i in range(model.nbody)]


def balances(model: mujoco.MjModel, data: mujoco.MjData, active: str | None = None) -> list[dict]:
    """List the balances as workcell entries, marking ``active``."""
    out = []
    for body_id, name in _body_names(model):
        m = _BALANCE.match(name)
        if not m:
            continue
        pos = data.xpos[body_id]
        out.append({"id": m.group(1), "position": S.vec3(*pos), "active": m.group(1) == active})
    return out


def vessels(model: mujoco.MjModel) -> list[Vessel]:
    """Find the free containers, in scene order."""
    children = {}
    for body_id, name in _body_names(model):
        m = _LOOSE_CHILD.match(name)
        if m:
            children[int(m.group(1))] = m.group(2)
    out = []
    for body_id, name in _body_names(model):
        m = _LOOSE.match(name)
        if not m:
            continue
        index = int(m.group(1))
        jnt = model.body_jntadr[body_id]
        if jnt < 0 or model.jnt_type[jnt] != mujoco.mjtJoint.mjJNT_FREE:
            continue
        sample_id = children.get(index, "")
        cls = "hdpe bottle" if sample_id.startswith("PWD") else "amber bottle"
        out.append(Vessel(index, name, sample_id, body_id, int(model.jnt_qposadr[jnt]), cls))
    return sorted(out, key=lambda v: v.index)


def workcell(model: mujoco.MjModel, data: mujoco.MjData, active_balance: str = "balance_2", rail: dict | None = None) -> dict:
    """Build the console's ``workcell`` document from the scene."""
    return S.workcell(BENCH, balances(model, data, active_balance), DEFAULT_CAMERAS, rail)


def tilt_deg(quat_wxyz: np.ndarray) -> float:
    """Angle in degrees between the body's Z axis and the world Z axis."""
    w, x, y, z = quat_wxyz
    zz = 1 - 2 * (x * x + y * y)
    return math.degrees(math.acos(max(-1.0, min(1.0, zz))))


def ground_truth(data: mujoco.MjData, vessel_list: list[Vessel]) -> list[dict]:
    """The ``evaluator.groundTruth`` list: exact poses, for the schematic and evaluation only."""
    return [
        {
            "index": v.index,
            "body": v.body,
            "position": S.vec3(*data.xpos[v.body_id]),
            "tiltDeg": tilt_deg(data.xquat[v.body_id]),
        }
        for v in vessel_list
    ]


def set_free_body_pose(model: mujoco.MjModel, data: mujoco.MjData, vessel: Vessel, position, quat_wxyz=None) -> None:
    """Move a free container kinematically (used by the mock run, not by physics)."""
    q = vessel.qpos_adr
    data.qpos[q : q + 3] = position
    if quat_wxyz is not None:
        data.qpos[q + 3 : q + 7] = quat_wxyz
    data.qvel[model.jnt_dofadr[model.body_jntadr[vessel.body_id]] : model.jnt_dofadr[model.body_jntadr[vessel.body_id]] + 6] = 0
    mujoco.mj_forward(model, data)


def quat_tilt_x(deg: float) -> np.ndarray:
    """Quaternion (w, x, y, z) tilting a body about the world X axis."""
    half = math.radians(deg) / 2
    return np.array([math.cos(half), math.sin(half), 0.0, 0.0])


class CameraStreamer:
    """Render scene cameras to JPEG for :class:`labbridge.server.FrameServer`."""

    def __init__(self, model: mujoco.MjModel, width: int = 1280, height: int = 720, quality: int = 80) -> None:
        import cv2  # local import: only needed when frames are streamed

        self._cv2 = cv2
        self._renderer = mujoco.Renderer(model, height=height, width=width)
        self._quality = quality

    def jpeg(self, data: mujoco.MjData, camera: str, lock: "threading.Lock | None" = None) -> bytes:
        """Render ``camera`` and encode it as JPEG bytes.

        ``lock`` guards ``data`` against the simulation thread; it is held only
        while the scene is copied out of ``data``, not during the render itself,
        so a slow software render never stalls the simulation loop.
        """
        if lock is not None:
            with lock:
                self._renderer.update_scene(data, camera=camera)
        else:
            self._renderer.update_scene(data, camera=camera)
        rgb = self._renderer.render()
        ok, buf = self._cv2.imencode(".jpg", self._cv2.cvtColor(rgb, self._cv2.COLOR_RGB2BGR), [self._cv2.IMWRITE_JPEG_QUALITY, self._quality])
        if not ok:
            raise RuntimeError(f"could not encode frame from camera {camera!r}")
        return buf.tobytes()

    def close(self) -> None:
        self._renderer.close()
