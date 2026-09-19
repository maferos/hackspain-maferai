"""Cut native-resolution training crops from fixed-camera frames, in YOLO and COCO

A 10 ml amber bottle is 8 x 15 px in the fixed camera's 1920 x 1080 frame.
Resizing the frame to a network's usual 640 px input would leave it 3 x 5 px,
so detectors are trained on square crops cut at the frame's own resolution
instead, and run at native resolution (or tile by tile) at inference. Crops
are centred near bottles on the worktop, plus one random crop of the worktop
region per frame for background and shelf clutter.

Every sample bottle in a crop is labelled, wherever it stands, as
``amber_bottle`` or ``hdpe_bottle``: a shelf bottle is a bottle, and telling
the bench from the shelf is the worktop filter's job, not the detector's.
A bottle is labelled when at least :data:`MIN_VISIBLE` of it is visible and
at least :data:`MIN_INSIDE` of its box lies in the crop; the box is clipped
to the crop.

    python scripts/fixedcam_crops.py --out ../simulation/out/fixedcam/crops640
    python scripts/fixedcam_crops.py --size 384 --degrade 0.5 --out .../crops384_deg

Layout written (images hard-linked between the two when possible):

- ``<out>/yolo/images/{train,val}``, ``<out>/yolo/labels/{train,val}``,
  ``<out>/yolo/data.yaml`` for Ultralytics.
- ``<out>/coco/{train,valid,test}/_annotations.coco.json`` next to the images,
  for RF-DETR (``test`` repeats ``valid``; the benchmark has its own tests).
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fixedcam_models as fm  # noqa: E402

from labvision import evaluation as ev  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "simulation" / "out" / "fixedcam"

MIN_VISIBLE = 0.3
"""Least visible fraction of a bottle for it to be labelled."""
MIN_INSIDE = 0.6
"""Least share of a bottle's box inside the crop for it to be labelled."""
MIN_SIDE_PX = 4
"""Boxes thinner than this after clipping are dropped."""


def crop_boxes(
    frame: dict, rect: tuple[int, int, int, int]
) -> list[tuple[int, float, float, float, float]]:
    """Return ``(kit, u0, v0, u1, v1)`` of the bottles labelled in a crop"""
    x0, y0, x1, y1 = rect
    out = []
    for bottle in frame["bottles"]:
        if bottle["visible_frac"] < MIN_VISIBLE or not bottle["pixels"]:
            continue
        box = bottle["xyxy"]
        if ev.fraction_inside(box, rect) < MIN_INSIDE:
            continue
        u0, v0 = max(box[0], x0) - x0, max(box[1], y0) - y0
        u1, v1 = min(box[2], x1) - x0, min(box[3], y1) - y0
        if u1 - u0 < MIN_SIDE_PX or v1 - v0 < MIN_SIDE_PX:
            continue
        kit = 0 if bottle["phase"] == "liquid" else 1
        out.append((kit, float(u0), float(v0), float(u1), float(v1)))
    return out


def pick_crops(
    frame: dict,
    roi: tuple[int, int, int, int],
    size: int,
    per_frame: int,
    rng: np.random.Generator,
    random_share: float = 1.0,
) -> list[tuple[int, int, int, int]]:
    """Choose crop rectangles: near uncovered bench bottles, and maybe one at random

    The random crop, drawn anywhere in the worktop region, is added to a
    ``random_share`` of the frames: it brings background and shelf clutter.
    """
    width, height = frame["width"], frame["height"]

    def clamp(cu: float, cv: float) -> tuple[int, int, int, int]:
        u0 = int(np.clip(cu - size / 2, 0, width - size))
        v0 = int(np.clip(cv - size / 2, 0, height - size))
        return u0, v0, u0 + size, v0 + size

    bench = [
        b for b in frame["bottles"]
        if b["where"] == "bench" and b["visible_frac"] >= MIN_VISIBLE
    ]  # fmt: skip
    uncovered = list(rng.permutation(len(bench)))
    rects = []
    while uncovered and len(rects) < per_frame:
        bottle = bench[uncovered.pop()]
        box = bottle["xyxy"]
        jitter = rng.uniform(-size / 3, size / 3, 2)
        rect = clamp(
            (box[0] + box[2]) / 2 + jitter[0], (box[1] + box[3]) / 2 + jitter[1]
        )
        rects.append(rect)
        uncovered = [
            i for i in uncovered if ev.fraction_inside(bench[i]["xyxy"], rect) < 0.99
        ]
    if rng.random() < random_share:
        u = rng.uniform(roi[0], max(roi[0] + 1, roi[2]))
        v = rng.uniform(roi[1], max(roi[1] + 1, roi[3]))
        rects.append(clamp(u, v))
    return rects


def link_or_copy(src: Path, dst: Path) -> None:
    """Hard-link a file, or copy it where links are not possible"""
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def export(
    splits: dict[str, str], out: Path, size: int, per_frame: int, degrade: float,
    seed: int, random_share: float = 1.0,
) -> dict[str, int]:  # fmt: skip
    """Cut and write the crops of every split, return how many per split"""
    rng = np.random.default_rng(seed)
    degrade_fn = None
    if degrade > 0:
        from fixedcam_dataset import degrade as degrade_fn
    counts = {}
    for sub_dir in ("yolo", "coco"):
        # Crops of an earlier export would stay in training otherwise.
        if (out / sub_dir).exists():
            shutil.rmtree(out / sub_dir)
    for source, target in splits.items():
        folder = DATA / source
        gt = json.loads((folder / "gt.json").read_text(encoding="utf-8"))
        worktop = ev.Worktop.from_gt(gt)
        img_dir = out / "yolo" / "images" / target
        lab_dir = out / "yolo" / "labels" / target
        img_dir.mkdir(parents=True, exist_ok=True)
        lab_dir.mkdir(parents=True, exist_ok=True)
        coco = {
            "images": [],
            "annotations": [],
            "categories": [
                {"id": k, "name": n, "supercategory": "bottle"}
                for k, n in enumerate(ev.CLASS_NAMES)
            ],
        }
        n = 0
        for frame in gt["frames"]:
            image = cv2.imread(str(folder / frame["file"]))
            roi = fm.worktop_roi(frame, worktop)
            for k, rect in enumerate(
                pick_crops(frame, roi, size, per_frame, rng, random_share)
            ):
                crop = image[rect[1] : rect[3], rect[0] : rect[2]]
                if degrade_fn is not None and rng.random() < degrade:
                    crop, _ = degrade_fn(np.ascontiguousarray(crop), rng)
                stem = f"{Path(frame['file']).stem}_c{k}"
                cv2.imwrite(str(img_dir / f"{stem}.jpg"), crop,
                            [cv2.IMWRITE_JPEG_QUALITY, 95])  # fmt: skip
                boxes = crop_boxes(frame, rect)
                lines = [
                    f"{kit} {(u0 + u1) / 2 / size:.6f} {(v0 + v1) / 2 / size:.6f} "
                    f"{(u1 - u0) / size:.6f} {(v1 - v0) / size:.6f}"
                    for kit, u0, v0, u1, v1 in boxes
                ]
                (lab_dir / f"{stem}.txt").write_text("\n".join(lines), encoding="utf-8")
                image_id = len(coco["images"])
                coco["images"].append(
                    {"id": image_id, "file_name": f"{stem}.jpg",
                     "width": size, "height": size}
                )  # fmt: skip
                for kit, u0, v0, u1, v1 in boxes:
                    coco["annotations"].append(
                        {"id": len(coco["annotations"]), "image_id": image_id,
                         "category_id": kit,
                         "bbox": [round(u0, 2), round(v0, 2), round(u1 - u0, 2),
                                  round(v1 - v0, 2)],
                         "area": round((u1 - u0) * (v1 - v0), 2), "iscrowd": 0}
                    )  # fmt: skip
                n += 1
        counts[target] = n
        coco_targets = ["train"] if target == "train" else ["valid", "test"]
        for name in coco_targets:
            coco_dir = out / "coco" / name
            coco_dir.mkdir(parents=True, exist_ok=True)
            for entry in coco["images"]:
                link_or_copy(
                    img_dir / entry["file_name"], coco_dir / entry["file_name"]
                )
            (coco_dir / "_annotations.coco.json").write_text(
                json.dumps(coco), encoding="utf-8"
            )
        boxes_total = len(coco["annotations"])
        print(f"{source} -> {target}: {n} crops, {boxes_total} boxes", flush=True)
    names = "\n".join(f"  {k}: {n}" for k, n in enumerate(ev.CLASS_NAMES))
    (out / "yolo" / "data.yaml").write_text(
        f"path: {(out / 'yolo').as_posix()}\ntrain: images/train\nval: images/val\n"
        f"names:\n{names}\n",
        encoding="utf-8",
    )
    return counts


def main() -> None:
    """Parse the command line and export"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=DATA / "crops640")
    parser.add_argument("--size", type=int, default=640, help="crop side, pixels")
    parser.add_argument("--per-frame", type=int, default=3, help="bottle crops/frame")
    parser.add_argument(
        "--degrade", type=float, default=0.0, help="share of crops degraded"
    )
    parser.add_argument("--train", default="train", help="split used for training")
    parser.add_argument("--val", default="val", help="split used for validation")
    parser.add_argument(
        "--random-share", type=float, default=1.0, help="frames with a random crop"
    )
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    export(
        {args.train: "train", args.val: "val"}, args.out, args.size,
        args.per_frame, args.degrade, args.seed, args.random_share,
    )  # fmt: skip


if __name__ == "__main__":
    main()
