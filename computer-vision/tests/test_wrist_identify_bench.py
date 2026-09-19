"""Tests for how the wrist identification benchmark grades a frame"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from wrist_identify_bench import (  # noqa: E402
    distance_bucket,
    distance_labels,
    score_frame,
)

from labvision.identify import Identity  # noqa: E402
from labvision.scene import BBox  # noqa: E402

MARKER_OF = {"SMP-0001": 0, "SMP-0002": 1, "PWD-0001": 100, "PWD-0099": 198}


def _bottle(sample_id, xyxy, where="bench", visible=1.0, clipped=False):
    return {
        "sample_id": sample_id,
        "xyxy": xyxy,
        "full_xyxy": xyxy,
        "where": where,
        "visible_frac": visible,
        "clipped": clipped,
    }


FRAME = {
    "bottles": [
        _bottle("SMP-0001", [100, 100, 140, 200]),
        _bottle("SMP-0002", [300, 100, 340, 200]),
        _bottle("PWD-0001", [500, 50, 600, 250], where="shelf"),
    ]
}


def _identity(marker_id, xyxy):
    return Identity(BBox(*xyxy), marker_id, 2, 2)


def test_a_box_naming_its_own_bottle_counts():
    found = [_identity(0, [100, 100, 140, 200]), _identity(None, [300, 100, 340, 200])]
    result = score_frame(FRAME, found, MARKER_OF, whole=False)
    assert result["required"] == [0, 1]
    assert result["named"] == [0]
    assert (result["wrong"], result["phantom"]) == (0, 0)


def test_a_box_naming_its_neighbour_is_wrong_and_names_nobody():
    found = [_identity(1, [100, 100, 140, 200])]
    result = score_frame(FRAME, found, MARKER_OF, whole=False)
    assert result["named"] == [] and result["wrong"] == 1


def test_an_id_no_bottle_in_view_carries_is_a_phantom():
    found = [_identity(198, [100, 100, 140, 200])]
    result = score_frame(FRAME, found, MARKER_OF, whole=False)
    assert result["named"] == [] and result["phantom"] == 1 and result["wrong"] == 0


def test_a_box_that_matches_no_bottle_is_neither_right_nor_wrong():
    found = [_identity(0, [800, 400, 840, 500])]
    result = score_frame(FRAME, found, MARKER_OF, whole=False)
    assert (result["named"], result["wrong"], result["phantom"]) == ([], 0, 0)


def test_a_whole_frame_read_counts_where_its_markers_lie():
    on_first = _identity(0, [110, 140, 130, 160])
    first_on_second = _identity(0, [310, 140, 330, 160])
    assert score_frame(FRAME, [on_first], MARKER_OF, whole=True)["named"] == [0]
    wrong = score_frame(FRAME, [first_on_second], MARKER_OF, whole=True)
    assert wrong["named"] == [] and wrong["wrong"] == 1


def test_only_visible_unclipped_bench_bottles_are_required():
    frame = {
        "bottles": [
            _bottle("SMP-0001", [0, 0, 10, 10], visible=0.4),
            _bottle("SMP-0002", [0, 0, 10, 10], clipped=True),
            _bottle("PWD-0001", [0, 0, 10, 10], where="shelf"),
        ]
    }
    assert score_frame(frame, [], MARKER_OF, whole=False)["required"] == []


def test_distance_buckets_cover_every_range():
    labels = distance_labels()
    assert [distance_bucket(d) for d in (0.3, 0.5, 0.7, 0.95)] == labels
