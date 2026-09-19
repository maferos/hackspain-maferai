"""Write fixed-camera splits as a whole-frame YOLO dataset, one bottle class

``fixedcam_crops.py`` cuts 384 px crops for CPU training; on a GPU the model
can take the whole 1920 x 1080 frame at native resolution, which is also how it
runs on the robot, so no crop or tile logic is needed at inference. Since the
v6 catalogue the bench holds liquids only, all in amber glass, so every sample
bottle is one class, ``amber_bottle`` (the name ``fixedcam_crops.py`` uses).

A bottle is labelled when at least ``MIN_VISIBLE`` of it shows, wherever it
stands, as in ``fixedcam_crops.py``; the few hidden further than that are left
unlabelled rather than taught as bottles the model cannot see.

With ``--crop`` every frame is cut to the part the bench occupies
(``bench_crop.py``), at full resolution: from the wall camera a band about
1920 x 448, the input the detector runs on to stay under 100 ms on a CPU.
Labels move with the crop, and a bottle the crop leaves with under
``bench_crop.KEEP`` of its box is dropped.

    python scripts/fixedcam_to_yolo.py rail_train:train rail_val:val --out DIR
    python scripts/fixedcam_to_yolo.py rail_train:train orbit_train:train \
        rail_val:val --out DIR --crop

Writes OUT/{images,labels}/<role>/<split>_NNNN.{png,txt} and OUT/data.yaml.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench_crop import bench_crop, crop_labels  # noqa: E402
from fixedcam_crops import MIN_VISIBLE  # noqa: E402
from fixedcam_dataset import DEFAULT_OUT  # noqa: E402

CLASS_NAME = "amber_bottle"


def put(src: Path, dst: Path, link: bool) -> None:
    """Hard-link or copy one image, once"""
    if dst.exists():
        return
    if link:
        try:
            os.link(src, dst)
            return
        except OSError:
            pass
    shutil.copy2(src, dst)


def main() -> None:
    """Convert the requested splits"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("pairs", nargs="+", help="split:role, role train or val")
    parser.add_argument("--src", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--link", action="store_true", help="hard-link the images")
    parser.add_argument(
        "--crop",
        action="store_true",
        help="crop every frame to the bench (bench_crop.py), as the detector runs",
    )
    args = parser.parse_args()

    for pair in args.pairs:
        split, role = pair.split(":")
        gt = json.loads((args.src / split / "gt.json").read_text(encoding="utf-8"))
        (args.out / "images" / role).mkdir(parents=True, exist_ok=True)
        (args.out / "labels" / role).mkdir(parents=True, exist_ok=True)
        boxes = hidden = 0
        for frame in gt["frames"]:
            w, h = frame["width"], frame["height"]
            crop = bench_crop(frame) if args.crop else (0, 0, w, h)
            source = args.src / split / frame["file"]
            target = args.out / "images" / role / frame["file"]
            if crop == (0, 0, w, h):
                put(source, target, args.link)
            elif not target.exists():
                image = cv2.imread(str(source))
                cv2.imwrite(str(target), image[crop[1] : crop[3], crop[0] : crop[2]])
            w, h = crop[2] - crop[0], crop[3] - crop[1]
            seen = []
            for bottle in frame["bottles"]:
                if bottle["visible_frac"] < MIN_VISIBLE or not bottle["pixels"]:
                    hidden += 1
                    continue
                seen.append(tuple(map(float, bottle["xyxy"])))
            lines = []
            for x0, y0, x1, y1 in crop_labels(seen, crop):
                x0, x1 = max(0.0, x0), min(float(w), x1)
                y0, y1 = max(0.0, y0), min(float(h), y1)
                if x1 <= x0 or y1 <= y0:
                    continue
                lines.append(
                    f"0 {(x0 + x1) / 2 / w:.6f} {(y0 + y1) / 2 / h:.6f} "
                    f"{(x1 - x0) / w:.6f} {(y1 - y0) / h:.6f}"
                )
            boxes += len(lines)
            stem = Path(frame["file"]).stem
            (args.out / "labels" / role / f"{stem}.txt").write_text("\n".join(lines))
        print(
            f"{split} -> {role}: {len(gt['frames'])} frames, {boxes} boxes, "
            f"{hidden} bottles under {MIN_VISIBLE:.0%} visible left out"
        )

    (args.out / "data.yaml").write_text(
        f"path: {args.out.resolve().as_posix()}\n"
        "train: images/train\n"
        "val: images/val\n"
        f"names: {{0: {CLASS_NAME}}}\n"
    )
    print(f"-> {args.out / 'data.yaml'}")


if __name__ == "__main__":
    main()
