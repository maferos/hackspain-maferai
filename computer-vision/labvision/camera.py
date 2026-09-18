"""Single-camera geometry: a pixel is a ray, a known plane turns it into a point

A monocular camera cannot measure depth. Every pixel back-projects to a ray,
and the object could be anywhere along it. One extra constraint closes the
gap, and a vessel standing on a bench supplies that constraint for free: its
base lies on the bench plane, whose height is known. Intersecting the ray with
that plane recovers all three coordinates, with no second camera and no depth
sensor.

What it costs is calibration. Turning a pixel into a ray needs the
**intrinsics** --- focal length in pixels, principal point, and lens
distortion if the lens is real. Expressing that ray in world coordinates needs
the **extrinsics** --- where the camera is *and* which way it points. Both are
required. Position alone is not enough: from 3 m away, rotating the camera by
one degree slides the intersection across the bench by 5 cm.

There is a shortcut, and it is in here too. If every answer is going to lie on
the same plane, the whole pinhole model collapses into one 3x3 homography
between image pixels and plane coordinates, and that matrix can be fitted from
four known points on the plane without anyone ever naming a focal length ---
see :func:`homography_from_points`. It absorbs intrinsics and extrinsics
together. The only thing it cannot absorb is lens distortion, which is not
projective and has to be removed first.

Conventions
-----------

**World**: right-handed, metres, **+Z up**.

**Camera**: the OpenCV frame --- **+X right, +Y down, +Z forward** along the
optical axis. MuJoCo and OpenGL use +Y up and -Z forward instead;
:meth:`Camera.from_mujoco` converts.

**Pixels**: ``(u, v)`` with u rightwards and v downwards, ``(0, 0)`` at the
*centre* of the top-left pixel. An ideal principal point therefore sits at
``((width - 1) / 2, (height - 1) / 2)``, which is what OpenCV assumes and what
dm_control's MuJoCo camera matrices produce.

**Failure is NaN, not an exception.** Every back-projection here is vectorised,
and a ray can legitimately miss the plane --- it is parallel to it, or it
points the other way, above the horizon. Those rows come back NaN.
:func:`labvision.scene.locate` is the layer that turns a NaN into a message.
"""

import math
from dataclasses import dataclass

import cv2
import numpy as np

_ORTHONORMAL_TOL = 1e-6
"""How far a rotation matrix may drift from orthonormal before it is rejected."""

_UNDISTORT_ITERATIONS = 5
"""Fixed-point steps used to invert the distortion model. OpenCV uses 5 too."""


class GeometryError(ValueError):
    """Raised when a camera, a plane or a set of correspondences is unusable"""


def _vector(value: object, name: str, size: int = 3) -> np.ndarray:
    """Coerce value to a read-only float vector of the given size"""
    arr = np.array(value, dtype=float).reshape(-1)
    if arr.shape != (size,):
        raise GeometryError(f"{name} must have {size} components, got {arr.size}")
    if not np.isfinite(arr).all():
        raise GeometryError(f"{name} must be finite, got {arr.tolist()}")
    arr.flags.writeable = False
    return arr


def _unit(vector: np.ndarray, name: str) -> np.ndarray:
    """Normalise a vector to unit length, rejecting a zero one"""
    norm = float(np.linalg.norm(vector))
    if norm < 1e-12:
        raise GeometryError(f"{name} must not be zero-length")
    unit = vector / norm
    unit.flags.writeable = False
    return unit


def _distort(xy: np.ndarray, coefficients: tuple[float, ...]) -> np.ndarray:
    """Apply Brown-Conrady distortion to ideal normalised coordinates

    Args:
        xy: (..., 2) ideal pinhole coordinates, focal lengths divided out.
        coefficients: (k1, k2, p1, p2) or (k1, k2, p1, p2, k3).

    Returns:
        The distorted coordinates, same shape.
    """
    k1, k2, p1, p2, k3 = (*coefficients, 0.0)[:5]
    x, y = xy[..., 0], xy[..., 1]
    r2 = x * x + y * y
    radial = 1.0 + r2 * (k1 + r2 * (k2 + r2 * k3))
    dx = 2.0 * p1 * x * y + p2 * (r2 + 2.0 * x * x)
    dy = p1 * (r2 + 2.0 * y * y) + 2.0 * p2 * x * y
    return np.stack([x * radial + dx, y * radial + dy], axis=-1)


def _undistort(xy: np.ndarray, coefficients: tuple[float, ...]) -> np.ndarray:
    """Invert :func:`_distort` by fixed-point iteration

    The model has no closed-form inverse. Rearranging it as
    ``x = (x_distorted - tangential) / radial`` and iterating converges in a
    handful of steps for any sane lens, which is exactly what OpenCV's
    ``undistortPoints`` does; ``test_camera.py`` pins the two against each
    other to 1e-9.

    Five steps is what OpenCV uses and what is used here, which on a strongly
    barrelled lens leaves about a hundredth of a pixel in the image corners.
    That is two orders of magnitude below what a detector contributes, and
    matching the oracle exactly is worth more than chasing it.

    Args:
        xy: (..., 2) distorted normalised coordinates, as measured.
        coefficients: (k1, k2, p1, p2) or (k1, k2, p1, p2, k3).

    Returns:
        The ideal pinhole coordinates, same shape.
    """
    k1, k2, p1, p2, k3 = (*coefficients, 0.0)[:5]
    xd, yd = xy[..., 0], xy[..., 1]
    x, y = xd.copy(), yd.copy()
    for _ in range(_UNDISTORT_ITERATIONS):
        r2 = x * x + y * y
        radial = 1.0 + r2 * (k1 + r2 * (k2 + r2 * k3))
        dx = 2.0 * p1 * x * y + p2 * (r2 + 2.0 * x * x)
        dy = p1 * (r2 + 2.0 * y * y) + 2.0 * p2 * x * y
        x = (xd - dx) / radial
        y = (yd - dy) / radial
    return np.stack([x, y], axis=-1)


@dataclass(frozen=True)
class Intrinsics:
    """What the lens and sensor do to a ray, in pixels

    Attributes:
        fx: Focal length along u, in pixels. Equal to fy for square pixels.
        fy: Focal length along v, in pixels.
        cx: Principal point u, where the optical axis meets the sensor.
        cy: Principal point v.
        width: Image width in pixels.
        height: Image height in pixels.
        distortion: Brown-Conrady coefficients, either (k1, k2, p1, p2) or
            (k1, k2, p1, p2, k3). Empty means an ideal pinhole, which is what
            a renderer gives you.
    """

    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int
    distortion: tuple[float, ...] = ()

    def __post_init__(self) -> None:
        """Reject focal lengths, image sizes and coefficient counts that cannot be"""
        if not (self.fx > 0 and self.fy > 0):
            raise GeometryError(f"focal lengths must be positive, got {self.fx}, "
                                f"{self.fy}")
        if not (self.width > 0 and self.height > 0):
            raise GeometryError(f"image size must be positive, got {self.width}x"
                                f"{self.height}")
        if len(self.distortion) not in (0, 4, 5):
            raise GeometryError("distortion must be 4 or 5 coefficients, got "
                                f"{len(self.distortion)}")

    @classmethod
    def from_fov(
        cls,
        width: int,
        height: int,
        *,
        fovy_deg: float | None = None,
        fovx_deg: float | None = None,
        distortion: tuple[float, ...] = (),
    ) -> "Intrinsics":
        """Build ideal intrinsics from an image size and one field of view

        Pixels are assumed square, so one field of view fixes both focal
        lengths and the other field of view follows from the aspect ratio.
        This is the constructor for a rendered camera: MuJoCo's ``fovy``
        drops straight in.

        Args:
            width: Image width in pixels.
            height: Image height in pixels.
            fovy_deg: Full vertical field of view in degrees.
            fovx_deg: Full horizontal field of view, as an alternative.
            distortion: Brown-Conrady coefficients, normally none here.

        Returns:
            Intrinsics with the principal point at the image centre.

        Raises:
            GeometryError: If not exactly one field of view is given, or it is
                not strictly between 0 and 180 degrees.

        Example:
            >>> round(Intrinsics.from_fov(640, 480, fovy_deg=45.0).fy, 3)
            579.411
        """
        if (fovy_deg is None) == (fovx_deg is None):
            raise GeometryError("give exactly one of fovy_deg and fovx_deg")
        fov = fovy_deg if fovy_deg is not None else fovx_deg
        if not 0.0 < float(fov) < 180.0:
            raise GeometryError(f"field of view must be in (0, 180), got {fov}")
        extent = height / 2.0 if fovy_deg is not None else width / 2.0
        focal = extent / math.tan(math.radians(float(fov)) / 2.0)
        return cls(focal, focal, (width - 1) / 2.0, (height - 1) / 2.0,
                   width, height, distortion)

    @classmethod
    def from_sensor(
        cls,
        width: int,
        height: int,
        *,
        focal_mm: float,
        sensor_width_mm: float,
        distortion: tuple[float, ...] = (),
    ) -> "Intrinsics":
        """Build ideal intrinsics from a lens and sensor datasheet

        Args:
            width: Image width in pixels.
            height: Image height in pixels.
            focal_mm: Lens focal length in millimetres.
            sensor_width_mm: Active sensor width in millimetres.
            distortion: Brown-Conrady coefficients.

        Returns:
            Intrinsics with the principal point at the image centre.

        Raises:
            GeometryError: If either millimetre figure is not positive.
        """
        if not (focal_mm > 0 and sensor_width_mm > 0):
            raise GeometryError("focal_mm and sensor_width_mm must be positive")
        focal = focal_mm * width / sensor_width_mm
        return cls(focal, focal, (width - 1) / 2.0, (height - 1) / 2.0,
                   width, height, distortion)

    @property
    def matrix(self) -> np.ndarray:
        """The 3x3 camera matrix K."""
        return np.array([[self.fx, 0.0, self.cx],
                         [0.0, self.fy, self.cy],
                         [0.0, 0.0, 1.0]])

    @property
    def distortion_vector(self) -> np.ndarray:
        """Distortion coefficients as the 5-vector OpenCV expects."""
        return np.array((*self.distortion, 0.0, 0.0, 0.0, 0.0, 0.0)[:5])

    @property
    def fovx_deg(self) -> float:
        """Full horizontal field of view in degrees."""
        return math.degrees(2.0 * math.atan(self.width / 2.0 / self.fx))

    @property
    def fovy_deg(self) -> float:
        """Full vertical field of view in degrees."""
        return math.degrees(2.0 * math.atan(self.height / 2.0 / self.fy))

    def normalise(self, uv: object) -> np.ndarray:
        """Turn measured pixels into ideal pinhole coordinates

        Args:
            uv: (..., 2) pixel coordinates.

        Returns:
            (..., 2) coordinates with the focal lengths divided out, the
            principal point subtracted and distortion removed.
        """
        pixels = np.asarray(uv, dtype=float)
        xy = np.stack([(pixels[..., 0] - self.cx) / self.fx,
                       (pixels[..., 1] - self.cy) / self.fy], axis=-1)
        return _undistort(xy, self.distortion) if self.distortion else xy

    def denormalise(self, xy: object) -> np.ndarray:
        """Turn ideal pinhole coordinates into the pixels a camera would record

        Args:
            xy: (..., 2) ideal pinhole coordinates.

        Returns:
            (..., 2) pixel coordinates, distortion applied.
        """
        ideal = np.asarray(xy, dtype=float)
        distorted = _distort(ideal, self.distortion) if self.distortion else ideal
        return np.stack([distorted[..., 0] * self.fx + self.cx,
                         distorted[..., 1] * self.fy + self.cy], axis=-1)

    def contains(self, uv: object) -> np.ndarray:
        """Say which pixels fall inside the image

        Args:
            uv: (..., 2) pixel coordinates.

        Returns:
            (...) boolean array. The image spans -0.5 to size - 0.5, since
            integer coordinates sit at pixel centres.
        """
        pixels = np.asarray(uv, dtype=float)
        return ((pixels[..., 0] >= -0.5) & (pixels[..., 0] <= self.width - 0.5)
                & (pixels[..., 1] >= -0.5) & (pixels[..., 1] <= self.height - 0.5))


@dataclass(frozen=True, eq=False)
class Plane:
    """An infinite plane, as a point on it and a unit normal

    Attributes:
        point: Any point lying on the plane, in world metres.
        normal: Unit normal. Which way it faces does not matter for
            intersection; it only flips the sign of :meth:`signed_distance`.
    """

    point: np.ndarray
    normal: np.ndarray

    def __post_init__(self) -> None:
        """Coerce both vectors to read-only floats and normalise the normal"""
        object.__setattr__(self, "point", _vector(self.point, "plane point"))
        object.__setattr__(
            self, "normal", _unit(_vector(self.normal, "plane normal"), "plane normal")
        )

    @classmethod
    def horizontal(cls, z: float) -> "Plane":
        """The horizontal plane at height z, which is what a table top is

        Args:
            z: Height above the floor in metres.

        Returns:
            The plane z = constant, normal pointing up.
        """
        return cls(np.array([0.0, 0.0, float(z)]), np.array([0.0, 0.0, 1.0]))

    def signed_distance(self, points: object) -> np.ndarray:
        """Distance from points to the plane, positive on the normal's side

        Args:
            points: (..., 3) world points.

        Returns:
            (...) signed distances in metres.
        """
        return (np.asarray(points, dtype=float) - self.point) @ self.normal


@dataclass(frozen=True, eq=False)
class Camera:
    """A calibrated camera: intrinsics plus where it is and where it looks

    Attributes:
        intrinsics: The pinhole model.
        position: Camera centre in world metres.
        rotation: 3x3 matrix whose columns are the camera's right, down and
            forward axes expressed in world coordinates, so it maps a
            direction from camera coordinates to world coordinates.
    """

    intrinsics: Intrinsics
    position: np.ndarray
    rotation: np.ndarray

    def __post_init__(self) -> None:
        """Coerce the pose to read-only floats and check the rotation is one"""
        object.__setattr__(self, "position", _vector(self.position, "position"))
        matrix = np.asarray(self.rotation, dtype=float)
        if matrix.shape != (3, 3):
            raise GeometryError(f"rotation must be 3x3, got {matrix.shape}")
        if not np.allclose(matrix @ matrix.T, np.eye(3), atol=_ORTHONORMAL_TOL):
            raise GeometryError("rotation must be orthonormal")
        if not math.isclose(float(np.linalg.det(matrix)), 1.0, abs_tol=1e-6):
            raise GeometryError("rotation must be right-handed, determinant +1")
        matrix = matrix.copy()
        matrix.flags.writeable = False
        object.__setattr__(self, "rotation", matrix)

    @classmethod
    def look_at(
        cls,
        intrinsics: Intrinsics,
        position: object,
        target: object,
        *,
        up: object = (0.0, 0.0, 1.0),
        roll_deg: float = 0.0,
    ) -> "Camera":
        """Point a camera at a world point

        Args:
            intrinsics: The pinhole model.
            position: Camera centre in world metres.
            target: World point the optical axis passes through.
            up: World direction that should appear upward in the image.
            roll_deg: Rotation about the optical axis, clockwise in the image.

        Returns:
            The camera.

        Raises:
            GeometryError: If the camera sits on the target, or if the viewing
                direction is parallel to up so that "up" says nothing.

        Example:
            >>> intr = Intrinsics.from_fov(640, 480, fovy_deg=45.0)
            >>> camera = Camera.look_at(intr, (7, 0, 3), (7, 2.5, 0.95))
            >>> [round(float(x), 4) for x in camera.forward]
            [0.0, 0.7733, -0.6341]
        """
        eye = _vector(position, "position")
        forward = _unit(_vector(target, "target") - eye, "target minus position")
        world_up = _unit(_vector(up, "up"), "up")
        right = np.cross(forward, world_up)
        if float(np.linalg.norm(right)) < 1e-9:
            raise GeometryError("the viewing direction is parallel to up; "
                                "pass a different up vector")
        right = _unit(right, "right")
        down = np.cross(forward, right)
        rotation = np.column_stack([right, down, forward])
        if roll_deg:
            angle = math.radians(roll_deg)
            spin = np.array([[math.cos(angle), -math.sin(angle), 0.0],
                             [math.sin(angle), math.cos(angle), 0.0],
                             [0.0, 0.0, 1.0]])
            rotation = rotation @ spin
        return cls(intrinsics, eye, rotation)

    @classmethod
    def from_pan_tilt(
        cls,
        intrinsics: Intrinsics,
        position: object,
        *,
        pan_deg: float,
        tilt_deg: float,
        roll_deg: float = 0.0,
    ) -> "Camera":
        """Point a camera by the angles a mount is actually adjusted with

        Args:
            intrinsics: The pinhole model.
            position: Camera centre in world metres.
            pan_deg: Azimuth of the optical axis, measured in the floor plane
                from +X towards +Y.
            tilt_deg: Angle below horizontal, positive looking down.
            roll_deg: Rotation about the optical axis, clockwise in the image.

        Returns:
            The camera.
        """
        pan, tilt = math.radians(pan_deg), math.radians(tilt_deg)
        forward = np.array([math.cos(tilt) * math.cos(pan),
                            math.cos(tilt) * math.sin(pan),
                            -math.sin(tilt)])
        eye = _vector(position, "position")
        return cls.look_at(intrinsics, eye, eye + forward, roll_deg=roll_deg)

    @classmethod
    def from_mujoco(
        cls, intrinsics: Intrinsics, cam_pos: object, cam_xmat: object,
    ) -> "Camera":
        """Adopt a MuJoCo camera pose, converting the frame

        MuJoCo, like OpenGL, has the camera look down its own -Z with +Y up,
        where OpenCV looks down +Z with +Y down. The two differ by a flip of
        the last two axes.

        Args:
            intrinsics: The pinhole model, normally from ``fovy``.
            cam_pos: ``data.cam_xpos[i]``, the camera centre in world metres.
            cam_xmat: ``data.cam_xmat[i]``, nine numbers, row-major, whose
                columns are the camera axes in world coordinates.

        Returns:
            The same camera in this module's convention.
        """
        gl = np.asarray(cam_xmat, dtype=float).reshape(3, 3)
        return cls(intrinsics, cam_pos, gl @ np.diag([1.0, -1.0, -1.0]))

    @classmethod
    def from_correspondences(
        cls,
        intrinsics: Intrinsics,
        image_uv: object,
        world_xyz: object,
        *,
        flags: int = cv2.SOLVEPNP_ITERATIVE,
    ) -> "Camera":
        """Recover the extrinsics from points whose world position is known

        This is how the extrinsics are obtained in practice. Nobody measures a
        mounted camera's orientation to a tenth of a degree with a protractor;
        you stick four markers on the table at measured positions, click them
        in one frame, and solve. Four coplanar points are enough, and more
        non-coplanar ones are better conditioned.

        Args:
            intrinsics: The pinhole model, already calibrated.
            image_uv: (N, 2) pixel coordinates of the markers.
            world_xyz: (N, 3) world coordinates of the same markers, in metres
                and in the same order.
            flags: OpenCV solvePnP method.

        Returns:
            The camera, intrinsics unchanged.

        Raises:
            GeometryError: If there are fewer than four points, the two sets
                disagree in length, or the solver fails.
        """
        image = np.asarray(image_uv, dtype=float).reshape(-1, 2)
        world = np.asarray(world_xyz, dtype=float).reshape(-1, 3)
        if len(image) != len(world):
            raise GeometryError(f"got {len(image)} pixels but {len(world)} "
                                "world points")
        if len(image) < 4:
            raise GeometryError(f"need at least 4 correspondences, got {len(image)}")
        found, rvec, tvec = cv2.solvePnP(
            world.reshape(-1, 1, 3), image.reshape(-1, 1, 2),
            intrinsics.matrix, intrinsics.distortion_vector, flags=flags,
        )
        if not found:
            raise GeometryError("solvePnP found no pose for these correspondences")
        rotation_cw, _ = cv2.Rodrigues(rvec)
        position = -rotation_cw.T @ tvec.reshape(3)
        return cls(intrinsics, position, rotation_cw.T)

    @property
    def rotation_world_to_camera(self) -> np.ndarray:
        """The inverse rotation, world directions into camera coordinates."""
        return self.rotation.T

    @property
    def right(self) -> np.ndarray:
        """Camera +X in world coordinates, rightwards in the image."""
        return self.rotation[:, 0]

    @property
    def down(self) -> np.ndarray:
        """Camera +Y in world coordinates, downwards in the image."""
        return self.rotation[:, 1]

    @property
    def forward(self) -> np.ndarray:
        """Camera +Z in world coordinates, the optical axis."""
        return self.rotation[:, 2]

    @property
    def extrinsic_matrix(self) -> np.ndarray:
        """The 3x4 [R|t] that takes world points into camera coordinates."""
        rotation_cw = self.rotation.T
        return np.column_stack([rotation_cw, -rotation_cw @ self.position])

    @property
    def projection_matrix(self) -> np.ndarray:
        """The 3x4 P = K[R|t] for an ideal pinhole, ignoring distortion."""
        return self.intrinsics.matrix @ self.extrinsic_matrix

    def project(self, points: object) -> np.ndarray:
        """Project world points into the image

        Args:
            points: (..., 3) world points in metres.

        Returns:
            (..., 2) pixel coordinates. Points at or behind the camera's
            principal plane come back NaN, since they have no image.
        """
        world = np.asarray(points, dtype=float)
        local = (world - self.position) @ self.rotation
        depth = local[..., 2]
        with np.errstate(divide="ignore", invalid="ignore"):
            xy = local[..., :2] / depth[..., None]
        pixels = self.intrinsics.denormalise(xy)
        return np.where(np.asarray(depth <= 0.0)[..., None], np.nan, pixels)

    def pixel_ray(self, uv: object) -> np.ndarray:
        """Back-project pixels to unit ray directions in world coordinates

        Args:
            uv: (..., 2) pixel coordinates.

        Returns:
            (..., 3) unit direction vectors leaving :attr:`position`.
        """
        xy = self.intrinsics.normalise(uv)
        camera_ray = np.concatenate([xy, np.ones(xy.shape[:-1] + (1,))], axis=-1)
        world_ray = camera_ray @ self.rotation.T
        return world_ray / np.linalg.norm(world_ray, axis=-1, keepdims=True)

    def range_to(self, points: object) -> np.ndarray:
        """Distance from the camera centre to world points

        Args:
            points: (..., 3) world points in metres.

        Returns:
            (...) distances in metres.
        """
        return np.linalg.norm(np.asarray(points, dtype=float) - self.position, axis=-1)


def ray_plane_intersection(
    origin: object, direction: object, plane: Plane, *, eps: float = 1e-12,
) -> np.ndarray:
    """Intersect rays with a plane

    Solving ``n . (o + t d - p0) = 0`` for t is one division. The two ways it
    has no answer are both real cases here, and both return NaN: the ray runs
    parallel to the plane (``n . d`` is zero, the object is on the horizon),
    or the plane is behind the camera (t is negative, the pixel is above the
    horizon and looking at the far wall).

    Args:
        origin: (3,) ray origin, or (..., 3) one origin per ray.
        direction: (..., 3) ray directions, not necessarily unit.
        plane: The plane to hit.
        eps: Below this, ``n . d`` counts as parallel.

    Returns:
        (..., 3) intersection points, NaN where there is none.
    """
    start = np.asarray(origin, dtype=float)
    ray = np.asarray(direction, dtype=float)
    denominator = ray @ plane.normal
    numerator = (plane.point - start) @ plane.normal
    with np.errstate(divide="ignore", invalid="ignore"):
        distance = np.asarray(numerator / denominator, dtype=float)
    distance = np.where(np.abs(denominator) < eps, np.nan, distance)
    distance = np.where(distance <= 0.0, np.nan, distance)
    return start + distance[..., None] * ray


def pixel_to_plane(camera: Camera, uv: object, plane: Plane) -> np.ndarray:
    """Back-project pixels onto a known plane --- the whole point of the module

    Args:
        camera: The calibrated camera.
        uv: (..., 2) pixel coordinates.
        plane: The plane the object is known to lie on.

    Returns:
        (..., 3) world points in metres, NaN where the ray misses the plane.

    Example:
        >>> intr = Intrinsics.from_fov(640, 480, fovy_deg=45.0)
        >>> camera = Camera.look_at(intr, (7, 0, 3), (7, 2.5, 0.95))
        >>> point = pixel_to_plane(camera, (319.5, 239.5), Plane.horizontal(0.95))
        >>> [round(float(x), 6) for x in point]
        [7.0, 2.5, 0.95]
    """
    return ray_plane_intersection(camera.position, camera.pixel_ray(uv), plane)


def plane_jacobian(camera: Camera, uv: object, plane: Plane) -> np.ndarray:
    """Differentiate the plane point with respect to the pixel

    This is the error budget in closed form: multiply it by a detector's pixel
    error to get metres on the table. Writing the unnormalised ray as
    ``D = R m`` with ``m = ((u - cx) / fx, (v - cy) / fy, 1)``, the hit is
    ``P = C + t D`` with ``t = n . (p0 - C) / (n . D)``, so

        dP/du = t dD/du + D dt/du,  dt/du = -t (n . dD/du) / (n . D)

    and ``dD/du`` is just the first column of R over fx.

    Lens distortion is left out of the derivative. It warps the pixel grid by
    a few percent, which is below the precision an error budget is quoted to.

    Args:
        camera: The calibrated camera.
        uv: (2,) pixel coordinate to linearise at.
        plane: The plane being intersected.

    Returns:
        (3, 2) matrix of metres per pixel, columns for u and v. All NaN if the
        ray misses the plane.
    """
    pixel = np.asarray(uv, dtype=float).reshape(2)
    ideal = camera.intrinsics.normalise(pixel)
    ray = camera.rotation @ np.array([ideal[0], ideal[1], 1.0])
    denominator = float(ray @ plane.normal)
    if abs(denominator) < 1e-12:
        return np.full((3, 2), np.nan)
    distance = float((plane.point - camera.position) @ plane.normal) / denominator
    if distance <= 0.0:
        return np.full((3, 2), np.nan)
    d_ray = np.column_stack([camera.rotation[:, 0] / camera.intrinsics.fx,
                             camera.rotation[:, 1] / camera.intrinsics.fy])
    d_distance = -distance * (plane.normal @ d_ray) / denominator
    return distance * d_ray + np.outer(ray, d_distance)


def metres_per_pixel(camera: Camera, uv: object, plane: Plane) -> tuple[float, float]:
    """Worst and best ground displacement caused by one pixel of image error

    The Jacobian is not isotropic: near the horizon a pixel of vertical error
    slides the hit far along the line of sight, while a pixel of horizontal
    error barely moves it. The two singular values are those two extremes.

    Args:
        camera: The calibrated camera.
        uv: (2,) pixel coordinate.
        plane: The plane being intersected.

    Returns:
        (worst, best) metres of world displacement per pixel. NaN if the ray
        misses the plane.
    """
    jacobian = plane_jacobian(camera, uv, plane)
    if not np.isfinite(jacobian).all():
        return (float("nan"), float("nan"))
    values = np.linalg.svd(jacobian, compute_uv=False)
    return (float(values[0]), float(values[1]))


def horizon_line(camera: Camera, plane: Plane) -> np.ndarray:
    """The image line beyond which no pixel ever meets the plane

    The plane's vanishing line. Rays through pixels on one side of it hit the
    plane in front of the camera; rays on the other side hit it behind, which
    in a real room means they are looking at the far wall. A detection whose
    anchor pixel lands on the wrong side is not a mis-measurement, it is a
    detection that cannot be on the table at all.

    Args:
        camera: The calibrated camera.
        plane: The plane in question.

    Returns:
        (3,) line coefficients (a, b, c) with ``a u + b v + c = 0``. For a
        table below the camera, ``a u + b v + c > 0`` is the half-plane that
        hits it.
    """
    normal_camera = camera.rotation.T @ plane.normal
    a = normal_camera[0] / camera.intrinsics.fx
    b = normal_camera[1] / camera.intrinsics.fy
    c = normal_camera[2] - a * camera.intrinsics.cx - b * camera.intrinsics.cy
    offset = float((plane.point - camera.position) @ plane.normal)
    return math.copysign(1.0, offset) * np.array([a, b, c])


def plane_footprint(camera: Camera, plane: Plane) -> np.ndarray:
    """Back-project the image corners to see what patch of the plane is in frame

    Args:
        camera: The calibrated camera.
        plane: The plane to trace onto.

    Returns:
        (4, 3) world points for the top-left, top-right, bottom-right and
        bottom-left image corners. A corner above the horizon comes back NaN,
        which means the view runs off the plane and the visible patch is
        unbounded in that direction.
    """
    width, height = camera.intrinsics.width, camera.intrinsics.height
    corners = np.array([[-0.5, -0.5], [width - 0.5, -0.5],
                        [width - 0.5, height - 0.5], [-0.5, height - 0.5]])
    return pixel_to_plane(camera, corners, plane)


def plane_homography(camera: Camera, z: float) -> np.ndarray:
    """Collapse the camera onto one horizontal plane, as a 3x3 matrix

    On a single plane the pinhole model is redundant. Substituting a fixed z
    into ``P = K [R | t] X`` deletes the third column of the rotation and what
    is left is a plane-to-image homography ``H`` with ``pixel ~ H (X, Y, 1)``.
    Inverting it maps pixels straight to table coordinates.

    Args:
        camera: The calibrated camera.
        z: Height of the horizontal plane in metres.

    Returns:
        3x3 matrix taking homogeneous plane coordinates (X, Y, 1) to
        homogeneous pixels, defined up to scale.

    Raises:
        GeometryError: If the camera has distortion. A homography is a
            projective map and cannot represent a radial one; undistort the
            image or the pixels first, then use ideal intrinsics here.
    """
    if camera.intrinsics.distortion:
        raise GeometryError("a homography cannot absorb lens distortion; "
                            "undistort first and use ideal intrinsics")
    rotation_cw = camera.rotation.T
    offset = rotation_cw @ (np.array([0.0, 0.0, float(z)]) - camera.position)
    return camera.intrinsics.matrix @ np.column_stack(
        [rotation_cw[:, 0], rotation_cw[:, 1], offset]
    )


def apply_homography(homography: np.ndarray, points: object) -> np.ndarray:
    """Map 2D points through a 3x3 homography

    Args:
        homography: 3x3 matrix.
        points: (..., 2) source points.

    Returns:
        (..., 2) destination points, NaN where the third coordinate vanishes
        (the source point maps to infinity).
    """
    source = np.asarray(points, dtype=float)
    homogeneous = np.concatenate(
        [source, np.ones(source.shape[:-1] + (1,))], axis=-1
    ) @ np.asarray(homography, dtype=float).T
    scale = homogeneous[..., 2]
    with np.errstate(divide="ignore", invalid="ignore"):
        mapped = homogeneous[..., :2] / scale[..., None]
    unusable = np.asarray(np.abs(scale) < 1e-12)[..., None]
    return np.where(unusable, np.nan, mapped)


def homography_from_points(plane_xy: object, image_uv: object) -> np.ndarray:
    """Fit a plane-to-image homography from four or more known points

    The calibration-free route. Stick markers on the table, measure their
    (X, Y) with a tape, click them in one frame, and this returns the same
    matrix :func:`plane_homography` builds from a full calibration --- without
    a focal length, a principal point or a camera pose ever being named. It is
    the right tool when all the answers lie on one plane and nothing else
    needs the camera model.

    Solved by the direct linear transform: each correspondence contributes two
    rows to a 2N x 9 system, and the homography is the null vector, taken as
    the last right singular vector. Both point sets are first translated to
    their centroid and scaled to a mean radius of sqrt(2), which is Hartley
    normalisation --- skip it and the system is badly conditioned enough to
    lose several digits.

    Args:
        plane_xy: (N, 2) coordinates on the plane, in metres, N >= 4.
        image_uv: (N, 2) pixel coordinates of the same points, in order.

    Returns:
        3x3 matrix taking (X, Y, 1) to homogeneous pixels, scaled so that the
        bottom-right entry is 1.

    Raises:
        GeometryError: If there are fewer than four points, the two sets
            disagree in length, or the points are degenerate (three or more
            collinear, or all coincident).
    """
    source = np.asarray(plane_xy, dtype=float).reshape(-1, 2)
    target = np.asarray(image_uv, dtype=float).reshape(-1, 2)
    if len(source) != len(target):
        raise GeometryError(f"got {len(source)} plane points but {len(target)} "
                            "image points")
    if len(source) < 4:
        raise GeometryError(f"need at least 4 correspondences, got {len(source)}")

    normalise_source, source_n = _hartley(source)
    normalise_target, target_n = _hartley(target)
    rows = []
    for (x, y), (u, v) in zip(source_n, target_n, strict=True):
        rows.append([-x, -y, -1.0, 0.0, 0.0, 0.0, u * x, u * y, u])
        rows.append([0.0, 0.0, 0.0, -x, -y, -1.0, v * x, v * y, v])
    _, singular, right = np.linalg.svd(np.array(rows))
    # The solution is the null vector, right[-1]. It is only defined if the
    # null space is one-dimensional, so the *second* smallest of the nine
    # singular directions has to be clear of zero. For four points the system
    # is 8x9 and numpy returns eight values, the ninth being the implicit zero
    # the solution lives in; for more points it returns all nine.
    second_smallest = singular[-1] if len(singular) == 8 else singular[-2]
    if second_smallest <= 1e-8 * singular[0]:
        raise GeometryError("these correspondences are degenerate --- three or "
                            "more of the points are collinear")
    homography = right[-1].reshape(3, 3)
    homography = np.linalg.inv(normalise_target) @ homography @ normalise_source
    if abs(homography[2, 2]) < 1e-12:
        raise GeometryError("the fitted homography is singular")
    return homography / homography[2, 2]


def _hartley(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Translate points to their centroid and scale them to a mean radius

    Args:
        points: (N, 2) points.

    Returns:
        The 3x3 normalising transform and the (N, 2) normalised points.
    """
    centroid = points.mean(axis=0)
    centred = points - centroid
    radius = float(np.sqrt((centred ** 2).sum(axis=1)).mean())
    if radius < 1e-12:
        raise GeometryError("all the points coincide")
    scale = math.sqrt(2.0) / radius
    transform = np.array([[scale, 0.0, -scale * centroid[0]],
                          [0.0, scale, -scale * centroid[1]],
                          [0.0, 0.0, 1.0]])
    return transform, centred * scale
