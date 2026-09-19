"""Tests for the detector benchmark scoring in labvision.evaluation"""

import math

import numpy as np
import pytest

from labvision import evaluation as ev


def truth(box, required=True, cls=0, full=None, kind="amber 10 ml"):
    return ev.Truth(
        box=box,
        full_box=full or box,
        cls=cls,
        kind=kind,
        required=required,
        side_px=ev.side(full or box),
    )


def det(box, score, cls=-1):
    return ev.Detection(box=box, score=score, cls=cls)


def test_iou_of_identical_disjoint_and_half_overlapping_boxes():
    assert ev.iou((0, 0, 10, 10), (0, 0, 10, 10)) == 1.0
    assert ev.iou((0, 0, 10, 10), (20, 20, 30, 30)) == 0.0
    assert ev.iou((0, 0, 10, 10), (5, 0, 15, 10)) == pytest.approx(50 / 150)


def test_perfect_detections_give_ap_one():
    truths = [truth((0, 0, 10, 20)), truth((50, 0, 60, 20))]
    dets = [det((0, 0, 10, 20), 0.9), det((50, 0, 60, 20), 0.8)]
    result = ev.match_frame(truths, dets)
    assert ev.ap_at([result]) == pytest.approx(1.0)


def test_no_detections_give_ap_zero_and_nothing_required_gives_nan():
    assert ev.ap_at([ev.match_frame([truth((0, 0, 10, 20))], [])]) == 0.0
    assert math.isnan(ev.ap_at([ev.match_frame([], [det((0, 0, 5, 5), 0.5)])]))


def test_a_false_box_scored_above_the_hit_halves_ap():
    truths = [truth((0, 0, 10, 20))]
    dets = [det((100, 100, 110, 120), 0.9), det((0, 0, 10, 20), 0.8)]
    assert ev.ap_at([ev.match_frame(truths, dets)]) == pytest.approx(0.5)


def test_a_false_box_scored_below_the_hit_costs_nothing():
    truths = [truth((0, 0, 10, 20))]
    dets = [det((0, 0, 10, 20), 0.9), det((100, 100, 110, 120), 0.1)]
    assert ev.ap_at([ev.match_frame(truths, dets)]) == pytest.approx(1.0)


def test_a_duplicate_box_is_false_because_each_bottle_is_found_once():
    truths = [truth((0, 0, 10, 20))]
    dets = [det((0, 0, 10, 20), 0.9), det((0, 1, 10, 20), 0.8)]
    result = ev.match_frame(truths, dets)
    assert result.hits == [True, False]
    assert len(result.false_boxes) == 1


def test_boxes_on_bottles_that_are_not_required_are_ignored():
    hidden = truth((0, 0, 10, 8), required=False, full=(0, 0, 10, 20))
    shelf = truth((50, 0, 60, 20), required=False)
    dets = [det((0, 0, 10, 9), 0.9), det((50, 0, 60, 20), 0.8)]
    result = ev.match_frame([hidden, shelf], dets)
    assert result.scores == []
    assert result.false_boxes == []


def test_a_box_mostly_inside_a_hidden_bottles_silhouette_is_ignored():
    hidden = truth((0, 0, 10, 4), required=False, full=(0, 0, 10, 20))
    result = ev.match_frame([hidden], [det((1, 8, 9, 18), 0.9)])
    assert result.false_boxes == []


def test_class_aware_matching_needs_the_right_kit():
    truths = [truth((0, 0, 10, 20), cls=1)]
    wrong = [det((0, 0, 10, 20), 0.9, cls=0)]
    assert ev.match_frame(truths, wrong).hits == [True]
    assert ev.match_frame(truths, wrong, class_aware=True).hits == [False]


def test_the_best_matching_bottle_wins_when_a_box_overlaps_two():
    left, right = truth((0, 0, 10, 20)), truth((6, 0, 16, 20))
    result = ev.match_frame([left, right], [det((5, 0, 15, 20), 0.9)], iou_min=0.3)
    assert result.found == [None, 0.9]


def test_best_f1_threshold_keeps_every_box_at_the_threshold():
    truths = [truth((0, 0, 10, 20)), truth((50, 0, 60, 20))]
    dets = [
        det((0, 0, 10, 20), 0.9),
        det((200, 0, 210, 20), 0.5),
        det((50, 0, 60, 20), 0.3),
    ]
    threshold, f1 = ev.best_f1_threshold([ev.match_frame(truths, dets)])
    # Keeping all three: 2 hits, 1 false, 2 required -> F1 = 4 / 5.
    assert threshold == pytest.approx(0.3)
    assert f1 == pytest.approx(0.8)


def test_operating_point_counts_found_missed_and_false():
    truths = [truth((0, 0, 10, 20)), truth((50, 0, 60, 20))]
    dets = [det((0, 0, 10, 20), 0.9), det((200, 0, 210, 20), 0.6)]
    point = ev.operating_point([ev.match_frame(truths, dets)], 0.5)
    assert point["found"] == 1
    assert point["required"] == 2
    assert point["false"] == 1
    assert point["recall"] == pytest.approx(0.5)
    assert point["precision"] == pytest.approx(0.5)


def test_breakdown_groups_required_bottles():
    truths = [
        truth((0, 0, 10, 20), kind="amber 10 ml"),
        truth((50, 0, 60, 20), kind="hdpe 2000 ml"),
    ]
    result = ev.match_frame(truths, [det((0, 0, 10, 20), 0.9)])
    table = ev.breakdown([result], 0.5, lambda t: t.kind)
    assert table == {"amber 10 ml": [1, 1], "hdpe 2000 ml": [0, 1]}


def test_side_buckets_cover_every_size():
    assert ev.side_bucket(8) == "0-16 px"
    assert ev.side_bucket(16) == "16-24 px"
    assert ev.side_bucket(100) == "48+ px"
    assert ev.side_buckets()[-1] == "48+ px"


def test_truths_of_reads_the_gt_format():
    frame = {
        "bottles": [
            {"phase": "liquid", "container_ml": 10.0, "where": "bench",
             "xyxy": [0, 0, 8, 15], "full_xyxy": [0, 0, 8, 15],
             "visible_frac": 1.0, "clipped": False},
            {"phase": "powder", "container_ml": 2000.0, "where": "shelf",
             "xyxy": [0, 0, 40, 70], "full_xyxy": [0, 0, 40, 70],
             "visible_frac": 1.0, "clipped": False},
        ]
    }  # fmt: skip
    first, second = ev.truths_of(frame)
    assert (first.kind, first.cls, first.required) == ("amber 10 ml", 0, True)
    assert (second.kind, second.cls, second.required) == ("hdpe 2000 ml", 1, False)


def test_bootstrap_interval_contains_the_estimate():
    rng = np.random.default_rng(1)
    results = []
    for _ in range(40):
        truths = [truth((0, 0, 10, 20))]
        dets = [det((0, 0, 10, 20), 0.9)] if rng.random() < 0.7 else []
        results.append(ev.match_frame(truths, dets))
    low, high = ev.bootstrap(results, ev.ap_at, reps=200)
    assert low <= ev.ap_at(results) <= high


def camera_frame():
    """The scene's general camera: at (-1.5, -2.9, 3.0), 39 degrees down"""
    c, s = math.cos(math.radians(50.65)), math.sin(math.radians(50.65))
    return {
        "width": 1920,
        "height": 1080,
        "fovy_deg": 60.44,
        "cam_pos": [-1.5, -2.9, 3.0],
        # Columns are the camera's right, up and back axes in the world.
        "cam_xmat": [1, 0, 0, 0, c, -s, 0, s, c],
    }


def test_project_and_to_plane_are_inverse():
    frame = camera_frame()
    u, v = ev.project(frame, (-1.0, -0.4, 0.9))
    point = ev.to_plane(frame, u, v, 0.9)
    assert point == pytest.approx([-1.0, -0.4, 0.9], abs=1e-6)


def bottle_box(frame, x, y, z, height, width_px=10):
    u_base, v_base = ev.project(frame, (x, y, z))
    _, v_top = ev.project(frame, (x, y, z + height))
    return (u_base - width_px / 2, v_top, u_base + width_px / 2, v_base)


def test_worktop_filter_keeps_a_bench_bottle_and_drops_a_shelf_bottle():
    frame = camera_frame()
    worktop = ev.Worktop()
    bench = bottle_box(frame, -1.0, -0.4, 0.90, 0.12)
    assert ev.on_worktop(frame, bench, worktop)
    # A bottle on a shelf 0.5 m above the bench, behind it: its base casts
    # onto the far bench and its pixel height is too tall for a bottle there.
    shelf = bottle_box(frame, -1.0, 0.3, 1.40, 0.24)
    assert not ev.on_worktop(frame, shelf, worktop)
    off_bench = bottle_box(frame, -1.0, -1.5, 0.90, 0.12)
    assert not ev.on_worktop(frame, off_bench, worktop)
