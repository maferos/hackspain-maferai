"""Try YOLO-World vocabularies on the perfumery frames, extra prompts included

Two ideas are tested against the frames of ``render_perfumery.py``: prompts
that name what the samples are (amber glass and white plastic bottles) instead
of generic vessels, and *distractor* prompts for what is not a sample (shelves,
balances, beakers, the room) whose boxes are dropped. With class-agnostic NMS,
a distractor that scores higher than a vessel prompt on the same box takes the
box with it, which is how a distractor can remove a false positive.

Each vocabulary gets a real forward pass. Replaying vocabularies from one pass
over their union would be cheaper but not exact: the YOLO-World v2 neck
(``C2fAttn``) attends to the text by taking the maximum over all prompts, so
adding prompts changes the image features themselves. Within one pass, raising
the threshold after NMS is exact, because greedy NMS decides a box using only
the boxes that score above it; so each vocabulary runs once at a low threshold
and the sweep is done afterwards, with and without the worktop filter.

    python scripts/world_prompts.py ../simulation/out/perfumery
    python scripts/world_prompts.py ../simulation/out/perfumery --only bottles

Detections are cached in ``<folder>/world_prompts/<vocabulary>.json``; the
report goes to ``<folder>/world_prompts.md`` and ``.json``.
"""

import argparse
import json
import sys
import time
from collections import Counter
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from perfumery_eval import match_frame, on_worktop  # noqa: E402

from labvision.detector import BACKENDS, _find_weights, input_size_for  # noqa: E402

CURRENT = BACKENDS["world"].prompts
"""The detector's vessel prompts today, tuned on real lab photographs."""
BOTTLES = (
    "bottle",
    "plastic bottle",
    "amber glass bottle",
    "brown glass bottle",
    "small brown bottle",
    "white plastic bottle",
    "reagent bottle",
    "medicine bottle",
    "bottle with a white label",
)
"""Prompts that name what the samples are: amber glass and white HDPE bottles."""
GLASSWARE = ("cup", "drinking glass", "glass", "jar", "beaker", "glass flask", "vial")
"""The rest of the current prompts: other vessels, which in this lab are not samples."""
SHELVES = ("shelf", "bookshelf", "shelf full of bottles", "row of bottles")
SCENERY = (
    "cabinet",
    "drawer",
    "countertop",
    "laboratory balance",
    "digital scale",
    "glass box",
    "computer monitor",
    "keyboard",
    "office chair",
    "sink",
    "water tap",
    "measuring cylinder",
    "wash bottle",
    "pipette",
    "tray",
    "sheet of paper",
    "cardboard box",
    "person",
    "ceiling lamp",
    "door",
    "window",
    "glass wall",
)
"""Everything else in the room that a vessel prompt might fire on."""
SCENERY_SAFE = tuple(p for p in SCENERY if p != "wash bottle")
"""The room without ``wash bottle``: a wash bottle is a bottle, and as a
distractor it took 26 of 96 sample bottles from ``bottle`` in a spot check."""

VARIANTS: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "current": (CURRENT, ()),
    "current + distractors": (CURRENT, SHELVES + SCENERY),
    "bottles": (BOTTLES, ()),
    "bottles + glassware as distractors": (BOTTLES, GLASSWARE),
    "bottles + shelves as distractors": (BOTTLES, SHELVES),
    "bottles + all distractors": (BOTTLES, GLASSWARE + SHELVES + SCENERY),
    "current + distractors, no wash bottle": (CURRENT, SHELVES + SCENERY_SAFE),
    "bottles + all distractors, no wash bottle": (
        BOTTLES,
        GLASSWARE + SHELVES + SCENERY_SAFE,
    ),
}
"""Name: (prompts whose boxes are kept, prompts whose boxes are dropped)."""

THRESHOLDS = (0.03, 0.05, 0.08, 0.11, 0.15, 0.2, 0.25, 0.3, 0.4)
FLOOR = 0.03
"""Threshold of the single pass; the sweep starts here."""
SETS = {"scene cameras": ("as_built", "walkthrough"), "close camera": ("perception",)}


def slug(name: str) -> str:
    """File name for a vocabulary"""
    return "".join(c if c.isalnum() else "_" for c in name).strip("_")


def run_variant(
    name: str, folder: Path, frames: list[dict], out: Path, device: str | None
) -> dict:
    """Detect with one vocabulary over every frame, or read the cached result"""
    cache = out / f"{slug(name)}.json"
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    from ultralytics import YOLOWorld

    keep, drop = VARIANTS[name]
    model = YOLOWorld(_find_weights(BACKENDS["world"].weights))
    model.set_classes(list(dict.fromkeys(keep + drop)))
    result = {}
    for k, frame in enumerate(frames):
        image = cv2.imread(str(folder / frame["file"]))
        start = time.perf_counter()
        hits = model.predict(
            image,
            imgsz=input_size_for(image, None),
            conf=FLOOR,
            iou=0.6,
            agnostic_nms=True,
            max_det=1000,
            device=device,
            verbose=False,
        )[0]
        boxes = []
        for hit in hits.boxes:
            label = hits.names[int(hit.cls)]
            if label in keep:
                xyxy = [round(float(v), 1) for v in hit.xyxy[0]]
                boxes.append({"xyxy": xyxy, "score": float(hit.conf), "label": label})
        seconds = time.perf_counter() - start
        result[frame["file"]] = {"seconds": round(seconds, 3), "boxes": boxes}
        print(
            f"{name} {k + 1}/{len(frames)}: {len(boxes)} boxes, {seconds:.1f} s",
            flush=True,
        )
    out.mkdir(exist_ok=True)
    cache.write_text(json.dumps(result), encoding="utf-8")
    return result


def score(folder: Path, frames: list[dict], detections: dict[str, dict]) -> dict:
    """Match every vocabulary's boxes to the truth, per set, filter and threshold"""
    results: dict = {}
    for name, found in detections.items():
        tally = {
            (s, filt, t): Counter()
            for s in SETS
            for filt in (False, True)
            for t in THRESHOLDS
        }
        labels: Counter = Counter()
        for frame in frames:
            group = next(s for s, members in SETS.items() if frame["set"] in members)
            boxes = found[frame["file"]]["boxes"]
            for filt in (False, True):
                kept = (
                    [b for b in boxes if on_worktop(frame, b["xyxy"])]
                    if filt
                    else boxes
                )
                for t in THRESHOLDS:
                    above = [b for b in kept if b["score"] > t]
                    required, taken, _, outcome = match_frame(folder, frame, above, 0.5)
                    c = tally[(group, filt, t)]
                    c["frames"] += 1
                    c["required"] += len(required)
                    c["found"] += sum(taken)
                    c["false"] += sum(v == "false" for _, v, _ in outcome)
                    c["false_shelf"] += sum(
                        u == "shelf_bottle" for _, v, u in outcome if v == "false"
                    )
                    if filt and t == BACKENDS["world"].score:
                        for box, verdict, _ in outcome:
                            if verdict != "ignored":
                                labels[(box["label"], verdict)] += 1
        seconds = [found[f["file"]]["seconds"] for f in frames]
        results[name] = {
            "seconds": sorted(seconds)[len(seconds) // 2],
            "tally": {f"{s}|{int(f)}|{t}": dict(c) for (s, f, t), c in tally.items()},
            "labels": {f"{p}|{v}": n for (p, v), n in labels.items()},
        }
    return results


def rates(tally: dict, key: str) -> tuple[float, float, float, float]:
    """Recall, precision, F1 and false boxes per frame of one tally cell"""
    c = tally[key]
    recall = c["found"] / c["required"]
    precision = c["found"] / max(c["found"] + c["false"], 1)
    f1 = 2 * recall * precision / max(recall + precision, 1e-9)
    return recall, precision, f1, c["false"] / c["frames"]


def summarise(results: dict) -> str:
    """Markdown tables: each vocabulary at the detector's threshold and at best F1"""
    t0 = BACKENDS["world"].score
    lines = ["# YOLO-World vocabularies on the perfumery frames", ""]
    for group in SETS:
        for filt in (0, 1):
            lines += [
                f"## {group}, {'with' if filt else 'without'} the worktop filter",
                "",
                f"| vocabulary | s/frame | found @{t0} | false/frame @{t0} "
                f"| precision @{t0} | best F1 | at | found | false/frame |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
            for name, r in results.items():
                rec, prec, _, fpf = rates(r["tally"], f"{group}|{filt}|{t0}")
                best = max(
                    THRESHOLDS,
                    key=lambda t, r=r: rates(r["tally"], f"{group}|{filt}|{t}")[2],
                )
                brec, _, bf1, bfpf = rates(r["tally"], f"{group}|{filt}|{best}")
                lines.append(
                    f"| {name} | {r['seconds']:.1f} | {100 * rec:.0f} % | {fpf:.1f} | "
                    f"{100 * prec:.0f} % | {bf1:.2f} | {best} | {100 * brec:.0f} % | "
                    f"{bfpf:.1f} |"
                )
            lines.append("")
    lines += [
        f"## Hits and false boxes per prompt, all frames, worktop filter on, @{t0}",
        "",
        "| prompt | " + " | ".join(f"{n}: hit / false" for n in results) + " |",
        "| --- |" + " --- |" * len(results),
    ]
    for p in dict.fromkeys(BOTTLES + CURRENT):
        cells = [
            f"{r['labels'].get(f'{p}|hit', 0)} / {r['labels'].get(f'{p}|false', 0)}"
            if p in VARIANTS[n][0]
            else "-"
            for n, r in results.items()
        ]
        lines.append(f"| {p} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    """Detect with each vocabulary, score and report"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder", type=Path)
    parser.add_argument("--only", nargs="*", help="run only these vocabularies")
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    frames = json.loads((args.folder / "gt.json").read_text(encoding="utf-8"))["frames"]
    out = args.folder / "world_prompts"
    names = [
        n for n in VARIANTS if not args.only or n in args.only or slug(n) in args.only
    ]
    for n in names:
        run_variant(n, args.folder, frames, out, args.device)
    detections = {
        n: run_variant(n, args.folder, frames, out, args.device)
        for n in VARIANTS
        if (out / f"{slug(n)}.json").exists()
    }
    results = score(args.folder, frames, detections)
    report = summarise(results)
    (args.folder / "world_prompts.md").write_text(report, encoding="utf-8")
    (args.folder / "world_prompts.json").write_text(
        json.dumps(results), encoding="utf-8"
    )
    print(report)


if __name__ == "__main__":
    main()
