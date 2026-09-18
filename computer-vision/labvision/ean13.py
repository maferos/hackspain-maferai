"""EAN-13 symbology: check digit, module encoding, decoding and rendering.

The encoder is written out here rather than taken from ``python-barcode`` for two
reasons. The pipeline then needs nothing beyond numpy and OpenCV, and rendering
takes an explicit *pixels per module* argument instead of a target image width.
That second point is the important one: EAN-13 is always 95 modules wide and
OpenCV needs roughly two pixels per module to decode, so a caller sizing a label
has to be able to pin the module width exactly rather than back it out of a
width in pixels.

Module strings here are ``"0"``/``"1"`` text where ``1`` is a dark bar, ordered
left to right, and always 95 characters long.
"""

import cv2
import numpy as np

# Left-hand odd parity ("L"), indexed by digit.
_L_CODES: tuple[str, ...] = (
    "0001101", "0011001", "0010011", "0111101", "0100011",
    "0110001", "0101111", "0111011", "0110111", "0001011",
)

# Left-hand even parity ("G"), indexed by digit.
_G_CODES: tuple[str, ...] = (
    "0100111", "0110011", "0011011", "0100001", "0011101",
    "0111001", "0000101", "0010001", "0001001", "0010111",
)

# Right-hand ("R"), indexed by digit. The bitwise complement of _L_CODES.
_R_CODES: tuple[str, ...] = (
    "1110010", "1100110", "1101100", "1000010", "1011100",
    "1001110", "1010000", "1000100", "1001000", "1110100",
)

# Parity of the six left-hand digits, selected by the first digit.
# "0" means encode with _L_CODES, "1" means encode with _G_CODES.
_PARITY: tuple[str, ...] = (
    "000000", "001011", "001101", "001110", "010011",
    "011001", "011100", "010101", "010110", "011010",
)

_START_GUARD = "101"
_CENTRE_GUARD = "01010"
_END_GUARD = "101"

MODULES_PER_SYMBOL = 95
"""Total module count of an EAN-13 symbol, excluding quiet zones."""

MIN_MODULE_PX = 2
"""Pixels per module below which OpenCV stops decoding reliably."""

_FONT = cv2.FONT_HERSHEY_SIMPLEX
_FONT_CAP_PX_AT_SCALE_1 = 22.0


class Ean13Error(ValueError):
    """Raised when a code is not a well-formed EAN-13."""


def check_digit(payload: str) -> int:
    """Compute the EAN-13 check digit for a 12-digit payload

    Digits are weighted 1 and 3 alternately from the left, and the check digit
    is whatever brings the weighted sum up to the next multiple of ten.

    Args:
        payload: Exactly 12 decimal digits, without the check digit.

    Returns:
        The check digit, 0-9.

    Raises:
        Ean13Error: If payload is not exactly 12 decimal digits.

    Example:
        >>> check_digit("400638133393")
        1
    """
    if len(payload) != 12 or not payload.isdigit():
        raise Ean13Error(f"payload must be 12 digits, got {payload!r}")
    weighted = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(payload))
    return (10 - weighted % 10) % 10


def full_code(payload: str) -> str:
    """Append the check digit to a 12-digit payload

    Args:
        payload: Exactly 12 decimal digits.

    Returns:
        The 13-digit EAN-13 code.

    Raises:
        Ean13Error: If payload is not exactly 12 decimal digits.

    Example:
        >>> full_code("400638133393")
        '4006381333931'
    """
    return payload + str(check_digit(payload))


def is_valid(code: str) -> bool:
    """Report whether a string is a 13-digit code with a correct check digit

    Args:
        code: The candidate code.

    Returns:
        True if the code is well formed and its check digit matches.
    """
    if len(code) != 13 or not code.isdigit():
        return False
    return check_digit(code[:12]) == int(code[12])


def encode_modules(code: str) -> str:
    """Encode a 13-digit code as its 95-module bar pattern

    Args:
        code: A 13-digit EAN-13 code, check digit included.

    Returns:
        A 95-character string of "0" (space) and "1" (bar).

    Raises:
        Ean13Error: If the code is malformed or its check digit is wrong.

    Example:
        >>> encode_modules("4006381333931")[:3]
        '101'
    """
    if not is_valid(code):
        raise Ean13Error(f"not a valid EAN-13: {code!r}")
    parity = _PARITY[int(code[0])]
    left = "".join(
        (_G_CODES if parity[i] == "1" else _L_CODES)[int(d)]
        for i, d in enumerate(code[1:7])
    )
    right = "".join(_R_CODES[int(d)] for d in code[7:13])
    return _START_GUARD + left + _CENTRE_GUARD + right + _END_GUARD


def decode_modules(modules: str) -> str:
    """Decode a 95-module bar pattern back to its 13-digit code

    Guards are checked first, then the six left digits are matched against the
    L and G tables. Their parity pattern recovers the first digit, which is
    never encoded as bars of its own.

    Args:
        modules: A 95-character string of "0" and "1".

    Returns:
        The 13-digit EAN-13 code.

    Raises:
        Ean13Error: If the length, guards, digit patterns, parity pattern or
            check digit do not decode.

    Example:
        >>> decode_modules(encode_modules("4006381333931"))
        '4006381333931'
    """
    if len(modules) != MODULES_PER_SYMBOL or set(modules) - {"0", "1"}:
        raise Ean13Error(f"expected {MODULES_PER_SYMBOL} modules of 0/1")
    if (
        modules[0:3] != _START_GUARD
        or modules[45:50] != _CENTRE_GUARD
        or modules[92:95] != _END_GUARD
    ):
        raise Ean13Error("guard patterns do not match")

    parity = ""
    left_digits = ""
    for i in range(6):
        chunk = modules[3 + 7 * i: 10 + 7 * i]
        if chunk in _L_CODES:
            parity += "0"
            left_digits += str(_L_CODES.index(chunk))
        elif chunk in _G_CODES:
            parity += "1"
            left_digits += str(_G_CODES.index(chunk))
        else:
            raise Ean13Error(f"left digit {i} matches neither L nor G: {chunk}")

    if parity not in _PARITY:
        raise Ean13Error(f"parity pattern {parity} maps to no first digit")

    right_digits = ""
    for i in range(6):
        chunk = modules[50 + 7 * i: 57 + 7 * i]
        if chunk not in _R_CODES:
            raise Ean13Error(f"right digit {i} does not match R: {chunk}")
        right_digits += str(_R_CODES.index(chunk))

    code = f"{_PARITY.index(parity)}{left_digits}{right_digits}"
    if not is_valid(code):
        raise Ean13Error(f"decoded {code} but its check digit is wrong")
    return code


def _scale_for_height(target_px: int) -> float:
    """Pick a cv2 font scale whose capitals are roughly target_px tall."""
    return max(0.3, target_px / _FONT_CAP_PX_AT_SCALE_1)


def _draw_centred(
    canvas: np.ndarray,
    text: str,
    centre_x: int,
    baseline_y: int,
    scale: float,
    thickness: int,
) -> None:
    """Draw text horizontally centred on centre_x, sitting on baseline_y."""
    (w, _), _ = cv2.getTextSize(text, _FONT, scale, thickness)
    cv2.putText(
        canvas,
        text,
        (int(centre_x - w / 2), baseline_y),
        _FONT,
        scale,
        (20, 20, 20),
        thickness,
        cv2.LINE_AA,
    )


def render_symbol(
    code: str,
    module_px: int = 4,
    bar_height_px: int | None = None,
    quiet_modules: int = 10,
    show_text: bool = True,
) -> np.ndarray:
    """Render an EAN-13 symbol with quiet zones and human-readable digits

    The image width is exactly ``(95 + 2 * quiet_modules) * module_px``, so the
    caller controls the module width to the pixel. Guard bars are drawn longer
    than the data bars, as the specification requires, and the human-readable
    line is laid out the conventional way: the first digit sits in the left
    quiet zone, the next six under the left half, the last six under the right.

    Args:
        code: A 13-digit EAN-13 code, check digit included.
        module_px: Pixels per module. Values below MIN_MODULE_PX render a symbol
            OpenCV is unlikely to decode. Defaults to 4.
        bar_height_px: Height of the data bars in pixels. Defaults to
            ``25 * module_px``, close to the printed aspect ratio.
        quiet_modules: Blank modules added either side. The specification asks
            for 11 left and 7 right; a symmetric 10 is used by default because
            these labels are cropped by a detector rather than printed on a
            carton. Defaults to 10.
        show_text: Whether to draw the human-readable digits. Defaults to True.

    Returns:
        A BGR uint8 image of the symbol on a white background.

    Raises:
        Ean13Error: If the code is malformed or its check digit is wrong.
        ValueError: If module_px or quiet_modules is negative.

    Example:
        >>> render_symbol("4006381333931", module_px=2).shape[1]
        230
    """
    if module_px < 1:
        raise ValueError(f"module_px must be >= 1, got {module_px}")
    if quiet_modules < 0:
        raise ValueError(f"quiet_modules must be >= 0, got {quiet_modules}")

    modules = encode_modules(code)
    bar_h = bar_height_px if bar_height_px is not None else 25 * module_px
    text_h = int(round(6 * module_px)) if show_text else 0
    guard_extra = text_h // 2 if show_text else 0
    pad_bottom = text_h // 3 if show_text else 0

    width = (MODULES_PER_SYMBOL + 2 * quiet_modules) * module_px
    height = bar_h + guard_extra + text_h + pad_bottom
    canvas = np.full((height, width, 3), 255, np.uint8)

    guard_spans = ((0, 3), (45, 50), (92, 95))
    for index, bit in enumerate(modules):
        if bit != "1":
            continue
        is_guard = any(lo <= index < hi for lo, hi in guard_spans)
        x0 = (quiet_modules + index) * module_px
        y1 = bar_h + (guard_extra if is_guard else 0)
        canvas[0:y1, x0:x0 + module_px] = 0

    if show_text:
        scale = _scale_for_height(text_h)
        thickness = max(1, round(module_px / 3))
        baseline = bar_h + guard_extra + text_h
        _draw_centred(
            canvas, code[0], (quiet_modules / 2) * module_px, baseline,
            scale, thickness,
        )
        _draw_centred(
            canvas, code[1:7], (quiet_modules + 24) * module_px, baseline,
            scale, thickness,
        )
        _draw_centred(
            canvas, code[7:13], (quiet_modules + 71) * module_px, baseline,
            scale, thickness,
        )
    return canvas


def render_tag(
    code: str,
    caption: str = "",
    subcaption: str = "",
    module_px: int = 4,
    border: bool = True,
) -> np.ndarray:
    """Render a printed label: an EAN-13 symbol above one or two caption lines

    Args:
        code: A 13-digit EAN-13 code, check digit included.
        caption: Primary caption, drawn in capitals under the symbol. Usually
            the material or sample name. Empty strings are skipped.
        subcaption: Secondary caption, drawn smaller under the primary one.
        module_px: Pixels per module passed through to render_symbol.
            Defaults to 4.
        border: Whether to draw a thin grey frame around the label.
            Defaults to True.

    Returns:
        A BGR uint8 image of the label on a white background.

    Raises:
        Ean13Error: If the code is malformed or its check digit is wrong.

    Example:
        >>> render_tag("4006381333931", "LIMONENE").ndim
        3
    """
    symbol = render_symbol(code, module_px=module_px)
    margin = 3 * module_px
    lines = [line for line in (caption, subcaption) if line]
    line_heights = [int(round(h * module_px)) for h in (6, 5)][: len(lines)]
    text_block = sum(h + margin for h in line_heights)

    width = symbol.shape[1] + 2 * margin
    height = symbol.shape[0] + 2 * margin + text_block
    canvas = np.full((height, width, 3), 250, np.uint8)
    canvas[margin:margin + symbol.shape[0], margin:margin + symbol.shape[1]] = symbol

    y = margin + symbol.shape[0]
    for line, line_h in zip(lines, line_heights, strict=True):
        y += margin + line_h
        _draw_centred(
            canvas, line.upper(), width / 2, y,
            _scale_for_height(line_h), max(1, round(module_px / 3)),
        )

    if border:
        cv2.rectangle(canvas, (0, 0), (width - 1, height - 1), (170, 170, 170), 2)
    return canvas
