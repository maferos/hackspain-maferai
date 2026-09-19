"""Tests for the Isaac Replicator to benchmark-truth converter, on synthetic output"""

import json
import math
import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import isaac_replicator_to_gt as conv  # noqa: E402

from labvision import evaluation as ev  # noqa: E402

DTYPE = [
    ("semanticId", "<u4"),
    ("x_min", "<i4"),
    ("y_min", "<i4"),
    ("x_max", "<i4"),
    ("y_max", "<i4"),
    ("occlusionRatio", "<f4"),
]


def look_down_camera():
    """A camera at (0, -2, 2) looking at the origin, as column-vector pose"""
    position = np.array([0.0, -2.0, 2.0])
    forward = -position / np.linalg.norm(position)
    right = np.cross(forward, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right)
    up = np.cross(right, forward)
    rotation = np.column_stack([right, up, -forward])
    return position, rotation


def row_vector_view(position, rotation):
    """World-to-camera transform in Replicator's flattened row-vector layout"""
    view = np.eye(4)
    view[:3, :3] = rotation.T
    view[:3, 3] = -rotation.T @ position
    return view.T.reshape(-1).tolist()


def write_frame(folder: Path, number: str = "0000") -> None:
    cv2.imwrite(str(folder / f"rgb_{number}.png"), np.zeros((80, 100, 4), np.uint8))
    tight = np.array(
        [(0, 10, 20, 17, 34, 0.0), (1, 40, 10, 60, 50, 0.4), (2, 70, 5, 99, 60, 0.0)],
        dtype=DTYPE,
    )
    loose = np.array(
        [(1, 40, 5, 60, 50, 0.4), (0, 10, 20, 17, 34, 0.0), (2, 70, 5, 99, 60, 0.0)],
        dtype=DTYPE,
    )
    labels = {"0": {"class": "amber_10ml"}, "1": {"class": "PWD-0005"},
              "2": {"class": "balance"}}  # fmt: skip
    np.save(folder / f"bounding_box_2d_tight_{number}.npy", tight)
    np.save(folder / f"bounding_box_2d_loose_{number}.npy", loose)
    for kind, prims in (
        ("tight", ["/World/a", "/World/b", "/World/scale"]),
        ("loose", ["/World/b", "/World/a", "/World/scale"]),
    ):
        (folder / f"bounding_box_2d_{kind}_labels_{number}.json").write_text(
            json.dumps(labels)
        )
        (folder / f"bounding_box_2d_{kind}_prim_paths_{number}.json").write_text(
            json.dumps(prims)
        )
    position, rotation = look_down_camera()
    params = {
        "cameraViewTransform": row_vector_view(position, rotation),
        "cameraFocalLength": 18.0,
        "cameraAperture": [20.955, 15.2908],
    }
    (folder / f"camera_params_{number}.json").write_text(json.dumps(params))


def test_camera_pose_round_trips_through_the_row_vector_view():
    position, rotation = look_down_camera()
    params = {
        "cameraViewTransform": row_vector_view(position, rotation),
        "cameraFocalLength": 18.0,
        "cameraAperture": [20.955, 15.2908],
    }
    pos, xmat, fovy = conv.camera_of(params, 1280, 720, 1.0)
    assert pos == pytest.approx(position.tolist())
    assert xmat == pytest.approx(rotation.reshape(-1).tolist())
    # Square pixels: the vertical aperture follows the image, not the USD value.
    vertical = 20.955 * 720 / 1280
    assert fovy == pytest.approx(math.degrees(2 * math.atan(vertical / 2 / 18.0)))


def test_fovy_comes_from_the_projection_matrix_when_there_is_one():
    position, rotation = look_down_camera()
    tan_half = math.tan(math.radians(40.0) / 2)
    projection = [0.0] * 16
    projection[0] = 1.0 / (tan_half * 16 / 9)
    projection[5] = 1.0 / tan_half
    params = {
        "cameraViewTransform": row_vector_view(position, rotation),
        "cameraProjection": projection,
        "cameraFocalLength": 18.0,
        "cameraAperture": [20.955, 15.2908],
    }
    _, _, fovy = conv.camera_of(params, 1280, 720, 1.0)
    assert fovy == pytest.approx(40.0)


def test_convert_keeps_bottles_pairs_tight_with_loose_and_drops_the_rest(tmp_path):
    source, out = tmp_path / "rep", tmp_path / "out"
    source.mkdir()
    write_frame(source)
    gt = conv.convert(source, out, "isaac_test", (0.0, 0.0), (3.0, 0.75), 0.9, 1.0,
                      inclusive_max=True)  # fmt: skip
    (frame,) = gt["frames"]
    assert (out / frame["file"]).exists()
    assert cv2.imread(str(out / frame["file"])).shape == (80, 100, 3)
    amber, hdpe = frame["bottles"]
    assert (amber["phase"], amber["container_ml"]) == ("liquid", 10.0)
    assert (hdpe["phase"], hdpe["sample_id"]) == ("powder", "PWD-0005")
    # Inclusive pixel maxima become exclusive box corners.
    assert amber["xyxy"] == [10, 20, 18, 35]
    # The loose box is found by prim path although the order differs.
    assert hdpe["full_xyxy"] == [40, 5, 61, 51]
    assert hdpe["visible_frac"] == pytest.approx(0.6)
    assert not amber["clipped"]
    truths = ev.truths_of(frame)
    assert [t.required for t in truths] == [True, True]
    assert json.loads((out / "gt.json").read_text())["bench_half"] == [3.0, 0.75]


def test_an_unknown_class_is_not_a_bottle():
    assert conv.bottle_of("balance", "/World/balance_1", {}) is None
    assert conv.bottle_of("hdpe", None, {})["phase"] == "powder"
    # "chamber" holds "amber"; only whole words in the label name a kit.
    assert conv.bottle_of("beaker", "/World/Chamber/beaker_01", {}) is None
    assert conv.bottle_of("amber_50ml", None, {})["container_ml"] == 50.0
