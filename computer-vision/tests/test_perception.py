"""Tests for the propose-and-confirm core: frames and cameras in, bottles out"""

import math

import cv2
import numpy as np
import pytest

from labvision.camera import Camera
from labvision.identify import DICTIONARY
from labvision.perception import (
    BENCH_TOP_Z,
    Confirmation,
    Proposal,
    confirm,
    perceived,
    propose,
    refine,
    ring_geometry,
)
from labvision.scene import BBox, gopro_intrinsics, predict_bbox

INTRINSICS = gopro_intrinsics(1920, 1080)
GENERAL = Camera.look_at(INTRINSICS, (0.0, -2.9, 3.0), (0.0, -0.4, BENCH_TOP_Z))


def _box_of(xy, radius=0.025, height=0.1):
    return predict_bbox(
        GENERAL, (*xy, BENCH_TOP_Z), radius=radius, height=height, samples=256
    )


def test_propose_places_a_box_on_the_bench_near_the_bottle():
    found = propose([(_box_of((0.2, -0.4)), 0.8, "bottle")], GENERAL)
    assert len(found) == 1
    assert math.dist(found[0].xy, (0.2, -0.4)) < 0.01


def test_nearby_boxes_are_one_bottle_and_the_best_score_wins():
    box = _box_of((0.2, -0.4))
    nudged = BBox(box.u_min + 1, box.v_min, box.u_max + 1, box.v_max)
    other = _box_of((0.6, -0.4))
    found = propose([(box, 0.4, "a"), (nudged, 0.9, "b"), (other, 0.5, "c")], GENERAL)
    assert [p.label for p in found] == ["b", "c"]


def test_the_caller_filter_drops_boxes():
    box = _box_of((0.2, -0.4))
    assert propose([(box, 0.8, "bottle")], GENERAL, keep=lambda b: False) == []


def test_a_box_above_the_horizon_is_not_proposed():
    level = Camera.look_at(INTRINSICS, (0.0, -2.9, 1.5), (0.0, 0.0, 1.5))
    assert propose([(BBox(900, 0, 940, 2), 0.9, "bottle")], level) == []


@pytest.mark.parametrize("eye", [(0.0, -0.3, 1.0), (0.12, -0.25, 1.05)])
def test_refine_recovers_the_axis_from_the_ring_centre(eye):
    axis, radius, ring_height = np.array([0.05, -0.02]), 0.02, 0.04
    camera = Camera.look_at(INTRINSICS, eye, (*axis, BENCH_TOP_Z + ring_height))
    toward = np.array(eye[:2]) - axis
    surface = axis + radius * toward / np.linalg.norm(toward)
    uv = camera.project(np.array([*surface, BENCH_TOP_Z + ring_height]))
    assert refine(camera, tuple(uv), radius, ring_height) == pytest.approx(
        tuple(axis), abs=1e-6
    )


def test_refine_gives_up_when_the_ray_never_reaches_the_ring():
    below = Camera.look_at(INTRINSICS, (0.0, -0.3, 0.5), (0.0, 0.0, 0.5))
    assert refine(below, (960.0, 1000.0), 0.02, 0.04) is None
    level = Camera.look_at(INTRINSICS, (0.0, -0.3, 0.94), (0.0, 0.0, 0.94))
    assert refine(level, (960.0, 539.5), 0.02, 0.04) is None


def test_ring_geometry_comes_from_the_label_mesh():
    radius, height = ring_geometry("flask_10ml")
    assert 0.009 < radius < 0.013
    assert 0.0 < height < 0.054


def _wrist_frame(camera, markers):
    """A grey frame with a marker of each ``(id, world point)`` centred on its image"""
    frame = np.full((1080, 1920, 3), 190, np.uint8)
    dictionary = cv2.aruco.getPredefinedDictionary(DICTIONARY)
    for marker_id, point in markers:
        u, v = camera.project(np.asarray(point, float))
        image = cv2.aruco.generateImageMarker(dictionary, marker_id, 60)
        image = cv2.copyMakeBorder(
            image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=255
        )
        top, left = int(round(v)) - 40, int(round(u)) - 40
        frame[top : top + 80, left : left + 80] = image[..., None]
    return frame


ROWS = {
    5: {"sample_id": "SMP-0006", "phase": "liquid", "vessel_class": "flask_10ml"},
    9: {"sample_id": "PWD-0010", "phase": "powder", "vessel_class": "bottle_100ml"},
    7: {"sample_id": "PWD-0020", "phase": "powder", "vessel_class": "bottle_2000ml"},
}
TARGET = (0.0, 0.0, BENCH_TOP_Z + 0.05)
WRIST = Camera.look_at(INTRINSICS, (0.0, -0.3, 1.0), TARGET)


def _ring_point(vessel, axis_xy):
    """Where a bottle's ring faces the wrist camera"""
    radius, height = ring_geometry(vessel)
    axis = np.array(axis_xy, float)
    toward = WRIST.position[:2] - axis
    surface = axis + radius * toward / np.linalg.norm(toward)
    return (*surface, BENCH_TOP_Z + height)


def test_confirm_names_the_ring_of_the_proposed_bottle_and_places_it():
    far = _ring_point("bottle_100ml", (0.25, 0.05))
    frame = _wrist_frame(WRIST, [(9, far), (5, _ring_point("flask_10ml", (0, 0)))])
    found = confirm(frame, WRIST, TARGET, ROWS)
    assert (found.sample_id, found.marker_id, found.phase) == ("SMP-0006", 5, "liquid")
    assert found.refined_xy == pytest.approx((0.0, 0.0), abs=0.004)


def test_a_neighbours_ring_seen_past_the_proposal_is_passed_over():
    # A 2 L bottle 20 cm behind the proposal: its ring projects near the
    # proposal, but placed from that ring the bottle stands far from it.
    behind = _ring_point("bottle_2000ml", (0.0, 0.2))
    frame = _wrist_frame(WRIST, [(7, behind)])
    assert confirm(frame, WRIST, TARGET, ROWS) == Confirmation()
    near = _ring_point("flask_10ml", (0.01, 0.0))
    frame = _wrist_frame(WRIST, [(7, behind), (5, near)])
    assert confirm(frame, WRIST, TARGET, ROWS).sample_id == "SMP-0006"


def test_confirm_reads_nothing_when_no_ring_is_near():
    frame = _wrist_frame(WRIST, [(9, _ring_point("bottle_100ml", (0.25, 0.05)))])
    assert confirm(frame, WRIST, TARGET, ROWS) == Confirmation()


def test_perceived_prefers_the_refined_position():
    proposal = Proposal((0.1, -0.4), 0.7, "bottle", BBox(0, 0, 1, 1))
    named = Confirmation("SMP-0006", 5, 3, "liquid", 12.0, (0.11, -0.41))
    bottle = perceived(proposal, named)
    assert bottle.position == (0.11, -0.41, BENCH_TOP_Z)
    assert bottle.refined and bottle.cls == "amber bottle"
    unread = perceived(proposal, Confirmation())
    assert unread.position == (0.1, -0.4, BENCH_TOP_Z) and unread.sample_id is None


ROWS[11] = {"sample_id": "NEIGHBOUR", "phase": "liquid", "vessel_class": "flask_50ml"}
ROWS[12] = {"sample_id": "PWD-0004", "phase": "powder", "vessel_class": "bottle_1000ml"}


def test_the_ring_whose_bottle_stands_on_the_proposal_beats_a_nearer_pixel():
    # A 50 ml flask 4.5 cm behind the proposed 10 ml one: within the 5 cm
    # limit, and its ring sits nearer the aim point in the image.
    own = _ring_point("flask_10ml", (0.0, 0.0))
    behind = _ring_point("flask_50ml", (0.0, 0.045))
    expected = WRIST.project(np.asarray(TARGET, float))
    assert math.dist(WRIST.project(np.asarray(behind)), expected) < math.dist(
        WRIST.project(np.asarray(own)), expected
    )
    frame = _wrist_frame(WRIST, [(11, behind), (5, own)])
    assert confirm(frame, WRIST, TARGET, ROWS).sample_id == "SMP-0006"


def _ring_frame(camera, vessel, axis_xy, marker_id, angles_deg=(-45, 0, 45)):
    """Markers of a ring drawn where they stand round a bottle, as a camera sees them"""
    radius, height = ring_geometry(vessel)
    side = 0.75 * radius * 2 * math.pi / 8
    axis = np.array([*axis_xy, BENCH_TOP_Z + height])
    toward = camera.position[:2] - axis[:2]
    facing = math.atan2(toward[1], toward[0])
    dictionary = cv2.aruco.getPredefinedDictionary(DICTIONARY)
    image = cv2.aruco.generateImageMarker(dictionary, marker_id, 120)
    image = cv2.copyMakeBorder(image, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
    frame = np.full((1080, 1920, 3), 150, np.uint8)
    up = np.array([0.0, 0.0, 1.0])
    for angle in angles_deg:
        a = facing + math.radians(angle)
        normal = np.array([math.cos(a), math.sin(a), 0.0])
        right = np.cross(up, normal)
        centre = axis + radius * normal
        half = side * 8 / 6 / 2  # the quiet zone widens the drawn square
        corners = [
            centre - half * right + half * up,
            centre + half * right + half * up,
            centre + half * right - half * up,
            centre - half * right - half * up,
        ]
        dst = camera.project(np.array(corners)).astype(np.float32)
        n = image.shape[0]
        src = np.float32([[0, 0], [n, 0], [n, n], [0, n]])
        warp = cv2.getPerspectiveTransform(src, dst)
        drawn = cv2.warpPerspective(image, warp, (1920, 1080), borderValue=0)
        mask = cv2.warpPerspective(np.full_like(image, 255), warp, (1920, 1080))
        frame[mask > 0] = drawn[mask > 0][..., None]
    return frame


def test_refine_places_a_big_bottle_from_its_frontal_marker():
    camera = Camera.look_at(
        INTRINSICS, (0.0, -0.3, 1.0), (0.0, 0.0, BENCH_TOP_Z + 0.08)
    )
    frame = _ring_frame(camera, "bottle_1000ml", (0.0, 0.0), 12)
    found = confirm(frame, camera, (0.0, 0.0, BENCH_TOP_Z + 0.05), ROWS)
    assert found.sample_id == "PWD-0004"
    assert math.dist(found.refined_xy, (0.0, 0.0)) < 0.004


def _marker_corners(camera, axis_xy, radius, height, angle, side=0.03, turn=0):
    """A marker's corners in the image, tangent to the ring at ``angle``"""
    normal = np.array([math.cos(angle), math.sin(angle), 0.0])
    up = np.array([0.0, 0.0, 1.0])
    right = np.cross(up, normal)
    centre = np.array([*axis_xy, BENCH_TOP_Z + height]) + radius * normal
    h = side / 2
    quad = [
        centre - h * right + h * up,
        centre + h * right + h * up,
        centre + h * right - h * up,
        centre - h * right - h * up,
    ]
    return np.roll(camera.project(np.array(quad)), turn, axis=0)


@pytest.mark.parametrize("turn", [0, 1])
def test_refine_marker_places_the_axis_from_a_marker_facing_away(turn):
    from labvision.perception import refine_marker

    camera = Camera.look_at(INTRINSICS, (0.0, -0.3, 1.1), (0.0, 0.0, BENCH_TOP_Z))
    radius, height = 0.044, 0.1
    facing = math.atan2(-0.3, 0.0)  # towards the camera, from the axis
    corners = _marker_corners(
        camera, (0.0, 0.0), radius, height, facing + math.radians(20), turn=turn
    )
    axis = refine_marker(camera, corners, radius, height)
    assert math.dist(axis, (0.0, 0.0)) < 0.0005
    along_view = refine(camera, tuple(corners.mean(axis=0)), radius, height)
    assert math.dist(along_view, (0.0, 0.0)) > 0.01  # what this replaces


def test_confirm_places_a_turned_ring_by_the_way_its_marker_faces():
    camera = Camera.look_at(
        INTRINSICS, (0.0, -0.3, 1.0), (0.0, 0.0, BENCH_TOP_Z + 0.08)
    )
    frame = _ring_frame(camera, "bottle_1000ml", (0.0, 0.0), 12, (-25, 20, 65))
    found = confirm(frame, camera, (0.0, 0.0, BENCH_TOP_Z + 0.05), ROWS)
    assert found.sample_id == "PWD-0004"
    assert math.dist(found.refined_xy, (0.0, 0.0)) < 0.003
