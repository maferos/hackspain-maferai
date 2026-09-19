"""Score the pretrained detectors on frames of Eki's perfumery lab

Takes the frames and ``gt.json`` written by ``render_perfumery.py``, runs a
detector backend on every frame at the frame's own resolution, and answers,
per set of frames:

1. What share of the sample bottles is found, by bottle and by apparent size?
2. How many boxes land on something that is not a sample bottle, and on what:
   the shelf library, other glassware, a balance, an instrument?

A bottle counts when at least half of its silhouette is visible and it is
not cut by the frame border; the others are neither required nor, when a box
lands on them, held against the detector. A box matches a bottle at an IoU of
0.5 with its visible box.

    python scripts/perfumery_eval.py ../simulation/out/perfumery
    python scripts/perfumery_eval.py ../simulation/out/perfumery --overlays

Detections are cached in ``detections_<backend>.json`` next to the frames, so
rescoring is instant. The cache remembers the size and date of every frame
file, so re-rendering the folder runs the detector again by itself; ``--redo``
forces that. Writes ``perfumery_eval.md`` and ``.json`` next to the frames.
"""

import argparse
import functools
import itertools
import json
import math
import statistics
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision.detector import BACKENDS, Detector  # noqa: E402

CATEGORIES = ("other", "sample", "shelf_bottle", "glassware", "balance", "instrument")
"""Values of the category maps, in the order ``render_perfumery.py`` writes them."""
SIDE_EDGES_PX = (16, 24, 48)
"""Apparent-size buckets; 24 and 48 are the detector module's floors."""
MIN_VISIBLE = 0.5
KINDS = [f"amber {v} ml" for v in (10, 20, 30, 50, 100)] + [
    f"hdpe {v} ml" for v in (100, 250, 500, 1000, 2000)
]


WORKTOP_Z = 0.90
"""Top of the minihannover worktop, as in ``render_perfumery.py``."""
WORKTOP_HALF = (3.0, 0.75)
"""Half the worktop's length and width."""
WORKTOP_CENTER = (0.0, 0.0)
"""Where the worktop is centred, as in ``render_perfumery.BENCH_CENTER``."""
VISION_SETS = ("perception", "general", "wrist")
"""Sets rendered from the vision system's own GoPros, which look down at the bench.
``perception`` is the close camera of the first perfumery benchmark."""


def base_on_worktop(frame: dict, box) -> tuple[float, float] | None:
    """Back-project a box's bottom centre onto the worktop plane

    Uses only the camera's pose and field of view from ``gt.json``, which a
    robot knows by calibration, never an object's pose.

    Returns:
        (x, y) in metres, or None when the ray does not head down to the bench.
    """
    rotation = np.array(frame["cam_xmat"]).reshape(3, 3)
    origin = np.array(frame["cam_pos"])
    f = (frame["height"] / 2) / math.tan(math.radians(frame["fovy_deg"]) / 2)
    u, v = (box[0] + box[2]) / 2, box[3]
    ray = rotation @ np.array(
        [(u - frame["width"] / 2) / f, -(v - frame["height"] / 2) / f, -1.0]
    )
    if ray[2] >= 0:
        return None
    x, y, _ = origin + (WORKTOP_Z - origin[2]) / ray[2] * ray
    return float(x), float(y)


def on_worktop(frame: dict, box) -> bool:
    """Say whether a box stands on the worktop: the worktop filter

    The walkthrough cameras are at eye height, where a shelf bottle's base
    projects off the bench, so landing on the worktop is enough. The vision
    system's cameras look down, and from there the lowest shelf projects onto
    the far half of the bench, so a box has to land on the camera's own half.
    """
    point = base_on_worktop(frame, box)
    if point is None or abs(point[0] - WORKTOP_CENTER[0]) > WORKTOP_HALF[0]:
        return False
    across = point[1] - WORKTOP_CENTER[1]
    if frame["set"] in VISION_SETS:
        side = math.copysign(1.0, frame["cam_pos"][1] - WORKTOP_CENTER[1])
        return 0.02 <= side * across <= WORKTOP_HALF[1]
    return abs(across) <= WORKTOP_HALF[1]


def kind(bottle: dict) -> str:
    """Name a bottle by kit and size, e.g. ``amber 10 ml``"""
    kit = "amber" if bottle["phase"] == "liquid" else "hdpe"
    return f"{kit} {int(bottle['container_ml'])} ml"


def side_px(xyxy) -> float:
    """Geometric mean of a box's width and height"""
    return math.sqrt(max(xyxy[2] - xyxy[0], 0) * max(xyxy[3] - xyxy[1], 0))


def side_bucket(side: float) -> str:
    """Label an apparent size by :data:`SIDE_EDGES_PX`"""
    lo = 0
    for edge in SIDE_EDGES_PX:
        if side < edge:
            return f"{lo}-{edge} px"
        lo = edge
    return f"{lo}+ px"


def side_labels() -> list[str]:
    """All size buckets, smallest first"""
    edges = (0, *SIDE_EDGES_PX)
    bounded = [f"{a}-{b} px" for a, b in itertools.pairwise(edges)]
    return [*bounded, f"{edges[-1]}+ px"]


def iou(a, b) -> float:
    """Intersection over union of two (u_min, v_min, u_max, v_max) boxes"""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    inter = w * h
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union


def covers(box, bottle: dict) -> bool:
    """Say whether a box lands on a bottle that is not required

    Either it matches the visible part, or most of it lies inside the bottle's
    full silhouette, as a box on the visible half of a hidden bottle does.
    """
    full = bottle["full_xyxy"]
    w = min(box[2], full[2]) - max(box[0], full[0])
    h = min(box[3], full[3]) - max(box[1], full[1])
    area = (box[2] - box[0]) * (box[3] - box[1])
    inside = max(w, 0) * max(h, 0) / area if area > 0 else 0.0
    return inside >= 0.7 or iou(box, bottle["xyxy"]) >= 0.5


def is_required(bottle: dict) -> bool:
    """Say whether a detector is expected to find this bottle"""
    return bottle["visible_frac"] >= MIN_VISIBLE and not bottle["clipped"]


def what_is_under(box, categories: np.ndarray) -> str:
    """Name what a box mostly covers, preferring any object over bare scenery

    Small boxes are mostly bench and wall, so the category is the object class
    covering the most of the box, provided it covers at least 15 % of it.
    """
    u0, v0, u1, v1 = (int(round(v)) for v in box)
    patch = categories[max(v0, 0) : max(v1, 1), max(u0, 0) : max(u1, 1)]
    if patch.size == 0:
        return "other"
    counts = np.bincount(patch.reshape(-1), minlength=len(CATEGORIES))
    counts[0] = 0
    best = int(counts.argmax())
    return CATEGORIES[best] if counts[best] >= 0.15 * patch.size else "other"


def frame_stamp(folder: Path, frames: list[dict]) -> dict[str, list[int]]:
    """Size and modification time of every frame file

    Stored with the cached detections: when the frames are rendered again the
    stamp no longer matches, and the cache is not scored against a truth it
    was never run on.
    """
    stamp = {}
    for frame in frames:
        st = (folder / frame["file"]).stat()
        stamp[frame["file"]] = [st.st_size, st.st_mtime_ns]
    return stamp


def detect_all(backend: str, folder: Path, frames: list[dict], args) -> dict:
    """Run a backend over every frame, or read its cached detections

    The cache file maps each frame file to its boxes, plus a ``_frames`` entry
    holding the :func:`frame_stamp` it was made for.
    """
    cache = folder / f"detections_{backend}.json"
    stamp = frame_stamp(folder, frames)
    if cache.exists() and not args.redo:
        cached = json.loads(cache.read_text(encoding="utf-8"))
        if cached.get("_frames") == stamp:
            return cached
        print(f"{cache.name} is from other frames, running {backend} again", flush=True)
    detector = Detector(backend, device=args.device)
    result = {"_frames": stamp}
    for k, frame in enumerate(frames):
        image = cv2.imread(str(folder / frame["file"]))
        if k == 0:
            detector.warmup(image.shape)
        start = time.perf_counter()
        boxes = detector.detect(image)
        seconds = time.perf_counter() - start
        result[frame["file"]] = {
            "seconds": round(seconds, 3),
            "boxes": [b.to_json() for b in boxes],
        }
        print(
            f"{backend} {k + 1}/{len(frames)} {frame['file']}: "
            f"{len(boxes)} boxes, {seconds:.1f} s",
            flush=True,
        )
    cache.write_text(json.dumps(result, indent=1), encoding="utf-8")
    return result


@functools.lru_cache(maxsize=128)
def category_map(path: Path) -> np.ndarray:
    """Read a frame's category map once, however many times it is scored"""
    return cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)


def match_frame(
    folder: Path, frame: dict, boxes: list[dict], iou_min: float
) -> tuple[list[dict], list[bool], list[dict], list[tuple[dict, str, str | None]]]:
    """Match one frame's detections to its bottles, highest score first

    Returns:
        The required bottles, whether each was found, the bottles not required,
        and one ``(box, verdict, what it landed on)`` per detection, the verdict
        being ``hit``, ``ignored`` or ``false``.
    """
    required = [b for b in frame["bottles"] if is_required(b)]
    ignored = [b for b in frame["bottles"] if not is_required(b)]
    taken = [False] * len(required)
    outcome: list[tuple[dict, str, str | None]] = []
    categories = None
    for box in sorted(boxes, key=lambda b: -b["score"]):
        best, best_iou = -1, iou_min
        for i, bottle in enumerate(required):
            overlap = iou(box["xyxy"], bottle["xyxy"])
            if not taken[i] and overlap >= best_iou:
                best, best_iou = i, overlap
        if best >= 0:
            taken[best] = True
            outcome.append((box, "hit", None))
        elif any(covers(box["xyxy"], b) for b in ignored):
            outcome.append((box, "ignored", None))
        else:
            if categories is None:
                categories = category_map(folder / frame["categories"])
            outcome.append((box, "false", what_is_under(box["xyxy"], categories)))
    return required, taken, ignored, outcome


def score(
    backend: str, folder: Path, frames: list[dict], detections: dict, args
) -> dict:
    """Match detections to the truth and tally found, missed and false boxes per set"""
    tally = defaultdict(lambda: {
        "frames": 0, "required": 0, "found": 0, "false": 0, "seconds": [],
        "by_kind": defaultdict(lambda: [0, 0]), "by_side": defaultdict(lambda: [0, 0]),
        "false_on": Counter(), "found_side": [],
    })  # fmt: skip
    overlay_dir = folder / f"overlay_{backend}"
    if args.overlays:
        overlay_dir.mkdir(exist_ok=True)
    for frame in frames:
        t = tally[frame["set"]]
        found = detections[frame["file"]]
        t["frames"] += 1
        t["seconds"].append(found["seconds"])
        required, taken, ignored, outcome = match_frame(
            folder, frame, found["boxes"], args.iou
        )
        for _, verdict, under in outcome:
            if verdict == "false":
                t["false"] += 1
                t["false_on"][under] += 1
        for i, bottle in enumerate(required):
            side = side_px(bottle["full_xyxy"])
            t["required"] += 1
            t["found"] += taken[i]
            t["by_kind"][kind(bottle)][0] += taken[i]
            t["by_kind"][kind(bottle)][1] += 1
            t["by_side"][side_bucket(side)][0] += taken[i]
            t["by_side"][side_bucket(side)][1] += 1
            if taken[i]:
                t["found_side"].append(side)
        if args.overlays:
            draw_overlay(folder, frame, required, taken, ignored, outcome, overlay_dir)

    result = {}
    for set_name, t in tally.items():
        result[set_name] = {
            "frames": t["frames"],
            "required": t["required"],
            "found": t["found"],
            "recall": t["found"] / t["required"] if t["required"] else None,
            "false_per_frame": t["false"] / t["frames"],
            "precision": t["found"] / (t["found"] + t["false"])
            if t["found"] + t["false"]
            else None,
            "seconds_per_frame": statistics.median(t["seconds"]),
            "by_kind": {k: t["by_kind"][k] for k in KINDS if k in t["by_kind"]},
            "by_side": {k: t["by_side"][k] for k in side_labels() if k in t["by_side"]},
            "false_on": dict(t["false_on"].most_common()),
            "smallest_found_px": min(t["found_side"]) if t["found_side"] else None,
        }
    return result


def draw_overlay(folder, frame, required, taken, ignored, outcome, overlay_dir) -> None:
    """Write the frame with the truth and the detector's boxes drawn on it

    Green: a bottle that was found. Magenta: a bottle that was missed. Grey: a
    bottle not required (mostly hidden or cut by the border). Red: a false box,
    captioned with what it landed on.
    """
    image = cv2.imread(str(folder / frame["file"]))
    thick = max(1, image.shape[1] // 960)

    def rect(xyxy, colour, text=None):
        p0 = (int(xyxy[0]), int(xyxy[1]))
        cv2.rectangle(image, p0, (int(xyxy[2]), int(xyxy[3])), colour, thick)
        if text:
            org = (p0[0], max(p0[1] - 3, 10))
            cv2.putText(image, text, org, cv2.FONT_HERSHEY_SIMPLEX,
                        0.4 * thick, colour, thick)  # fmt: skip

    for bottle in ignored:
        rect(bottle["xyxy"], (160, 160, 160))
    for bottle, hit in zip(required, taken, strict=True):
        rect(
            bottle["xyxy"],
            (0, 200, 0) if hit else (255, 0, 255),
            None if hit else kind(bottle),
        )
    for box, verdict, under in outcome:
        if verdict == "false":
            rect(box["xyxy"], (0, 0, 255), under)
    cv2.imwrite(str(overlay_dir / frame["file"].replace(".png", ".jpg")), image)


def pct(n: int, d: int) -> str:
    """Format n of d as a percentage with the counts"""
    return f"{100 * n / d:.0f} % ({n}/{d})" if d else "-"


def to_markdown(results: dict[str, dict]) -> str:
    """Render the per-backend, per-set results as markdown tables"""
    lines = ["# Pretrained detectors on the perfumery lab", ""]
    sets = sorted({s for r in results.values() for s in r})
    lines += [
        "| set | backend | frames | found | false / frame | precision | s/frame |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for s in sets:
        for backend, r in results.items():
            if s not in r:
                continue
            x = r[s]
            precision = (
                f"{100 * x['precision']:.0f} %" if x["precision"] is not None else "-"
            )
            lines.append(
                f"| {s} | {backend} | {x['frames']} | "
                f"{pct(x['found'], x['required'])} | {x['false_per_frame']:.1f} | "
                f"{precision} | {x['seconds_per_frame']:.1f} |"
            )
    for s in sets:
        backends = [b for b in results if s in results[b]]
        lines += ["", f"## {s}", "", "| bottle | " + " | ".join(backends) + " |",
                  "| --- |" + " --- |" * len(backends)]  # fmt: skip
        for k in KINDS:
            cells = [pct(*results[b][s]["by_kind"].get(k, (0, 0))) for b in backends]
            if any(c != "-" for c in cells):
                lines.append(f"| {k} | " + " | ".join(cells) + " |")
        lines += ["", "| apparent side | " + " | ".join(backends) + " |",
                  "| --- |" + " --- |" * len(backends)]  # fmt: skip
        for k in side_labels():
            cells = [pct(*results[b][s]["by_side"].get(k, (0, 0))) for b in backends]
            if any(c != "-" for c in cells):
                lines.append(f"| {k} | " + " | ".join(cells) + " |")
        lines += ["", "| false boxes on | " + " | ".join(backends) + " |",
                  "| --- |" + " --- |" * len(backends)]  # fmt: skip
        for c in CATEGORIES:
            cells = [str(results[b][s]["false_on"].get(c, 0)) for b in backends]
            if any(v != "0" for v in cells):
                lines.append(f"| {c} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    """Detect, score and report"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder", type=Path)
    parser.add_argument(
        "--backend", default="both", help=f"one of {sorted(BACKENDS)} or both"
    )
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--device", default=None)
    parser.add_argument("--redo", action="store_true", help="ignore cached detections")
    parser.add_argument(
        "--overlays", action="store_true", help="write overlay_<backend>/ images"
    )
    args = parser.parse_args()

    gt = json.loads((args.folder / "gt.json").read_text(encoding="utf-8"))
    frames = gt["frames"]
    backends = ["world", "coco"] if args.backend == "both" else [args.backend]
    results = {}
    for backend in backends:
        detections = detect_all(backend, args.folder, frames, args)
        results[backend] = score(backend, args.folder, frames, detections, args)
    report = to_markdown(results)
    (args.folder / "perfumery_eval.md").write_text(report, encoding="utf-8")
    (args.folder / "perfumery_eval.json").write_text(
        json.dumps(results, indent=1), encoding="utf-8"
    )
    print(report)


if __name__ == "__main__":
    main()
