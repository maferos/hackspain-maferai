"""Tests for how the general-camera ring experiment decides a bottle was named"""

import sys
from pathlib import Path

import cv2
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
pytest.importorskip("mujoco")
from general_4k_identify import named  # noqa: E402

from labvision.identify import DICTIONARY, MarkerReader  # noqa: E402

ROWS = {5: {"sample_id": "SMP-0006"}, 9: {"sample_id": "PWD-0010"}}
MARKER_OF = {"SMP-0006": 5, "PWD-0010": 9}


def _bottle(sample_id, xyxy, phase="liquid", ml=10.0, where="bench"):
    return {
        "sample_id": sample_id,
        "phase": phase,
        "container_ml": ml,
        "where": where,
        "xyxy": xyxy,
        "full_xyxy": xyxy,
        "visible_frac": 1.0,
        "clipped": False,
    }


def test_a_bottle_counts_as_named_only_where_its_own_ring_reads():
    frame = np.full((400, 600, 3), 180, np.uint8)
    marker = cv2.aruco.generateImageMarker(
        cv2.aruco.getPredefinedDictionary(DICTIONARY), 5, 60
    )
    marker = cv2.copyMakeBorder(marker, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=255)
    frame[100:180, 100:180] = marker[..., None]
    bottles = [
        _bottle("SMP-0006", [90, 60, 190, 260]),
        _bottle("PWD-0010", [350, 60, 450, 260], phase="powder", ml=250.0),
        _bottle("SMP-0006", [0, 0, 10, 10], where="shelf"),
    ]
    result = named(frame, bottles, ROWS, MARKER_OF, MarkerReader())
    assert result["kinds"] == ["amber 10 ml", "hdpe 250 ml"]
    assert result["whole"] == [True, False]
    assert result["true box"] == [True, False]
    assert result["whole wrong"] == [False, False]
    assert result["true box wrong"] == [False, False]


def test_another_bottle_s_ring_on_a_bottle_is_a_wrong_name():
    frame = np.full((400, 600, 3), 180, np.uint8)
    marker = cv2.aruco.generateImageMarker(
        cv2.aruco.getPredefinedDictionary(DICTIONARY), 9, 60
    )
    marker = cv2.copyMakeBorder(marker, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=255)
    frame[100:180, 100:180] = marker[..., None]
    bottles = [_bottle("SMP-0006", [90, 60, 190, 260])]
    result = named(frame, bottles, ROWS, MARKER_OF, MarkerReader())
    assert result["whole"] == [False] and result["whole wrong"] == [True]
    assert result["true box"] == [False] and result["true box wrong"] == [True]
