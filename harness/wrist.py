"""Put a camera in front of a bottle and look at it from arm's length

The fixed cameras propose; this is what confirms. A flask on the rail bench is
12 to 24 pixels across in every fixed view, which is not enough to resolve a
4x4 marker, so reading the ring from across the room cannot work however good
the detector is. The ring reads from about 0.30 m, which is where the arm
carries its camera anyway.

Only the moving is here: how the camera gets in front of a bottle and how a
frame is taken from it. What is read in that frame, and what it means, stays in
:mod:`vision`.

Two ways to get there, and the difference between them is the difference
between a demo and a robot:

:class:`ArmCamera`
    The scene's real eye-in-hand camera, bolted to the UR10e's wrist flange,
    driven by :func:`rail_kinematics.look_at_point`: the rail carriage is put
    at a station and the six arm joints are solved so that the camera --- not a
    proxy for it --- ends up looking at the point. A pose the arm cannot hold
    yields nothing, and a bottle it cannot reach from any bearing is never
    looked at, which is a real outcome and is recorded as one. The camera's
    pose is then read back from the simulation, because the solver lands within
    1.5 mm and 15 mrad of what was asked and the difference belongs in the
    measurement.

:class:`MocapCamera`
    A camera on a mocap mount, teleported to the pose. No arm, no rail, no
    reach to fail. It is what the scenes without an arm have, and it measures
    the vision alone.

Neither asks the simulator whether a view is blocked: if a pose reads nothing,
the next one is tried, which is what an arm in a real lab has to do.
"""

import sys
from pathlib import Path

import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "simulation/scripts"))
import rail_kinematics as rk  # noqa: E402

STANDOFF_M = 0.30
"""What the ring needs, and what both cameras aim for. A GoPro's near focus,
and the range at which the ring reads on every bottle size
(``computer-vision/scripts/ring_experiment.py``). The arm treats it as a
preference, not a rule: see ``rail_kinematics.LOOK_STANDOFFS``."""
ELEVATION_DEG = 15.0
"""How far above level the mocap camera looks down from. A camera level with
the ring cannot place it: its ray runs along the ring's height instead of
crossing it (``labvision.perception.refine``)."""
AZIMUTHS_DEG = (0, 25, -25, 50, -50)
"""Views the mocap camera tries in turn, from straight across the aisle to 50
degrees either side. The arm uses ``rail_kinematics.BEARINGS`` instead, which
starts on the side the arm actually stands on."""


class Eye:
    """A camera in the scene and a renderer for it"""

    def __init__(self, model: mujoco.MjModel, data: mujoco.MjData, cam: int,
                 width: int, height: int):
        self.model, self.cam = model, cam
        self.name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_CAMERA, cam)
        self.home = data.qpos.copy(), data.mocap_pos.copy(), data.mocap_quat.copy()
        model.vis.global_.offwidth = max(model.vis.global_.offwidth, width)
        model.vis.global_.offheight = max(model.vis.global_.offheight, height)
        self.renderer = mujoco.Renderer(model, height=height, width=width)
        self.views = 0
        self.unreachable = 0

    def frame(self, data: mujoco.MjData) -> tuple[np.ndarray, np.ndarray]:
        """Render where the camera stands now, in BGR, with its depth buffer"""
        self.views += 1
        self.renderer.update_scene(data, camera=self.cam)
        self.renderer.disable_depth_rendering()
        rgb = self.renderer.render()
        self.renderer.enable_depth_rendering()
        depth = self.renderer.render().copy()
        self.renderer.disable_depth_rendering()
        return rgb[:, :, ::-1].copy(), depth

    def park(self, data: mujoco.MjData) -> None:
        """Put the scene back the way it was found"""
        data.qpos[:], data.mocap_pos[:], data.mocap_quat[:] = self.home
        mujoco.mj_kinematics(self.model, data)
        mujoco.mj_camlight(self.model, data)

    def close(self) -> None:
        self.renderer.close()

    def report(self) -> dict:
        """What the pass did, for the scene's metrics"""
        return {"camera": self.name, "mount": type(self).__name__,
                "views": self.views}


class ArmCamera(Eye):
    """The eye-in-hand camera, taken to the bottle by the arm that carries it"""

    def look(self, data: mujoco.MjData, aim: np.ndarray):
        """Every view of a point the arm can actually hold, best first

        Yields:
            The BGR frame, its depth buffer, and the pose the arm is holding.
        """
        held = 0
        for look in rk.look_at_point(self.model, data, aim):
            held += 1
            frame, depth = self.frame(data)
            yield frame, depth, look
        if not held:
            # Not "looked and saw nothing": never looked. The two are
            # different and the table has to be able to say which.
            self.unreachable += 1

    def report(self) -> dict:
        return {**super().report(), "standoffs_m": rk.LOOK_STANDOFFS,
                "elevation_deg": rk.LOOK_ELEVATION,
                "bearings": len(rk.BEARINGS),
                "out_of_reach": self.unreachable}


class MocapCamera(Eye):
    """A camera on a mocap mount, teleported to each pose"""

    def __init__(self, model, data, cam, width, height):
        super().__init__(model, data, cam, width, height)
        self.mocap = int(model.body_mocapid[model.cam_bodyid[cam]])
        self.local = (model.cam_pos[cam].copy(), model.cam_quat[cam].copy())

    def look(self, data: mujoco.MjData, aim: np.ndarray):
        """Every view of a point, from each azimuth in turn

        Yields:
            The BGR frame, its depth buffer, and the pose it was taken at.
        """
        aim = np.asarray(aim, float)
        side = -1.0 if aim[1] < 0 else 1.0
        rise = np.radians(ELEVATION_DEG)
        for azimuth in np.radians(AZIMUTHS_DEG):
            position = aim + STANDOFF_M * np.array([
                np.cos(rise) * np.sin(azimuth),
                side * np.cos(rise) * np.cos(azimuth),
                np.sin(rise),
            ])
            self._fly(data, position, aim)
            frame, depth = self.frame(data)
            yield frame, depth, position

    def _fly(self, data: mujoco.MjData, position: np.ndarray,
             target: np.ndarray) -> None:
        """Set the mount to whatever puts the camera where asked, looking there

        The camera keeps the pose relative to its mount that the scene file
        gives it, so the mount carries the difference.
        """
        quat = np.zeros(4)
        mujoco.mju_mulQuat(quat, _look_at(position, target),
                           _conjugate(self.local[1]))
        offset = np.zeros(3)
        mujoco.mju_rotVecQuat(offset, self.local[0], quat)
        data.mocap_pos[self.mocap] = np.asarray(position, float) - offset
        data.mocap_quat[self.mocap] = quat
        # Camera poses are mj_camlight's job, not mj_kinematics'. A renderer
        # reads cam_xpos, so skipping it renders the parked view over and over
        # wherever the mount was put.
        mujoco.mj_kinematics(self.model, data)
        mujoco.mj_camlight(self.model, data)

    def report(self) -> dict:
        return {**super().report(), "standoff_m": STANDOFF_M,
                "elevation_deg": ELEVATION_DEG, "azimuths": len(AZIMUTHS_DEG)}


def mover(model: mujoco.MjModel, data: mujoco.MjData, how: str,
          size) -> Eye | None:
    """The camera this scene can confirm with, and the thing that moves it

    Args:
        model: Compiled scene.
        data: Its data, at the state the home pose is read from.
        how: ``arm``, ``mocap``, or ``auto`` for the arm where there is one.
        size: Called with a camera id, returns its (width, height).

    Returns:
        A mover, or None when the scene has no camera it can take to a bottle.
    """
    if how in ("arm", "auto") and rk.has_arm(model):
        cam = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, rk.EIH_CAMERA)
        return ArmCamera(model, data, cam, *size(cam))
    if how == "arm":
        return None
    cam = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "wrist")
    if cam < 0 or model.body_mocapid[model.cam_bodyid[cam]] < 0:
        return None
    return MocapCamera(model, data, cam, *size(cam))


def _look_at(position: np.ndarray, target: np.ndarray) -> np.ndarray:
    """The quaternion of a camera at ``position`` looking at ``target``

    MuJoCo cameras look down their -Z with +Y up, so the rotation's columns are
    right, up and back.
    """
    forward = np.asarray(target, float) - np.asarray(position, float)
    forward = forward / np.linalg.norm(forward)
    right = np.cross(forward, (0.0, 0.0, 1.0))
    right /= np.linalg.norm(right)
    quat = np.zeros(4)
    mujoco.mju_mat2Quat(quat, np.column_stack(
        [right, np.cross(right, forward), -forward]).reshape(-1))
    return quat


def _conjugate(quat: np.ndarray) -> np.ndarray:
    out = np.zeros(4)
    mujoco.mju_negQuat(out, quat)
    return out
