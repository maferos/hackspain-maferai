"""Run a detector on the ten demo benches exactly as the viewer shows them

The viewer builds the rail scene with one of the ten catalogued bench patterns
(``view/backend/scene_patterns.py``), renders the ``general`` wall camera at
1920 x 1080, crops the table band (``view/backend/table_crop.py``) and predicts
on it at native size. This does the same for every pattern, p01 to p10, and
checks the boxes against the truth of that very frame: each flask's box from a
segmentation render of the same model.

    python scripts/demo_patterns_check.py full --out DIR
    python scripts/demo_patterns_check.py weights/other.pt --threshold 0.3 --out DIR

Writes ``<out>/<pattern>.jpg`` (the band, found flasks in green, missed ones in
red, false boxes in orange) and ``<out>/demo_patterns.json``; prints a table.
A flask counts when at least ``MIN_VISIBLE`` of it shows in the band; a box is
right at IoU 0.5 with a flask no other box has taken.
"""

import argparse
import json
import sys
from pathlib import Path

import cv2
import mujoco
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "view" / "backend"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scene_patterns  # noqa: E402
from table_crop import table_region  # noqa: E402

from labvision import detector as det  # noqa: E402

SCENE = REPO / "simulation" / "models" / "minihannover_rail_scene.xml"
WIDTH, HEIGHT = 1920, 1080
MIN_VISIBLE = 0.3
FOUND, MISSED, FALSE = (60, 200, 40), (40, 40, 230), (0, 150, 255)


def flasks_in_view(model: mujoco.MjModel, data: mujoco.MjData) -> list[dict]:
    """Every pattern flask's visible box in the ``general`` camera's frame

    Two segmentation renders, as the dataset's truth: one of the whole scene for
    what shows, one of the flasks alone for what would show with nothing in
    front, so a flask mostly hidden by the arm or an instrument can be left out.
    """
    owner = np.full(model.ngeom, -1)
    for g in range(model.ngeom):
        root = model.body_rootid[model.geom_bodyid[g]]
        if model.body(root).name.startswith("dyn_"):
            owner[g] = root
    boxes = []
    with mujoco.Renderer(model, HEIGHT, WIDTH) as renderer:
        renderer.enable_segmentation_rendering()
        renderer.update_scene(data, camera="general")
        seen = renderer.render()[:, :, 0]
        shown = np.where(seen >= 0, owner[np.clip(seen, 0, None)], -1)
        # The flasks alone: everything else goes to a geom group that is off.
        option = mujoco.MjvOption()
        groups = model.geom_group.copy()
        model.geom_group[owner < 0] = 5
        model.geom_group[owner >= 0] = 0
        option.geomgroup[:] = [1, 0, 0, 0, 0, 0]
        renderer.update_scene(data, camera="general", scene_option=option)
        alone = renderer.render()[:, :, 0]
        model.geom_group[:] = groups
    full = np.where(alone >= 0, owner[np.clip(alone, 0, None)], -1)
    for root in sorted(set(owner[owner >= 0])):
        ys, xs = np.nonzero(shown == root)
        whole = int((full == root).sum())
        if not len(xs) or not whole:
            continue
        boxes.append({
            "name": model.body(root).name,
            "xyxy": [int(xs.min()), int(ys.min()),
                     int(xs.max()) + 1, int(ys.max()) + 1],
            "visible": round(len(xs) / whole, 3),
        })  # fmt: skip
    return boxes


def iou(a: list[float], b: list[float]) -> float:
    """Intersection over union of two boxes"""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - w * h
    return w * h / union


def main() -> None:
    """Render, detect, score and draw the ten patterns"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("weights", help="backend name or path to weights")
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    from ultralytics import YOLO

    weights, backend_threshold = det.resolve(args.weights)
    threshold = args.threshold or backend_threshold or 0.25
    detector = YOLO(weights)
    args.out.mkdir(parents=True, exist_ok=True)
    report = []
    for entry in scene_patterns.CATALOGUE:
        model, info = scene_patterns.build_pattern(SCENE, entry["pattern"])
        data = mujoco.MjData(model)
        mujoco.mj_forward(model, data)
        with mujoco.Renderer(model, HEIGHT, WIDTH) as renderer:
            renderer.update_scene(data, camera="general")
            frame = np.ascontiguousarray(renderer.render()[:, :, ::-1])
        band, top = table_region(frame)
        truths = [
            t for t in flasks_in_view(model, data)
            if t["visible"] >= MIN_VISIBLE and t["xyxy"][1] >= top
            and t["xyxy"][3] <= top + band.shape[0]
        ]  # fmt: skip
        out = detector.predict(band, imgsz=max(band.shape[:2]), conf=threshold,
                               max_det=300, verbose=False)[0]  # fmt: skip
        dets = sorted(
            ([*(float(v) for v in xyxy), float(score)]
             for xyxy, score in zip(out.boxes.xyxy.tolist(), out.boxes.conf.tolist(),
                                    strict=True)),
            key=lambda d: -d[4],
        )  # fmt: skip
        taken: set[int] = set()
        false = []
        for d in dets:
            box = [d[0], d[1] + top, d[2], d[3] + top]
            best = max(
                (i for i in range(len(truths)) if i not in taken),
                key=lambda i: iou(box, truths[i]["xyxy"]), default=None,
            )  # fmt: skip
            if best is not None and iou(box, truths[best]["xyxy"]) >= 0.5:
                taken.add(best)
            else:
                false.append(d)
        image = band.copy()
        for i, t in enumerate(truths):
            x0, y0, x1, y1 = t["xyxy"]
            colour = FOUND if i in taken else MISSED
            cv2.rectangle(image, (x0 - 2, y0 - top - 2), (x1 + 2, y1 - top + 2), colour,
                          1 if i in taken else 2)  # fmt: skip
        for d in false:
            cv2.rectangle(image, (int(d[0]) - 3, int(d[1]) - 3),
                          (int(d[2]) + 3, int(d[3]) + 3), FALSE, 2)  # fmt: skip
        cv2.imwrite(str(args.out / f"{info['pattern']}.jpg"), image,
                    [cv2.IMWRITE_JPEG_QUALITY, 88])  # fmt: skip
        row = {**info, "flasks_in_band": len(truths), "found": len(taken),
               "missed": [truths[i]["name"] for i in range(len(truths))
                          if i not in taken],
               "false": len(false), "boxes": len(dets)}  # fmt: skip
        report.append(row)
        print(f"{row['pattern']} seed {row['seed']:>3} {row['style']:<8} "
              f"{row['count']:>2} flasks: {row['found']}/{row['flasks_in_band']} "
              f"found, "
              f"{row['false']} false, missed {row['missed']}", flush=True)  # fmt: skip
    result = {"weights": Path(weights).name, "threshold": threshold, "patterns": report}
    (args.out / "demo_patterns.json").write_text(json.dumps(result, indent=1))
    found = sum(r["found"] for r in report)
    total = sum(r["flasks_in_band"] for r in report)
    false = sum(r["false"] for r in report)
    print(f"{found}/{total} flasks found, {false} false boxes")


if __name__ == "__main__":
    main()
