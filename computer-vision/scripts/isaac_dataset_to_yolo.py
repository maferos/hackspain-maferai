"""Convert the Isaac Sim lab dataset (COCO, 5 camera folders) to a YOLO layout

Input is `lab_dataset_v2`'s own layout: `images/<cam>/rgb_NNNN.png` and
`annotations/instances.json`, where `file_name` already starts with `images/`
and the category name is the sample id (`PWD_0005`, `SMP_0012`).

Isaac boxes every mesh of a bottle separately (body, cap, label), so a bottle
has 2-4 boxes with the same category in one image. They are merged into one
box per (image, category), the union of the parts. A bottle is dropped when
even its most visible part is more than `--max-occlusion` hidden.

In v2 the bottles never move (only the light changes), so frames of the same
camera are near-duplicates: validation holds out whole cameras (`--val-cams`).

    python scripts/isaac_dataset_to_yolo.py DATASET_DIR OUT_DIR
        [--classes kind|bottle|barcode] [--val-cams room_wash] [--max-occlusion 0.9]
        [--link] [--extra extra_boxes.json]

Writes OUT_DIR/{images,labels}/{train,val}/<cam>_rgb_NNNN.{png,txt} and
OUT_DIR/data.yaml for `model.train(data=...)`.
"""

import argparse
import collections
import json
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("dataset", type=Path)
parser.add_argument("out", type=Path)
parser.add_argument(
    "--classes",
    choices=["kind", "bottle", "barcode"],
    default="kind",
    help="kind: PWD/SMP from the id prefix; bottle: one class; barcode: one per id",
)
parser.add_argument(
    "--val-cams", default="room_wash", help="comma-separated cameras held out"
)
parser.add_argument("--max-occlusion", type=float, default=0.9)
parser.add_argument(
    "--link", action="store_true", help="hardlink images instead of copying"
)
parser.add_argument(
    "--extra",
    type=Path,
    help="per-camera boxes from isaac_pseudo_label.py, added to every frame",
)
args = parser.parse_args()

coco = json.loads((args.dataset / "annotations" / "instances.json").read_text())
cat_name = {c["id"]: c["name"] for c in coco["categories"]}

if args.classes == "kind":
    names = sorted({n.split("_")[0] for n in cat_name.values()})
    class_of = {cid: names.index(n.split("_")[0]) for cid, n in cat_name.items()}
elif args.classes == "bottle":
    names = ["bottle"]
    class_of = {cid: 0 for cid in cat_name}
else:
    names = [cat_name[cid] for cid in sorted(cat_name)]
    class_of = {cid: names.index(cat_name[cid]) for cid in cat_name}

parts = collections.defaultdict(list)
for ann in coco["annotations"]:
    parts[(ann["image_id"], ann["category_id"])].append(ann)

bottles = collections.defaultdict(list)
dropped = 0
for (iid, cid), anns in parts.items():
    if min(a["occlusion"] for a in anns) > args.max_occlusion:
        dropped += 1
        continue
    x0 = min(a["bbox"][0] for a in anns)
    y0 = min(a["bbox"][1] for a in anns)
    x1 = max(a["bbox"][0] + a["bbox"][2] for a in anns)
    y1 = max(a["bbox"][1] + a["bbox"][3] for a in anns)
    bottles[iid].append((class_of[cid], x0, y0, x1, y1))

extra_by_cam = {}
if args.extra:
    extra = json.loads(args.extra.read_text())
    if args.classes == "barcode":
        parser.error("--extra boxes have no barcode id")
    extra_cls = names.index(extra["class"]) if args.classes == "kind" else 0
    extra_by_cam = {
        cam: [(extra_cls, *b) for b in bs] for cam, bs in extra["cameras"].items()
    }

val_cams = set(args.val_cams.split(",")) if args.val_cams else set()
for split in ("train", "val"):
    (args.out / "images" / split).mkdir(parents=True, exist_ok=True)
    (args.out / "labels" / split).mkdir(parents=True, exist_ok=True)

counts = collections.Counter()
for im in coco["images"]:
    split = "val" if im["camera"] in val_cams else "train"
    src = args.dataset / im["file_name"]
    flat = im["file_name"].removeprefix("images/").replace("/", "_")
    dst = args.out / "images" / split / flat
    if not dst.exists():
        if args.link:
            dst.hardlink_to(src)
        else:
            shutil.copy2(src, dst)

    w, h = im["width"], im["height"]
    lines = []
    for cls, x0, y0, x1, y1 in bottles.get(im["id"], []) + extra_by_cam.get(
        im["camera"], []
    ):
        x0, x1 = max(0.0, x0), min(float(w), x1)
        y0, y1 = max(0.0, y0), min(float(h), y1)
        if x1 <= x0 or y1 <= y0:
            continue
        lines.append(
            f"{cls} {(x0 + x1) / 2 / w:.6f} {(y0 + y1) / 2 / h:.6f} "
            f"{(x1 - x0) / w:.6f} {(y1 - y0) / h:.6f}"
        )
    (args.out / "labels" / split / (Path(flat).stem + ".txt")).write_text(
        "\n".join(lines)
    )
    counts[split, "images"] += 1
    counts[split, "boxes"] += len(lines)

(args.out / "data.yaml").write_text(
    f"path: {args.out.resolve().as_posix()}\n"
    "train: images/train\n"
    "val: images/val\n"
    f"names: {json.dumps(dict(enumerate(names)))}\n"
)

print(f"classes ({args.classes}): {names}")
print(
    f"{len(parts)} bottles after merging {len(coco['annotations'])} part boxes; "
    f"{dropped} dropped as > {args.max_occlusion} occluded"
)
for split in ("train", "val"):
    print(f"{split}: {counts[split, 'images']} images, {counts[split, 'boxes']} boxes")
print(f"-> {args.out / 'data.yaml'}")
