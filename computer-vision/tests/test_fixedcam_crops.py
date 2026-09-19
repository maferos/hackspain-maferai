"""Tests for the training-crop exporter: which bottles are labelled and how"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fixedcam_crops as fc  # noqa: E402


def bottle(xyxy, phase="liquid", where="bench", visible=1.0, pixels=100):
    return {
        "xyxy": list(xyxy),
        "full_xyxy": list(xyxy),
        "phase": phase,
        "where": where,
        "visible_frac": visible,
        "pixels": pixels,
        "container_ml": 10.0,
    }


def frame(*bottles):
    return {"width": 1920, "height": 1080, "bottles": list(bottles)}


def test_every_sample_bottle_in_the_crop_is_labelled_wherever_it_stands():
    f = frame(
        bottle((110, 110, 120, 130)),
        bottle((200, 50, 240, 120), phase="powder", where="shelf"),
    )
    boxes = fc.crop_boxes(f, (100, 40, 484, 424))
    assert boxes == [(0, 10.0, 70.0, 20.0, 90.0), (1, 100.0, 10.0, 140.0, 80.0)]


def test_mostly_hidden_or_mostly_outside_bottles_are_not_labelled():
    f = frame(
        bottle((110, 110, 120, 130), visible=0.2),
        bottle((470, 110, 510, 170)),  # 35 % of it inside the crop
        bottle((150, 150, 160, 170), pixels=0),
    )
    assert fc.crop_boxes(f, (100, 40, 484, 424)) == []


def test_a_box_mostly_inside_is_clipped_to_the_crop():
    f = frame(bottle((470, 110, 490, 170)))  # 70 % inside
    ((kit, u0, v0, u1, v1),) = fc.crop_boxes(f, (100, 40, 484, 424))
    assert (kit, u0, v0, u1, v1) == (0, 370.0, 70.0, 384.0, 130.0)


def test_crops_stay_inside_the_frame_and_cover_every_bench_bottle():
    rng = np.random.default_rng(0)
    bench = [bottle((u, 500, u + 10, 520)) for u in (5, 400, 900, 1400, 1900)]
    f = frame(*bench)
    rects = fc.pick_crops(f, (0, 400, 1920, 700), 384, per_frame=10, rng=rng)
    for u0, v0, u1, v1 in rects:
        assert 0 <= u0 < u1 <= 1920
        assert 0 <= v0 < v1 <= 1080
        assert (u1 - u0, v1 - v0) == (384, 384)
    for b in bench:
        assert any(fc.ev.fraction_inside(b["xyxy"], r) >= 0.99 for r in rects)


def test_the_random_crop_is_added_only_to_the_requested_share_of_frames():
    f = frame(bottle((900, 500, 910, 520)))
    counts = [
        len(fc.pick_crops(f, (0, 400, 1920, 700), 384, 1, np.random.default_rng(k),
                          random_share=0.0))
        for k in range(5)
    ]  # fmt: skip
    assert counts == [1] * 5
