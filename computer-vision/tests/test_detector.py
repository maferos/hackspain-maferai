"""Tests for the vessel detector: box maths, barcode attachment, the size floor"""

import json
from pathlib import Path

import numpy as np
import pytest

from labvision import ean13
from labvision.detector import (
    BACKENDS,
    SIDE_PX_MARGINAL,
    SIDE_PX_RELIABLE,
    Box,
    apparent_size_px,
    attach_barcodes,
    iter_frames,
)
from labvision.scene import VESSELS, BBox, default_intrinsics


def _box(u0, v0, u1, v1, label="bottle", score=0.5):
    return Box(label, score, BBox(u0, v0, u1, v1))


def test_side_px_is_geometric_mean_of_width_and_height():
    assert _box(0, 0, 40, 90).side_px == pytest.approx(60.0)


def test_to_json_round_trips():
    box = _box(1.25, 2.5, 30, 40)
    box.barcode = "2006943906698"
    record = json.loads(json.dumps(box.to_json()))
    assert record["barcode"] == "2006943906698"
    assert record["xyxy"] == [1.2, 2.5, 30, 40] or record["xyxy"] == [1.3, 2.5, 30, 40]


def test_attach_barcodes_reads_the_label_inside_the_box():
    code = ean13.full_code("200694390669")
    symbol = ean13.render_symbol(code, module_px=3)
    symbol = np.repeat(symbol[..., None], 3, axis=-1) if symbol.ndim == 2 else symbol
    canvas = np.full((600, 900, 3), 255, np.uint8)
    h, w = symbol.shape[:2]
    canvas[120 : 120 + h, 200 : 200 + w] = symbol
    box = _box(200, 120, 200 + w, 120 + h)
    decoy = _box(700, 400, 760, 500)
    attach_barcodes(canvas, [box, decoy])
    assert box.barcode == code
    assert decoy.barcode is None


def test_apparent_size_matches_the_documented_wall_camera():
    """The room camera puts a 1 L bottle at 16 px wide in a 640x480 frame.

    That is below the marginal floor, which is the point the module docstring
    makes; if this number changes, so must that paragraph.
    """
    width, height = apparent_size_px(VESSELS["bottle_1000ml"], 3.23)
    assert round(width) == 16
    assert round(height) == 39
    assert (width * height) ** 0.5 < SIDE_PX_RELIABLE


def test_apparent_size_scales_with_network_input():
    cam = default_intrinsics(1280, 960)
    width_frame, _ = apparent_size_px(VESSELS["bottle_1000ml"], 3.23, cam)
    width_net, _ = apparent_size_px(VESSELS["bottle_1000ml"], 3.23, cam, input_px=640)
    assert width_net == pytest.approx(width_frame / 2)
    assert SIDE_PX_MARGINAL < SIDE_PX_RELIABLE


def test_iter_frames_reads_a_folder_in_name_order(tmp_path):
    import cv2

    for name in ("b.png", "a.png", "notes.txt"):
        if name.endswith(".png"):
            cv2.imwrite(str(tmp_path / name), np.zeros((8, 8, 3), np.uint8))
        else:
            (tmp_path / name).write_text("x")
    assert [name for name, _ in iter_frames(tmp_path)] == ["a", "b"]
    assert [name for name, _ in iter_frames(tmp_path, limit=1)] == ["a"]


@pytest.mark.skipif(
    not any(
        (folder / BACKENDS["coco"].weights).exists()
        for folder in (Path.cwd(), Path(__file__).resolve().parents[2])
    ),
    reason="yolo11s weights not downloaded",
)
def test_coco_backend_finds_nothing_in_a_blank_frame():
    from labvision.detector import Detector

    detector = Detector("coco", input_px=320)
    assert detector.detect(np.zeros((240, 320, 3), np.uint8)) == []
