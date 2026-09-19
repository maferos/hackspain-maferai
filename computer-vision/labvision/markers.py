"""ArUco ring reader that says how sure it is which sample it just read.

``cv2.aruco`` returns an id and nothing else: the per-cell grey levels it
computed on the way are thrown away, so a read that lands on the wrong valid
codeword is indistinguishable from a right one. That is the dangerous failure
here, because every id resolves through ``lookup_table.json`` to a real sample
and the robot would chain the wrong compound to the scanned pot.

This module decodes the same markers with the soft information kept, and
returns a posterior instead of an id. Two properties of the problem make that
exact rather than approximate:

* The candidate set is tiny and fully known --- 250 dictionary ids, of which
  only the registry's rows are possible --- so the posterior is computed by
  **enumeration**, with no learned model.
* The decoder is invertible: a hypothesised id has one known bit pattern, so
  ``P(image | id)`` is read straight off the cell measurements.

Three things are scored, in order:

:func:`read_quad`
    One candidate quad. Each of the 16 data cells contributes a
    log-likelihood ratio proportional to how far its grey level sits from the
    black/white references taken from the marker's own border and quiet zone.
    An ambiguous grey cell therefore contributes almost nothing, where hard
    thresholding would have contributed a confident wrong bit.

:func:`read_markers`
    Every candidate quad in a frame, including the ones OpenCV *rejected*.
    Rejection means the bits matched no codeword within its correction budget,
    which on the default settings is zero bits --- those quads still carry
    evidence, and they are where the soft decoding earns its keep.

:func:`fuse`
    The eight copies of the marker round one bottle, whose log-likelihoods add.
    Their disagreement is itself the alarm. The copies are only approximately
    independent --- they share pose, blur and lighting error, which does not
    average out --- so the sum is tempered by :data:`TEMPER`, which is a
    calibration knob and not a constant of nature.

Nothing here is calibrated yet. ``probability`` is a posterior under the noise
model below, not a frequency measured against ground truth; see
``docs/READ_CONFIDENCE.md`` for what calibration has to establish before these
numbers can be used to gate a decision.
"""

import logging
from dataclasses import dataclass
from functools import lru_cache

import cv2
import numpy as np

from labvision.bottles import (
    ARUCO_DICTIONARY,
    ARUCO_MARKER_MODULES,
    ARUCO_QUIET_MODULES,
)

logger = logging.getLogger(__name__)

DATA_CELLS = ARUCO_MARKER_MODULES - 2
"""Data cells along one side of a marker, inside its black border."""

GRID_CELLS = ARUCO_MARKER_MODULES + 2 * ARUCO_QUIET_MODULES
"""Cells a side in the sampled grid: quiet zone, border, then the data."""

RECTIFIED_CELL_PX = 8
"""Pixels per cell a candidate quad is rectified to before sampling."""

CELL_INSET = 0.3
"""Fraction of each cell ignored at its edge, to survive misregistration."""

_DATA_SLICE = slice(ARUCO_QUIET_MODULES + 1, ARUCO_QUIET_MODULES + 1 + DATA_CELLS)
"""Where the data cells sit in the sampled grid, past the quiet zone and border."""

NOISE_FLOOR = 0.25
"""Smallest per-cell noise the model will believe, in units of contrast.

Two jobs. Without a floor a clean synthetic render reports probability 1.0,
which is false: it only means the image matched the model perfectly, not that
no other sample could have produced it.

The size of the floor then decides whether the decoding is soft at all. The
noise sets the slope of the log-likelihood ratio, so a small floor makes the
ratio so steep that every cell saturates at the bound below and a grey cell
counts for as much as a white one --- which is hard thresholding again, wearing
a posterior. At a quarter of contrast, cells past about three quarters of the
way to white are taken as certain and everything between them is graded, which
is the behaviour this module exists for.
"""

CELL_CONTAMINATION = 0.02
"""Chance a cell's grey level says nothing at all about its bit.

A smudge, a specular highlight, a chip in the printing or a quad detected half
a module out are not in the Gaussian noise model, and without an allowance for
them one clean-looking cell can contribute unbounded evidence. Bounding each
cell's contribution at ``log((1 - eps) / eps)`` is the standard robust stand-in
for mixing the Gaussian with a uniform component, and it is what stops a
noiseless render reporting probability exactly one.
"""

MIN_CONTRAST = 8.0
"""Least black-to-white separation, in grey levels, for a quad to be scored."""

TEMPER = 0.5
"""How much of each extra copy's evidence to believe when fusing the ring.

One is full independence, which the ring's eight copies do not have. Below one
it discounts the shared pose, blur and lighting error. Calibrate it; do not
trust the default.
"""

ACCEPT_P = 0.999
"""Posterior at or above which a read is taken as the sample's identity."""

REJECT_P = 0.9
"""Posterior below which a read is refused outright rather than re-scanned."""

TOP_K = 3
"""How many alternatives a result carries, so the runner-up stays visible."""


class MarkerError(Exception):
    """Raised when a frame or a quad cannot be scored."""


@dataclass(frozen=True)
class MarkerReading:
    """One candidate quad, soft-decoded against the whole dictionary.

    Attributes:
        marker_id: Most probable id under this quad alone.
        probability: Its posterior, marginalised over the four rotations.
        runner_up: Second most probable id, the one a corrupted read would
            most plausibly have been.
        runner_up_probability: The runner-up's posterior.
        rotation: Quarter turns between the printed marker and the quad, 0 to 3.
        bit_errors: Hamming distance between the hard-thresholded cells and the
            winning codeword. Zero on a clean read; this is what OpenCV would
            have had to correct.
        contrast: Black-to-white separation in grey levels, as measured on the
            marker's own border and quiet zone.
        noise: Per-cell noise in units of contrast, estimated from the spread
            of those reference cells and floored at NOISE_FLOOR.
        accepted: Whether OpenCV's own detector identified this quad, as
            against having rejected it.
        corners: The quad in the frame's pixel coordinates, shape (4, 2).
        candidates: Ids that were scored, shape (n,).
        log_likelihood: log P(cells | id) per candidate, up to a shared
            constant, shape (n,). This is what :func:`fuse` adds up; it carries
            no prior, so fusing it twice does not count the prior twice.
    """

    marker_id: int
    probability: float
    runner_up: int
    runner_up_probability: float
    rotation: int
    bit_errors: int
    contrast: float
    noise: float
    accepted: bool
    corners: np.ndarray
    candidates: np.ndarray
    log_likelihood: np.ndarray


@dataclass(frozen=True)
class ScanResult:
    """What one frame says about which sample a bottle is.

    Attributes:
        marker_id: Most probable id over every quad in the frame, or None when
            nothing scorable was found.
        probability: Its fused posterior.
        posterior: The top few ids and their posteriors, most probable first.
        decision: ``"accept"``, ``"rescan"`` or ``"reject"``, from
            :func:`decide`.
        readings: Every quad that was scored, most confident first.
        record: The lookup-table row the winning id resolves to, or None when
            no table was given or the id is not in it.
    """

    marker_id: int | None
    probability: float
    posterior: list[tuple[int, float]]
    decision: str
    readings: list[MarkerReading]
    record: dict[str, object] | None


def make_detector(dictionary: int = ARUCO_DICTIONARY) -> "cv2.aruco.ArucoDetector":
    """Build the ArUco detector the ring experiments use

    The perimeter rate is loosened from OpenCV's default because the ring's
    copies are small: eight of them share the bottle's circumference. The
    error-correction rate is left alone deliberately --- on DICT_4X4_250 the
    default corrects no bits at all, so a corrupted marker is rejected rather
    than silently renamed, and this module recovers it from the soft cells
    instead of by loosening the codeword test.

    Args:
        dictionary: A ``cv2.aruco.DICT_*`` constant.

    Returns:
        A detector ready for detectMarkers.
    """
    parameters = cv2.aruco.DetectorParameters()
    parameters.minMarkerPerimeterRate = 0.02
    parameters.cornerRefinementMethod = cv2.aruco.CORNER_REFINE_SUBPIX
    return cv2.aruco.ArucoDetector(
        cv2.aruco.getPredefinedDictionary(dictionary), parameters
    )


@lru_cache(maxsize=4)
def codeword_bits(dictionary: int = ARUCO_DICTIONARY) -> np.ndarray:
    """Every id's bit pattern, in all four rotations

    The patterns are read back out of the dictionary's own rendered markers
    rather than unpacked from ``bytesList``, so the table cannot disagree with
    what ``generateImageMarker`` prints on a bottle.

    Args:
        dictionary: A ``cv2.aruco.DICT_*`` constant.

    Returns:
        A (n_ids, 4, DATA_CELLS ** 2) array of 0/1 bytes, where 1 is white.

    Example:
        >>> codeword_bits().shape
        (250, 4, 16)
    """
    book = cv2.aruco.getPredefinedDictionary(dictionary)
    size = ARUCO_MARKER_MODULES * RECTIFIED_CELL_PX
    rows = []
    for index in range(book.bytesList.shape[0]):
        marker = cv2.aruco.generateImageMarker(book, index, size)
        cells = marker.reshape(
            ARUCO_MARKER_MODULES, RECTIFIED_CELL_PX,
            ARUCO_MARKER_MODULES, RECTIFIED_CELL_PX,
        ).mean(axis=(1, 3))
        upright = (cells[1:-1, 1:-1] > 127).astype(np.uint8)
        rows.append([np.rot90(upright, k).flatten() for k in range(4)])
    return np.asarray(rows, np.uint8)


def _as_gray(image: np.ndarray) -> np.ndarray:
    """Return a single-channel view of a BGR or already-grey image."""
    if image.ndim == 2:
        return image
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def _log_sum_exp(values: np.ndarray, axis: int | None = None) -> np.ndarray:
    """Sum in the log domain without overflowing."""
    peak = np.max(values, axis=axis, keepdims=True)
    total = peak + np.log(np.sum(np.exp(values - peak), axis=axis, keepdims=True))
    return np.squeeze(total, axis=axis) if axis is not None else total.reshape(())


def sample_cells(gray: np.ndarray, quad: np.ndarray) -> np.ndarray:
    """Rectify a quad and measure the mean grey of every cell in its grid

    The quad is grown by one module a side first, so the grid takes in the
    quiet zone as well as the marker: the outer ring of cells is then a white
    reference and the ring inside it the marker's black border, which is where
    the black and white levels come from. Only the middle of each cell is
    averaged, so a quad that is a third of a module out still samples the right
    cell.

    Anything outside the frame is filled with mid grey rather than replicated,
    so a marker running off the edge loses confidence instead of gaining false
    evidence.

    Args:
        gray: Single-channel image.
        quad: The marker's four corners, shape (4, 2).

    Returns:
        A (GRID_CELLS, GRID_CELLS) array of mean grey levels.

    Raises:
        MarkerError: If gray is not single-channel or quad is not (4, 2).
    """
    if gray.ndim != 2:
        raise MarkerError(f"expected a single-channel image, got {gray.ndim}D")
    quad = np.asarray(quad, np.float32).reshape(-1, 2)
    if quad.shape != (4, 2):
        raise MarkerError(f"expected a (4, 2) quad, got {quad.shape}")

    grown = GRID_CELLS / ARUCO_MARKER_MODULES
    centre = quad.mean(axis=0)
    source = (centre + (quad - centre) * grown).astype(np.float32)

    span = GRID_CELLS * RECTIFIED_CELL_PX
    target = np.array(
        [[0, 0], [span - 1, 0], [span - 1, span - 1], [0, span - 1]], np.float32
    )
    warped = cv2.warpPerspective(
        gray,
        cv2.getPerspectiveTransform(source, target),
        (span, span),
        flags=cv2.INTER_AREA,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=127,
    )

    inset = int(round(RECTIFIED_CELL_PX * CELL_INSET))
    grid = warped.reshape(
        GRID_CELLS, RECTIFIED_CELL_PX, GRID_CELLS, RECTIFIED_CELL_PX
    ).astype(np.float64)
    return grid[:, inset:-inset, :, inset:-inset].mean(axis=(1, 3))


def _references(cells: np.ndarray) -> tuple[float, float, float]:
    """Return (black, white, noise) from a grid's quiet zone and border.

    The quiet ring is white by construction and the ring inside it is the
    marker's black border, so both levels are measured on cells whose true
    value is known. Their spread is what a cell mean does when the bit is not
    in doubt, which is exactly the noise the data cells face.
    """
    quiet = np.concatenate([cells[0], cells[-1], cells[1:-1, 0], cells[1:-1, -1]])
    inner = cells[1:-1, 1:-1]
    border = np.concatenate([inner[0], inner[-1], inner[1:-1, 0], inner[1:-1, -1]])
    white, black = float(np.median(quiet)), float(np.median(border))
    spread = float(max(np.std(quiet), np.std(border)))
    return black, white, spread


def read_quad(
    gray: np.ndarray,
    quad: np.ndarray,
    candidates: np.ndarray | None = None,
    accepted: bool = False,
    noise_floor: float = NOISE_FLOOR,
    contamination: float = CELL_CONTAMINATION,
    dictionary: int = ARUCO_DICTIONARY,
) -> MarkerReading | None:
    """Soft-decode one candidate quad into a posterior over ids

    Each data cell's grey level is turned into a log-likelihood ratio, linear
    in how far it sits between the black and white references and divided by
    the measured noise. Every candidate id and every rotation is then scored by
    summing the ratios of the cells it claims are white. Because the candidate
    set is enumerated in full, the result is a true posterior and not a score.

    Args:
        gray: Single-channel image.
        quad: The marker's four corners, shape (4, 2).
        candidates: Ids that are possible, typically the registry's
            ``marker_id`` column. Every id in the dictionary when omitted.
        accepted: Whether OpenCV's detector identified this quad itself.
            Recorded on the reading; it does not change the scoring.
        noise_floor: Smallest believable per-cell noise, in units of contrast.
        contamination: Chance a cell is uninformative, which bounds how much
            evidence any one of them may contribute.
        dictionary: A ``cv2.aruco.DICT_*`` constant.

    Returns:
        The reading, or None when the quad has too little black-to-white
        contrast to say anything at all.

    Raises:
        MarkerError: If gray or quad is the wrong shape, or a candidate id is
            not in the dictionary.

    Example:
        >>> from labvision import bottles
        >>> ring = bottles.render_ring(7)
        >>> marker = cv2.copyMakeBorder(ring[:, 448:576], 40, 40, 40, 40,
        ...                             cv2.BORDER_CONSTANT, value=255)
        >>> detector = make_detector()
        >>> corners, ids, _ = detector.detectMarkers(marker)
        >>> read_quad(marker, corners[0]).marker_id
        7
    """
    cells = sample_cells(gray, quad)
    black, white, spread = _references(cells)
    contrast = white - black
    if contrast < MIN_CONTRAST:
        logger.debug("quad skipped: contrast %.1f grey levels", contrast)
        return None

    noise = max(spread / contrast, noise_floor)
    data = cells[_DATA_SLICE, _DATA_SLICE]
    level = np.clip((data - black) / contrast, -0.5, 1.5).flatten()
    # log p(level | 1) - log p(level | 0) under a Gaussian of width `noise`,
    # which is linear in the level: the quadratic terms cancel. Bounded so that
    # no single cell can outvote the rest, however clean it looks.
    cap = float(np.log((1.0 - contamination) / contamination))
    ratio = np.clip((2.0 * level - 1.0) / (2.0 * noise**2), -cap, cap)

    book = codeword_bits(dictionary)
    ids = (
        np.arange(book.shape[0])
        if candidates is None
        else np.asarray(sorted(set(int(c) for c in candidates)), int)
    )
    if ids.size == 0 or ids.min() < 0 or ids.max() >= book.shape[0]:
        raise MarkerError(
            f"candidate ids outside the dictionary: {ids.min()}..{ids.max()}"
        )

    scores = book[ids].astype(np.float64) @ ratio          # (n ids, 4 rotations)
    per_id = _log_sum_exp(scores, axis=1)                  # rotation marginalised out
    posterior = np.exp(per_id - _log_sum_exp(per_id))

    order = np.argsort(-posterior)
    best, second = int(order[0]), int(order[min(1, order.size - 1)])
    rotation = int(np.argmax(scores[best]))
    hard = (level > 0.5).astype(np.uint8)
    return MarkerReading(
        marker_id=int(ids[best]),
        probability=float(posterior[best]),
        runner_up=int(ids[second]),
        runner_up_probability=float(posterior[second]) if order.size > 1 else 0.0,
        rotation=rotation,
        bit_errors=int((hard != book[ids[best], rotation]).sum()),
        contrast=float(contrast),
        noise=float(noise),
        accepted=accepted,
        corners=np.asarray(quad, np.float32).reshape(4, 2),
        candidates=ids,
        log_likelihood=per_id - per_id.max(),
    )


def read_markers(
    image: np.ndarray,
    candidates: np.ndarray | None = None,
    detector: "cv2.aruco.ArucoDetector | None" = None,
    include_rejected: bool = True,
    noise_floor: float = NOISE_FLOOR,
    contamination: float = CELL_CONTAMINATION,
) -> list[MarkerReading]:
    """Soft-decode every candidate quad in a frame

    The quads OpenCV rejected are scored alongside the ones it accepted.
    Rejection only means the thresholded bits matched no codeword within the
    correction budget, which on DICT_4X4_250's defaults is zero bits, so a
    rejected quad is usually a real marker seen badly --- and a frame where
    every copy was rejected still has plenty to say about which sample this is.

    Args:
        image: BGR or grayscale frame.
        candidates: Ids that are possible. Every id when omitted.
        detector: Detector to reuse across frames. Built when omitted.
        include_rejected: Whether to score the rejected quads too. Defaults to
            True.
        noise_floor: Smallest believable per-cell noise, in units of contrast.
        contamination: Chance a cell is uninformative; see CELL_CONTAMINATION.

    Returns:
        One reading per scorable quad, most confident first. Possibly empty.

    Raises:
        MarkerError: If the image is empty or not 2- or 3-dimensional.
    """
    if image is None or image.size == 0:
        raise MarkerError("image is empty")
    if image.ndim not in (2, 3):
        raise MarkerError(f"expected a 2D or 3D image, got {image.ndim}D")

    gray = _as_gray(image)
    found, _ids, rejected = (detector or make_detector()).detectMarkers(gray)
    quads = [(q, True) for q in found]
    if include_rejected:
        quads += [(q, False) for q in rejected]

    readings = []
    for quad, accepted in quads:
        reading = read_quad(
            gray, quad, candidates, accepted, noise_floor, contamination
        )
        if reading is not None:
            readings.append(reading)
    logger.debug(
        "%d quads scored (%d accepted by opencv)",
        len(readings), sum(r.accepted for r in readings),
    )
    return sorted(readings, key=lambda r: -r.probability)


def fuse(
    readings: list[MarkerReading],
    prior: dict[int, float] | None = None,
    temper: float = TEMPER,
) -> list[tuple[int, float]]:
    """Combine the ring's copies into one posterior over ids

    The copies' log-likelihoods add, which is why a bottle read badly eight
    times can still be identified and why eight copies disagreeing shows up as
    a posterior that never reaches the accept threshold rather than as a
    confident answer.

    The sum is tempered because the copies are not independent: they share the
    bottle's pose, the camera's focus and the bench's lighting, and a bias in
    any of those biases all eight the same way. Tempering is the honest way to
    stop the fused number running away from what the evidence supports.

    Args:
        readings: Readings from one bottle, from :func:`read_markers`.
        prior: Prior probability per id, unnormalised. Uniform over the
            candidates when omitted.
        temper: Weight on each reading's log-likelihood, in (0, 1].

    Returns:
        Ids and posteriors, most probable first. Empty when there are no
        readings.

    Raises:
        MarkerError: If the readings do not share one candidate set, or temper
            is outside (0, 1].
    """
    if not readings:
        return []
    if not 0.0 < temper <= 1.0:
        raise MarkerError(f"temper must be in (0, 1], got {temper}")
    ids = readings[0].candidates
    if any(r.candidates.shape != ids.shape or (r.candidates != ids).any()
           for r in readings):
        raise MarkerError("readings were scored against different candidate sets")

    total = temper * np.sum([r.log_likelihood for r in readings], axis=0)
    if prior is not None:
        weights = np.array([max(prior.get(int(i), 0.0), 1e-12) for i in ids])
        total = total + np.log(weights)
    posterior = np.exp(total - _log_sum_exp(total))
    order = np.argsort(-posterior)
    return [(int(ids[i]), float(posterior[i])) for i in order]


def decide(
    probability: float, accept: float = ACCEPT_P, reject: float = REJECT_P
) -> str:
    """Turn a posterior into what the arm should do about it

    Three outcomes, not two. Refusing to answer is cheap --- the arm moves and
    looks again, which ``scripts/wrist_scan.py`` already does --- whereas
    answering wrongly chains the wrong compound to the pot and nothing
    downstream can catch it.

    Args:
        probability: Fused posterior of the winning id.
        accept: At or above this, take the read as the sample's identity.
        reject: Below this, refuse rather than spend another look on it.

    Returns:
        ``"accept"``, ``"rescan"`` or ``"reject"``.

    Raises:
        MarkerError: If the thresholds are not ordered reject <= accept.

    Example:
        >>> decide(0.9999), decide(0.99), decide(0.2)
        ('accept', 'rescan', 'reject')
    """
    if not 0.0 <= reject <= accept <= 1.0:
        raise MarkerError(f"thresholds out of order: {reject} then {accept}")
    if probability >= accept:
        return "accept"
    return "rescan" if probability >= reject else "reject"


def scan(
    image: np.ndarray,
    table: dict[str, dict[str, object]] | None = None,
    detector: "cv2.aruco.ArucoDetector | None" = None,
    temper: float = TEMPER,
    noise_floor: float = NOISE_FLOOR,
    contamination: float = CELL_CONTAMINATION,
) -> ScanResult:
    """Read one bottle out of a frame and say how sure the answer is

    When a lookup table is given it is also the prior: only the ids the
    catalogue actually prints are possible, which is both more accurate and
    more conservative than scoring against all 250, since a corrupted read can
    no longer land on an id no bottle carries.

    Args:
        image: BGR or grayscale frame, cropped to one bottle.
        table: Lookup table, as returned by ``labvision.registry.load_table``.
            Without it every dictionary id is a candidate and no record is
            resolved.
        detector: Detector to reuse across frames.
        temper: Weight on each copy's evidence when fusing the ring.
        noise_floor: Smallest believable per-cell noise, in units of contrast.
        contamination: Chance a cell is uninformative; see CELL_CONTAMINATION.

    Returns:
        The frame's verdict. ``marker_id`` is None and ``decision`` is
        ``"reject"`` when nothing scorable was found.

    Raises:
        MarkerError: If the image is empty or the wrong shape.
    """
    by_marker: dict[int, dict[str, object]] = {}
    candidates = None
    if table:
        by_marker = {int(row["marker_id"]): row for row in table.values()}
        candidates = np.array(sorted(by_marker), int)

    readings = read_markers(
        image, candidates, detector,
        noise_floor=noise_floor, contamination=contamination,
    )
    posterior = fuse(readings, temper=temper)[:TOP_K]
    if not posterior:
        return ScanResult(None, 0.0, [], "reject", readings, None)

    best, probability = posterior[0]
    return ScanResult(
        marker_id=best,
        probability=probability,
        posterior=posterior,
        decision=decide(probability),
        readings=readings,
        record=by_marker.get(best),
    )
