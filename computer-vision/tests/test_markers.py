"""Tests for the ArUco ring reader and the posterior it returns."""

import cv2
import numpy as np
import pytest

from labvision import bottles, markers

MARKER_PX = 96
"""Side of one rendered marker in the test frames, generously large."""


def marker_image(marker_id: int, size: int = MARKER_PX) -> np.ndarray:
    """One marker on a white field, with room for its quiet zone."""
    book = cv2.aruco.getPredefinedDictionary(bottles.ARUCO_DICTIONARY)
    marker = cv2.aruco.generateImageMarker(book, marker_id, size)
    pad = size // 4
    return cv2.copyMakeBorder(
        marker, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=255
    )


def frame_with(marker_id: int, copies: int = 4) -> np.ndarray:
    """A frame holding several copies of one marker, as a ring would present."""
    tile = marker_image(marker_id)
    strip = np.hstack([tile] * copies)
    return cv2.copyMakeBorder(strip, 24, 24, 24, 24, cv2.BORDER_CONSTANT, value=255)


def only_quad(image: np.ndarray) -> np.ndarray:
    """The first quad OpenCV finds in an image."""
    corners, _ids, _rejected = markers.make_detector().detectMarkers(image)
    assert len(corners), "the detector found no marker to score"
    return corners[0]


def test_the_codeword_table_covers_every_id_in_four_rotations() -> None:
    book = markers.codeword_bits()
    assert book.shape == (250, 4, markers.DATA_CELLS**2)
    assert set(np.unique(book)) <= {0, 1}


def test_the_codeword_table_agrees_with_what_opencv_prints() -> None:
    """The table is read back out of generateImageMarker, so it cannot drift."""
    book = cv2.aruco.getPredefinedDictionary(bottles.ARUCO_DICTIONARY)
    for marker_id in (0, 7, 137, 249):
        bits = markers.codeword_bits()[marker_id, 0].reshape(4, 4).astype(np.uint8)
        found, index, _rotation = book.identify(bits, 0.6)
        assert found and index == marker_id


def test_a_clean_marker_reads_with_the_right_id() -> None:
    image = marker_image(42)
    reading = markers.read_quad(image, only_quad(image))
    assert reading is not None
    assert reading.marker_id == 42
    assert reading.bit_errors == 0
    assert reading.probability > 0.999


def test_confidence_never_reaches_one_even_on_a_perfect_render() -> None:
    """A noiseless render matching the model is not proof; the cap says so."""
    image = marker_image(42)
    reading = markers.read_quad(image, only_quad(image))
    assert reading is not None
    assert reading.probability < 1.0
    assert reading.runner_up != reading.marker_id


def test_losing_resolution_costs_confidence() -> None:
    """What distance does to a marker: cells drift towards each other."""
    sharp = marker_image(42)
    quad = only_quad(sharp)
    small = cv2.resize(sharp, None, fx=0.09, fy=0.09, interpolation=cv2.INTER_AREA)
    far = cv2.resize(small, sharp.shape[::-1], interpolation=cv2.INTER_LINEAR)

    clean = markers.read_quad(sharp, quad)
    degraded = markers.read_quad(far, quad)
    assert clean is not None and degraded is not None
    assert degraded.probability < clean.probability


def test_a_blank_quad_scores_nothing_rather_than_guessing() -> None:
    blank = np.full((MARKER_PX, MARKER_PX), 200, np.uint8)
    quad = np.array([[8, 8], [88, 8], [88, 88], [8, 88]], np.float32)
    assert markers.read_quad(blank, quad) is None


def test_restricting_the_candidates_to_the_catalogue_raises_confidence() -> None:
    """Only ids the catalogue prints are possible, which is a real prior."""
    image = marker_image(42)
    quad = only_quad(image)
    everything = markers.read_quad(image, quad)
    catalogue = markers.read_quad(image, quad, candidates=np.arange(0, 50))
    assert everything is not None and catalogue is not None
    assert catalogue.probability >= everything.probability


def test_more_copies_of_the_same_marker_fuse_into_more_confidence() -> None:
    readings = markers.read_markers(frame_with(42, copies=4))
    assert len(readings) >= 2
    one = markers.fuse(readings[:1])
    several = markers.fuse(readings)
    assert one[0][0] == several[0][0] == 42
    assert several[0][1] > one[0][1]


def test_one_corrupted_copy_does_not_outvote_the_others() -> None:
    """The ring's point: a marker seen badly is outweighed, not obeyed."""
    frame = frame_with(42, copies=4)
    tile = MARKER_PX + MARKER_PX // 2
    frame[24:24 + tile, 24:24 + tile] = cv2.GaussianBlur(
        frame[24:24 + tile, 24:24 + tile], (0, 0), 7.0
    )
    result = markers.fuse(markers.read_markers(frame))
    assert result[0][0] == 42


def test_fusing_readings_from_different_candidate_sets_is_refused() -> None:
    image = marker_image(42)
    quad = only_quad(image)
    wide = markers.read_quad(image, quad)
    narrow = markers.read_quad(image, quad, candidates=np.arange(0, 50))
    with pytest.raises(markers.MarkerError, match="candidate sets"):
        markers.fuse([wide, narrow])


def test_fuse_rejects_a_temper_outside_its_range() -> None:
    readings = markers.read_markers(marker_image(42))
    with pytest.raises(markers.MarkerError, match="temper"):
        markers.fuse(readings, temper=1.5)


def test_fusing_nothing_says_nothing() -> None:
    assert markers.fuse([]) == []


def test_the_decision_rule_has_three_outcomes() -> None:
    assert markers.decide(0.99999) == "accept"
    assert markers.decide(0.99) == "rescan"
    assert markers.decide(0.1) == "reject"


def test_the_decision_rule_refuses_thresholds_out_of_order() -> None:
    with pytest.raises(markers.MarkerError, match="out of order"):
        markers.decide(0.5, accept=0.5, reject=0.9)


def test_scanning_a_frame_resolves_the_sample_it_belongs_to() -> None:
    entries = bottles.registry.build_registry(bottles.registry.default_samples())
    table = {e.code: {"marker_id": e.marker_id, "sample_id": e.sample.sample_id}
             for e in entries[:20]}
    wanted = entries[3]
    result = markers.scan(frame_with(wanted.marker_id, copies=3), table)
    assert result.marker_id == wanted.marker_id
    assert result.record is not None
    assert result.record["sample_id"] == wanted.sample.sample_id
    assert result.decision in {"accept", "rescan", "reject"}


def test_scanning_an_empty_bench_returns_no_identity() -> None:
    bench = np.full((240, 240, 3), 150, np.uint8)
    result = markers.scan(bench, {})
    assert result.marker_id is None
    assert result.decision == "reject"
    assert result.record is None


def test_scanning_refuses_an_empty_image() -> None:
    with pytest.raises(markers.MarkerError, match="empty"):
        markers.scan(np.zeros((0, 0), np.uint8))


def test_sampling_refuses_a_colour_image_or_a_malformed_quad() -> None:
    with pytest.raises(markers.MarkerError, match="single-channel"):
        markers.sample_cells(np.zeros((8, 8, 3), np.uint8), np.zeros((4, 2)))
    with pytest.raises(markers.MarkerError, match="quad"):
        markers.sample_cells(np.zeros((8, 8), np.uint8), np.zeros((3, 2)))


def test_the_sampled_grid_takes_in_the_quiet_zone_and_the_border() -> None:
    image = marker_image(42)
    cells = markers.sample_cells(image, only_quad(image))
    assert cells.shape == (markers.GRID_CELLS, markers.GRID_CELLS)
    assert cells[0].mean() > 200, "the outer ring should be the white quiet zone"
    inner = cells[1:-1, 1:-1]
    assert inner[0].mean() < 60, "the ring inside it should be the black border"
