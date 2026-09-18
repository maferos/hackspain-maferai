"""Tests for the barcode reader, end to end from rendered label to sample."""

import cv2
import numpy as np
import pytest

from labvision import ean13, reader, registry

CODE = "4006381333931"


@pytest.fixture(scope="module")
def detector() -> "cv2.barcode.BarcodeDetector":
    """One detector shared across the module; construction is not free."""
    return reader.make_detector()


def _codes(image: np.ndarray, detector: object) -> list[str]:
    return [d.code for d in reader.decode_image(image, detector)]


def test_decode_image_reads_a_rendered_tag(detector: object) -> None:
    tag = ean13.render_tag(CODE, "LIMONENE", "SMP-0001")
    assert _codes(tag, detector) == [CODE]


def test_decode_image_returns_a_quad(detector: object) -> None:
    tag = ean13.render_tag(CODE, "LIMONENE", "SMP-0001")
    detection = reader.decode_image(tag, detector)[0]
    assert detection.corners is not None
    assert detection.corners.shape == (4, 2)


def test_decode_image_reads_a_tight_crop_that_fills_the_frame(
    detector: object,
) -> None:
    """OpenCV alone misses this; it is the case the fallback reader exists for."""
    symbol = ean13.render_symbol(CODE, module_px=4)
    assert _codes(symbol, detector) == [CODE]


def test_decode_image_reads_an_upside_down_label(detector: object) -> None:
    tag = ean13.render_tag(CODE, "LIMONENE", "SMP-0001")
    assert _codes(cv2.rotate(tag, cv2.ROTATE_180), detector) == [CODE]


@pytest.mark.parametrize("angle", [5, 15, 30, 45, 90])
def test_decode_image_tolerates_rotation(angle: int, detector: object) -> None:
    tag = ean13.render_tag(CODE, "LIMONENE", "SMP-0001", module_px=5)
    height, width = tag.shape[:2]
    side = int(1.6 * max(height, width))
    canvas = np.full((side, side, 3), 255, np.uint8)
    y0, x0 = (side - height) // 2, (side - width) // 2
    canvas[y0:y0 + height, x0:x0 + width] = tag

    matrix = cv2.getRotationMatrix2D((side / 2, side / 2), angle, 1)
    rotated = cv2.warpAffine(canvas, matrix, (side, side), borderValue=(255,) * 3)
    assert _codes(rotated, detector) == [CODE]


def test_decode_image_tolerates_noise_and_blur(detector: object) -> None:
    tag = ean13.render_tag(CODE, "LIMONENE", "SMP-0001")
    rng = np.random.default_rng(0)
    noisy = np.clip(
        tag.astype(np.int16) + rng.normal(0, 12, tag.shape), 0, 255,
    ).astype(np.uint8)
    assert _codes(noisy, detector) == [CODE]
    assert _codes(cv2.GaussianBlur(tag, (3, 3), 0), detector) == [CODE]


def test_decode_image_reads_several_labels_in_one_frame(detector: object) -> None:
    entries = registry.build_registry(registry.default_samples(4))
    scene = np.full((900, 1400, 3), 235, np.uint8)
    spots = [(60, 60), (760, 60), (60, 520), (760, 520)]
    for entry, (x, y) in zip(entries, spots, strict=True):
        tag = ean13.render_tag(
            entry.code, entry.sample.material, entry.sample.sample_id, module_px=5,
        )
        scene[y:y + tag.shape[0], x:x + tag.shape[1]] = tag
    assert sorted(_codes(scene, detector)) == sorted(e.code for e in entries)


def test_decode_image_finds_nothing_in_a_blank_frame(detector: object) -> None:
    assert reader.decode_image(np.full((400, 600, 3), 255, np.uint8), detector) == []


@pytest.mark.parametrize(
    "image",
    [np.zeros((0, 0, 3), np.uint8), np.zeros((4, 4, 4, 3), np.uint8)],
)
def test_decode_image_rejects_a_bad_image(image: np.ndarray) -> None:
    with pytest.raises(ValueError):
        reader.decode_image(image)


def test_decode_scanline_reads_a_bare_symbol() -> None:
    symbol = ean13.render_symbol(CODE, module_px=4)
    gray = cv2.cvtColor(symbol, cv2.COLOR_BGR2GRAY)
    assert reader.decode_scanline(gray) == CODE


@pytest.mark.parametrize("module_px", [2, 3, 4, 6, 9])
def test_decode_scanline_works_across_module_widths(module_px: int) -> None:
    symbol = ean13.render_symbol(CODE, module_px=module_px)
    gray = cv2.cvtColor(symbol, cv2.COLOR_BGR2GRAY)
    assert reader.decode_scanline(gray) == CODE


@pytest.mark.parametrize("scale", [0.55, 0.8, 1.3, 2.1])
def test_decode_scanline_survives_rescaling(scale: float) -> None:
    """Check the module width is refined rather than taken from the guard

    Rescaling puts the module width off a whole number of pixels, and a
    guard-only estimate drifts far enough across 95 modules to lose the right
    half of the symbol.
    """
    symbol = ean13.render_symbol(CODE, module_px=6)
    resized = cv2.resize(symbol, None, fx=scale, fy=scale,
                         interpolation=cv2.INTER_AREA)
    assert reader.decode_scanline(cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)) == CODE


def test_decode_scanline_reads_a_mirrored_symbol() -> None:
    symbol = ean13.render_symbol(CODE, module_px=4, show_text=False)
    gray = cv2.cvtColor(symbol, cv2.COLOR_BGR2GRAY)
    assert reader.decode_scanline(gray[:, ::-1]) == CODE


def test_decode_scanline_returns_none_on_a_blank_image() -> None:
    assert reader.decode_scanline(np.full((80, 400), 255, np.uint8)) is None


def test_decode_scanline_rejects_a_colour_image() -> None:
    with pytest.raises(ValueError):
        reader.decode_scanline(np.zeros((10, 10, 3), np.uint8))


def test_locate_candidates_finds_the_symbol() -> None:
    tag = ean13.render_tag(CODE, "LIMONENE", "SMP-0001", module_px=5)
    scene = np.full((700, 900, 3), 235, np.uint8)
    scene[100:100 + tag.shape[0], 100:100 + tag.shape[1]] = tag
    quads = reader.locate_candidates(cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY))
    assert quads
    assert all(q.shape == (4, 2) for q in quads)


def test_locate_candidates_rejects_a_colour_image() -> None:
    with pytest.raises(ValueError):
        reader.locate_candidates(np.zeros((10, 10, 3), np.uint8))


def test_rectified_quad_decodes() -> None:
    tag = ean13.render_tag(CODE, "LIMONENE", "SMP-0001", module_px=5)
    scene = np.full((700, 900, 3), 235, np.uint8)
    scene[100:100 + tag.shape[0], 100:100 + tag.shape[1]] = tag
    gray = cv2.cvtColor(scene, cv2.COLOR_BGR2GRAY)
    assert any(
        reader.decode_scanline(reader.rectify(gray, q)) == CODE
        for q in reader.locate_candidates(gray)
    )


def test_resolve_pairs_codes_with_records() -> None:
    entries = registry.build_registry(registry.default_samples(2))
    table = registry.to_table(entries)["entries"]
    detections = [reader.Detection(entries[0].code, None, "opencv")]
    (detection, record), = reader.resolve(detections, table)
    assert detection.code == entries[0].code
    assert record["sample_id"] == entries[0].sample.sample_id


def test_resolve_reports_an_unknown_code_as_none() -> None:
    (_, record), = reader.resolve([reader.Detection(CODE, None, "opencv")], {})
    assert record is None


def test_every_generated_label_decodes_to_its_own_sample(
    tmp_path, detector: object,
) -> None:
    """The whole loop: hash a record, print it, read it back, look it up."""
    entries = registry.build_registry(registry.default_samples(25))
    table = registry.to_table(entries)["entries"]
    paths = registry.write_label_images(entries, tmp_path)

    for entry, path in zip(entries, paths, strict=True):
        detections = reader.decode_image(cv2.imread(str(path)), detector)
        assert len(detections) == 1, f"{path.name} gave {len(detections)} hits"
        (_, record), = reader.resolve(detections, table)
        assert record is not None, f"{path.name} decoded outside the table"
        assert record["sample_id"] == entry.sample.sample_id
        assert record["material"] == entry.sample.material
