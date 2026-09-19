"""Fly the scene's wrist camera to a bottle and look at it from arm's length

The fixed cameras propose; this is what confirms. A flask on the rail bench is
12 to 24 pixels across in every fixed view, which is not enough to resolve a
4x4 marker, so reading the ring from across the room cannot work however good
the detector is. The ring reads from :data:`STANDOFF_M`, which is where the arm
would carry the camera anyway.

Only the flying is here: where to put the camera and how to render from it.
What is read in the frame, and what it means, stays in :mod:`vision`.

The camera is the scene's own ``wrist`` camera, which sits on a mocap mount
(``wrist_camera_mount``), so it is moved by writing a pose rather than by
solving the arm. That is the same camera and the same standoff the arm reaches
with; the poses it is flown to are checked for reach in
``simulation/scripts/rail_kinematics.py``, not here.

Nothing is asked of the simulator about whether a view is blocked: if a pose
reads nothing, the next of :data:`AZIMUTHS_DEG` is tried, which is what an arm
would do.
"""

import mujoco
import numpy as np

STANDOFF_M = 0.30
"""Camera to bottle. A GoPro's near focus, and the range at which the ring
reads on every bottle size (``computer-vision/scripts/ring_experiment.py``)."""
ELEVATION_DEG = 15.0
"""How far above level the camera looks down from. A camera level with the ring
cannot place it: its ray runs along the ring's height instead of crossing it
(``labvision.perception.refine``)."""
AZIMUTHS_DEG = (0, 25, -25, 50, -50)
"""Views tried in turn, from straight across the aisle to 50 degrees either
side, until one reads the ring."""


def find(model: mujoco.MjModel, name: str = "wrist") -> int | None:
    """The scene's movable camera of that name, or None if it has none

    Returns:
        Its camera id, or None when the scene has no such camera or the camera
        cannot be moved --- a fixed one would be part of the proposing pass.
    """
    cam = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, name)
    if cam < 0:
        return None
    return cam if model.body_mocapid[model.cam_bodyid[cam]] >= 0 else None


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


def poses(aim: np.ndarray, standoff: float = STANDOFF_M,
          elevation_deg: float = ELEVATION_DEG,
          azimuths_deg=AZIMUTHS_DEG) -> list[np.ndarray]:
    """Where to put the camera to look at a bottle, best view first

    It uses nothing but the aim point: which aisle is the nearer, and the
    azimuths to try from there.

    Args:
        aim: World point on the bottle's axis, at about the ring's height.
        standoff: Distance from the aim point.
        elevation_deg: How far above level to look down from.
        azimuths_deg: Azimuths to try, in order.

    Returns:
        One position per azimuth.
    """
    aim = np.asarray(aim, float)
    side = -1.0 if aim[1] < 0 else 1.0
    elevation = np.radians(elevation_deg)
    return [aim + standoff * np.array([
        np.cos(elevation) * np.sin(np.radians(azimuth)),
        side * np.cos(elevation) * np.cos(np.radians(azimuth)),
        np.sin(elevation),
    ]) for azimuth in azimuths_deg]


class WristCamera:
    """The scene's wrist camera, flown to wherever it is asked to look

    The camera keeps the pose relative to its mount that the scene file gives
    it; the mount is set to whatever puts the camera where asked.
    """

    def __init__(self, model: mujoco.MjModel, data: mujoco.MjData, cam: int,
                 width: int, height: int):
        """Take the camera's mount and home pose, and open a renderer for it

        Args:
            model: The compiled scene.
            data: Its data, at the state the home pose is read from.
            cam: The camera's id, from :func:`find`.
            width: Frame width to render.
            height: Frame height.
        """
        self.model, self.cam = model, cam
        self.width, self.height = width, height
        self.mocap = int(model.body_mocapid[model.cam_bodyid[cam]])
        self.local = (model.cam_pos[cam].copy(), model.cam_quat[cam].copy())
        self.home = (data.mocap_pos[self.mocap].copy(),
                     data.mocap_quat[self.mocap].copy())
        model.vis.global_.offwidth = max(model.vis.global_.offwidth, width)
        model.vis.global_.offheight = max(model.vis.global_.offheight, height)
        self.renderer = mujoco.Renderer(model, height=height, width=width)
        self.views = 0

    def look(self, data: mujoco.MjData, position: np.ndarray,
             target: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Put the camera at ``position``, aim it at ``target`` and render

        Returns:
            The BGR frame and MuJoCo's depth buffer for it.
        """
        quat = np.zeros(4)
        mujoco.mju_mulQuat(quat, _look_at(position, target),
                           _conjugate(self.local[1]))
        offset = np.zeros(3)
        mujoco.mju_rotVecQuat(offset, self.local[0], quat)
        data.mocap_pos[self.mocap] = np.asarray(position, float) - offset
        data.mocap_quat[self.mocap] = quat
        self._pose(data)
        self.views += 1

        self.renderer.update_scene(data, camera=self.cam)
        self.renderer.disable_depth_rendering()
        rgb = self.renderer.render()
        self.renderer.enable_depth_rendering()
        depth = self.renderer.render().copy()
        self.renderer.disable_depth_rendering()
        return rgb[:, :, ::-1].copy(), depth

    def _pose(self, data: mujoco.MjData) -> None:
        """Move the scene to the mount's new pose, cameras included

        mj_kinematics alone leaves ``cam_xpos`` where it was --- camera poses
        are mj_camlight's job --- and a renderer reads exactly that, so
        skipping it renders the parked view over and over, no matter where the
        mount was put. It looks like a camera that sees only what happens to
        stand near its parking spot, which is how this was found.
        """
        mujoco.mj_kinematics(self.model, data)
        mujoco.mj_camlight(self.model, data)

    def park(self, data: mujoco.MjData) -> None:
        """Put the mount back where the scene file had it"""
        data.mocap_pos[self.mocap], data.mocap_quat[self.mocap] = self.home
        self._pose(data)

    def close(self) -> None:
        self.renderer.close()


def _conjugate(quat: np.ndarray) -> np.ndarray:
    out = np.zeros(4)
    mujoco.mju_negQuat(out, quat)
    return out
