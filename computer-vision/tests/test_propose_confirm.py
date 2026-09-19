"""Tests for how the propose-and-confirm experiment scores a layout"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
pytest.importorskip("mujoco")
from propose_confirm import MATCH_M, score, summarise  # noqa: E402


def _found(xy, named=None, refined=None):
    return {"xy": list(xy), "confirm": {"sample_id": named, "refined_xy": refined}}


BOTTLES = [
    {"sample_id": "SMP-0001", "xy": [0.0, 0.0]},
    {"sample_id": "SMP-0002", "xy": [0.02, 0.0]},
    {"sample_id": "PWD-0001", "xy": [1.0, 0.0]},
]


def test_each_proposal_counts_for_one_bottle_only():
    result = score(BOTTLES, set(), [_found((0.005, 0.0), "SMP-0001")])
    assert [b["proposed"] for b in result["bottles"]] == [True, False, False]
    assert result["stray"] == []


def test_a_proposal_too_far_from_every_bottle_is_stray():
    far = _found((0.5, 0.5), "SMP-0001")
    result = score(BOTTLES, set(), [far])
    assert not any(b["proposed"] for b in result["bottles"])
    assert result["stray"] == [far]
    edge = _found((1.0 + MATCH_M * 0.99, 0.0))
    assert score(BOTTLES, set(), [edge])["bottles"][2]["proposed"]


def test_naming_is_right_wrong_or_missing():
    found = [
        _found((0.0, 0.0), "SMP-0001"),
        _found((0.02, 0.0), "SMP-0001"),
        _found((1.0, 0.0)),
    ]
    graded = score(BOTTLES, set(), found)["bottles"]
    assert [(b["correct"], b["wrong"]) for b in graded] == [
        (True, False),
        (False, True),
        (False, False),
    ]


def test_errors_are_measured_from_the_proposal_and_the_refinement():
    found = [_found((0.003, 0.004), "SMP-0001", refined=(0.0, 0.001))]
    bottle = score(BOTTLES[:1], {"SMP-0001"}, found)["bottles"][0]
    assert bottle["error_m"] == pytest.approx(0.005)
    assert bottle["refined_error_m"] == pytest.approx(0.001)
    assert bottle["visible"]
    unrefined = score(BOTTLES[:1], set(), [_found((0.0, 0.0), "SMP-0001")])
    assert unrefined["bottles"][0]["refined_error_m"] is None


def test_the_summary_counts_over_every_layout():
    layouts = [
        {
            "scored": score(
                BOTTLES[:2], {"SMP-0001", "SMP-0002"}, [_found((0, 0), "SMP-0001")]
            ),
            "seconds": {"render": 1.0, "propose": 2.0, "confirm": 3.0},
        }
    ]
    report = summarise(layouts, "world-b")
    assert "| named correctly | 50 % (1/2) | 50 % (1/2) |" in report
    assert "| named wrongly | 0 | 0 |" in report


def test_the_loose_filter_keeps_the_far_half_that_the_strict_one_drops():
    from propose_confirm import on_any_worktop

    from labvision.scene import BBox

    meta = {
        "set": "general",
        "width": 1920,
        "height": 1080,
        "fovy_deg": 60.44,
        "cam_pos": [0.0, -2.9, 3.0],
        # The scene's general camera: xyaxes "1 0 0  0 0.6341 0.7733", its
        # axes as the columns of a row-major matrix, as MuJoCo stores them.
        "cam_xmat": [1, 0, 0, 0, 0.6341, -0.7733, 0, 0.7733, 0.6341],
    }
    from perfumery_eval import base_on_worktop, on_worktop

    # A box whose base lands just past the bench spine, on the far half.
    far = [
        BBox(950, v - 30, 970, v)
        for v in range(40, 1080, 4)
        if (p := base_on_worktop(meta, (950, v - 30, 970, v)))
        and 0.05 < p[1] < 0.5
        and abs(p[0]) < 1
    ]
    assert far, "no pixel row of this camera lands on the far half"
    box = far[len(far) // 2]
    assert not on_worktop(meta, box.as_tuple())
    assert on_any_worktop(meta, box)
