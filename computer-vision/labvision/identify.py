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
    """

    bbox: BBox
    marker_id: int | None
    votes: int
    markers: int
    row: dict | None = None
    label: str | None = None
    score: float | None = None

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


class MarkerReader:
    """ArUco reading tuned the way ``scripts/wrist_scan.py`` reads the rings

    Args:
        dictionary: A ``cv2.aruco`` predefined dictionary id.
    """

    def __init__(self, dictionary: int = DICTIONARY) -> None:
        """Build the detector with the parameters the ring was measured with"""
        parameters = cv2.aruco.DetectorParameters()
        parameters.minMarkerPerimeterRate = 0.02
        parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
        self._detector = cv2.aruco.ArucoDetector(
            cv2.aruco.getPredefinedDictionary(dictionary), parameters
        )

    def read(self, image: np.ndarray) -> list[Marker]:
        """Every marker in an image, in that image's pixels"""
        corners, ids, _ = self._detector.detectMarkers(image)
        if ids is None:
            return []
        return [
            Marker(int(i), c.reshape(4, 2).astype(np.float64))
            for i, c in zip(ids.flatten(), corners, strict=True)
        ]

    def read_region(
        self,
        frame: np.ndarray,
        bbox: BBox,
        *,
        margin: float = MARGIN,
        scales: tuple[float, ...] = SCALES,
    ) -> list[Marker]:
        """Every marker in a box and its margin, in frame pixels

        The crop is read at each of ``scales`` in turn until any marker reads.
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
        for scale in scales:
            image = (
                crop
                if scale == 1.0
                else cv2.resize(
                    crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC
                )
            )
            found = self.read(image)
            if found:
                offset = np.array([u0, v0], np.float64)
                return [Marker(m.marker_id, m.corners / scale + offset) for m in found]
        return []


def vote(markers: Iterable[Marker], bbox: BBox) -> tuple[int | None, int, int]:
    """The id the markers inside a box agree on

    Returns:
        ``(marker_id or None, votes for it, markers inside the box)``. None when
        no marker lies inside or two ids tie for the most markers.
    """
    inside = [
        m
        for m in markers
        if bbox.u_min <= m.centre[0] <= bbox.u_max
        and bbox.v_min <= m.centre[1] <= bbox.v_max
    ]
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
        found.append(
            Identity(
                bbox=bbox,
                marker_id=marker_id,
                votes=votes,
                markers=total,
                row=rows.get(marker_id) if marker_id is not None else None,
                label=getattr(box, "label", None),
                score=getattr(box, "score", None),
            )
        )
    return found


def identify_frame(
    frame: np.ndarray, rows: dict[int, dict], *, reader: MarkerReader | None = None
) -> list[Identity]:
    """Read the whole frame without a detector: one identity per marker id seen

    Each identity's box is the bounds of that id's markers, which is the part
    of the ring facing the camera, not the bottle.
    """
    reader = reader or MarkerReader()
    by_id: dict[int, list[Marker]] = {}
    for marker in reader.read(frame):
        by_id.setdefault(marker.marker_id, []).append(marker)
    found = []
    for marker_id, markers in sorted(by_id.items()):
        points = np.concatenate([m.corners for m in markers])
        (u0, v0), (u1, v1) = points.min(axis=0), points.max(axis=0)
        found.append(
            Identity(
                bbox=BBox(float(u0), float(v0), float(u1), float(v1)),
                marker_id=marker_id,
                votes=len(markers),
                markers=len(markers),
                row=rows.get(marker_id),
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
