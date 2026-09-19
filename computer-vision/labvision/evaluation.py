"""Score a detector's boxes against simulator truth, the same way for every model

The benchmark of the fixed camera compares zero-shot and fine-tuned detectors
on the same frames, so the scoring lives here, once, with tests, rather than in
each script. It follows COCO where COCO has an answer and says so where it
does not:

- **Truth that must be found** is a sample bottle standing on the bench, at
  least half visible and not cut by the frame border (:func:`is_required`).
- **Truth that is ignored** is every other sample bottle in view: on a shelf,
  mostly hidden, or clipped. A box on one of those is neither a hit nor a
  false positive, as with COCO's crowd regions. A box counts as being on one
  when it overlaps its visible box at the IoU threshold, or lies mostly inside
  its full silhouette (a box on the visible part of a hidden bottle).
- **Matching** is greedy by score, each box to the unmatched required bottle
  it overlaps most, as in COCO.
- **AP** is the area under the precision-recall curve with COCO's 101-point
  interpolation, at IoU 0.5 (``ap50``) and averaged over 0.50:0.05:0.95
  (``ap``). Class-agnostic unless asked: the detector's job is *there is a
  bottle here*; the kit (amber or HDPE) is a second, class-aware score.
- **Operating point**: a detector is used at one score threshold. It is chosen
  on the validation split (best F1) and then applied unchanged to the tests.
- **Confidence**: 95 % intervals by resampling whole frames (bootstrap).

The truth format is the ``gt.json`` of ``scripts/render_perfumery.py`` and
``scripts/fixedcam_dataset.py``: per frame, per bottle, a visible box
``xyxy``, the full silhouette ``full_xyxy``, ``visible_frac``, ``clipped``,
``where`` and the kit and size. Boxes are ``(u_min, v_min, u_max, v_max)`` in
pixels.
"""

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

import numpy as np

CLASS_NAMES: tuple[str, ...] = ("amber_bottle", "hdpe_bottle")
"""Detector classes: the two sample kits. Amber glass holds liquids, white HDPE
holds powders."""

MIN_VISIBLE = 0.5
"""Least visible fraction of a bottle's silhouette for it to be required."""

COVER_INSIDE = 0.7
"""A box this much inside an ignored bottle's full silhouette lands on it."""

IOU_THRESHOLDS: tuple[float, ...] = tuple(round(0.5 + 0.05 * k, 2) for k in range(10))
"""COCO's IoU thresholds, 0.50 to 0.95."""

RECALL_POINTS = np.linspace(0.0, 1.0, 101)
"""COCO's 101 recall points for interpolated AP."""

SIDE_EDGES_PX: tuple[int, ...] = (16, 24, 32, 48)
"""Edges of the apparent-size buckets, by the side (geometric mean of width and
height) of the full silhouette."""

Box = tuple[float, float, float, float]


@dataclass(frozen=True)
class Truth:
    """One sample bottle in a frame

    Attributes:
        box: Visible box.
        full_box: Box of the whole silhouette, hidden parts included.
        cls: Index in :data:`CLASS_NAMES`.
        kind: Kit and size, e.g. ``amber 10 ml``.
        required: Whether a detector must find it (see :func:`is_required`).
        side_px: Side of the full silhouette, for the size buckets.
    """

    box: Box
    full_box: Box
    cls: int
    kind: str
    required: bool
    side_px: float


@dataclass(frozen=True)
class Detection:
    """One box a detector returned

    Attributes:
        box: The box.
        score: Confidence in [0, 1].
        cls: Index in :data:`CLASS_NAMES`, or -1 when the model has no kit.
    """

    box: Box
    score: float
    cls: int = -1


@dataclass
class FrameResult:
    """The outcome of matching one frame's detections at one IoU threshold

    Attributes:
        scores: Score of every detection that is not ignored, highest first.
        hits: Whether each of those matched a required bottle.
        found: For each required bottle, the score it was found at, or None.
        truths: The required bottles, in the order of ``found``.
        false_boxes: The detections counted false, with their score.
    """

    scores: list[float] = field(default_factory=list)
    hits: list[bool] = field(default_factory=list)
    found: list[float | None] = field(default_factory=list)
    truths: list[Truth] = field(default_factory=list)
    false_boxes: list[Detection] = field(default_factory=list)


def iou(a: Sequence[float], b: Sequence[float]) -> float:
    """Return the intersection over union of two boxes"""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    inter = w * h
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def fraction_inside(box: Sequence[float], region: Sequence[float]) -> float:
    """Return the share of ``box``'s area that lies inside ``region``"""
    w = min(box[2], region[2]) - max(box[0], region[0])
    h = min(box[3], region[3]) - max(box[1], region[1])
    area = (box[2] - box[0]) * (box[3] - box[1])
    if w <= 0 or h <= 0 or area <= 0:
        return 0.0
    return w * h / area


def side(box: Sequence[float]) -> float:
    """Return the geometric mean of a box's width and height"""
    return math.sqrt(max(box[2] - box[0], 0.0) * max(box[3] - box[1], 0.0))


def side_bucket(side_px: float) -> str:
    """Name the apparent-size bucket of a side, e.g. ``16-24 px``"""
    low = 0
    for edge in SIDE_EDGES_PX:
        if side_px < edge:
            return f"{low}-{edge} px"
        low = edge
    return f"{low}+ px"


def side_buckets() -> list[str]:
    """Return every size bucket name, smallest first"""
    edges = (0, *SIDE_EDGES_PX)
    names = [f"{a}-{b} px" for a, b in zip(edges[:-1], edges[1:], strict=True)]
    return [*names, f"{edges[-1]}+ px"]


def kind_of(bottle: dict) -> str:
    """Name a truth record's kit and size, e.g. ``amber 10 ml``"""
    kit = "amber" if bottle["phase"] == "liquid" else "hdpe"
    return f"{kit} {int(bottle['container_ml'])} ml"


KINDS: tuple[str, ...] = tuple(
    [f"amber {v} ml" for v in (10, 20, 30, 50, 100)]
    + [f"hdpe {v} ml" for v in (100, 250, 500, 1000, 2000)]
)
"""Every kit and size, smallest first within a kit."""


def is_required(bottle: dict, min_visible: float = MIN_VISIBLE) -> bool:
    """Say whether a truth record is a bottle a detector must find"""
    return (
        bottle.get("where", "bench") == "bench"
        and bottle["visible_frac"] >= min_visible
        and not bottle["clipped"]
    )


def truths_of(frame: dict, min_visible: float = MIN_VISIBLE) -> list[Truth]:
    """Turn one ``gt.json`` frame into :class:`Truth` records"""
    out = []
    for bottle in frame["bottles"]:
        full = tuple(float(v) for v in bottle["full_xyxy"])
        out.append(
            Truth(
                box=tuple(float(v) for v in bottle["xyxy"]),
                full_box=full,
                cls=0 if bottle["phase"] == "liquid" else 1,
                kind=kind_of(bottle),
                required=is_required(bottle, min_visible),
                side_px=side(full),
            )
        )
    return out


def match_frame(
    truths: Sequence[Truth],
    detections: Sequence[Detection],
    iou_min: float = 0.5,
    class_aware: bool = False,
) -> FrameResult:
    """Match one frame's detections to its truth, highest score first

    A detection takes the unmatched required bottle it overlaps most, at
    ``iou_min`` or more (and of its class when ``class_aware``). Failing that it
    is ignored if it lands on a bottle that is not required, else it is false.

    Returns:
        The frame's :class:`FrameResult`.
    """
    required = [t for t in truths if t.required]
    ignored = [t for t in truths if not t.required]
    taken: list[float | None] = [None] * len(required)
    result = FrameResult(truths=required)
    for det in sorted(detections, key=lambda d: -d.score):
        best, best_iou = -1, iou_min
        for i, truth in enumerate(required):
            if taken[i] is not None or (class_aware and det.cls != truth.cls):
                continue
            overlap = iou(det.box, truth.box)
            if overlap >= best_iou:
                best, best_iou = i, overlap
        if best >= 0:
            taken[best] = det.score
            result.scores.append(det.score)
            result.hits.append(True)
            continue
        if any(
            iou(det.box, t.box) >= iou_min
            or fraction_inside(det.box, t.full_box) >= COVER_INSIDE
            for t in ignored
        ):
            continue
        result.scores.append(det.score)
        result.hits.append(False)
        result.false_boxes.append(det)
    result.found = taken
    return result


def average_precision(
    scores: Sequence[float], hits: Sequence[bool], n_required: int
) -> float:
    """Return COCO's 101-point interpolated AP of scored hits and misses

    Args:
        scores: One score per counted detection, pooled over frames.
        hits: Whether each detection is a true positive.
        n_required: How many bottles had to be found.

    Returns:
        AP in [0, 1]; NaN when nothing had to be found.
    """
    if n_required == 0:
        return float("nan")
    if not len(scores):
        return 0.0
    order = np.argsort(-np.asarray(scores, dtype=float), kind="mergesort")
    tp = np.asarray(hits, dtype=bool)[order]
    tp_cum = np.cumsum(tp)
    fp_cum = np.cumsum(~tp)
    recall = tp_cum / n_required
    precision = tp_cum / np.maximum(tp_cum + fp_cum, np.finfo(float).eps)
    # Make precision monotone from the right, then sample it at 101 recalls.
    precision = np.maximum.accumulate(precision[::-1])[::-1]
    index = np.searchsorted(recall, RECALL_POINTS, side="left")
    sampled = np.where(
        index < len(precision), precision[np.minimum(index, len(precision) - 1)], 0.0
    )
    return float(sampled.mean())


def pooled(results: Sequence[FrameResult]) -> tuple[list[float], list[bool], int]:
    """Pool the frames' scored detections and count their required bottles"""
    scores = [s for r in results for s in r.scores]
    hits = [h for r in results for h in r.hits]
    return scores, hits, sum(len(r.found) for r in results)


def ap_at(results: Sequence[FrameResult]) -> float:
    """Return the AP of already-matched frames"""
    return average_precision(*pooled(results))


def best_f1_threshold(results: Sequence[FrameResult]) -> tuple[float, float]:
    """Return the score threshold with the best F1, and that F1

    A detection is kept when its score is at or above the threshold.
    """
    scores, hits, n_required = pooled(results)
    if not scores or n_required == 0:
        return 0.0, 0.0
    order = np.argsort(-np.asarray(scores), kind="mergesort")
    sorted_scores = np.asarray(scores)[order]
    tp = np.cumsum(np.asarray(hits)[order])
    kept = np.arange(1, len(scores) + 1)
    f1 = 2 * tp / (kept + n_required)
    # Only cut between distinct scores: every box at the threshold is kept.
    last_of_score = np.r_[sorted_scores[1:] != sorted_scores[:-1], True]
    f1 = np.where(last_of_score, f1, -1.0)
    best = int(np.argmax(f1))
    return float(sorted_scores[best]), float(f1[best])


def operating_point(results: Sequence[FrameResult], threshold: float) -> dict:
    """Count found, missed and false boxes at one score threshold

    Returns:
        ``required``, ``found``, ``recall``, ``false``, ``false_per_frame``,
        ``precision`` and ``f1``.
    """
    n_required = sum(len(r.found) for r in results)
    found = sum(1 for r in results for s in r.found if s is not None and s >= threshold)
    false = sum(1 for r in results for d in r.false_boxes if d.score >= threshold)
    frames = max(len(results), 1)
    precision = found / (found + false) if found + false else float("nan")
    recall = found / n_required if n_required else float("nan")
    f1 = 2 * found / (found + false + n_required) if found + false + n_required else 0
    return {
        "threshold": threshold,
        "required": n_required,
        "found": found,
        "recall": recall,
        "false": false,
        "false_per_frame": false / frames,
        "precision": precision,
        "f1": f1,
    }


def breakdown(
    results: Sequence[FrameResult], threshold: float, key: Callable[[Truth], str]
) -> dict[str, list[int]]:
    """Count ``[found, required]`` per group of required bottles at a threshold"""
    table: dict[str, list[int]] = {}
    for r in results:
        for truth, score in zip(r.truths, r.found, strict=True):
            row = table.setdefault(key(truth), [0, 0])
            row[0] += score is not None and score >= threshold
            row[1] += 1
    return table


def bootstrap(
    results: Sequence[FrameResult],
    statistic: Callable[[Sequence[FrameResult]], float],
    reps: int = 1000,
    seed: int = 0,
) -> tuple[float, float]:
    """Return a 95 % interval of a statistic by resampling whole frames

    Frames, not boxes, are resampled: bottles in one frame share its light,
    layout and clutter, so they are not independent.
    """
    if not results:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    values = []
    for _ in range(reps):
        pick = rng.integers(0, len(results), len(results))
        values.append(statistic([results[i] for i in pick]))
    low, high = np.nanpercentile(values, [2.5, 97.5])
    return float(low), float(high)


# --------------------------------------------------------------------------
# Worktop filter: geometry the robot knows, never an object's pose.


def camera_ray(frame: dict, u: float, v: float) -> tuple[np.ndarray, np.ndarray]:
    """Return the camera centre and the world direction through pixel (u, v)

    Uses the pose and field of view stored with the frame (MuJoCo camera
    convention: looking down -Z, +Y up), which a robot knows by calibration.
    """
    rotation = np.asarray(frame["cam_xmat"], dtype=float).reshape(3, 3)
    origin = np.asarray(frame["cam_pos"], dtype=float)
    f = (frame["height"] / 2) / math.tan(math.radians(frame["fovy_deg"]) / 2)
    local = np.array(
        [(u - frame["width"] / 2) / f, -(v - frame["height"] / 2) / f, -1.0]
    )
    return origin, rotation @ local


def to_plane(frame: dict, u: float, v: float, z: float) -> np.ndarray | None:
    """Intersect the ray through pixel (u, v) with the plane at height ``z``"""
    origin, ray = camera_ray(frame, u, v)
    if ray[2] >= -1e-9:
        return None
    return origin + (z - origin[2]) / ray[2] * ray


def project(frame: dict, point: Sequence[float]) -> tuple[float, float] | None:
    """Project a world point into the frame's pixels, or None if behind"""
    rotation = np.asarray(frame["cam_xmat"], dtype=float).reshape(3, 3)
    local = rotation.T @ (np.asarray(point, dtype=float) - np.asarray(frame["cam_pos"]))
    if local[2] >= 0:
        return None
    f = (frame["height"] / 2) / math.tan(math.radians(frame["fovy_deg"]) / 2)
    return (
        frame["width"] / 2 + f * local[0] / -local[2],
        frame["height"] / 2 - f * local[1] / -local[2],
    )


@dataclass(frozen=True)
class Worktop:
    """The bench plane and outline a box must stand on

    Attributes:
        z: Height of the worktop surface, metres.
        centre: Centre of the worktop outline, (x, y).
        half: Half length and half depth of the outline.
        height_range: Shortest and tallest bottle, metres, for the size check.
    """

    z: float = 0.90
    centre: tuple[float, float] = (0.0, 0.0)
    half: tuple[float, float] = (3.0, 0.75)
    height_range: tuple[float, float] = (0.045, 0.26)

    @classmethod
    def from_gt(cls, gt: dict) -> "Worktop":
        """Read the worktop of a ``gt.json`` written by ``fixedcam_dataset.py``"""
        return cls(
            z=float(gt.get("worktop_z", 0.90)),
            centre=tuple(gt.get("bench_centre", (0.0, 0.0))),
            half=tuple(gt.get("bench_half", (3.0, 0.75))),
        )


def on_worktop(
    frame: dict, box: Sequence[float], worktop: Worktop, size_check: bool = True
) -> bool:
    """Say whether a box can be a bottle standing on the worktop

    Two checks, both from the camera's calibrated pose alone:

    1. The bottom centre of the box, cast onto the worktop plane, lands inside
       the worktop outline.
    2. With ``size_check``, the box's height is one a bottle standing at that
       point could have: between the shortest bottle's image height (with a
       little slack for a partly hidden one) and the tallest's. A shelf bottle
       casts its base far behind the bench, where a bottle of that pixel
       height would have to be much taller than any in the kit.
    """
    u, v = (box[0] + box[2]) / 2, box[3]
    base = to_plane(frame, u, v, worktop.z)
    if base is None:
        return False
    if (
        abs(base[0] - worktop.centre[0]) > worktop.half[0]
        or abs(base[1] - worktop.centre[1]) > worktop.half[1]
    ):
        return False
    if not size_check:
        return True
    heights = []
    for h in worktop.height_range:
        top = project(frame, (base[0], base[1], worktop.z + h))
        if top is None:
            return False
        heights.append(v - top[1])
    observed = box[3] - box[1]
    return 0.4 * heights[0] <= observed <= 1.35 * heights[1]
