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
   proposal, reads every ArUco ring in it and keeps the marker group nearest
   to where the proposal projects. That names the bottle; knowing it gives its
   ring's radius and height, and :func:`refine` turns the ring's image into the
   bottle's axis on the bench. A ring whose bottle would then stand more than
   :data:`MAX_SHIFT_M` from the proposal belongs to a neighbour and is passed
   over for the next nearest.

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
PROPOSAL_RADIUS_M = 0.025
"""Radius for the base anchor's correction before the bottle is known: between
the smallest flask (11 mm) and the 1 L bottle (44 mm)."""
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
    candidates = []
    for identity in identify_frame(frame, rows, reader=reader):
        centre = (
            (identity.bbox.u_min + identity.bbox.u_max) / 2,
            (identity.bbox.v_min + identity.bbox.v_max) / 2,
        )
        distance = math.dist(centre, expected)
        if distance < associate_px:
            candidates.append((distance, centre, identity))
    for distance, centre, identity in sorted(candidates, key=lambda c: c[0]):
        row = identity.row or {}
        refined = None
        vessel = row.get("vessel_class")
        if vessel and (kit / "meshes" / f"{vessel}_label.obj").exists():
            radius, ring_height = ring_geometry(vessel, kit)
            refined = refine(camera, centre, radius, ring_height, bench_z=bench_z)
            # Placed as the bottle its ring names, it must stand where the
            # proposal is; if not, the ring belongs to a neighbour seen past it.
            if refined is None or math.dist(refined, target[:2]) > max_shift_m:
                continue
        return Confirmation(
            sample_id=identity.sample_id,
            marker_id=identity.marker_id,
            votes=identity.votes,
            phase=row.get("phase"),
            offset_px=round(distance, 1),
            refined_xy=refined,
        )
    return Confirmation()


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
