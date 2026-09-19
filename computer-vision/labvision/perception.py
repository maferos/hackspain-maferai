"""Fixed camera proposes, wrist camera confirms: the vision system's core, frames in

Two steps, each a pure function of frames, boxes and calibrated cameras, so
the same code serves a render loop (``scripts/propose_confirm.py``), the
console bridge that renders the scene's cameras itself, or real GoPros:

1. :func:`propose` places every detector box of the fixed camera on the bench:
   base anchor of :func:`labvision.scene.locate` on the bench plane, with a
   generic radius because the bottle is not known yet. Boxes a caller's filter
   rejects (the worktop test) are dropped, and proposals closer than
   :data:`MERGE_M` are one bottle.
2. :func:`confirm` takes the wrist camera's frame, taken looking at a
   proposal, and reads every ArUco ring in it near where the proposal
   projects. Each ring names a bottle, and knowing the bottle gives its ring's
   radius and height, so :func:`refine_marker` places it on the bench from
   the ring's most frontal marker and the way that marker faces. The ring
   whose bottle then stands closest to the proposal, and within
   :data:`MAX_SHIFT_M`, names it: a neighbour seen past the proposed bottle
   projects close by in the image, but stands elsewhere on the bench.

Frames: the MuJoCo scene's world frame, metres, whose origin is under the
centre of the minihannover bench; the bench top is at :data:`BENCH_TOP_Z`.
Nothing here reads the simulator's state.
"""

import functools
import math
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from labvision.camera import Camera, GeometryError
from labvision.identify import MarkerReader, identify_frame
from labvision.scene import BBox, locate, table_plane
from labvision.world import PerceivedBottle

BENCH_TOP_Z = 0.90
"""Top of the minihannover worktop in the scene frame."""
PROPOSAL_RADIUS_M = 0.018
"""Radius for the base anchor's correction before the bottle is known.

Measured, not guessed. The correction moves a proposal along the line of
sight, so getting it wrong is a *bias*, the same size and direction for every
bottle, and bias was most of the placement error: at 0.025 the fixed camera
put 25 bottles 8.1 mm out at the median, of which 7.0 mm was a fixed offset
away from the camera. Sweeping the radius against simulator truth on that run:

    radius   bias y    median   p90
      8 mm   -10.2 mm   9.6 mm  16.8 mm
     14 mm    -4.2 mm   5.0 mm  10.9 mm
     18 mm    -0.2 mm   3.9 mm   7.2 mm
     25 mm    +6.8 mm   8.1 mm  12.3 mm

18 mm is the bench of flasks this is used on, whose radii run 11 to 24 mm. A
bench carrying the 1 L bottles as well wants a larger one; pass ``radius`` to
:func:`propose` rather than changing this.

A residual +1.9 mm along x survives every radius, so it is not this correction
--- it is the camera's own pose, and worth about a fifth of what this was."""
MERGE_M = 0.03
"""Proposals closer than this on the bench are taken to be the same bottle."""
ASSOCIATE_PX = 200
"""A marker group farther than this from where the proposal projects in the
wrist frame is taken to be a different bottle."""
MAX_SHIFT_M = 0.05
"""Placed from its own ring, a bottle farther than this from the proposal is a
neighbour seen past it, not the proposed bottle. From the aisle a neighbour
behind or in front can project within :data:`ASSOCIATE_PX`; on the bench it is
10 cm or more away, while a proposal is within 3 cm of its bottle nine times in
ten (``scripts/propose_confirm.py``)."""
KIT = Path(__file__).resolve().parents[2] / "simulation" / "assets" / "labelled_bottles"
"""The labelled bottle assets, whose label meshes give each ring's geometry."""


@dataclass
class Proposal:
    """A bottle the fixed camera found, placed on the bench

    Attributes:
        xy: Base centre on the bench, world metres.
        score: The detector's confidence.
        label: The detector's class name.
        bbox: The detector's box in the fixed camera's frame.
    """

    xy: tuple[float, float]
    score: float
    label: str
    bbox: BBox


@dataclass
class Confirmation:
    """What the wrist camera read at a proposal

    Attributes:
        sample_id: The sample the ring names, or None if none was read near it.
        marker_id: The marker read, or None.
        votes: How many markers of that id were read.
        phase: ``liquid`` or ``powder`` from the sample's record, or None.
        offset_px: Distance from the proposal's projection to the ring read.
        refined_xy: The bottle's axis from the ring, or None if not refined.
    """

    sample_id: str | None = None
    marker_id: int | None = None
    votes: int = 0
    phase: str | None = None
    offset_px: float | None = None
    refined_xy: tuple[float, float] | None = None


def propose(
    boxes: Iterable[tuple[BBox, float, str]],
    camera: Camera,
    *,
    keep: Callable[[BBox], bool] | None = None,
    bench_z: float = BENCH_TOP_Z,
    radius: float = PROPOSAL_RADIUS_M,
    merge_m: float = MERGE_M,
) -> list[Proposal]:
    """Place the fixed camera's boxes on the bench, one proposal per bottle

    Args:
        boxes: ``(bbox, score, label)`` per detection.
        camera: The fixed camera, calibrated.
        keep: Optional test a box has to pass, such as the worktop filter.
        bench_z: Height of the bench plane.
        radius: Radius for the base anchor's correction.
        merge_m: Proposals closer than this merge, the higher score winning.

    Returns:
        Proposals by descending score.
    """
    placed = []
    for bbox, score, label in boxes:
        if keep is not None and not keep(bbox):
            continue
        try:
            where = locate(
                bbox,
                camera,
                plane=table_plane(bench_z),
                radius=radius,
                anchor="base",
                room_size=None,
                table_size=None,
            )
        except GeometryError:
            continue
        xy = (float(where.position[0]), float(where.position[1]))
        placed.append(Proposal(xy, float(score), label, bbox))
    placed.sort(key=lambda p: -p.score)
    merged: list[Proposal] = []
    for proposal in placed:
        if all(math.dist(proposal.xy, other.xy) >= merge_m for other in merged):
            merged.append(proposal)
    return merged


@functools.lru_cache(maxsize=32)
def ring_geometry(vessel: str, kit: Path = KIT) -> tuple[float, float]:
    """Radius of a vessel's label ring and its centre's height above the base

    Read from the label mesh the scene's bottles carry, so a regenerated kit
    needs no change here.

    Returns:
        ``(radius, height)`` in metres.
    """
    rows = [
        line.split()[1:4]
        for line in (kit / "meshes" / f"{vessel}_label.obj").read_text().splitlines()
        if line.startswith("v ")
    ]
    vertices = np.array(rows, dtype=float)
    radius = float(np.median(np.hypot(vertices[:, 0], vertices[:, 1])))
    return radius, float((vertices[:, 2].min() + vertices[:, 2].max()) / 2)


@functools.lru_cache(maxsize=32)
def vessel_height(vessel: str, kit: Path = KIT) -> float:
    """Height of a vessel from its base to the top of its cap, in metres

    Read from the glass and cap meshes, like :func:`ring_geometry`. It is what
    a gripper needs once the ring has named the bottle: how far up the wall to
    close, without asking the simulator how tall the thing is.
    """
    top = 0.0
    for part in ("glass", "cap"):
        mesh = kit / "meshes" / f"{vessel}_{part}.obj"
        for line in mesh.read_text().splitlines():
            if line.startswith("v "):
                top = max(top, float(line.split()[3]))
    return top


def refine(
    camera: Camera,
    uv: tuple[float, float],
    radius: float,
    ring_height: float,
    *,
    bench_z: float = BENCH_TOP_Z,
) -> tuple[float, float] | None:
    """The axis of a bottle standing on the bench from where its ring shows

    The ring's visible centre lies on the bottle's surface at the ring's height,
    facing the camera: the ray through it meets that height on the surface, and
    the axis is one radius further along the view, horizontally.

    A camera level with the ring cannot place it this way, since its ray runs
    along the ring's height instead of crossing it; the wrist camera looks down
    at the bottle for that reason.

    Returns:
        The axis (x, y), or None if the ray does not cross that height ahead.
    """
    ray = camera.pixel_ray(np.array(uv, dtype=float))
    height = bench_z + ring_height
    if abs(ray[2]) < 1e-6:
        return None
    t = (height - camera.position[2]) / ray[2]
    if t <= 0:
        return None
    hit = camera.position + t * ray
    along = np.array([ray[0], ray[1]])
    norm = float(np.linalg.norm(along))
    if norm < 1e-9:
        return None
    axis = hit[:2] + radius * along / norm
    return float(axis[0]), float(axis[1])


def _on_height(camera: Camera, uv: object, height: float) -> np.ndarray | None:
    """Where the ray through a pixel meets the horizontal plane at ``height``"""
    ray = camera.pixel_ray(np.asarray(uv, dtype=float))
    if abs(ray[2]) < 1e-6:
        return None
    t = (height - camera.position[2]) / ray[2]
    return camera.position + t * ray if t > 0 else None


def _quad_centre(corners: np.ndarray) -> np.ndarray:
    """Where a quad's diagonals cross: the image of a square's centre

    The mean of the four corners is not, under perspective; on a marker 0.3 m
    away that difference is about a millimetre on the bench.
    """
    p0, p1, p2, p3 = corners
    d1, d2 = p2 - p0, p3 - p1
    denominator = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(denominator) < 1e-9:
        return corners.mean(axis=0)
    s = ((p1[0] - p0[0]) * d2[1] - (p1[1] - p0[1]) * d2[0]) / denominator
    return p0 + s * d1


def refine_marker(
    camera: Camera,
    corners: np.ndarray,
    radius: float,
    ring_height: float,
    *,
    bench_z: float = BENCH_TOP_Z,
) -> tuple[float, float] | None:
    """The axis of a bottle standing on the bench from one marker of its ring

    The ring carries a marker every 45 degrees, so the one seen most squarely
    can face up to 22.5 degrees away from the camera, and pushing one radius
    along the view, as :func:`refine` does, then lands up to
    ``radius * sin(22.5 deg)`` beside the axis: 17 mm on a 1 L bottle. The
    marker says which way it faces instead. It is printed round the ring, so
    its four corners lie on the surface and span a flat quad whose centre sits
    on a chord, short of the surface. The midpoints of the two edges that run
    up the bottle are that chord's ends, at the ring's height; the axis lies
    along the chord's normal, ``sqrt(r^2 - (chord / 2)^2)`` behind the centre
    (a full radius would put it 0.5 mm too far on a 10 ml flask and 2.5 mm on
    a 2 L bottle). Which edges run up the bottle is read from the direction
    the world's vertical takes in the image at the marker, not from the
    image's own vertical, so a rolled or steeply pitched camera still pairs
    them right.

    Args:
        camera: The camera the marker was seen by.
        corners: (4, 2) the marker's corners in that camera's pixels, in
            order round the quad, whichever way the marker is turned.
        radius: The ring's radius.
        ring_height: Height of the ring's centre above the bottle's base.
        bench_z: Height of the bench plane.

    Returns:
        The axis (x, y), or None if the geometry cannot be read, such as a
        camera level with the ring or looking straight down on it.
    """
    corners = np.asarray(corners, dtype=float)
    height = bench_z + ring_height
    centre = _on_height(camera, _quad_centre(corners), height)
    if centre is None:
        return None
    up = camera.project(np.array([centre, centre + (0.0, 0.0, 0.01)]))
    vertical = up[1] - up[0]
    if not np.all(np.isfinite(vertical)) or np.linalg.norm(vertical) < 1e-3:
        return None
    vertical /= np.linalg.norm(vertical)
    edges = [(corners[i], corners[(i + 1) % 4]) for i in range(4)]

    def upright(edge: tuple[np.ndarray, np.ndarray]) -> float:
        direction = edge[1] - edge[0]
        return abs(float(direction @ vertical)) / (np.linalg.norm(direction) + 1e-9)

    first, second = max(
        ((0, 2), (1, 3)),
        key=lambda pair: upright(edges[pair[0]]) + upright(edges[pair[1]]),
    )
    ends = [
        _on_height(camera, (edges[i][0] + edges[i][1]) / 2, height)
        for i in (first, second)
    ]
    if ends[0] is None or ends[1] is None:
        return None
    chord = ends[1][:2] - ends[0][:2]
    length = float(np.linalg.norm(chord))
    if length < 1e-6:
        return None
    normal = np.array([-chord[1], chord[0]]) / length
    if np.dot(normal, camera.position[:2] - centre[:2]) < 0:
        normal = -normal  # the marker faces the camera that saw it
    behind = math.sqrt(radius**2 - min(length / 2, radius) ** 2)
    axis = centre[:2] - behind * normal
    return float(axis[0]), float(axis[1])


def confirm(
    frame: np.ndarray,
    camera: Camera,
    target: object,
    rows: dict[int, dict],
    *,
    reader: MarkerReader | None = None,
    associate_px: float = ASSOCIATE_PX,
    max_shift_m: float = MAX_SHIFT_M,
    bench_z: float = BENCH_TOP_Z,
    kit: Path = KIT,
) -> Confirmation:
    """Name and place the bottle at a proposal from the wrist camera's frame

    Args:
        frame: The wrist camera's BGR frame, taken looking at ``target``.
        camera: The wrist camera, calibrated, at the pose the frame was taken.
        target: The world point looked at, normally the proposal lifted a
            little above the bench.
        rows: Lookup-table rows by marker id.
        reader: A reader to reuse; a new one is built if None.
        associate_px: See :data:`ASSOCIATE_PX`.
        max_shift_m: See :data:`MAX_SHIFT_M`.
        bench_z: Height of the bench plane.
        kit: Where the label meshes are, for the ring's geometry.

    Returns:
        What was read; an empty :class:`Confirmation` if no ring was near.
    """
    target = np.asarray(target, dtype=float)
    expected = camera.project(target)
    if not np.all(np.isfinite(expected)):
        return Confirmation()
    best = None
    for identity in identify_frame(frame, rows, reader=reader):
        row = identity.row
        vessel = row.get("vessel_class") if row else None
        if not vessel or not (kit / "meshes" / f"{vessel}_label.obj").exists():
            continue  # not a catalogue bottle, or no geometry to check it against
        facing = identity.frontal
        uv = facing.centre if facing else identity.bbox.centre
        offset = math.dist(uv, expected)
        if offset >= associate_px:
            continue
        radius, ring_height = ring_geometry(vessel, kit)
        refined = None
        if facing is not None:
            refined = refine_marker(
                camera, facing.corners, radius, ring_height, bench_z=bench_z
            )
        if refined is None:
            refined = refine(camera, uv, radius, ring_height, bench_z=bench_z)
        if refined is None:
            continue
        # Placed as the bottle its ring names, it must stand where the proposal
        # is; a ring further off belongs to a neighbour seen past it. Of those
        # that fit, the one whose bottle stands closest to the proposal wins.
        shift = math.dist(refined, target[:2])
        if shift <= max_shift_m and (best is None or shift < best[0]):
            best = (shift, offset, identity, refined)
    if best is None:
        return Confirmation()
    _, offset, identity, refined = best
    return Confirmation(
        sample_id=identity.sample_id,
        marker_id=identity.marker_id,
        votes=identity.votes,
        phase=identity.row.get("phase"),
        offset_px=round(offset, 1),
        refined_xy=refined,
    )


def perceived(
    proposal: Proposal, confirmation: Confirmation, *, bench_z: float = BENCH_TOP_Z
) -> PerceivedBottle:
    """The world-state record for a proposal and what the wrist read there"""
    xy = confirmation.refined_xy or proposal.xy
    return PerceivedBottle(
        position=(xy[0], xy[1], bench_z),
        confidence=proposal.score,
        sample_id=confirmation.sample_id,
        marker_id=confirmation.marker_id,
        phase=confirmation.phase,
        refined=confirmation.refined_xy is not None,
    )
