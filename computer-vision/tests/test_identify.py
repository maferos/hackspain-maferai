"""Tests for naming a detector's box by the ArUco markers inside it"""

import cv2
import numpy as np
import pytest

from labvision.identify import (
    DICTIONARY,
    Identity,
    Marker,
    MarkerReader,
    identify,
    identify_frame,
    rows_by_marker,
    vote,
)
from labvision.scene import BBox

MARKER_PX = 60
"""Side of a drawn marker, quiet zone excluded."""


def _canvas(markers: list[tuple[int, int, int]], size=(480, 640)) -> np.ndarray:
    """A grey BGR frame with a marker of each ``(id, u, v)``, top-left at (u, v)"""
    frame = np.full((*size, 3), 200, np.uint8)
    dictionary = cv2.aruco.getPredefinedDictionary(DICTIONARY)
    quiet = MARKER_PX // 6
    for marker_id, u, v in markers:
        image = cv2.aruco.generateImageMarker(dictionary, marker_id, MARKER_PX)
        image = cv2.copyMakeBorder(
            image, quiet, quiet, quiet, quiet, cv2.BORDER_CONSTANT, value=255
        )
        side = image.shape[0]
        frame[v : v + side, u : u + side] = image[..., None]
    return frame


def _marker(marker_id: int, u: float, v: float) -> Marker:
    corners = np.array([[u, v], [u + 10, v], [u + 10, v + 10], [u, v + 10]], float)
    return Marker(marker_id, corners)


ROWS = {5: {"sample_id": "SMP-0006", "marker_id": 5}, 9: {"sample_id": "PWD-0010"}}


def test_reader_finds_every_marker_with_its_corners():
    found = MarkerReader().read(_canvas([(3, 40, 40), (7, 300, 200)]))
    by_id = {m.marker_id: m for m in found}
    assert set(by_id) == {3, 7}
    quiet = MARKER_PX // 6
    u, v = by_id[7].centre
    assert u == pytest.approx(300 + quiet + MARKER_PX / 2, abs=1.5)
    assert v == pytest.approx(200 + quiet + MARKER_PX / 2, abs=1.5)


def test_region_read_maps_corners_back_to_the_frame_at_any_scale():
    frame = _canvas([(7, 300, 200)])
    box = BBox(290, 190, 390, 290)
    direct = MarkerReader().read(frame)[0]
    for scales in ((1.0,), (3.0,)):
        found = MarkerReader().read_region(frame, box, scales=scales)
        assert [m.marker_id for m in found] == [7]
        assert found[0].corners == pytest.approx(direct.corners, abs=0.35)


def test_region_read_sees_only_the_box_and_its_margin():
    frame = _canvas([(3, 40, 40), (7, 300, 200)])
    found = MarkerReader().read_region(frame, BBox(290, 190, 390, 290))
    assert [m.marker_id for m in found] == [7]


def test_the_majority_wins():
    box = BBox(0, 0, 100, 100)
    markers = [_marker(5, 10, 10), _marker(5, 40, 10), _marker(9, 70, 70)]
    assert vote(markers, box) == (5, 2, 3)


def test_a_tie_names_nobody():
    box = BBox(0, 0, 100, 100)
    assert vote([_marker(5, 10, 10), _marker(9, 60, 60)], box) == (None, 1, 2)


def test_a_marker_in_the_margin_does_not_vote():
    box = BBox(0, 0, 100, 100)
    outside = _marker(9, 101, 40)  # centre at u = 106, in a 15 % margin
    assert vote([_marker(5, 10, 10), outside, outside], box) == (5, 1, 1)
    assert vote([outside], box) == (None, 0, 0)


def test_identify_names_each_box_and_keeps_the_detector_fields():
    class Box:
        def __init__(self, bbox, label, score):
            self.bbox, self.label, self.score = bbox, label, score

    frame = _canvas([(5, 40, 40), (9, 300, 200), (240, 480, 40)])
    boxes = [
        Box(BBox(30, 30, 130, 130), "amber", 0.9),
        BBox(290, 190, 390, 290),
        BBox(470, 30, 570, 130),
        BBox(150, 350, 250, 450),
    ]
    found = identify(frame, boxes, ROWS)
    assert [f.sample_id for f in found] == ["SMP-0006", "PWD-0010", None, None]
    assert [f.marker_id for f in found] == [5, 9, 240, None]
    assert (found[0].label, found[0].score) == ("amber", 0.9)
    assert found[1].label is None
    assert found[3].markers == 0


def test_whole_frame_reading_gives_one_identity_per_id():
    frame = _canvas([(5, 40, 40), (5, 200, 40), (9, 300, 200)])
    found = identify_frame(frame, ROWS)
    assert [(f.marker_id, f.votes, f.sample_id) for f in found] == [
        (5, 2, "SMP-0006"),
        (9, 1, "PWD-0010"),
    ]
    assert found[0].bbox.u_min < 60 and found[0].bbox.u_max > 250


def test_rows_by_marker_indexes_the_lookup_table():
    table = {
        "2000000000001": {"sample_id": "SMP-0001", "marker_id": 0},
        "2000000000002": {"sample_id": "PWD-0001", "marker_id": 100},
        "2000000000003": {"sample_id": "OLD-0001"},
    }
    rows = rows_by_marker(table)
    assert {k: v["sample_id"] for k, v in rows.items()} == {
        0: "SMP-0001",
        100: "PWD-0001",
    }


def test_identity_serialises():
    record = Identity(BBox(1.24, 2, 3, 4), 5, 2, 3, ROWS[5], "amber", 0.91234).to_json()
    assert record == {
        "xyxy": [1.2, 2, 3, 4],
        "marker_id": 5,
        "sample_id": "SMP-0006",
        "votes": 2,
        "markers": 3,
        "label": "amber",
        "score": 0.912,
    }


def test_twin_bottles_with_one_id_are_two_identities():
    frame = _canvas([(5, 40, 40), (5, 400, 300)])
    found = identify_frame(frame, ROWS)
    assert [(f.marker_id, f.votes) for f in found] == [(5, 1), (5, 1)]


def test_a_ring_s_neighbouring_markers_are_one_identity():
    frame = _canvas([(5, 40, 40), (5, 120, 40)])
    found = identify_frame(frame, ROWS)
    assert [(f.marker_id, f.votes) for f in found] == [(5, 2)]
    assert len(found[0].read) == 2


def test_a_margin_marker_does_not_stop_the_enlargement():
    class Fake(MarkerReader):
        """Reads a neighbour in the margin at 1x and the boxed marker only at 2x"""

        def read(self, image):
            if image.shape[0] < 150:
                return [_marker(9, 105, 40)]  # centre (110, 45): in the margin
            return [_marker(5, 100, 100)]  # centre (105, 105) at 2x: (52, 52)

    found = Fake().read_region(np.zeros((200, 200, 3), np.uint8), BBox(0, 0, 100, 100))
    assert [m.marker_id for m in found] == [5]
    assert found[0].centre == pytest.approx((52.25, 52.25))


def test_the_frontal_marker_is_the_one_seen_largest():
    small, large = _marker(5, 0, 0), Marker(5, 2.0 * _marker(5, 0, 0).corners)
    identity = Identity(BBox(0, 0, 30, 30), 5, 2, 2, read=(small, large))
    assert identity.frontal is large
    assert Identity(BBox(0, 0, 1, 1), None, 0, 0).frontal is None
