"""Tests for the perceived world state and its shape for the console"""

import json
import sys
from pathlib import Path

import pytest

from labvision.world import PerceivedBottle, to_dashboard

BRIDGE = Path(__file__).resolve().parents[2] / "dashboard" / "bridge"


def _bottles():
    return [
        PerceivedBottle((0.1, -0.4, 0.9), 0.874, "SMP-0005", 4, "liquid", refined=True),
        PerceivedBottle((0.5, -0.3, 0.9), 0.5, "PWD-0012", 111, "powder"),
        PerceivedBottle((0.9, -0.2, 0.9), 0.31),
    ]


def test_records_carry_the_console_fields_in_order():
    records = to_dashboard(_bottles())
    assert [r["index"] for r in records] == [0, 1, 2]
    assert set(records[0]) == {"index", "id", "cls", "confidence", "position", "stale"}
    assert records[0]["position"] == {"x": 0.1, "y": -0.4, "z": 0.9}
    json.dumps(records)


def test_class_follows_the_kit_once_named():
    assert [r["cls"] for r in to_dashboard(_bottles())] == [
        "amber bottle",
        "hdpe bottle",
        "bottle",
    ]


def test_an_unconfirmed_bottle_has_no_id():
    record = to_dashboard(_bottles())[2]
    assert record["id"] is None and record["confidence"] == 0.31


def test_the_bridge_accepts_the_records():
    """Checked against the console bridge itself when it is importable"""
    if not BRIDGE.is_dir():
        pytest.skip("dashboard bridge not in this checkout")
    sys.path.insert(0, str(BRIDGE))
    try:
        from labbridge import state
    except ImportError as error:  # pragma: no cover - depends on the checkout
        pytest.skip(f"labbridge not importable: {error}")
    perception = state.perception_state(vessels=to_dashboard(_bottles()))
    assert perception["detections"] == 3
    assert perception["vessels"][0]["id"] == "SMP-0005"
