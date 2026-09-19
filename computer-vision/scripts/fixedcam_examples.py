r"""Draw a model's cached boxes on test frames: an animated GIF and a contact sheet

No model is run: the boxes come from ``fixedcam_bench.py``'s cache and are drawn
at the model's validation threshold, after the worktop filter, on the worktop
band of each frame. Green is a bottle found, magenta a bottle missed, red a
false box, grey a bottle that did not have to be found (shelf, hidden, cut).

    python scripts/fixedcam_examples.py "ft:runs/fixedcam/yolo26n_fixedcam.pt+roi" \\
        --split test --frames 12

Output: ``results/fixedcam/examples/<model>_<split>.gif`` and ``..._sheet.jpg``.
"""

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fixedcam_bench as fb  # noqa: E402
import fixedcam_models as fm  # noqa: E402

from labvision import evaluation as ev  # noqa: E402

OUT = fb.RESULTS / "examples"


def panels(model: str, split: str, count: int, width: int) -> list[np.ndarray]:
    """Return one annotated worktop crop per frame, as BGR images of one width"""
    folder, gt = fb.load_split(split)
    worktop = ev.Worktop.from_gt(gt)
    metrics = json.loads(
        (fb.RESULTS / fb.slug(model) / "metrics.json").read_text(encoding="utf-8")
    )
    threshold = metrics["val"]["worktop"]["threshold"]
    cache_path = fb.RESULTS / fb.slug(model) / split / "predictions.json"
    cache = json.loads(cache_path.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / "_frame.jpg"
    out = []
    for frame in gt["frames"]:
        if len(out) == count:
            break
        if frame["file"] not in cache:
            continue
        dets = [d for d in fb.detections(cache[frame["file"]])
                if ev.on_worktop(frame, d.box, worktop)]  # fmt: skip
        fb.draw_overlay(folder, frame, dets, threshold, tmp)
        u0, v0, u1, v1 = fm.worktop_roi(frame, worktop, margin_px=8)
        crop = cv2.imread(str(tmp))[v0:v1, u0:u1]
        kept = [d for d in dets if d.score >= threshold]
        result = ev.match_frame(ev.truths_of(frame), kept)
        found = sum(s is not None for s in result.found)
        caption = (f"{frame['file']}: {found}/{len(result.found)} found, "
                   f"{len(result.false_boxes)} false")  # fmt: skip
        scale = width / crop.shape[1]
        crop = cv2.resize(crop, (width, int(round(crop.shape[0] * scale))),
                          interpolation=cv2.INTER_AREA)  # fmt: skip
        banner = np.full((28, width, 3), 250, np.uint8)
        cv2.putText(banner, caption, (8, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                    (30, 30, 30), 1, cv2.LINE_AA)  # fmt: skip
        out.append(np.vstack([banner, crop]))
    if tmp.exists():
        tmp.unlink()
    return out


def main() -> None:
    """Parse the command line and write the GIF and the sheet"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("model")
    parser.add_argument("--split", default="test")
    parser.add_argument("--frames", type=int, default=12)
    parser.add_argument("--width", type=int, default=1280)
    args = parser.parse_args()
    images = panels(args.model, args.split, args.frames, args.width)
    if not images:
        raise SystemExit("no cached frames to draw")
    height = max(i.shape[0] for i in images)
    images = [np.vstack([i, np.full((height - i.shape[0], args.width, 3), 255,
                                    np.uint8)]) for i in images]  # fmt: skip
    stem = OUT / f"{fb.slug(args.model)}_{args.split}"
    frames = [Image.fromarray(cv2.cvtColor(i, cv2.COLOR_BGR2RGB)) for i in images]
    frames[0].save(f"{stem}.gif", save_all=True, append_images=frames[1:],
                   duration=1200, loop=0, optimize=True)  # fmt: skip
    columns = 2
    rows = [np.hstack(images[k : k + columns]) for k in range(0, len(images), columns)
            if len(images[k : k + columns]) == columns]  # fmt: skip
    if rows:
        cv2.imwrite(f"{stem}_sheet.jpg", np.vstack(rows),
                    [cv2.IMWRITE_JPEG_QUALITY, 80])  # fmt: skip
    print(f"{stem}.gif and {stem}_sheet.jpg, {len(images)} frames")


if __name__ == "__main__":
    main()
