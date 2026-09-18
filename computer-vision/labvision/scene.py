"""The hackathon room, and the step from a detector's box to a point on the table

:mod:`labvision.camera` is general optics. This module is the specific room it
gets pointed at, plus the one piece of reasoning that sits between a detector
and the geometry: *which pixel of a bounding box should be back-projected*.

The room
--------

14 m along X, 5 m along Y, 3 m to the ceiling, origin at a floor corner. The
camera hangs at ceiling height in the middle of the long wall, at
(7, 0, 3), and the bench top --- the plane everything is intersected with ---
is at z = 0.95. The bench stands in the middle of the floor, so the camera
looks 2.5 m in and 2.05 m down at it: a 3.23 m line of sight at 39 degrees of
elevation.

Two of those numbers are assumptions rather than measurements, and both are
easy to replace once someone measures them:

- **Where the camera points.** Only its position was given. The default aims
  it at the middle of the bench, which is the sane mounting but not a fact.
  Get the real thing from four markers on the bench with
  :meth:`labvision.camera.Camera.from_correspondences`.
- **The bench footprint.** Unknown, so ``TABLE_SIZE`` is None and the
  "is it even on the table" check is skipped.

Which pixel to back-project
---------------------------

A box has four numbers and the object has two coordinates, so something has
to say what in the box stands for the object. Three ways are offered, and
``test_scene.py`` scores all three against exact boxes.

``"base"`` takes the **bottom-centre** of the box, which images the vessel's
contact patch with the bench --- already on the plane, no height needed. It
has one bias worth correcting. The lowest pixel of a vessel of radius r is not
its axis but the point of its base circle *nearest the camera*, so the raw
intersection lands short by exactly r along the plane direction in which image
v increases. That direction is not "towards the camera on the floor"; it is
the plane normal to the iso-v line, which :func:`~labvision.camera.plane_jacobian`
already provides. Subtracting r there removes the bias --- 2 to 6 cm for these
bottles, which is more than the whole pixel-noise budget.

``"centre"`` takes the **centre** of the box and intersects a plane lifted to
half the vessel's height. Use it when the base is hidden --- occluded by
another vessel, or cropped by the image edge --- at the cost of needing the
height and of a residual bias of its own, since the box centre is not the
image of the mid-height point under perspective.

``"fit"`` throws away no part of the box. :func:`predict_bbox` gives the exact
box a cylinder of known radius and height standing at a known point would
produce, so the position is simply the one whose predicted box matches the
observed one --- :func:`fit_position` solves that with Gauss-Newton on the
four edge residuals, started from the base anchor, in two or three steps. It
has no anchor bias at all, and its residual is the only thing in the pipeline
that notices a box labelled as the wrong vessel. It needs the dimensions,
which the barcode already supplies, and it is what ``"auto"`` picks whenever
they are known.

Whichever is used, the answer returned is the **base centre**, on the bench
plane; the mouth, which is where a pipette goes, is that plus the vessel
height.
"""

import argparse
import json
import math
from dataclasses import dataclass

import numpy as np

from labvision.camera import (
    Camera,
    GeometryError,
    Intrinsics,
    Plane,
    metres_per_pixel,
    pixel_to_plane,
    plane_jacobian,
)

ROOM_SIZE: tuple[float, float, float] = (14.0, 5.0, 3.0)
"""Room extent in metres, origin at a floor corner, X along the long wall."""

CAMERA_POSITION: tuple[float, float, float] = (7.0, 0.0, 3.0)
"""Camera centre: ceiling height, halfway along the 14 m wall."""

TABLE_TOP_Z = 0.95
"""Height of the bench top, the plane every ray is intersected with."""

TABLE_CENTRE: tuple[float, float] = (7.0, 2.5)
"""Bench centre in the floor plane; it is centred in the room."""

TABLE_SIZE: tuple[float, float] | None = None
"""Bench footprint in metres. Not measured yet, so on-table checks are skipped."""

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
DEFAULT_FOVY_DEG = 45.0
"""Frame size and vertical field of view of the MuJoCo renders, as a default."""

ANCHORS = ("auto", "fit", "base", "centre")
"""How a box is reduced to a position. ``auto`` fits when it can, anchors
on the base when the vessel's dimensions are unknown."""


@dataclass(frozen=True)
class Vessel:
    """A container standing upright on the bench

    Dimensions are the modelled ones from ``assets/agrochemical-bottles``,
    which are real labware sizes. Bottle and cap are separate objects there,
    and a closed bottle overlaps them by about a millimetre.

    Attributes:
        name: Key in :data:`VESSELS`.
        diameter_m: Body diameter, the width of the silhouette.
        height_m: Body height without the cap.
        cap_height_m: Cap height, or zero for an open vessel.
    """

    name: str
    diameter_m: float
    height_m: float
    cap_height_m: float = 0.0

    @property
    def radius_m(self) -> float:
        """Half the body diameter, the bias the base anchor has to undo."""
        return self.diameter_m / 2.0

    def silhouette_height_m(self, *, capped: bool = True) -> float:
        """Height of the whole shape a detector boxes

        Args:
            capped: Whether the cap is on, which it is on a stored bottle.

        Returns:
            Height in metres, cap included and overlapped by 1 mm when capped.
        """
        if not capped or self.cap_height_m == 0.0:
            return self.height_m
        return self.height_m + self.cap_height_m - 0.001


VESSELS: dict[str, Vessel] = {
    "bottle_100ml": Vessel("bottle_100ml", 0.046, 0.097, 0.019),
    "bottle_250ml": Vessel("bottle_250ml", 0.060, 0.131, 0.022),
    "bottle_500ml": Vessel("bottle_500ml", 0.074, 0.164, 0.025),
    "bottle_1000ml": Vessel("bottle_1000ml", 0.088, 0.216, 0.027),
    "bottle_1000ml_wide": Vessel("bottle_1000ml_wide", 0.102, 0.182, 0.032),
    "bottle_2000ml": Vessel("bottle_2000ml", 0.116, 0.245, 0.032),
}
"""The measured agrochemical bottle kit, keyed by the registry's vessel class.

The keys are :attr:`labvision.registry.Sample.vessel_class` exactly, so a
decoded barcode indexes straight into this table. ``bottle_1000ml_wide`` is
the one exception: the kit's wide-mouth 1 L bottle is left out of the sample
catalogue because it duplicates a nominal capacity, but its mesh exists, so
its dimensions are kept here.

The five flask classes (``flask_10ml`` and friends) are absent because
nothing in this repo records their dimensions yet. Pass ``radius`` and
``height`` explicitly for those, or add them here once they are measured.
"""


@dataclass(frozen=True)
class BBox:
    """An axis-aligned detection box in pixels

    Attributes:
        u_min: Left edge.
        v_min: Top edge.
        u_max: Right edge.
        v_max: Bottom edge.
    """

    u_min: float
    v_min: float
    u_max: float
    v_max: float

    def __post_init__(self) -> None:
        """Reject a box with no area"""
        if not (self.u_max > self.u_min and self.v_max > self.v_min):
            raise GeometryError(
                f"box must have positive area, got {self.as_tuple()}"
            )

    @classmethod
    def from_xywh(cls, u: float, v: float, width: float, height: float) -> "BBox":
        """Build a box from the top-left corner and a size

        Args:
            u: Left edge.
            v: Top edge.
            width: Width in pixels.
            height: Height in pixels.

        Returns:
            The box.
        """
        return cls(u, v, u + width, v + height)

    @classmethod
    def around(cls, points: object) -> "BBox":
        """Tightest box containing a set of image points

        Args:
            points: (N, 2) pixel coordinates. NaN rows are ignored.

        Returns:
            The box.

        Raises:
            GeometryError: If no point is finite.
        """
        pixels = np.asarray(points, dtype=float).reshape(-1, 2)
        pixels = pixels[np.isfinite(pixels).all(axis=1)]
        if len(pixels) == 0:
            raise GeometryError("no finite points to bound")
        return cls(*pixels.min(axis=0), *pixels.max(axis=0))

    def as_tuple(self) -> tuple[float, float, float, float]:
        """The box as (u_min, v_min, u_max, v_max)."""
        return (self.u_min, self.v_min, self.u_max, self.v_max)

    @property
    def width(self) -> float:
        """Box width in pixels."""
        return self.u_max - self.u_min

    @property
    def height(self) -> float:
        """Box height in pixels."""
        return self.v_max - self.v_min

    @property
    def centre(self) -> tuple[float, float]:
        """Centre pixel of the box."""
        return ((self.u_min + self.u_max) / 2.0, (self.v_min + self.v_max) / 2.0)

    @property
    def bottom_centre(self) -> tuple[float, float]:
        """Middle of the bottom edge, where a standing vessel meets the bench."""
        return ((self.u_min + self.u_max) / 2.0, self.v_max)

    def touches_frame(self, intrinsics: Intrinsics, *, margin: float = 1.0) -> bool:
        """Say whether the box runs into the image border

        A box clipped by the border is a box whose edges are the frame's, not
        the object's, which silently invalidates whichever anchor uses them.

        Args:
            intrinsics: The camera the box was detected in.
            margin: How many pixels from the border still counts as touching.

        Returns:
            True if any edge is within margin of the image boundary.
        """
        return bool(self.u_min <= -0.5 + margin
                    or self.v_min <= -0.5 + margin
                    or self.u_max >= intrinsics.width - 0.5 - margin
                    or self.v_max >= intrinsics.height - 0.5 - margin)


@dataclass(frozen=True, eq=False)
class Placement:
    """Where a detected vessel stands

    Attributes:
        position: Centre of the vessel's base, on the bench plane, in world
            metres. This is the answer.
        mouth: Centre of the vessel's opening, or None if no height was given.
        anchor_uv: The pixel that was back-projected.
        raw_hit: Where that pixel's ray met the plane, before the radius
            correction. ``position`` minus this is the correction applied.
        range_m: Distance from the camera to the position.
        metres_per_pixel: Worst-case ground displacement per pixel of
            detection error, at this point. Multiply by the detector's pixel
            error for the position error.
        inside_room: Whether the position lies within the room's walls.
        on_table: Whether it lies on the bench footprint, or None when the
            footprint is unknown.
        clipped: Whether the box touched the image border, which makes the
            answer unreliable whatever it says.
        residual_px: RMS disagreement in pixels between the observed box and
            the box the fitted position would produce, or None unless the
            ``fit`` anchor was used. A large value means the detection does
            not look like this vessel standing on this plane.
    """

    position: np.ndarray
    mouth: np.ndarray | None
    anchor_uv: tuple[float, float]
    raw_hit: np.ndarray
    range_m: float
    metres_per_pixel: float
    inside_room: bool
    on_table: bool | None
    clipped: bool
    residual_px: float | None = None


def table_plane(z: float = TABLE_TOP_Z) -> Plane:
    """The bench top as a plane

    Args:
        z: Height of the bench top in metres.

    Returns:
        The horizontal plane at that height.
    """
    return Plane.horizontal(z)


def default_intrinsics(
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    fovy_deg: float = DEFAULT_FOVY_DEG,
) -> Intrinsics:
    """Intrinsics matching the MuJoCo renders, as a stand-in for a calibration

    Args:
        width: Frame width in pixels.
        height: Frame height in pixels.
        fovy_deg: Vertical field of view, MuJoCo's ``fovy``.

    Returns:
        Ideal pinhole intrinsics, no distortion.
    """
    return Intrinsics.from_fov(width, height, fovy_deg=fovy_deg)


def default_camera(
    intrinsics: Intrinsics | None = None,
    *,
    position: object = CAMERA_POSITION,
    target: object | None = None,
) -> Camera:
    """The wall camera, aimed at the middle of the bench

    The aim is an assumption; see the module docstring. Replace this camera
    with one solved from markers before trusting a millimetre.

    Args:
        intrinsics: Pinhole model, defaulting to :func:`default_intrinsics`.
        position: Camera centre in world metres.
        target: World point to look at, defaulting to the bench centre.

    Returns:
        The camera.
    """
    aim = target if target is not None else (*TABLE_CENTRE, TABLE_TOP_Z)
    return Camera.look_at(intrinsics or default_intrinsics(), position, aim)


def _increasing_v_direction(camera: Camera, uv: object, plane: Plane) -> np.ndarray:
    """In-plane unit vector along which image v increases fastest

    The lines of constant v in the image are straight lines on the plane, and
    the extreme point of a circle in v is where one of them is tangent to it.
    The offset from the circle's centre to that tangency point is the radius
    along the in-plane normal to the iso-v line, which is what this returns:
    the v column of the Jacobian with its component along the u column
    projected out.

    Args:
        camera: The calibrated camera.
        uv: (2,) pixel to linearise at.
        plane: The plane being intersected.

    Returns:
        (3,) unit vector lying in the plane.

    Raises:
        GeometryError: If the Jacobian is degenerate there.
    """
    jacobian = plane_jacobian(camera, uv, plane)
    if not np.isfinite(jacobian).all():
        raise GeometryError(f"pixel {tuple(np.asarray(uv).tolist())} does not "
                            "meet the plane in front of the camera")
    along_u, along_v = jacobian[:, 0], jacobian[:, 1]
    u_norm = float(np.linalg.norm(along_u))
    if u_norm < 1e-12:
        raise GeometryError("the image u axis is degenerate on this plane")
    u_hat = along_u / u_norm
    normal = along_v - (along_v @ u_hat) * u_hat
    normal_norm = float(np.linalg.norm(normal))
    if normal_norm < 1e-12:
        raise GeometryError("the image axes are degenerate on this plane")
    return normal / normal_norm


def silhouette_pixels(
    camera: Camera,
    position: object,
    *,
    radius: float,
    height: float,
    samples: int = 512,
) -> np.ndarray:
    """Project the outline of an upright cylinder standing at a point

    Every extreme of a cylinder's silhouette lies on one of its two rim
    circles --- the sides of the silhouette are straight vertical generators,
    which contribute no extremum of their own --- so projecting the rims is
    enough to bound the shape.

    Args:
        camera: The calibrated camera.
        position: (3,) world position of the base centre.
        radius: Cylinder radius in metres.
        height: Cylinder height in metres.
        samples: Points per rim circle.

    Returns:
        (2 * samples, 2) pixel coordinates.

    Raises:
        GeometryError: If any part of the outline falls behind the camera.
    """
    base = np.asarray(position, dtype=float).reshape(3)
    angles = np.linspace(0.0, 2.0 * math.pi, samples, endpoint=False)
    ring = base + np.stack(
        [radius * np.cos(angles), radius * np.sin(angles), np.zeros(samples)], axis=-1
    )
    outline = np.concatenate([ring, ring + np.array([0.0, 0.0, height])])
    pixels = camera.project(outline)
    if not np.isfinite(pixels).all():
        raise GeometryError(f"a vessel at {base.tolist()} is not fully in front "
                            "of the camera")
    return pixels


def predict_bbox(
    camera: Camera,
    position: object,
    *,
    radius: float,
    height: float,
    samples: int = 512,
) -> BBox:
    """Box a detector would draw around an upright cylinder at a known point

    Args:
        camera: The calibrated camera.
        position: (3,) world position of the base centre.
        radius: Cylinder radius in metres.
        height: Cylinder height in metres.
        samples: Points per rim circle.

    Returns:
        The tight axis-aligned box, in pixels.

    Raises:
        GeometryError: If the vessel is not fully in front of the camera.
    """
    return BBox.around(
        silhouette_pixels(
            camera, position, radius=radius, height=height, samples=samples
        )
    )


def fit_position(
    bbox: BBox,
    camera: Camera,
    *,
    radius: float,
    height: float,
    plane: Plane,
    start: object,
    iterations: int = 12,
    step_tol: float = 1e-7,
    samples: int = 512,
) -> tuple[np.ndarray, float]:
    """Invert :func:`predict_bbox` --- find the point whose box is this one

    The anchor heuristics each throw away three of the box's four numbers and
    inherit whatever bias the one they keep has. Since the forward model is
    cheap and there are only two unknowns, the box can simply be inverted
    instead: Gauss-Newton on the four edge residuals, with a numerical 4x2
    Jacobian, started from the base anchor. Two or three iterations converge,
    and with an exact box the answer is exact --- no anchor bias at all.

    The price is the dimensions. The top edge in particular is where the
    assumed height enters, so a wrong height biases the fit; the base anchor
    never looks at it.

    Args:
        bbox: The observed box.
        camera: The calibrated camera.
        radius: Vessel radius in metres.
        height: Vessel silhouette height in metres.
        plane: The bench plane the base stands on.
        start: (3,) initial guess for the base centre.
        iterations: Maximum Gauss-Newton steps.
        step_tol: Stop once a step moves less than this, in metres.
        samples: Points per rim circle in the forward model.

    Returns:
        The (3,) base centre and the RMS edge residual in pixels.

    Raises:
        GeometryError: If the vessel leaves the camera's view during the fit.
    """
    target = np.array(bbox.as_tuple())
    guess = np.asarray(start, dtype=float).reshape(3).copy()
    delta = 1e-4

    def edges(point: np.ndarray) -> np.ndarray:
        return np.array(
            predict_bbox(
                camera, point, radius=radius, height=height, samples=samples
            ).as_tuple()
        )

    residual = edges(guess) - target
    for _ in range(iterations):
        jacobian = np.empty((4, 2))
        for axis in (0, 1):
            offset = np.zeros(3)
            offset[axis] = delta
            jacobian[:, axis] = (edges(guess + offset) - edges(guess - offset)) / (
                2.0 * delta
            )
        step, *_ = np.linalg.lstsq(jacobian, -residual, rcond=None)
        guess = guess + np.array([step[0], step[1], 0.0])
        residual = edges(guess) - target
        if float(np.linalg.norm(step)) < step_tol:
            break
    guess[2] = plane.point[2]
    return guess, float(np.sqrt((residual ** 2).mean()))


def locate(
    bbox: BBox,
    camera: Camera,
    *,
    plane: Plane | None = None,
    vessel: Vessel | None = None,
    radius: float | None = None,
    height: float | None = None,
    capped: bool = True,
    anchor: str = "auto",
    room_size: tuple[float, float, float] | None = ROOM_SIZE,
    table_size: tuple[float, float] | None = TABLE_SIZE,
    table_centre: tuple[float, float] = TABLE_CENTRE,
) -> Placement:
    """Turn a detection box into a position on the bench

    Args:
        bbox: The detector's box, in pixels.
        camera: The calibrated camera the box was detected in.
        plane: Bench plane, defaulting to :func:`table_plane`.
        vessel: Known vessel, supplying radius and height.
        radius: Vessel radius in metres, overriding the vessel's. Zero
            disables the base anchor's bias correction.
        height: Vessel silhouette height in metres, overriding the vessel's.
        capped: Whether the vessel's cap is on, for the height taken from it.
        anchor: One of :data:`ANCHORS`; see the module docstring. The
            default fits the full forward model when the vessel's dimensions
            are known and falls back to the base anchor when they are not.
        room_size: Room extent for the sanity check, or None to skip it.
        table_size: Bench footprint for the sanity check, or None to skip it.
        table_centre: Bench centre in the floor plane.

    Returns:
        Where the vessel stands, plus the checks and the error scale.

    Raises:
        GeometryError: If the anchor is unknown, the centre anchor is asked
            for without a height, or the anchor pixel's ray never meets the
            plane in front of the camera --- which for a table below the
            camera means the box sits above the horizon, so whatever was
            detected is not standing on the bench.
    """
    if anchor not in ANCHORS:
        raise GeometryError(f"anchor must be one of {ANCHORS}, got {anchor!r}")
    bench = plane if plane is not None else table_plane()
    if radius is None:
        radius = vessel.radius_m if vessel is not None else 0.0
    if height is None and vessel is not None:
        height = vessel.silhouette_height_m(capped=capped)

    if anchor == "auto":
        anchor = "fit" if radius > 0.0 and height is not None else "base"
    if anchor == "centre":
        if height is None:
            raise GeometryError("the centre anchor needs a vessel or a height")
        anchor_uv = bbox.centre
        target = Plane(bench.point + bench.normal * (height / 2.0), bench.normal)
    else:
        anchor_uv = bbox.bottom_centre
        target = bench

    hit = pixel_to_plane(camera, anchor_uv, target)
    if not np.isfinite(hit).all():
        raise GeometryError(
            f"the ray through {anchor_uv} never meets the plane in front of "
            "the camera; the box is above the horizon, so it is not standing "
            "on the bench"
        )

    residual_px = None
    if anchor == "centre":
        position = hit - bench.normal * (height / 2.0)
    else:
        position = hit - radius * _increasing_v_direction(camera, anchor_uv, bench)
        if anchor == "fit":
            if not radius > 0.0 or height is None:
                raise GeometryError("the fit needs both a radius and a height; "
                                    "pass a vessel, or use the base anchor")
            position, residual_px = fit_position(
                bbox, camera, radius=radius, height=height, plane=bench,
                start=position,
            )

    inside_room = True
    if room_size is not None:
        inside_room = bool(
            0.0 <= position[0] <= room_size[0]
            and 0.0 <= position[1] <= room_size[1]
            and 0.0 <= position[2] <= room_size[2]
        )
    on_table = None
    if table_size is not None:
        on_table = bool(
            abs(position[0] - table_centre[0]) <= table_size[0] / 2.0
            and abs(position[1] - table_centre[1]) <= table_size[1] / 2.0
        )

    return Placement(
        position=position,
        mouth=None if height is None else position + bench.normal * height,
        anchor_uv=anchor_uv,
        raw_hit=hit,
        range_m=float(camera.range_to(position)),
        metres_per_pixel=metres_per_pixel(camera, anchor_uv, bench)[0],
        residual_px=residual_px,
        inside_room=inside_room,
        on_table=on_table,
        clipped=bbox.touches_frame(camera.intrinsics),
    )


def error_budget(
    camera: Camera,
    *,
    plane: Plane | None = None,
    extent: float = 1.0,
    steps: int = 3,
    centre: tuple[float, float] = TABLE_CENTRE,
) -> list[tuple[float, float, float]]:
    """Sample how many millimetres of table one pixel of error is worth

    Args:
        camera: The calibrated camera.
        plane: Bench plane, defaulting to :func:`table_plane`.
        extent: Half-width of the square of bench to sample, in metres.
        steps: Samples per axis.
        centre: Centre of the sampled square in the floor plane.

    Returns:
        One (x, y, millimetres per pixel) per sample, worst case at that
        point. Samples that fall outside the frame are dropped.
    """
    bench = plane if plane is not None else table_plane()
    axis = np.linspace(-extent, extent, steps)
    rows: list[tuple[float, float, float]] = []
    for dy in axis:
        for dx in axis:
            point = np.array([centre[0] + dx, centre[1] + dy, bench.point[2]])
            uv = camera.project(point)
            if not np.isfinite(uv).all() or not camera.intrinsics.contains(uv):
                continue
            worst, _ = metres_per_pixel(camera, uv, bench)
            rows.append((float(point[0]), float(point[1]), worst * 1000.0))
    return rows


def _elevation_deg(camera: Camera, point: object) -> float:
    """Angle below horizontal from the camera down to a point, in degrees"""
    delta = np.asarray(point, dtype=float) - camera.position
    horizontal = float(np.hypot(delta[0], delta[1]))
    return math.degrees(math.atan2(-delta[2], horizontal))


def main(argv: list[str] | None = None) -> None:
    """Locate a bounding box on the bench, or print the room's error budget."""
    parser = argparse.ArgumentParser(
        description="Turn a detection box into a 3D position on the bench.",
    )
    parser.add_argument(
        "--bbox", type=float, nargs=4, metavar=("U_MIN", "V_MIN", "U_MAX", "V_MAX"),
        help="Detection box in pixels.",
    )
    parser.add_argument(
        "--vessel", choices=sorted(VESSELS), help="Vessel class, for its dimensions.",
    )
    parser.add_argument(
        "--anchor", choices=ANCHORS, default="base",
        help="Which point of the box to back-project (default: %(default)s).",
    )
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH,
                        help="Frame width (default: %(default)s).")
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT,
                        help="Frame height (default: %(default)s).")
    parser.add_argument("--fovy", type=float, default=DEFAULT_FOVY_DEG,
                        help="Vertical field of view (default: %(default)s).")
    parser.add_argument("--camera", type=float, nargs=3, default=list(CAMERA_POSITION),
                        metavar=("X", "Y", "Z"), help="Camera position in metres.")
    parser.add_argument("--target", type=float, nargs=3, metavar=("X", "Y", "Z"),
                        help="World point the camera looks at (default: bench "
                             "centre).")
    parser.add_argument("--table-z", type=float, default=TABLE_TOP_Z,
                        help="Bench top height (default: %(default)s).")
    parser.add_argument("--budget", action="store_true",
                        help="Print millimetres per pixel across the bench.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args(argv)

    camera = default_camera(
        default_intrinsics(args.width, args.height, args.fovy),
        position=args.camera,
        target=args.target,
    )
    bench = table_plane(args.table_z)

    if args.budget or args.bbox is None:
        centre = np.array([*TABLE_CENTRE, args.table_z])
        print(f"camera   {tuple(camera.position.tolist())}  "
              f"{camera.intrinsics.fovx_deg:.1f} x {camera.intrinsics.fovy_deg:.1f} "
              f"deg, {args.width}x{args.height}")
        print(f"bench    z = {args.table_z} m, centre {TABLE_CENTRE}")
        print(f"sight    {camera.range_to(centre):.2f} m at "
              f"{_elevation_deg(camera, centre):.1f} deg elevation")
        print("mm of bench per pixel of detection error, worst case:")
        for x, y, scale in error_budget(camera, plane=bench):
            print(f"  ({x:5.2f}, {y:5.2f})  {scale:6.1f} mm/px")
        if args.bbox is None:
            return

    placement = locate(
        BBox(*args.bbox), camera, plane=bench,
        vessel=VESSELS[args.vessel] if args.vessel else None,
        anchor=args.anchor,
    )
    if args.json:
        print(json.dumps({
            "position": placement.position.tolist(),
            "mouth": None if placement.mouth is None else placement.mouth.tolist(),
            "range_m": placement.range_m,
            "mm_per_pixel": placement.metres_per_pixel * 1000.0,
            "inside_room": placement.inside_room,
            "on_table": placement.on_table,
            "clipped": placement.clipped,
        }, indent=2))
        return
    x, y, z = placement.position
    print(f"position  x={x:.3f}  y={y:.3f}  z={z:.3f}  m")
    if placement.mouth is not None:
        print(f"mouth     x={placement.mouth[0]:.3f}  y={placement.mouth[1]:.3f}  "
              f"z={placement.mouth[2]:.3f}  m")
    correction = float(np.linalg.norm(placement.position - placement.raw_hit))
    print(f"range     {placement.range_m:.3f} m")
    print(f"scale     {placement.metres_per_pixel * 1000:.1f} mm per pixel of error")
    print(f"radius correction applied: {correction * 1000:.1f} mm")
    if not placement.inside_room:
        print("WARNING: outside the room")
    if placement.on_table is False:
        print("WARNING: off the bench footprint")
    if placement.clipped:
        print("WARNING: box touches the frame border, so its edges are the "
              "frame's, not the object's")


if __name__ == "__main__":
    main()
