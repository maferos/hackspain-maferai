"""Benchmark bottle detectors on the fixed room camera, all scored the same way

Runs a model over the frames of one or more splits written by
``fixedcam_dataset.py``, caches its boxes, and scores them with
:mod:`labvision.evaluation`: AP at IoU 0.5 and 0.50:0.95, recall and false
boxes per frame at one operating threshold, recall by bottle size and by
apparent size in pixels, 95 % bootstrap intervals, and latency on this
machine. The operating threshold is the best-F1 score on ``val`` and is then
applied unchanged to every test split.

Every score is given twice: ``raw``, the boxes as the model returns them, and
``worktop``, after the worktop filter (:func:`labvision.evaluation.on_worktop`),
which keeps a box only if its base casts onto the bench and its height fits a
bottle standing there. The filter uses the camera's calibration, never an
object's pose; it is what removes the gantry's shelf bottles.

    python scripts/fixedcam_bench.py run world-l-bottles --splits val,test
    python scripts/fixedcam_bench.py run yoloe-26l-bottles+tile640x2 --max 20
    python scripts/fixedcam_bench.py run ft:runs/fixedcam/yolo26n/weights/best.pt
    python scripts/fixedcam_bench.py summary
    python scripts/fixedcam_bench.py compare MODEL_A MODEL_B --splits test --max 30

A model name is a key of :data:`MODELS`, optionally followed by
``+tile<T>x<S>`` to run it on T-pixel tiles of the worktop region upsampled S
times, ``+roi`` / ``+roix<S>`` to run it once on the worktop region,
enlarged S times, or ``+scale<S>`` to resize the whole frame by S;
``ft:<weights>`` for fine-tuned Ultralytics weights; or
``rfdetr:<checkpoint>:<size>:<resolution>`` for a fine-tuned RF-DETR, tiled at
its resolution. Output: ``results/fixedcam/<model>/<split>/predictions.json``,
``results/fixedcam/<model>/metrics.json``, overlays next to them, and
``results/fixedcam/summary.md``.
"""

import argparse
import functools
import json
import re
import statistics
import sys
import time
from collections import Counter
from collections.abc import Callable
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fixedcam_models as fm  # noqa: E402

from labvision import evaluation as ev  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "simulation" / "out" / "fixedcam"
RESULTS = REPO / "computer-vision" / "results" / "fixedcam"
CATEGORIES = ("other", "sample", "shelf_bottle", "glassware", "balance", "instrument")
"""Values of the ``*_cat.png`` maps, as ``render_perfumery.py`` writes them."""


def visual_prompt_reference(split: str = "val", frame_index: int = 3) -> tuple:
    """Take one validation frame and its bench bottles as YOLOE visual prompts

    The boxes are the kit examples a person would draw once by hand on a
    single frame; nothing is trained. The frame comes from ``val``, never from
    a test split.
    """
    gt = json.loads((DATA / split / "gt.json").read_text(encoding="utf-8"))
    frame = gt["frames"][frame_index]
    image = cv2.imread(str(DATA / split / frame["file"]))
    boxes, kits = [], []
    for bottle in frame["bottles"]:
        if ev.is_required(bottle):
            boxes.append(bottle["xyxy"])
            kits.append(0 if bottle["phase"] == "liquid" else 1)
    return image, np.array(boxes, dtype=np.float32), np.array(kits, dtype=np.int64)


MODELS: dict[str, Callable[[], object]] = {
    "world-l-generic": lambda: fm.UltralyticsPredictor(
        "yolov8l-worldv2.pt", "world", fm.GENERIC_PROMPTS
    ),
    "world-l-bottles": lambda: fm.UltralyticsPredictor(
        "yolov8l-worldv2.pt", "world", fm.BOTTLE_PROMPTS
    ),
    "yoloe-26l-bottles": lambda: fm.UltralyticsPredictor(
        "yoloe-26l-seg.pt", "yoloe", fm.BOTTLE_PROMPTS
    ),
    "yoloe-11l-bottles": lambda: fm.UltralyticsPredictor(
        "yoloe-11l-seg.pt", "yoloe", fm.BOTTLE_PROMPTS
    ),
    "yoloe-26l-visual": lambda: fm.UltralyticsPredictor(
        "yoloe-26l-seg.pt", "yoloe", visual=visual_prompt_reference()
    ),
    "yoloe-11l-visual": lambda: fm.UltralyticsPredictor(
        "yoloe-11l-seg.pt", "yoloe", visual=visual_prompt_reference()
    ),
    "coco-yolo11s": lambda: fm.UltralyticsPredictor(
        "yolo11s.pt", "yolo", fm.COCO_VESSELS
    ),
    "coco-yolo26s": lambda: fm.UltralyticsPredictor(
        "yolo26s.pt", "yolo", fm.COCO_VESSELS
    ),
    "coco-yolo26l": lambda: fm.UltralyticsPredictor(
        "yolo26l.pt", "yolo", fm.COCO_VESSELS
    ),
    "gdino-tiny": lambda: fm.GroundingDinoPredictor(prompts=fm.BOTTLE_PROMPTS),
    "chemex-bottles": lambda: fm.RoboflowPredictor(
        "chemistry-lab-object-detection", 1, fm.CHEMEX_BOTTLES
    ),
}
"""Pretrained models, built on demand. Fine-tuned ones come by path."""

TILE_SUFFIX = re.compile(r"^(?P<base>.+)\+tile(?P<tile>\d+)x(?P<scale>[\d.]+)$")
ROI_SUFFIX = re.compile(r"^(?P<base>.+)\+roi(?:x(?P<scale>[\d.]+))?$")
SCALE_SUFFIX = re.compile(r"^(?P<base>.+)\+scale(?P<scale>[\d.]+)$")


def slug(name: str) -> str:
    """Turn a model name into a folder name"""
    return re.sub(r"[^A-Za-z0-9._+-]+", "_", name.replace(":", "=")).strip("_")[:120]


def build(name: str, gt: dict | None = None) -> object:
    """Build the predictor a model name stands for"""
    match = TILE_SUFFIX.match(name)
    if match:
        tile, scale = int(match["tile"]), float(match["scale"])
        inner = build_inner(match["base"], imgsz=int(round(tile * scale / 32) * 32))
        return fm.TiledPredictor(
            inner, tile=tile, upscale=scale, roi=roi_for(gt) if gt else None
        )
    match = SCALE_SUFFIX.match(name)
    if match:
        # The whole frame resized: puts bottles back at the scale a model
        # was trained on when a camera sees them larger or smaller.
        return fm.RoiPredictor(
            build_inner(match["base"]), upscale=float(match["scale"])
        )
    match = ROI_SUFFIX.match(name)
    if match:
        scale = float(match["scale"] or 1.0)
        return fm.RoiPredictor(
            build_inner(match["base"]), roi=roi_for(gt) if gt else None, upscale=scale
        )
    if name.startswith("rfdetr:"):
        weights, size, resolution = name.removeprefix("rfdetr:").rsplit(":", 2)
        inner = fm.RfDetrPredictor(weights, size=size, resolution=int(resolution))
        return fm.TiledPredictor(
            inner, tile=int(resolution), roi=roi_for(gt) if gt else None
        )
    return build_inner(name)


def build_inner(name: str, imgsz: int | None = None) -> object:
    """Build an untiled predictor, at a fixed input size if given"""
    if name.startswith("ft:"):
        return fm.UltralyticsPredictor(name[3:], "yolo", None, imgsz=imgsz)
    if name not in MODELS:
        raise SystemExit(f"unknown model {name!r}; one of {sorted(MODELS)}")
    predictor = MODELS[name]()
    if imgsz is not None and hasattr(predictor, "imgsz"):
        predictor.imgsz = imgsz
    return predictor


def roi_for(gt: dict) -> Callable[[dict], tuple[int, int, int, int]]:
    """Return the worktop-region function for the frames of one split"""
    worktop = ev.Worktop.from_gt(gt)
    return lambda frame: fm.worktop_roi(frame, worktop)


def frame_stamp(folder: Path, frames: list[dict]) -> dict[str, list[int]]:
    """Size and modification time of every frame, to spot a re-render"""
    stamp = {}
    for frame in frames:
        st = (folder / frame["file"]).stat()
        stamp[frame["file"]] = [st.st_size, st.st_mtime_ns]
    return stamp


def weights_stamp(name: str) -> list[int] | None:
    """Size and date of a fine-tuned model's weights file, to spot a new checkpoint"""
    base = re.sub(r"\+(tile|roi).*$", "", name)
    if base.startswith("ft:"):
        path = Path(base[3:])
    elif base.startswith("rfdetr:"):
        path = Path(base.removeprefix("rfdetr:").rsplit(":", 2)[0])
    else:
        return None
    if not path.exists():
        return None
    st = path.stat()
    return [st.st_size, st.st_mtime_ns]


def load_split(split: str) -> tuple[Path, dict]:
    """Return a split's folder and its ground truth"""
    folder = DATA / split
    gt_path = folder / "gt.json"
    if not gt_path.exists():
        raise SystemExit(f"no {gt_path}; render it with fixedcam_dataset.py")
    return folder, json.loads(gt_path.read_text(encoding="utf-8"))


def predict_split(
    name: str, split: str, limit: int | None, redo: bool, cached_only: bool = False
) -> tuple[dict | None, list[dict]]:
    """Run a model over a split, or read its cached boxes

    Returns:
        The cache (frame file to boxes and milliseconds) and the frames scored.
        With ``cached_only``, the cache is None when it does not cover them all.
    """
    folder, gt = load_split(split)
    frames = gt["frames"][:limit] if limit else gt["frames"]
    out = RESULTS / slug(name) / split
    out.mkdir(parents=True, exist_ok=True)
    cache_path = out / "predictions.json"
    stamp = frame_stamp(folder, frames)
    fresh = {"_model": weights_stamp(name)}
    cache: dict = dict(fresh)
    if cache_path.exists() and not redo:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
        old = cache.get("_frames", {})
        if any(f in old and old[f] != s for f, s in stamp.items()):
            print(f"{cache_path} was made on other frames, running again")
            cache = dict(fresh)
        elif cache.get("_model") != fresh["_model"]:
            print(f"{cache_path} was made with other weights, running again")
            cache = dict(fresh)
    if cached_only and any(f["file"] not in cache for f in frames):
        return None, frames
    todo = [f for f in frames if f["file"] not in cache]
    if todo:
        predictor = build(name, gt)
        first = cv2.imread(str(folder / todo[0]["file"]))
        if hasattr(predictor, "frame"):
            predictor.frame = todo[0]
        predictor.predict(first)  # warm up at the frame's size
        for k, frame in enumerate(todo):
            image = cv2.imread(str(folder / frame["file"]))
            if hasattr(predictor, "frame"):
                predictor.frame = frame
            start = time.perf_counter()
            dets = predictor.predict(image)
            ms = 1000.0 * (time.perf_counter() - start)
            cache[frame["file"]] = {
                "ms": round(ms, 1),
                "boxes": [
                    [*(round(v, 1) for v in d.box), round(d.score, 4), d.cls]
                    for d in dets
                ],
            }
            print(
                f"[{name} | {split}] {k + 1}/{len(todo)} {frame['file']}: "
                f"{len(dets)} boxes, {ms:.0f} ms",
                flush=True,
            )
            if (k + 1) % 10 == 0:  # so an interrupted run resumes here
                save_cache(cache_path, cache, stamp)
        save_cache(cache_path, cache, stamp)
    return cache, frames


def save_cache(path: Path, cache: dict, stamp: dict) -> None:
    """Write the cached boxes with the stamps of the frames they cover"""
    done = {f: v for f, v in stamp.items() if f in cache}
    cache["_frames"] = {**cache.get("_frames", {}), **done}
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(cache), encoding="utf-8")
    tmp.replace(path)


def detections(entry: dict) -> list[ev.Detection]:
    """Turn cached boxes back into detections"""
    return [ev.Detection(tuple(b[:4]), b[4], int(b[5])) for b in entry["boxes"]]


@functools.lru_cache(maxsize=64)
def category_map(path: str) -> np.ndarray | None:
    """Read a frame's per-pixel category map"""
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)


def what_is_under(box, categories: np.ndarray | None) -> str:
    """Name what a false box mostly covers, preferring any object to scenery"""
    if categories is None:
        return "other"
    u0, v0, u1, v1 = (int(round(v)) for v in box)
    patch = categories[max(v0, 0) : max(v1, 1), max(u0, 0) : max(u1, 1)]
    if patch.size == 0:
        return "other"
    counts = np.bincount(patch.reshape(-1), minlength=len(CATEGORIES))
    counts[0] = 0
    best = int(counts.argmax())
    return CATEGORIES[best] if counts[best] >= 0.15 * patch.size else "other"


def score(
    split: str, frames: list[dict], cache: dict, gt: dict, *, worktop: bool,
    threshold: float | None, boot: int = 1000,
) -> dict:  # fmt: skip
    """Score one split with or without the worktop filter

    Args:
        split: Split name, for the category maps.
        frames: The frames to score.
        cache: Cached boxes per frame file.
        gt: The split's ground truth, for the worktop.
        worktop: Whether to apply the worktop filter first.
        threshold: Operating threshold; None picks the best-F1 one here (val).
        boot: Bootstrap resamples for the intervals; 0 skips them.
    """
    top = ev.Worktop.from_gt(gt)
    by_iou: dict[float, list[ev.FrameResult]] = {t: [] for t in ev.IOU_THRESHOLDS}
    kit_frames: list[tuple[list[ev.Truth], list[ev.Detection]]] = []
    has_kits = False
    ms = []
    for frame in frames:
        entry = cache[frame["file"]]
        ms.append(entry["ms"])
        dets = detections(entry)
        if worktop:
            dets = [d for d in dets if ev.on_worktop(frame, d.box, top)]
        has_kits |= any(d.cls >= 0 for d in dets)
        truths = ev.truths_of(frame)
        for t in ev.IOU_THRESHOLDS:
            by_iou[t].append(ev.match_frame(truths, dets, t))
        kit_frames.append((truths, dets))
    at50 = by_iou[0.5]
    chosen = threshold
    best_f1 = None
    if chosen is None:
        chosen, best_f1 = ev.best_f1_threshold(at50)
    point = ev.operating_point(at50, chosen)
    folder = DATA / split
    false_on: Counter = Counter()
    for frame, result in zip(frames, at50, strict=True):
        for det in result.false_boxes:
            if det.score >= chosen:
                cat = category_map(str(folder / frame.get("categories", "")))
                false_on[what_is_under(det.box, cat)] += 1
    out = {
        "frames": len(frames),
        "ap50": ev.ap_at(at50),
        "ap": float(np.nanmean([ev.ap_at(by_iou[t]) for t in ev.IOU_THRESHOLDS])),
        "kit_ap50": ev.kit_ap(kit_frames) if has_kits else None,
        "threshold": chosen,
        "threshold_from": "this split (best F1)" if threshold is None else "val",
        "best_f1_here": best_f1,
        **{k: v for k, v in point.items() if k != "threshold"},
        "by_kind": {
            k: v
            for k, v in sorted(
                ev.breakdown(at50, chosen, lambda t: t.kind).items(),
                key=lambda kv: (
                    ev.KINDS.index(kv[0]) if kv[0] in ev.KINDS else len(ev.KINDS)
                ),
            )
        },
        "by_side": {
            k: v
            for k, v in sorted(
                ev.breakdown(at50, chosen, lambda t: ev.side_bucket(t.side_px)).items(),
                key=lambda kv: ev.side_buckets().index(kv[0]),
            )
        },
        "false_on": dict(false_on.most_common()),
        "ms_median": statistics.median(ms) if ms else None,
    }
    if boot:
        out["ap50_ci"] = ev.bootstrap(at50, ev.ap_at, reps=boot)
        out["recall_ci"] = ev.bootstrap(
            at50, lambda rs: ev.operating_point(rs, chosen)["recall"], reps=boot
        )
    return out


def draw_overlay(
    folder: Path, frame: dict, dets: list[ev.Detection], threshold: float, path: Path
) -> None:
    """Draw truth and boxes: green found, magenta missed, grey ignored, red false"""
    image = cv2.imread(str(folder / frame["file"]))
    truths = ev.truths_of(frame)
    kept = [d for d in dets if d.score >= threshold]
    result = ev.match_frame(truths, kept)

    def rect(box, colour, width=2):
        p0 = (int(box[0]) - 1, int(box[1]) - 1)
        p1 = (int(box[2]) + 1, int(box[3]) + 1)
        cv2.rectangle(image, p0, p1, colour, width)

    for truth in truths:
        if not truth.required:
            rect(truth.box, (170, 170, 170), 1)
    for truth, found in zip(result.truths, result.found, strict=True):
        rect(truth.box, (0, 200, 0) if found is not None else (255, 0, 255))
    for det in result.false_boxes:
        rect(det.box, (0, 0, 255))
    cv2.imwrite(str(path), image, [cv2.IMWRITE_JPEG_QUALITY, 85])


def threshold_split(split: str) -> str:
    """Name the split whose best-F1 threshold ``split`` is scored at

    Every split of a scene takes it from that scene's validation split: the
    rail scene's from ``rail_val``, the others from ``val``.
    """
    return "rail_val" if split.startswith("rail_") else "val"


def score_both(
    split: str, frames: list[dict], cache: dict, gt: dict, metrics: dict, args
) -> dict:
    """Score a split raw and filtered, at its validation split's thresholds"""
    entry = {}
    source = threshold_split(split)
    for mode in ("raw", "worktop"):
        threshold = None
        if split != source:
            threshold = metrics.get(source, {}).get(mode, {}).get("threshold")
            if threshold is None and not args.threshold_here:
                raise SystemExit(
                    f"score {source} first: {split} takes its threshold from it "
                    "(or pass --threshold-here to pick it on this split)"
                )
        entry[mode] = score(
            split, frames, cache, gt, worktop=mode == "worktop",
            threshold=threshold, boot=args.boot,
        )  # fmt: skip
        if threshold is not None:
            entry[mode]["threshold_from"] = source
    return entry


def run(args: argparse.Namespace) -> None:
    """Predict, score and write metrics for one model over the given splits"""
    splits = [s.strip() for s in args.splits.split(",") if s.strip()]
    # Validation splits first: they set the thresholds.
    splits.sort(key=lambda s: threshold_split(s) != s)
    root = RESULTS / slug(args.model)
    metrics_path = root / "metrics.json"
    metrics = (
        json.loads(metrics_path.read_text(encoding="utf-8"))
        if metrics_path.exists()
        else {}
    )
    metrics["model"] = args.model
    for split in splits:
        cache, frames = predict_split(args.model, split, args.max, args.redo)
        folder, gt = load_split(split)
        entry = score_both(split, frames, cache, gt, metrics, args)
        metrics[split] = entry
        if args.overlays:
            over = root / split / "overlays"
            over.mkdir(parents=True, exist_ok=True)
            top = ev.Worktop.from_gt(gt)
            for frame in frames[: args.overlays]:
                dets = [
                    d
                    for d in detections(cache[frame["file"]])
                    if ev.on_worktop(frame, d.box, top)
                ]
                draw_overlay(
                    folder, frame, dets, entry["worktop"]["threshold"],
                    over / frame["file"].replace(".png", ".jpg"),
                )  # fmt: skip
        w = entry["worktop"]
        print(
            f"\n{args.model} | {split} | worktop filter: AP50 {w['ap50']:.3f} "
            f"AP {w['ap']:.3f} recall {w['recall']:.3f} precision "
            f"{w['precision']:.3f} false/frame {w['false_per_frame']:.2f} "
            f"at {w['threshold']:.3f}, {w['ms_median']:.0f} ms/frame\n",
            flush=True,
        )
    # New validation thresholds: rescore the other splits already on file.
    sources = {s for s in splits if threshold_split(s) == s}
    for split in [k for k in metrics if k not in ("model", *splits)]:
        if threshold_split(split) not in sources:
            continue
        cache, frames = predict_split(args.model, split, None, False, True)
        if cache is None:
            print(f"{split}: cached boxes incomplete, not rescored")
            continue
        _, gt = load_split(split)
        metrics[split] = score_both(split, frames, cache, gt, metrics, args)
        print(f"{split}: rescored with the new {threshold_split(split)} thresholds")
    root.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=1), encoding="utf-8")


def fmt_ci(value: float, ci) -> str:
    """Format a proportion with its interval, e.g. ``0.91 [0.88-0.93]``"""
    if value is None or value != value:
        return "-"
    if not ci:
        return f"{value:.3f}"
    return f"{value:.3f} [{ci[0]:.2f}-{ci[1]:.2f}]"


def summary(args: argparse.Namespace) -> None:
    """Write one markdown table over every scored model and split"""
    rows = []
    for path in sorted(RESULTS.glob("*/metrics.json")):
        metrics = json.loads(path.read_text(encoding="utf-8"))
        for split, entry in metrics.items():
            if split == "model" or (args.splits and split not in args.splits):
                continue
            for mode in ("worktop", "raw") if args.raw else ("worktop",):
                m = entry[mode]
                kinds = m["by_kind"]
                small = [kinds.get(k, [0, 0]) for k in ("amber 10 ml", "amber 20 ml")]
                found, need = sum(s[0] for s in small), sum(s[1] for s in small)
                rows.append(
                    (split, mode, metrics["model"], m["frames"],
                     fmt_ci(m["ap50"], m.get("ap50_ci")), f"{m['ap']:.3f}",
                     fmt_ci(m["recall"], m.get("recall_ci")),
                     f"{m['precision']:.3f}", f"{m['false_per_frame']:.2f}",
                     f"{found / need:.2f}" if need else "-",
                     f"{m['threshold']:.3f}", f"{m['ms_median']:.0f}")
                )  # fmt: skip

    def ap_of(row: tuple) -> float:
        try:
            return -float(row[4].split()[0])
        except ValueError:
            return 0.0

    rows.sort(key=lambda r: (r[0], r[1], ap_of(r)))
    header = (
        "| split | filter | model | frames | AP50 [95 % CI] | AP50:95 | recall "
        "[95 % CI] | precision | false/frame | amber 10-20 ml recall | "
        "threshold | ms/frame |"
    )
    lines = ["# Fixed-camera detector benchmark", "", header,
             "|" + " --- |" * 12]  # fmt: skip
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    text = "\n".join(lines) + "\n"
    (RESULTS / "summary.md").write_text(text, encoding="utf-8")
    print(text)


def compare(args: argparse.Namespace) -> None:
    """Score several models on exactly the same frames, from their cached boxes

    Each model keeps its own val threshold; nothing is run and no model's
    ``metrics.json`` is touched. The table goes to stdout and, with ``--out``,
    to a JSON file.
    """
    splits = [s.strip() for s in args.splits.split(",") if s.strip()]
    table: dict[str, dict] = {}
    for name in args.models:
        path = RESULTS / slug(name) / "metrics.json"
        if not path.exists():
            print(f"{name}: not scored yet")
            continue
        metrics = json.loads(path.read_text(encoding="utf-8"))
        for split in splits:
            cache, frames = predict_split(name, split, args.max, False, True)
            if cache is None:
                print(f"{name}: cached boxes do not cover {split}[:{args.max}]")
                continue
            _, gt = load_split(split)
            entry = score_both(split, frames, cache, gt, metrics, args)["worktop"]
            table.setdefault(split, {})[name] = entry
    lines = []
    for split, rows in table.items():
        lines += [f"## {split}", "",
                  "| model | frames | AP50 [95 % CI] | AP50:95 | recall [95 % CI] "
                  "| precision | false/frame | s/frame |",
                  "|" + " --- |" * 8]  # fmt: skip
        for name, m in rows.items():
            lines.append(
                f"| {name} | {m['frames']} | {fmt_ci(m['ap50'], m.get('ap50_ci'))} "
                f"| {m['ap']:.3f} | {fmt_ci(m['recall'], m.get('recall_ci'))} "
                f"| {m['precision']:.3f} | {m['false_per_frame']:.2f} "
                f"| {m['ms_median'] / 1000:.1f} |"
            )
        lines.append("")
    text = "\n".join(lines)
    print(text)
    if args.out:
        Path(args.out).write_text(json.dumps(table, indent=1), encoding="utf-8")


def main() -> None:
    """Parse the command line"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p_run = sub.add_parser("run", help="predict and score one model")
    p_run.add_argument("model")
    p_run.add_argument("--splits", default="val")
    p_run.add_argument("--max", type=int, default=None, help="first N frames only")
    p_run.add_argument("--redo", action="store_true", help="ignore cached boxes")
    p_run.add_argument("--overlays", type=int, default=6, help="frames to draw")
    p_run.add_argument("--boot", type=int, default=1000, help="bootstrap resamples")
    p_run.add_argument(
        "--max-det",
        type=int,
        default=fm.MAX_DET,
        help="most boxes per image; run with --redo when changing it",
    )
    p_run.add_argument(
        "--threshold-here",
        action="store_true",
        help="pick the threshold on a test split when val is not scored",
    )
    p_sum = sub.add_parser("summary", help="table over every scored model")
    p_sum.add_argument("--splits", nargs="*", default=None)
    p_sum.add_argument("--raw", action="store_true", help="also the unfiltered rows")
    p_cmp = sub.add_parser("compare", help="several models on the same frames")
    p_cmp.add_argument("models", nargs="+")
    p_cmp.add_argument("--splits", default="test")
    p_cmp.add_argument("--max", type=int, default=None, help="first N frames only")
    p_cmp.add_argument("--boot", type=int, default=1000, help="bootstrap resamples")
    p_cmp.add_argument("--out", default=None, help="also write the table as JSON")
    p_cmp.set_defaults(threshold_here=False)
    args = parser.parse_args()
    if args.command == "run":
        fm.MAX_DET = args.max_det
        run(args)
    elif args.command == "compare":
        compare(args)
    else:
        summary(args)


if __name__ == "__main__":
    main()
