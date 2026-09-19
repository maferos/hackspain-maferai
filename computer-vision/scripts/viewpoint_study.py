"""Score a bottle detector by where the camera stands, not only overall

``fixedcam_bench.py`` gives one number per split. This breaks a split's frames
down by what ``fixedcam_dataset.py`` drew for them, to show which views a
detector fails on: the camera's elevation above the bench and its distance
from its aim point (``orbit_*`` splits), and for every split the bottle's
height in pixels and how far from the frame's centre it stands. Each row is
recall and false boxes per frame at one threshold, plus AP at IoU 0.5.

    python scripts/viewpoint_study.py rail --splits orbit_test,rail_test
    python scripts/viewpoint_study.py runs/orbit/yolo26s_rail_orbit/weights/best.pt \
        --threshold 0.2 --splits orbit_test

WEIGHTS is a backend of :data:`labvision.detector.BACKENDS`, which brings its
threshold, or a path; ``--pick-on SPLITS`` takes the best-F1 threshold over
those validation splits instead. Boxes are cached next to the results, so a second run
with another threshold costs nothing. Output:
``results/viewpoint/<name>/<split>.json`` and a Markdown table on stdout.
"""

import argparse
import json
import math
import sys
import time
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bench_crop import bench_crop  # noqa: E402
from fixedcam_dataset import DEFAULT_OUT  # noqa: E402

from labvision import detector as det  # noqa: E402
from labvision import evaluation as ev  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results" / "viewpoint"

ELEVATION_BINS = (30, 45, 60, 75, 90)
RANGE_BINS = (0.35, 1.0, 1.75, 2.5, 3.5)
HEIGHT_BINS = (0, 12, 20, 32, 64, 96, 160, 10_000)
OFF_CENTRE_BINS = (0.0, 0.5, 0.8, 1.01)
"""Distance of a bottle from the frame's centre, as a share of the half diagonal."""


def bucket(value: float, edges: tuple[float, ...], unit: str) -> str:
    """Name the bin of ``edges`` that ``value`` falls in"""
    for low, high in zip(edges, edges[1:], strict=False):
        if value < high or high == edges[-1]:
            top = "+" if high >= 10_000 else f"-{high:g}"
            return f"{low:g}{top} {unit}"
    return f"{edges[-1]:g}+ {unit}"


def low_edge(name: str) -> float:
    """Lower edge of a bin named by :func:`bucket`, to sort bins by"""
    return float(name.split("-")[0].split("+")[0])


def predict(weights: Path, frames: list[dict], folder: Path, imgsz: int | None,
            cache: Path, crop: bool = False) -> dict[str, list]:  # fmt: skip
    """Boxes of every frame as ``[x0, y0, x1, y1, score]``, from ``cache`` if there

    With ``crop`` the model sees only the part of the frame the bench occupies
    (:func:`bench_crop.bench_crop`), as it does when trained on cropped frames
    and run by the viewer; the boxes come back in whole-frame pixels.
    """
    if cache.exists():
        return json.loads(cache.read_text())
    from ultralytics import YOLO

    model = YOLO(str(weights))
    boxes = {}
    start = time.perf_counter()
    for i, frame in enumerate(frames):
        image = cv2.imread(str(folder / frame["file"]))
        left, top = 0, 0
        if crop:
            left, top, right, bottom = bench_crop(frame)
            image = image[top:bottom, left:right]
        size = imgsz or math.ceil(max(image.shape[:2]) / 32) * 32
        out = model.predict(image, imgsz=size, conf=0.01, max_det=300, verbose=False)[0]
        boxes[frame["file"]] = [
            [x0 + left, y0 + top, x1 + left, y1 + top, float(score)]
            for (x0, y0, x1, y1), score in zip(out.boxes.xyxy.tolist(),
                                               out.boxes.conf.tolist(), strict=True)
        ]  # fmt: skip
        if (i + 1) % 20 == 0:
            rate = (time.perf_counter() - start) / (i + 1)
            print(f"  {i + 1}/{len(frames)}, {rate:.2f} s/frame", file=sys.stderr)
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(boxes))
    return boxes


def row(results: list[ev.FrameResult], threshold: float) -> dict:
    """One table row for a group of matched frames or bottles"""
    point = ev.operating_point(results, threshold)
    return {
        "bottles": point["required"],
        "recall": point["recall"],
        "false_per_frame": point["false_per_frame"],
        "ap50": ev.ap_at(results) if point["required"] else float("nan"),
    }


def study(frames: list[dict], boxes: dict[str, list], threshold: float) -> dict:
    """Match every frame once and group the outcome every way"""
    matched = []
    for frame in frames:
        dets = [ev.Detection(tuple(b[:4]), b[4]) for b in boxes[frame["file"]]]
        matched.append((frame, ev.match_frame(ev.truths_of(frame), dets)))
    tables: dict[str, dict] = {"all": {"all": row([r for _, r in matched], threshold)}}

    by_frame = {}
    if all(f["randomisation"].get("orbit") for f in frames):
        by_frame = {
            "elevation": lambda o: bucket(o["elevation_deg"], ELEVATION_BINS, "deg"),
            "range": lambda o: bucket(o["range_m"], RANGE_BINS, "m"),
        }
    for name, key in by_frame.items():
        groups: dict[str, list] = {}
        for frame, result in matched:
            groups.setdefault(key(frame["randomisation"]["orbit"]), []).append(result)
        tables[name] = {k: row(v, threshold) for k, v in sorted(groups.items())}

    def off_centre(frame: dict, truth: ev.Truth) -> str:
        w, h = frame["width"], frame["height"]
        x0, y0, x1, y1 = truth.box
        r = math.hypot((x0 + x1) / 2 - w / 2, (y0 + y1) / 2 - h / 2)
        return bucket(r / math.hypot(w / 2, h / 2), OFF_CENTRE_BINS, "of half diagonal")

    by_bottle = {
        "bottle height": lambda f, t: bucket(t.full_box[3] - t.full_box[1],
                                             HEIGHT_BINS, "px"),  # fmt: skip
        "off centre": off_centre,
    }
    for name, key in by_bottle.items():
        counts: dict[str, list[int]] = {}
        for frame, result in matched:
            for truth, score in zip(result.truths, result.found, strict=True):
                cell = counts.setdefault(key(frame, truth), [0, 0])
                cell[0] += score is not None and score >= threshold
                cell[1] += 1
        tables[name] = {
            k: {"bottles": n, "recall": found / n}
            for k, (found, n) in sorted(counts.items(), key=lambda kv: low_edge(kv[0]))
        }
    return tables


def markdown(tables: dict) -> str:
    """The tables as one Markdown table"""
    lines = ["| by | group | bottles | recall | false/frame | AP50 |",
             "| --- | --- | ---: | ---: | ---: | ---: |"]  # fmt: skip
    for name, groups in tables.items():
        for group, r in groups.items():
            extra = (
                f"{r['false_per_frame']:.2f} | {r['ap50']:.3f}" if "ap50" in r else "| "
            )
            lines.append(
                f"| {name} | {group} | {r['bottles']} | {r['recall']:.3f} | {extra} |"
            )
    return "\n".join(lines)


def main() -> None:
    """Score one detector on the requested splits"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("weights", help="backend name or path to weights")
    parser.add_argument("--splits", default="orbit_test,rail_test")
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--pick-on", default=None, help="validation splits, a,b,c")
    parser.add_argument("--imgsz", type=int, default=None, help="default: native")
    parser.add_argument("--crop", action="store_true",
                        help="predict on the bench crop, as the trained model runs")
    parser.add_argument("--max", type=int, default=None, help="first N frames only")
    parser.add_argument("--src", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--name", default=None, help="results folder name")
    args = parser.parse_args()

    weights, backend_threshold = det.resolve(args.weights)
    threshold = args.threshold or backend_threshold or 0.25
    name = args.name or (
        args.weights if backend_threshold else Path(args.weights).parent.parent.name
    )
    if args.imgsz and not args.name:
        name += f"_{args.imgsz}"
    if args.crop and not args.name:
        name += "_crop"

    def load(split: str) -> tuple[list[dict], dict[str, list]]:
        gt = json.loads((args.src / split / "gt.json").read_text(encoding="utf-8"))
        frames = gt["frames"][: args.max]
        cache = RESULTS / name / f"{split}.boxes.json"
        boxes = predict(
            Path(weights), frames, args.src / split, args.imgsz, cache, args.crop
        )
        return frames, boxes

    if args.pick_on:
        matched = []
        for split in args.pick_on.split(","):
            frames, boxes = load(split)
            matched += [
                ev.match_frame(
                    ev.truths_of(f),
                    [ev.Detection(tuple(b[:4]), b[4]) for b in boxes[f["file"]]],
                )
                for f in frames
            ]
        threshold, f1 = ev.best_f1_threshold(matched)
        print(f"threshold {threshold:.3f}: best F1 {f1:.3f} on {args.pick_on}")

    for split in args.splits.split(","):
        frames, boxes = load(split)
        tables = study(frames, boxes, threshold)
        (RESULTS / name / f"{split}.json").write_text(json.dumps(tables, indent=1))
        print(f"\n### {name} on {split}, {len(frames)} frames, threshold {threshold}\n")
        print(markdown(tables))


if __name__ == "__main__":
    main()
