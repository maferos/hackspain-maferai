"""Score the detector and the geometric size classifier on rendered bottle frames

Takes the frames and ``gt.json`` written by ``render_bottles.py``, runs a
detector backend on every frame at the frame's own resolution, matches its
boxes to the true ones, and answers three questions per bottle size:

1. Is the bottle found at all?
2. Given its box, does the geometry pick the right size? Every vessel class
   in :data:`labvision.scene.VESSELS` is fitted with the ``fit`` anchor and the
   one with the smallest residual wins. Scored twice: on the detector's box
   and on the exact box, so detector noise and geometric ambiguity are
   separated.
3. How far is the fitted position from the true one, in millimetres?

The cap matters. ``--cap-model scene`` takes the silhouette height from
:meth:`labvision.scene.Vessel.silhouette_height_m`, which stacks the cap on
top of the body. ``--cap-model kit`` (the default) follows the bottle kit's own
README, which seats the cap over the neck so a closed bottle is only 1 mm
taller than its body height; that is how ``render_bottles.py`` closes them.

    python scripts/size_experiment.py ../simulation/out/bottles_1920x1080
    python scripts/size_experiment.py ../simulation/out/bottles_1920x1080 --backend both
    python scripts/size_experiment.py ../simulation/out/bottles_1920x1080 --oracle-only

Writes ``size_experiment_<backend>_<cap model>.json`` and ``.md`` next to the frames.
"""

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision.camera import Camera, GeometryError  # noqa: E402
from labvision.detector import BACKENDS, Detector, draw  # noqa: E402
from labvision.scene import VESSELS, BBox, gopro_intrinsics, locate  # noqa: E402

CAP_MODELS = ("kit", "scene")
RANGE_EDGES_M = (3.0, 3.5, 4.0)
"""Camera-to-bottle distance buckets; the bench runs from 2.9 m to 4.4 m."""


def range_bucket(camera_pos: np.ndarray, position) -> str:
    """Label the distance from the camera to a bottle by :data:`RANGE_EDGES_M`"""
    r = float(np.linalg.norm(np.asarray(position, float) - camera_pos))
    lo = None
    for edge in RANGE_EDGES_M:
        if r < edge:
            return f"< {edge:.1f} m" if lo is None else f"{lo:.1f}-{edge:.1f} m"
        lo = edge
    return f"> {lo:.1f} m"


def range_labels() -> list[str]:
    """All bucket labels, nearest first"""
    labels, lo = [], None
    for edge in RANGE_EDGES_M:
        labels.append(f"< {edge:.1f} m" if lo is None else f"{lo:.1f}-{edge:.1f} m")
        lo = edge
    return [*labels, f"> {lo:.1f} m"]


def silhouette_height(vessel: str, cap_model: str) -> float:
    """Height of a closed bottle's silhouette under the chosen cap convention"""
    spec = VESSELS[vessel]
    if cap_model == "scene":
        return spec.silhouette_height_m(capped=True)
    return spec.height_m + 0.001


def iou(a, b) -> float:
    """Intersection over union of two xyxy boxes"""
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


def fit(bbox: BBox, camera: Camera, vessel: str, cap_model: str):
    """Fit one vessel class to a box, or None if the geometry rejects it"""
    try:
        return locate(
            bbox,
            camera,
            vessel=VESSELS[vessel],
            height=silhouette_height(vessel, cap_model),
            anchor="fit",
        )
    except GeometryError:
        return None


def classify(
    bbox: BBox, camera: Camera, candidates: list[str], cap_model: str
) -> tuple[str | None, dict[str, float]]:
    """Return the vessel class whose fitted box matches best, and every residual"""
    residuals: dict[str, float] = {}
    for name in candidates:
        placement = fit(bbox, camera, name, cap_model)
        if placement is None or placement.residual_px is None:
            continue
        if np.isfinite(placement.residual_px):
            residuals[name] = float(placement.residual_px)
    if not residuals:
        return None, residuals
    return min(residuals, key=residuals.get), residuals


def position_error_mm(
    bbox: BBox, camera: Camera, vessel: str, truth, cap_model: str
) -> float | None:
    """Fitted base position error against the truth, for the true vessel class"""
    placement = fit(bbox, camera, vessel, cap_model)
    if placement is None:
        return None
    offset = placement.position[:2] - np.asarray(truth[:2])
    return float(np.linalg.norm(offset) * 1000.0)


def run(backend: str | None, folder: Path, gt: dict, args) -> dict:
    """Run one backend over the frames and return the scores"""
    intrinsics = gopro_intrinsics(gt["width"], gt["height"], lens=gt["lens"])
    camera = Camera.from_mujoco(intrinsics, gt["camera"]["pos"], gt["camera"]["xmat"])
    candidates = [v for v in VESSELS if args.include_wide or v != "bottle_1000ml_wide"]
    detector = None
    overlay_dir = None
    if backend is not None:
        detector = Detector(
            backend, input_px=args.input_px, score=args.score, device=args.device
        )
        detector.warmup((gt["height"], gt["width"], 3))
        overlay_dir = folder / f"overlay_{backend}"
        overlay_dir.mkdir(exist_ok=True)

    camera_pos = np.asarray(gt["camera"]["pos"], float)
    per: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    by_range: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    oracle_confusion: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    false_positives = 0
    frames_done = 0
    for frame in gt["frames"]:
        image = cv2.imread(str(folder / frame["file"]))
        boxes = detector.detect(image) if detector else []
        truths = [b for b in frame["bottles"] if b["pixels"] >= args.min_pixels]
        taken: set[int] = set()
        for truth in truths:
            vessel = truth["vessel"]
            per[vessel]["n"].append(1)
            bucket = range_bucket(camera_pos, truth["position"])
            by_range[bucket]["n"].append(1)
            exact = BBox(*truth["xyxy"])
            oracle, _ = classify(exact, camera, candidates, args.cap_model)
            per[vessel]["oracle_ok"].append(int(oracle == vessel))
            by_range[bucket]["oracle_ok"].append(int(oracle == vessel))
            oracle_confusion[vessel][oracle or "none"] += 1
            err = position_error_mm(
                exact, camera, vessel, truth["position"], args.cap_model
            )
            if err is not None:
                per[vessel]["oracle_pos_mm"].append(err)
            best, best_iou = None, args.iou
            for j, box in enumerate(boxes):
                if j in taken:
                    continue
                v = iou(box.bbox.as_tuple(), truth["xyxy"])
                if v > best_iou:
                    best, best_iou = j, v
            per[vessel]["found"].append(int(best is not None))
            by_range[bucket]["found"].append(int(best is not None))
            if best is None:
                continue
            taken.add(best)
            predicted, _ = classify(
                boxes[best].bbox, camera, candidates, args.cap_model
            )
            per[vessel]["size_ok"].append(int(predicted == vessel))
            by_range[bucket]["size_ok"].append(int(predicted == vessel))
            confusion[vessel][predicted or "none"] += 1
            err = position_error_mm(
                boxes[best].bbox, camera, vessel, truth["position"], args.cap_model
            )
            if err is not None:
                per[vessel]["pos_mm"].append(err)
        # A box on a bottle too small to be required is not held against the
        # detector: finding it was not asked for, but it is not wrong either.
        small = [b for b in frame["bottles"] if b["pixels"] < args.min_pixels]
        for j, box in enumerate(boxes):
            if j in taken:
                continue
            if any(iou(box.bbox.as_tuple(), b["xyxy"]) > args.iou for b in small):
                continue
            false_positives += 1
        frames_done += 1
        if overlay_dir is not None:
            cv2.imwrite(str(overlay_dir / frame["file"]), draw(image, boxes))
        print(
            f"[{backend or 'oracle'}] {frame['file']}: {len(boxes)} boxes, "
            f"{len(truths)} bottles",
            flush=True,
        )

    rows = []
    for vessel in candidates:
        d = per.get(vessel)
        if not d:
            continue
        n = len(d["n"])
        found = sum(d["found"])
        rows.append(
            {
                "vessel": vessel,
                "n": n,
                "found_pct": round(100.0 * found / n, 1),
                "size_ok_pct": round(100.0 * sum(d["size_ok"]) / found, 1)
                if found
                else None,
                "oracle_ok_pct": round(100.0 * sum(d["oracle_ok"]) / n, 1),
                "pos_mm_median": round(statistics.median(d["pos_mm"]), 1)
                if d["pos_mm"]
                else None,
                "oracle_pos_mm_median": round(statistics.median(d["oracle_pos_mm"]), 1)
                if d["oracle_pos_mm"]
                else None,
            }
        )
    range_rows = []
    for label in range_labels():
        d = by_range.get(label)
        if not d:
            continue
        n, found = len(d["n"]), sum(d["found"])
        range_rows.append(
            {
                "range": label,
                "n": n,
                "found_pct": round(100.0 * found / n, 1),
                "size_ok_pct": round(100.0 * sum(d["size_ok"]) / found, 1)
                if found
                else None,
                "oracle_ok_pct": round(100.0 * sum(d["oracle_ok"]) / n, 1),
            }
        )
    return {
        "backend": backend or "oracle",
        "cap_model": args.cap_model,
        "input_px": args.input_px or max(gt["width"], gt["height"]),
        "frames": frames_done,
        "false_positives_per_frame": round(false_positives / max(frames_done, 1), 2),
        "rows": rows,
        "by_range": range_rows,
        "confusion": {k: dict(v) for k, v in confusion.items()},
        "oracle_confusion": {k: dict(v) for k, v in oracle_confusion.items()},
    }


def _matrix(title: str, names: list[str], confusion: dict) -> list[str]:
    """Markdown lines for one confusion matrix"""
    short = [n.replace("bottle_", "") for n in names]
    lines = [
        "",
        f"{title}: true \\ predicted | " + " | ".join(short) + " | none",
        "|---|" + "---|" * (len(names) + 1),
    ]
    for t in names:
        row = confusion.get(t, {})
        cells = " | ".join(str(row.get(p, 0)) for p in names)
        lines.append(f"| {t.replace('bottle_', '')} | {cells} | {row.get('none', 0)} |")
    return lines


def to_markdown(result: dict) -> str:
    """Render the scores as Markdown tables plus the confusion matrices"""
    lines = [
        f"backend `{result['backend']}`, cap model `{result['cap_model']}`, "
        f"input {result['input_px']} px, {result['frames']} frames, "
        f"{result['false_positives_per_frame']} false boxes per frame",
        "",
        "| bottle | n | found | size right (detector box) "
        "| size right (exact box) | position error, detector box | exact box |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in result["rows"]:
        size_ok = "-" if r["size_ok_pct"] is None else f"{r['size_ok_pct']} %"
        pos = "-" if r["pos_mm_median"] is None else f"{r['pos_mm_median']} mm"
        opos = (
            "-"
            if r["oracle_pos_mm_median"] is None
            else f"{r['oracle_pos_mm_median']} mm"
        )
        lines.append(
            f"| {r['vessel']} | {r['n']} | {r['found_pct']} % | {size_ok} "
            f"| {r['oracle_ok_pct']} % | {pos} | {opos} |"
        )
    lines += [
        "",
        "| distance to camera | n | found | size right (detector box) "
        "| size right (exact box) |",
        "|---|---|---|---|---|",
    ]
    for r in result["by_range"]:
        size_ok = "-" if r["size_ok_pct"] is None else f"{r['size_ok_pct']} %"
        lines.append(
            f"| {r['range']} | {r['n']} | {r['found_pct']} % | {size_ok} "
            f"| {r['oracle_ok_pct']} % |"
        )
    names = [r["vessel"] for r in result["rows"]]
    lines += _matrix("detector boxes", names, result["confusion"])
    lines += _matrix("exact boxes", names, result["oracle_confusion"])
    return "\n".join(lines) + "\n"


def main() -> None:
    """Score one or both backends and write the results next to the frames"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder", help="output folder of render_bottles.py")
    parser.add_argument("--backend", default="world", choices=[*BACKENDS, "both"])
    parser.add_argument("--oracle-only", action="store_true", help="skip the detector")
    parser.add_argument("--cap-model", default="kit", choices=CAP_MODELS)
    parser.add_argument(
        "--input-px", type=int, default=None, help="default: frame size"
    )
    parser.add_argument("--score", type=float, default=None)
    parser.add_argument("--device", default=None)
    parser.add_argument("--iou", type=float, default=0.5, help="match threshold")
    parser.add_argument(
        "--min-pixels", type=int, default=150, help="skip smaller bottles"
    )
    parser.add_argument("--include-wide", action="store_true")
    args = parser.parse_args()

    folder = Path(args.folder)
    gt = json.loads((folder / "gt.json").read_text(encoding="utf-8"))
    if args.oracle_only:
        backends: list[str | None] = [None]
    elif args.backend == "both":
        backends = ["world", "coco"]
    else:
        backends = [args.backend]
    for backend in backends:
        result = run(backend, folder, gt, args)
        stem = f"size_experiment_{backend or 'oracle'}_{args.cap_model}"
        (folder / f"{stem}.json").write_text(json.dumps(result, indent=1))
        md = to_markdown(result)
        (folder / f"{stem}.md").write_text(md, encoding="utf-8")
        print("\n" + md)


if __name__ == "__main__":
    main()
