"""Draw the limits sweeps as image strips, both detectors on the same frames

Needs the frames ``limits_sweep.py`` rendered and the two weights in ``weights/``.
"""

import json
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ultralytics import YOLO  # noqa: E402

from labvision import evaluation as ev  # noqa: E402

if len(sys.argv) != 2:
    sys.exit(
        "usage: demo_strips.py SWEEPS   (the folder holding limits_sweep.py's sweep_*)"
    )
SWEEPS = Path(sys.argv[1])
WEIGHTS = ROOT / "weights"
OUT = ROOT / "docs" / "demo" / "3_results"
DETECTORS = (
    ("previous detector, threshold 0.10", "yolo26n_rail_general.pt", 0.10),
    ("retrained, 100 epochs, threshold 0.52", "yolo26n_full_1920_e100.pt", 0.52),
)
STRIPS = (
    (
        "light",
        "examples_as_the_light_goes.jpg",
        0,
        (1, 0.3, 0.15, 0.1, 0.06),
        lambda v: f"{v:.0%} of the room's light",
    ),
    (
        "range",
        "examples_as_the_camera_nears.jpg",
        0,
        (3.5, 1.5, 0.75, 0.5, 0.25),
        lambda v: f"{v:g} m from the bench",
    ),
    (
        "elevation",
        "examples_as_the_camera_tilts.jpg",
        0,
        (88, 60, 30, 20, 10),
        lambda v: f"{v:g} degrees above the bench",
    ),
)
CELL = (640, 360)
INK, PAPER, FOUND, MISSED = (30, 30, 30), (251, 252, 252), (90, 200, 40), (40, 40, 235)


def window(boxes: np.ndarray, width: int, height: int) -> tuple[int, int, int, int]:
    """The 16:9 window round the vials, inside the frame"""
    x0, y0, x1, y1 = (
        boxes[:, 0].min(),
        boxes[:, 1].min(),
        boxes[:, 2].max(),
        boxes[:, 3].max(),
    )
    w = max((x1 - x0) * 1.25, (y1 - y0) * 1.25 * 16 / 9, 480)
    w = min(w, width)
    h = w * 9 / 16
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    left = int(np.clip(cx - w / 2, 0, width - w))
    top = int(np.clip(cy - h / 2, 0, height - h))
    return left, top, int(left + w), int(top + h)


models = {name: YOLO(str(WEIGHTS / file)) for name, file, _ in DETECTORS}
for sweep, filename, k, levels, caption in STRIPS:
    gutter, label_h, head = 10, 34, 44
    w, h = CELL
    canvas = np.full(
        (
            head + (h + label_h + gutter) * len(DETECTORS) + gutter,
            (w + gutter) * len(levels) + gutter,
            3,
        ),
        PAPER,
        np.uint8,
    )
    for c, level in enumerate(levels):
        folder = SWEEPS / f"sweep_{sweep}" / f"{level:g}"
        frames = json.loads((folder / "gt.json").read_text(encoding="utf-8"))["frames"]
        frame = next(f for f in frames if f["file"] == f"{k:03d}.png")
        image = cv2.imread(str(folder / frame["file"]))
        truths = ev.truths_of(frame)
        required = [t for t in truths if t.required]
        left, top, right, bottom = window(
            np.array([t.full_box for t in required]), frame["width"], frame["height"]
        )
        x = gutter + c * (w + gutter)
        cv2.putText(
            canvas,
            caption(level),
            (x, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            INK,
            2,
            cv2.LINE_AA,
        )
        for r, (name, _, threshold) in enumerate(DETECTORS):
            out = models[name].predict(
                image, imgsz=1920, conf=0.01, max_det=300, verbose=False
            )[0]
            dets = [
                ev.Detection(tuple(b), s)
                for b, s in zip(
                    out.boxes.xyxy.tolist(), out.boxes.conf.tolist(), strict=True
                )
            ]
            result = ev.match_frame(truths, dets)
            shown = image.copy()
            scale = (right - left) / w
            thick = max(1, round(1.6 * scale))
            hits = 0
            for truth, score in zip(result.truths, result.found, strict=True):
                ok = score is not None and score >= threshold
                hits += ok
                a, b, cc, d = (round(v) for v in truth.full_box)
                cv2.rectangle(shown, (a, b), (cc, d), FOUND if ok else MISSED, thick)
            cell = cv2.resize(
                shown[top:bottom, left:right], (w, h), interpolation=cv2.INTER_AREA
            )
            y = head + r * (h + label_h + gutter)
            canvas[y + label_h : y + label_h + h, x : x + w] = cell
            text = f"{hits} of {len(result.truths)} found"
            cv2.putText(
                canvas,
                f"{name}: {text}" if not c else text,
                (x, y + 24),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                INK,
                1,
                cv2.LINE_AA,
            )
            print(sweep, level, name, text)
    cv2.imwrite(str(OUT / filename), canvas, [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(filename, canvas.shape[1], "x", canvas.shape[0])
