"""Tests for the benchmark's tiling and worktop-region wrappers, with a fake model"""

import math
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fixedcam_models as fm  # noqa: E402

from labvision import evaluation as ev  # noqa: E402


class PaintedBoxes:
    """A fake detector that returns every white rectangle painted in its input"""

    def __init__(self) -> None:
        """Start with no calls recorded"""
        self.calls: list[tuple[int, int]] = []

    def predict(self, image: np.ndarray) -> list[ev.Detection]:
        """Return one box per painted rectangle, scanning rows then columns"""
        self.calls.append(image.shape[:2])
        mask = image[..., 0] > 128
        out = []
        seen = np.zeros_like(mask)
        for v, u in zip(*np.nonzero(mask), strict=True):
            if seen[v, u]:
                continue
            v1 = v
            while v1 < mask.shape[0] and mask[v1, u]:
                v1 += 1
            u1 = u
            while u1 < mask.shape[1] and mask[v, u1]:
                u1 += 1
            seen[v:v1, u:u1] = True
            out.append(ev.Detection((float(u), float(v), float(u1), float(v1)), 0.9, 0))
        return out


def frame_with(boxes, size=(400, 900)):
    image = np.zeros((*size, 3), np.uint8)
    for u0, v0, u1, v1 in boxes:
        image[v0:v1, u0:u1] = 255
    return image


def test_tiling_finds_every_box_once_even_across_tile_edges():
    boxes = [(10, 10, 30, 50), (190, 100, 215, 140), (380, 300, 400, 340)]
    tiled = fm.TiledPredictor(PaintedBoxes(), tile=200, overlap=0.3)
    found = sorted(d.box for d in tiled.predict(frame_with(boxes)))
    assert found == sorted(tuple(float(c) for c in b) for b in boxes)


def test_tiling_keeps_a_box_on_the_regions_outer_border():
    # The box touches the right edge of the tiled region, which no tile overlaps.
    tiled = fm.TiledPredictor(
        PaintedBoxes(), tile=200, overlap=0.25, roi=lambda frame: (0, 0, 500, 400)
    )
    tiled.frame = {}
    found = tiled.predict(frame_with([(480, 50, 500, 90)]))
    assert [d.box for d in found] == [(480.0, 50.0, 500.0, 90.0)]


def test_upscaled_tiles_map_boxes_back_to_frame_pixels():
    tiled = fm.TiledPredictor(PaintedBoxes(), tile=200, upscale=2.0)
    (found,) = tiled.predict(frame_with([(50, 60, 70, 100)]))
    assert found.box == pytest.approx((50, 60, 70, 100), abs=1.0)


def test_roi_predictor_crops_enlarges_and_shifts_back():
    inner = PaintedBoxes()
    roi = fm.RoiPredictor(inner, roi=lambda frame: (100, 50, 600, 350), upscale=2.0)
    roi.frame = {}
    (found,) = roi.predict(frame_with([(300, 200, 320, 240)]))
    assert inner.calls == [(600, 1000)]
    assert found.box == pytest.approx((300, 200, 320, 240), abs=1.0)


def test_worktop_roi_brackets_the_bench_in_the_general_camera():
    c, s = math.cos(math.radians(50.65)), math.sin(math.radians(50.65))
    frame = {
        "width": 1920,
        "height": 1080,
        "fovy_deg": 60.44,
        "cam_pos": [-1.5, -2.9, 3.0],
        "cam_xmat": [1, 0, 0, 0, c, -s, 0, s, c],
    }
    u0, v0, u1, v1 = fm.worktop_roi(frame, ev.Worktop())
    assert 0 <= u0 < u1 <= 1920 and 0 <= v0 < v1 <= 1080
    # A bottle base at the bench centre projects inside the region.
    u, v = ev.project(frame, (0.0, -0.3, 0.9))
    assert u0 <= u <= u1 and v0 <= v <= v1
    # The region is a band: much less than the whole frame is searched.
    assert (v1 - v0) < 1080


def test_nms_keeps_the_best_of_overlapping_boxes():
    dets = [
        ev.Detection((0, 0, 10, 20), 0.5),
        ev.Detection((1, 0, 11, 20), 0.9),
        ev.Detection((50, 0, 60, 20), 0.3),
    ]
    kept = fm.nms(dets)
    assert sorted(d.score for d in kept) == [0.3, 0.9]
