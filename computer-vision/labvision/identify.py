"""Name the sample in a detector's box by the ArUco ring on its label

Every sample bottle carries one ``DICT_4X4_250`` marker, its ``marker_id``,
printed eight times round the straight wall (:mod:`labvision.bottles`). The
detector says *there is a bottle in these pixels*; this module says *which
one*: it reads the markers inside each box and lets them vote.

Why read inside a box rather than the whole frame:

- **Association.** A frame from the wrist camera often holds two or three
  bottles. Reading the whole frame gives a set of ids with no bottle attached;
  reading each box gives each detection its own id, which is what the robot
  needs to pick up the right one.
- **A second try.** When nothing reads in a crop at its own size, it is read
  again enlarged. On clean synthetic markers this rescues nothing (they read
  down to about 12 px a side either way), so whether it buys reach on rendered
  frames is measured by ``scripts/wrist_identify_bench.py``, not assumed.

A marker counts for a box only if its centre lies inside the box itself, not
the margin read around it, so the neighbour's ring does not vote. The id with
the most markers wins; a tie names nobody, because a guess would be a wrong
bottle in the gripper.

    python -m labvision.identify frame.png                  # whole frame
    python -m labvision.identify frame.png --backend world  # boxes, then rings
    python -m labvision.identify frames/ --backend world --json
"""

import argparse
import json
import math
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from labvision import registry
from labvision.scene import BBox

DICTIONARY = cv2.aruco.DICT_4X4_250
"""The marker family on the bottles, as :mod:`labvision.bottles` prints it."""
MARGIN = 0.15
"""Share of the box's width and height added on each side before reading."""
SCALES = (1.0, 2.0, 3.0)
"""Enlargements tried in turn on a crop until one reads any marker. The crop as
it is comes first: enlarging a blurred marker can lose one that reads unscaled,
so a larger scale is only a second try."""
DEFAULT_TABLE = Path(__file__).resolve().parents[1] / "barcodes" / "lookup_table.json"


@dataclass(frozen=True)
class Marker:
    """One ArUco marker read in a frame

    Attributes:
        marker_id: The marker's id in :data:`DICTIONARY`.
        corners: (4, 2) corner pixels in the frame, clockwise from top-left.
    """

    marker_id: int
    corners: np.ndarray

    @property
    def centre(self) -> tuple[float, float]:
        """Mean of the four corners, as (u, v)"""
        u, v = self.corners.mean(axis=0)
        return float(u), float(v)

    @property
    def area(self) -> float:
        """Area of the marker's quad in pixels: largest for the one facing the camera"""
        u, v = self.corners[:, 0], self.corners[:, 1]
        return float(abs(np.dot(u, np.roll(v, -1)) - np.dot(v, np.roll(u, -1))) / 2)

    @property
    def side(self) -> float:
        """Mean edge length of the quad in pixels"""
        edges = np.roll(self.corners, -1, axis=0) - self.corners
        return float(np.linalg.norm(edges, axis=1).mean())


@dataclass
class Identity:
    """What a box, or a group of markers read without one, was found to be

    Attributes:
        bbox: The detector's box, or the markers' bounds when read without one.
        marker_id: The winning marker id, or None if nothing or a tie was read.
        votes: Markers inside the box carrying the winning id.
        markers: Markers inside the box, whatever their id.
        row: The lookup-table row of the winning id, or None if it has none.
        label: The detector's class name, if a detector gave the box.
        score: The detector's confidence, if a detector gave the box.
        read: The winning id's markers themselves, in frame pixels.
    """

    bbox: BBox
    marker_id: int | None
    votes: int
    markers: int
    row: dict | None = None
    label: str | None = None
    score: float | None = None
    read: tuple[Marker, ...] = ()

    @property
    def frontal(self) -> Marker | None:
        """The winning marker seen most squarely: the one facing the camera"""
        return max(self.read, key=lambda m: m.area, default=None)

    @property
    def sample_id(self) -> str | None:
        """The sample the winning marker names, or None"""
        return str(self.row["sample_id"]) if self.row else None

    def to_json(self) -> dict[str, object]:
        """Return a JSON-serialisable record of this identity"""
        return {
            "xyxy": [round(v, 1) for v in self.bbox.as_tuple()],
            "marker_id": self.marker_id,
            "sample_id": self.sample_id,
            "votes": self.votes,
            "markers": self.markers,
            "label": self.label,
            "score": None if self.score is None else round(self.score, 3),
        }


def rows_by_marker(table: dict[str, dict]) -> dict[int, dict]:
    """Index the rows of a :func:`labvision.registry.load_table` table by marker"""
    return {int(row["marker_id"]): row for row in table.values() if "marker_id" in row}


def _squareness(marker: Marker) -> float:
    """A marker's shortest side over its longest, 1 for a square seen head-on"""
    corners = np.asarray(marker.corners, dtype=float)
    sides = np.linalg.norm(np.roll(corners, -1, axis=0) - corners, axis=1)
    return float(sides.min() / sides.max()) if sides.max() > 0 else 0.0


class MarkerReader:
    """ArUco reading tuned the way ``scripts/wrist_scan.py`` reads the rings

    A marker seen nearly edge-on is dropped: squashed to a few pixels, its
    4 x 4 cells merge and it can decode, bit for bit, as another id. In 100
    wrist frames from 0.25 to 1 m this happened twice, both from 50 degrees
    or more above the ring, and requiring the shortest side to be at least
    half the longest removed both at the cost of 3 of 220 right reads, all
    from as high up. A marker the wrist faces from the aisle is close to
    square, and one at 45 degrees round the ring still keeps about 0.7.

    Args:
        dictionary: A ``cv2.aruco`` predefined dictionary id.
        min_squareness: Shortest side over longest side a marker needs.
    """

    def __init__(
        self, dictionary: int = DICTIONARY, *, min_squareness: float = 0.5
    ) -> None:
        """Build the detector with the parameters the ring was measured with"""
        parameters = cv2.aruco.DetectorParameters()
        parameters.minMarkerPerimeterRate = 0.02
        parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
        self._detector = cv2.aruco.ArucoDetector(
            cv2.aruco.getPredefinedDictionary(dictionary), parameters
        )
        self.min_squareness = min_squareness

    def read(self, image: np.ndarray) -> list[Marker]:
        """Every marker in an image, in that image's pixels"""
        corners, ids, _ = self._detector.detectMarkers(image)
        if ids is None:
            return []
        markers = [
            Marker(int(i), c.reshape(4, 2).astype(np.float64))
            for i, c in zip(ids.flatten(), corners, strict=True)
        ]
        return [m for m in markers if _squareness(m) >= self.min_squareness]

    def read_region(
        self,
        frame: np.ndarray,
        bbox: BBox,
        *,
        margin: float = MARGIN,
        scales: tuple[float, ...] = SCALES,
    ) -> list[Marker]:
        """Every marker in a box and its margin, in frame pixels

        The crop is read at each of ``scales`` in turn until a marker whose
        centre lies inside the box itself reads; a neighbour's marker in the
        margin does not stop the next enlargement from being tried. If none is
        found inside at any scale, whatever the last read found is returned.
        """
        height, width = frame.shape[:2]
        dx, dy = margin * bbox.width, margin * bbox.height
        u0 = int(max(0.0, np.floor(bbox.u_min - dx)))
        v0 = int(max(0.0, np.floor(bbox.v_min - dy)))
        u1 = int(min(float(width), np.ceil(bbox.u_max + dx)))
        v1 = int(min(float(height), np.ceil(bbox.v_max + dy)))
        if u1 <= u0 or v1 <= v0:
            return []
        crop = frame[v0:v1, u0:u1]
        offset = np.array([u0, v0], np.float64)
        last: list[Marker] = []
        for scale in scales:
            image = (
                crop
                if scale == 1.0
                else cv2.resize(
                    crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC
                )
            )
            # A pixel centre q in the enlarged crop is (q + 0.5) / scale - 0.5 here.
            found = [
                Marker(m.marker_id, (m.corners + 0.5) / scale - 0.5 + offset)
                for m in self.read(image)
            ]
            if any(_inside(m, bbox) for m in found):
                return found
            last = found or last
        return last


def _inside(marker: Marker, bbox: BBox) -> bool:
    """Whether a marker's centre lies inside a box, margin excluded"""
    u, v = marker.centre
    return bbox.u_min <= u <= bbox.u_max and bbox.v_min <= v <= bbox.v_max


def vote(markers: Iterable[Marker], bbox: BBox) -> tuple[int | None, int, int]:
    """The id the markers inside a box agree on

    Returns:
        ``(marker_id or None, votes for it, markers inside the box)``. None when
        no marker lies inside or two ids tie for the most markers.
    """
    inside = [m for m in markers if _inside(m, bbox)]
    if not inside:
        return None, 0, 0
    ranked = Counter(m.marker_id for m in inside).most_common()
    top, votes = ranked[0]
    if len(ranked) > 1 and ranked[1][1] == votes:
        return None, votes, len(inside)
    return top, votes, len(inside)


def identify(
    frame: np.ndarray,
    boxes: Iterable,
    rows: dict[int, dict],
    *,
    reader: MarkerReader | None = None,
    margin: float = MARGIN,
    scales: tuple[float, ...] = SCALES,
) -> list[Identity]:
    """Name the sample in every detector box by the markers inside it

    Args:
        frame: (H, W, 3) BGR frame, as OpenCV reads it.
        boxes: :class:`labvision.detector.Box` objects, or bare
            :class:`labvision.scene.BBox` ones.
        rows: Lookup-table rows by marker id, from :func:`rows_by_marker`.
        reader: A reader to reuse; a new one is built if None.
        margin: See :data:`MARGIN`.
        scales: See :data:`SCALES`.

    Returns:
        One :class:`Identity` per box, in the order given.
    """
    reader = reader or MarkerReader()
    found = []
    for box in boxes:
        bbox = getattr(box, "bbox", box)
        markers = reader.read_region(frame, bbox, margin=margin, scales=scales)
        marker_id, votes, total = vote(markers, bbox)
        winners = tuple(
            m for m in markers if m.marker_id == marker_id and _inside(m, bbox)
        )
        found.append(
            Identity(
                bbox=bbox,
                marker_id=marker_id,
                votes=votes,
                markers=total,
                row=rows.get(marker_id) if marker_id is not None else None,
                label=getattr(box, "label", None),
                score=getattr(box, "score", None),
                read=winners,
            )
        )
    return found


def cluster(markers: list[Marker], reach: float = 3.0) -> list[list[Marker]]:
    """Split one id's markers into the bottles they stand on

    A ring shows its markers side by side, about one marker apart; two bottles
    with the same id stand further apart than that. Markers join a group when
    their centres are within ``reach`` times their mean side of a member.
    """
    groups: list[list[Marker]] = []
    for marker in markers:
        near = [
            g
            for g in groups
            if any(
                math.dist(marker.centre, m.centre) <= reach * (marker.side + m.side) / 2
                for m in g
            )
        ]
        merged = [marker]
        for g in near:
            merged += g
            groups.remove(g)
        groups.append(merged)
    return groups


def identify_frame(
    frame: np.ndarray, rows: dict[int, dict], *, reader: MarkerReader | None = None
) -> list[Identity]:
    """Read the whole frame without a detector: one identity per ring seen

    Markers are grouped by id and then by :func:`cluster`, so two bottles
    carrying the same id are two identities. Each identity's box is the bounds
    of its markers, which is the part of the ring facing the camera, not the
    bottle.
    """
    reader = reader or MarkerReader()
    by_id: dict[int, list[Marker]] = {}
    for marker in reader.read(frame):
        by_id.setdefault(marker.marker_id, []).append(marker)
    found = []
    for marker_id, markers in sorted(by_id.items()):
        for group in cluster(markers):
            points = np.concatenate([m.corners for m in group])
            (u0, v0), (u1, v1) = points.min(axis=0), points.max(axis=0)
            found.append(
                Identity(
                    bbox=BBox(float(u0), float(v0), float(u1), float(v1)),
                    marker_id=marker_id,
                    votes=len(group),
                    markers=len(group),
                    row=rows.get(marker_id),
                    read=tuple(group),
                )
            )
    return found


def main(argv: list[str] | None = None) -> None:
    """Print what is in each frame, with or without a detector"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("paths", nargs="+", type=Path, help="images or folders")
    parser.add_argument(
        "--backend", default=None, help="detector backend; omit to read the whole frame"
    )
    parser.add_argument("--table", type=Path, default=DEFAULT_TABLE)
    parser.add_argument("--json", action="store_true", help="one JSON line per frame")
    args = parser.parse_args(argv)

    rows = rows_by_marker(registry.load_table(args.table))
    reader = MarkerReader()
    detector = None
    if args.backend:
        from labvision.detector import Detector

        detector = Detector(args.backend)
    files = []
    for path in args.paths:
        if path.is_dir():
            # render_perfumery.py writes a category map beside every frame
            frames = path.glob("*.png")
            files += sorted(p for p in frames if not p.stem.endswith("_cat"))
        else:
            files.append(path)
    for path in files:
        frame = cv2.imread(str(path))
        if frame is None:
            print(f"{path}: not an image")
            continue
        if detector is None:
            found = identify_frame(frame, rows, reader=reader)
        else:
            found = identify(frame, detector.detect(frame), rows, reader=reader)
        if args.json:
            print(
                json.dumps({"file": str(path), "found": [f.to_json() for f in found]})
            )
            continue
        names = [
            f"{f.sample_id or '?'} (marker {f.marker_id}, {f.votes}/{f.markers})"
            for f in found
        ]
        print(f"{path.name}: {', '.join(names) if names else 'nothing read'}")


if __name__ == "__main__":
    main()
