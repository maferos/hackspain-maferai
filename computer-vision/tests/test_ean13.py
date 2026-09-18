"""Tests for the EAN-13 encoder, decoder and renderer."""

import importlib.util

import cv2
import numpy as np
import pytest

from labvision import ean13

# Real EAN-13 codes, used to pin the check-digit arithmetic against the
# published standard rather than against our own implementation.
KNOWN_CODES = (
    ("400638133393", 1),
    ("978014300723", 4),
    ("501234567890", 0),
)


@pytest.mark.parametrize(("payload", "expected"), KNOWN_CODES)
def test_check_digit_matches_published_codes(payload: str, expected: int) -> None:
    assert ean13.check_digit(payload) == expected


@pytest.mark.parametrize(("payload", "expected"), KNOWN_CODES)
def test_full_code_appends_check_digit(payload: str, expected: int) -> None:
    assert ean13.full_code(payload) == f"{payload}{expected}"


@pytest.mark.parametrize("payload", ["", "123", "40063813339", "40063813339x"])
def test_check_digit_rejects_malformed_payload(payload: str) -> None:
    with pytest.raises(ean13.Ean13Error):
        ean13.check_digit(payload)


def test_is_valid_rejects_a_wrong_check_digit() -> None:
    assert ean13.is_valid("4006381333931")
    assert not ean13.is_valid("4006381333932")
    assert not ean13.is_valid("400638133393")
    assert not ean13.is_valid("abcdefghijklm")


def test_encode_modules_has_the_right_shape_and_guards() -> None:
    modules = ean13.encode_modules("4006381333931")
    assert len(modules) == ean13.MODULES_PER_SYMBOL
    assert set(modules) <= {"0", "1"}
    assert modules[0:3] == "101"
    assert modules[45:50] == "01010"
    assert modules[92:95] == "101"


def test_encode_modules_rejects_an_invalid_code() -> None:
    with pytest.raises(ean13.Ean13Error):
        ean13.encode_modules("4006381333932")


def test_first_digit_is_carried_by_parity_not_by_bars() -> None:
    """The first digit is never drawn, so it must change only the L/G pattern."""
    a = ean13.encode_modules(ean13.full_code("000638133393"))
    b = ean13.encode_modules(ean13.full_code("500638133393"))
    assert a != b
    assert a[45:50] == b[45:50]


@pytest.mark.parametrize("first", range(10))
def test_module_roundtrip_over_every_parity_pattern(first: int) -> None:
    code = ean13.full_code(f"{first}00638133393")
    assert ean13.decode_modules(ean13.encode_modules(code)) == code


def test_module_roundtrip_over_many_codes() -> None:
    rng = np.random.default_rng(7)
    for _ in range(300):
        payload = "".join(str(d) for d in rng.integers(0, 10, 12))
        code = ean13.full_code(payload)
        assert ean13.decode_modules(ean13.encode_modules(code)) == code


@pytest.mark.parametrize(
    "modules",
    [
        "1" * 94,
        "0" * 95,
        "2" * 95,
        "1" * 95,
    ],
)
def test_decode_modules_rejects_junk(modules: str) -> None:
    with pytest.raises(ean13.Ean13Error):
        ean13.decode_modules(modules)


def test_decode_modules_rejects_a_corrupted_digit() -> None:
    modules = list(ean13.encode_modules("4006381333931"))
    modules[10] = "1" if modules[10] == "0" else "0"
    with pytest.raises(ean13.Ean13Error):
        ean13.decode_modules("".join(modules))


@pytest.mark.parametrize("module_px", [2, 3, 4, 8])
def test_render_symbol_width_is_exactly_module_px_times_modules(
    module_px: int,
) -> None:
    quiet = 10
    image = ean13.render_symbol("4006381333931", module_px=module_px,
                                quiet_modules=quiet)
    expected = (ean13.MODULES_PER_SYMBOL + 2 * quiet) * module_px
    assert image.shape[1] == expected
    assert image.dtype == np.uint8
    assert image.ndim == 3


def test_render_symbol_bars_land_on_module_boundaries() -> None:
    """The top row of the image must reproduce the module pattern exactly."""
    module_px, quiet = 4, 10
    code = "4006381333931"
    image = ean13.render_symbol(code, module_px=module_px, quiet_modules=quiet)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    top = gray[0]
    read = "".join(
        "1" if top[(quiet + i) * module_px + module_px // 2] < 128 else "0"
        for i in range(ean13.MODULES_PER_SYMBOL)
    )
    assert read == ean13.encode_modules(code)


def test_render_symbol_quiet_zones_are_blank() -> None:
    """Check the bars themselves put no ink in the quiet zones

    Text is disabled because the first digit is printed in the left quiet zone
    by design, which would otherwise mask the thing being asserted.
    """
    module_px, quiet = 4, 10
    image = ean13.render_symbol("4006381333931", module_px=module_px,
                                quiet_modules=quiet, show_text=False)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    assert (gray[:, : quiet * module_px] == 255).all()
    assert (gray[:, -quiet * module_px:] == 255).all()


@pytest.mark.parametrize(("module_px", "quiet"), [(0, 10), (-1, 10), (4, -1)])
def test_render_symbol_rejects_bad_geometry(module_px: int, quiet: int) -> None:
    with pytest.raises(ValueError):
        ean13.render_symbol("4006381333931", module_px=module_px,
                            quiet_modules=quiet)


def test_render_tag_is_larger_than_the_bare_symbol() -> None:
    code = "4006381333931"
    symbol = ean13.render_symbol(code)
    tag = ean13.render_tag(code, "LIMONENE", "SMP-0001")
    assert tag.shape[0] > symbol.shape[0]
    assert tag.shape[1] > symbol.shape[1]


def test_render_tag_without_captions_still_renders() -> None:
    assert ean13.render_tag("4006381333931").size > 0


# python-barcode is an optional dev dependency used purely as an independent
# oracle: it encodes EAN-13 but cannot decode, so it can validate our tables
# without being able to replace them. Install it with
#   pip install python-barcode --index-url https://pypi.org/simple
# The skip is per-test rather than module-level, so the rest of this file still
# runs where it is absent.
needs_oracle = pytest.mark.skipif(
    importlib.util.find_spec("barcode") is None,
    reason="python-barcode not installed",
)


@needs_oracle
def test_check_digit_agrees_with_python_barcode() -> None:
    import barcode

    rng = np.random.default_rng(1)
    for _ in range(500):
        payload = "".join(str(d) for d in rng.integers(0, 10, 12))
        assert ean13.full_code(payload) == barcode.get("ean13", payload).get_fullcode()


@needs_oracle
def test_module_pattern_agrees_with_python_barcode() -> None:
    """Pin our hand-written L/G/R tables against an independent implementation"""
    import barcode

    rng = np.random.default_rng(2)
    for _ in range(500):
        payload = "".join(str(d) for d in rng.integers(0, 10, 12))
        theirs = "".join(barcode.get("ean13", payload).build()[0])
        assert ean13.encode_modules(ean13.full_code(payload)) == theirs
