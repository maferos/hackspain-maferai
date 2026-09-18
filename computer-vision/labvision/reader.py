"""Barcode reader: find EAN-13 codes in an image and resolve them to samples.

Two decoders sit behind one entry point, :func:`decode_image`, whose results
are merged rather than raced.

OpenCV's ``cv2.barcode.BarcodeDetector`` is the first. It has two awkward
habits. It will not find a barcode that fills the frame, since it searches a
fixed set of scales relative to the image, and on this build the setters that
used to widen those scales (``setDetectorScales``, ``setGradientThreshold``)
are no longer exposed, leaving image conditioning as the only lever --- hence
the ladder of white padding and upscaling. It also returns an empty points
vector even on a successful decode, so it yields no corner coordinates.

:func:`locate_and_decode` is the second. It finds candidate symbols by closing
the thresholded image with a wide, short horizontal kernel, rectifies each one
and reads it with :func:`decode_scanline`, a pure numpy reader working from
:mod:`labvision.ean13`'s own tables. This is the path that supplies quads, and
the path that copes with a barcode filling the frame.

The two are unioned because neither is reliably a superset of the other: a
padding rung that decodes one label in a frame holding four would otherwise
mask the three the localiser had already read.
"""

import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from labvision import ean13
from labvision.registry import RegistryError, load_table

logger = logging.getLogger(__name__)

PAD_LADDER: tuple[float, ...] = (0.0, 0.25, 0.6, 1.2)
"""White border to add, as a fraction of the shorter side, tried in order."""

UPSCALE_LADDER: tuple[float, ...] = (1.0, 2.0)
"""Image scale factors tried at each padding step."""

SCANLINE_ROWS = 48
"""How many horizontal scanlines the fallback reader samples."""

CLOSE_KERNELS: tuple[tuple[int, int], ...] = ((21, 3), (41, 5), (11, 3))
"""Horizontal closing kernels used to merge bars into one blob, tried in order."""

QUIET_ZONE_MARGIN = 1.3
"""Factor the located bar blob is widened by, to take in the quiet zones."""

RECTIFIED_MODULE_PX = 4
"""Pixels per module a located symbol is rectified to before scanline reading."""

_ASPECT_RANGE = (1.3, 18.0)
"""Long-side / short-side range a candidate blob must fall in to be a symbol."""

_GUARD_TOLERANCE = 0.45
"""Allowed relative spread between the three start-guard run lengths."""


@dataclass(frozen=True)
class Detection:
    """One decoded barcode.

    Attributes:
        code: The 13-digit EAN-13 that was read.
        corners: The symbol's four corners in the input image's pixel
            coordinates as a (4, 2) float array, long edge first. None when the
            localiser did not find this code and OpenCV, which read it, supplied
            no quad of its own.
        decoder: Which reader produced the code, ``"opencv"`` or ``"scanline"``.
            Corners may come from the localiser either way.
    """

    code: str
    corners: np.ndarray | None
    decoder: str


def make_detector() -> "cv2.barcode.BarcodeDetector":
    """Build the OpenCV barcode detector

    Kept as a function so callers share one construction site if a future
    OpenCV build re-exposes tuning parameters.

    Returns:
        A detector ready for detectAndDecodeMulti.
    """
    return cv2.barcode.BarcodeDetector()


def _as_gray(image: np.ndarray) -> np.ndarray:
    """Return a single-channel view of a BGR or already-grey image."""
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def _decode_once(
    image: np.ndarray,
    detector: "cv2.barcode.BarcodeDetector",
) -> list[tuple[str, np.ndarray]]:
    """Run the OpenCV detector once and return valid EAN-13 hits with quads."""
    ok, infos, _types, points = detector.detectAndDecodeMulti(image)
    if not ok or infos is None:
        return []
    # points may come back empty even when infos is populated, so it is indexed
    # defensively rather than assumed to be parallel to infos.
    hits = []
    for i, info in enumerate(infos):
        if info and ean13.is_valid(info):
            has_quad = points is not None and i < len(points)
            quad = np.asarray(points[i], np.float32) if has_quad else None
            hits.append((info, quad))
    return hits


def decode_image(
    image: np.ndarray,
    detector: "cv2.barcode.BarcodeDetector | None" = None,
    allow_fallback: bool = True,
) -> list[Detection]:
    """Find and decode every EAN-13 barcode in an image

    Both readers run and their results are merged. The localiser contributes
    corner coordinates, which OpenCV does not supply. OpenCV contributes its
    own decodes, tried on the image as given and then with progressively more
    white padding and optional upscaling, because it searches scales relative
    to the frame and so misses a barcode that fills it.

    The two are unioned rather than raced. A padding rung that decodes one
    label in a frame holding four would otherwise mask the three the localiser
    had already read.

    Args:
        image: BGR or grayscale image.
        detector: Detector to reuse across calls. A fresh one is built when
            omitted.
        allow_fallback: Whether to run the localiser and scanline reader at
            all. With it False only OpenCV is used, and no corners are
            returned. Defaults to True.

    Returns:
        One detection per distinct code found, possibly empty.

    Raises:
        ValueError: If image is empty or not 2- or 3-dimensional.

    Example:
        >>> img = ean13.render_tag("4006381333931", "LIMONENE")
        >>> [d.code for d in decode_image(img)]
        ['4006381333931']
    """
    if image is None or image.size == 0:
        raise ValueError("image is empty")
    if image.ndim not in (2, 3):
        raise ValueError(f"expected a 2D or 3D image, got {image.ndim}D")

    det = detector if detector is not None else make_detector()
    gray = _as_gray(image)
    short_side = min(image.shape[:2])

    # The localiser is the only path that yields corner coordinates, because
    # detectAndDecodeMulti returns an empty points vector on the OpenCV builds
    # seen so far even when it decodes successfully.
    located: list[tuple[str, np.ndarray | None]] = []
    if allow_fallback:
        located = list(locate_and_decode(gray))
        if not located:
            whole = decode_scanline(gray)
            if whole is not None:
                located = [(whole, None)]

    opencv_hits: dict[str, np.ndarray | None] = {}
    for pad_fraction in PAD_LADDER:
        pad = int(round(short_side * pad_fraction))
        padded = cv2.copyMakeBorder(
            image, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255),
        ) if pad else image

        for scale in UPSCALE_LADDER:
            candidate = padded if scale == 1.0 else cv2.resize(
                padded, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC,
            )
            hits = _decode_once(candidate, det)
            if not hits:
                continue
            logger.debug(
                "opencv decoded %d code(s) at pad=%.2f scale=%.1f", len(hits),
                pad_fraction, scale,
            )
            for code, quad in hits:
                if code in opencv_hits:
                    continue
                corners = None
                if quad is not None and quad.size:
                    corners = quad.reshape(-1, 2) / scale - pad
                opencv_hits[code] = corners
            break
        if opencv_hits:
            break

    quads = dict(located)
    out: list[Detection] = []
    for code, corners in opencv_hits.items():
        out.append(Detection(code, quads.get(code, corners), "opencv"))
    for code, corners in located:
        if code not in opencv_hits:
            out.append(Detection(code, corners, "scanline"))
    return out


def _runs(row: np.ndarray) -> list[tuple[bool, int, int]]:
    """Run-length encode a boolean row as (is_dark, start_x, length) tuples."""
    changes = np.flatnonzero(np.diff(row)) + 1
    bounds = np.concatenate(([0], changes, [row.size]))
    return [
        (bool(row[start]), int(start), int(end - start))
        for start, end in zip(bounds[:-1], bounds[1:], strict=True)
    ]


def _sample_modules(row: np.ndarray, start_x: int, module_w: float) -> str | None:
    """Sample 95 module centres from start_x, or None if they run off the row."""
    centres = start_x + (np.arange(ean13.MODULES_PER_SYMBOL) + 0.5) * module_w
    if centres[-1] >= row.size:
        return None
    return "".join("1" if row[int(c)] else "0" for c in centres)


def _module_widths(
    runs: list[tuple[bool, int, int]],
    start_x: int,
    guard_w: float,
) -> list[float]:
    """Propose module widths for a symbol starting at start_x, best first.

    The three start-guard runs give a first estimate, but it is quantised to
    whole pixels and so drifts by tens of pixels across 95 modules once an image
    has been rescaled. Spanning from the start guard to a candidate end guard
    gives a far better estimate, and a narrow sweep covers what is left.
    """
    proposals = [
        (end - start_x) / ean13.MODULES_PER_SYMBOL
        for dark, start, length in runs
        if dark and (end := start + length) > start_x
    ]
    proposals = [w for w in proposals if 0.75 * guard_w <= w <= 1.25 * guard_w]
    proposals.append(guard_w)
    proposals.extend(guard_w * (1 + k * 0.01) for k in range(-12, 13))

    unique: list[float] = []
    for width in proposals:
        if width >= 1.0 and not any(abs(width - u) < 0.01 for u in unique):
            unique.append(width)
    return unique


def _read_row(row: np.ndarray) -> str | None:
    """Try to decode one thresholded scanline, left to right.

    Every dark run is tried as the start guard. The guard is three runs of one
    module each, which rejects most false starts and bounds the module width,
    and each proposed width is sampled and handed to
    :func:`labvision.ean13.decode_modules`.
    """
    runs = _runs(row)
    for i in range(len(runs) - 2):
        dark, start_x, _ = runs[i]
        if not dark:
            continue
        widths = [runs[i + k][2] for k in range(3)]
        guard_w = sum(widths) / 3.0
        if guard_w < 1.0:
            continue
        if max(abs(w - guard_w) for w in widths) > _GUARD_TOLERANCE * guard_w:
            continue

        for module_w in _module_widths(runs, start_x, guard_w):
            bits = _sample_modules(row, start_x, module_w)
            if bits is None:
                continue
            try:
                return ean13.decode_modules(bits)
            except ean13.Ean13Error:
                continue
    return None


def decode_scanline(gray: np.ndarray) -> str | None:
    """Decode a roughly rectified barcode crop without OpenCV's detector

    The crop is thresholded with Otsu, then horizontal scanlines are read one by
    one until one decodes. Each line is also read right-to-left, so a label
    photographed upside down still resolves. Lines that cross the caption text
    rather than the bars simply fail to decode and are skipped.

    Args:
        gray: Single-channel image of a barcode, approximately axis-aligned.

    Returns:
        The 13-digit code, or None if no scanline decoded.

    Raises:
        ValueError: If gray is not a single-channel image.

    Example:
        >>> sym = ean13.render_symbol("4006381333931")
        >>> decode_scanline(cv2.cvtColor(sym, cv2.COLOR_BGR2GRAY))
        '4006381333931'
    """
    if gray.ndim != 2:
        raise ValueError(f"expected a single-channel image, got {gray.ndim}D")
    _, binary = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    dark = binary.astype(bool)

    height = dark.shape[0]
    ys = np.unique(np.linspace(0, height - 1, min(SCANLINE_ROWS, height)).astype(int))
    for y in ys:
        row = dark[y]
        if not row.any():
            continue
        for candidate in (row, row[::-1]):
            code = _read_row(candidate)
            if code is not None:
                return code
    return None


def _long_edge_first(box: np.ndarray) -> np.ndarray:
    """Rotate a 4-point box so its first edge is the long one."""
    edges = [np.linalg.norm(box[(i + 1) % 4] - box[i]) for i in range(4)]
    start = int(np.argmax(edges[:2]))
    return np.roll(box, -start, axis=0)


def locate_candidates(gray: np.ndarray) -> list[np.ndarray]:
    """Find quads that plausibly bound a barcode symbol

    A barcode is a dense run of parallel bars, so closing the thresholded image
    with a wide, short horizontal kernel melts the bars into a single solid
    blob while leaving text and background largely alone. The blobs are then
    filtered by aspect ratio and area. Several kernel widths are tried because
    the right one depends on the module width, which is not known in advance.

    Args:
        gray: Single-channel image.

    Returns:
        Candidate quads as (4, 2) float32 arrays with the long edge first,
        ordered largest area first. Possibly empty.

    Raises:
        ValueError: If gray is not a single-channel image.
    """
    if gray.ndim != 2:
        raise ValueError(f"expected a single-channel image, got {gray.ndim}D")
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU,
    )
    min_area = 0.0004 * gray.size

    found: list[tuple[float, np.ndarray]] = []
    for kernel_size in CLOSE_KERNELS:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
        closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(
            closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,
        )
        for contour in contours:
            (cx, cy), (w, h), angle = cv2.minAreaRect(contour)
            if w < 1 or h < 1 or w * h < min_area:
                continue
            long_side, short_side = max(w, h), min(w, h)
            if not _ASPECT_RANGE[0] <= long_side / short_side <= _ASPECT_RANGE[1]:
                continue
            grown = (w * QUIET_ZONE_MARGIN, h) if w >= h else (w, h * QUIET_ZONE_MARGIN)
            box = cv2.boxPoints(((cx, cy), grown, angle)).astype(np.float32)
            found.append((w * h, _long_edge_first(box)))

    found.sort(key=lambda item: -item[0])
    kept: list[np.ndarray] = []
    for _, box in found:
        centre = box.mean(axis=0)
        if any(np.linalg.norm(centre - k.mean(axis=0)) < 20 for k in kept):
            continue
        kept.append(box)
    return kept


def rectify(gray: np.ndarray, quad: np.ndarray) -> np.ndarray:
    """Warp a located quad to an axis-aligned, canonically sized crop

    Args:
        gray: Single-channel source image.
        quad: A (4, 2) quad with its long edge first, as returned by
            locate_candidates.

    Returns:
        A single-channel crop sized for the scanline reader.
    """
    width = (ean13.MODULES_PER_SYMBOL + 20) * RECTIFIED_MODULE_PX
    height = 30 * RECTIFIED_MODULE_PX
    dst = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        np.float32,
    )
    matrix = cv2.getPerspectiveTransform(quad.astype(np.float32), dst)
    return cv2.warpPerspective(
        gray, matrix, (width, height), flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_CONSTANT, borderValue=255,
    )


def locate_and_decode(gray: np.ndarray) -> list[tuple[str, np.ndarray]]:
    """Locate barcode symbols, rectify each and read it with the scanline reader

    This is the path that yields corner coordinates, since OpenCV's detector
    does not return usable quads on every build.

    Args:
        gray: Single-channel image.

    Returns:
        One (code, quad) pair per distinct code read, quads in the input
        image's pixel coordinates.
    """
    results: list[tuple[str, np.ndarray]] = []
    seen: set[str] = set()
    for quad in locate_candidates(gray):
        crop = rectify(gray, quad)
        code = decode_scanline(crop)
        if code is None:
            # The long edge may have been picked the wrong way round.
            code = decode_scanline(cv2.rotate(crop, cv2.ROTATE_180))
        if code is not None and code not in seen:
            seen.add(code)
            results.append((code, quad))
    return results


def resolve(
    detections: list[Detection],
    table: dict[str, dict[str, object]],
) -> list[tuple[Detection, dict[str, object] | None]]:
    """Pair each detection with its lookup-table row

    Args:
        detections: Codes read from an image.
        table: Barcode-keyed entries, as returned by
            :func:`labvision.registry.load_table`.

    Returns:
        One (detection, record) pair per detection. The record is None for a
        code that decoded cleanly but is not in the table.

    Example:
        >>> resolve([], {})
        []
    """
    return [(d, table.get(d.code)) for d in detections]


def read_file(
    path: Path,
    table: dict[str, dict[str, object]] | None = None,
) -> list[tuple[Detection, dict[str, object] | None]]:
    """Decode every barcode in an image file and resolve it

    Args:
        path: Image file to read.
        table: Lookup table to resolve against. Records come back None when
            omitted.

    Returns:
        One (detection, record) pair per barcode found.

    Raises:
        RegistryError: If the image cannot be read.
    """
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise RegistryError(f"could not read image: {path}")
    return resolve(decode_image(image), table or {})


def main() -> None:
    """Read barcodes from image files and print what they resolve to."""
    parser = argparse.ArgumentParser(
        description="Decode EAN-13 barcodes and resolve them to samples.",
    )
    parser.add_argument("images", type=Path, nargs="+", help="Image files to read.")
    parser.add_argument(
        "--table", type=Path, default=Path("barcodes/lookup_table.json"),
        help="Lookup table JSON (default: barcodes/lookup_table.json).",
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit JSON instead of a text report.",
    )
    parser.add_argument("--verbose", action="store_true", help="Log decoder detail.")
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(message)s",
    )

    try:
        table = load_table(args.table)
    except RegistryError as e:
        logger.warning("%s; codes will be reported unresolved", e)
        table = {}

    report = []
    for path in args.images:
        for detection, record in read_file(path, table):
            report.append({
                "image": str(path),
                "code": detection.code,
                "decoder": detection.decoder,
                "sample": record,
            })

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    if not report:
        print("no barcodes decoded")
        return
    for row in report:
        sample = row["sample"]
        if sample is None:
            print(f"{row['code']}  [{row['decoder']}]  not in lookup table")
        else:
            print(
                f"{row['code']}  [{row['decoder']}]  {sample['sample_id']}  "
                f"{sample['material']:<20} {sample['container_ml']:>5g} ml  "
                f"{sample['phase']:<7} lot {sample['lot']}"
            )


if __name__ == "__main__":
    main()
