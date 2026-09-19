"""Export a trained detector for this machine and time it on rendered frames

The detector has 100 ms a frame (``docs/YOLO26_STUDY.md``), and whether it
makes it depends on the machine and the runtime far more than on the weights.
Run this on the machine that will run the demo:

    python scripts/export_and_time.py rail --format coreml --imgsz 1280   # a Mac
    python scripts/export_and_time.py rail --format torch --device mps    # a Mac
    python scripts/export_and_time.py rail --format openvino --imgsz 1280 # Intel CPU
    python scripts/export_and_time.py rail --format torch --device 0      # NVIDIA
    python scripts/export_and_time.py rail --format torch --device mps --band 512

``coreml`` and ``openvino`` export fp16 with a fixed 16:9 input, because a
dynamic shape recompiles and runs several times slower; the exported model is
written next to the weights and every ``--weights`` that takes a path accepts
it. ``torch`` times the ``.pt`` as it is on ``--device``. Prints the median and
the 90th percentile of whole ``predict`` calls, pre- and post-processing
included, over the frames of ``--split``, and the memory the process holds at
the end.
"""

import argparse
import json
import math
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import psutil

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fixedcam_dataset import DEFAULT_OUT, HEIGHT, WIDTH  # noqa: E402

from labvision import detector as det  # noqa: E402


def main() -> None:
    """Export if asked, then time the model on rendered frames"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("weights", help="backend name or path to .pt weights")
    parser.add_argument("--format", default="openvino",
                        choices=["openvino", "coreml", "torch"])  # fmt: skip
    parser.add_argument("--device", default=None, help="torch only: cpu, mps, 0")
    parser.add_argument("--imgsz", type=int, default=1280, help="input width")
    parser.add_argument("--band", type=int, default=None, metavar="ROWS",
                        help="time the bench band, ROWS rows at full width, as the "
                        "viewer crops it: 512 for 1920 x 512")  # fmt: skip
    parser.add_argument("--split", default="rail_test")
    parser.add_argument("--frames", type=int, default=30)
    parser.add_argument("--src", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    from ultralytics import YOLO

    weights, _ = det.resolve(args.weights)
    shape = [math.ceil(args.imgsz * HEIGHT / WIDTH / 32) * 32, args.imgsz]
    if args.band:
        shape = [math.ceil(args.band / 32) * 32, math.ceil(WIDTH / 32) * 32]
    options = {}
    if args.format == "torch":
        loaded = weights
        if args.device is not None:
            options["device"] = args.device
    else:
        loaded = YOLO(weights).export(format=args.format, half=True, imgsz=shape)
    model = YOLO(loaded, task="detect")

    gt = json.loads((args.src / args.split / "gt.json").read_text(encoding="utf-8"))
    images = [
        cv2.imread(str(args.src / args.split / frame["file"]))
        for frame in gt["frames"][: args.frames]
    ]
    if args.band:
        top = (HEIGHT - shape[0]) // 2 + 36  # the bench sits just under mid-frame
        images = [image[top : top + shape[0]] for image in images]
    for image in images[:3]:
        model.predict(image, imgsz=shape, verbose=False, **options)
    times = []
    for image in images:
        start = time.perf_counter()
        model.predict(image, imgsz=shape, verbose=False, **options)
        times.append(1000 * (time.perf_counter() - start))
    held = psutil.Process().memory_info().rss / 2**20
    print(
        f"{loaded} [{args.format} {args.device or ''}]: {shape[1]}x{shape[0]}, "
        f"median {np.median(times):.0f} ms, p90 {np.percentile(times, 90):.0f} ms "
        f"over {len(times)} frames, {held:.0f} MB held"
    )


if __name__ == "__main__":
    main()
