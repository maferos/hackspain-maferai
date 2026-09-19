"""Box the amber vials Isaac left unlabelled, once per camera

The open-bench scene has ~220 `stock_reserve` vials with no semantics, so
`lab_dataset_v2` has no boxes for them: amber vials identical to the labelled
SMP ones would train as background. In v2 no camera or bottle moves between
frames (checked here from the annotations), so YOLO-World L is run on one
frame per camera and its amber detections that match no label are written
out, to be added to every frame of that camera by `isaac_dataset_to_yolo.py
--extra`.

    python scripts/isaac_pseudo_label.py DATASET_DIR OUT_JSON [--conf 0.15]

Also writes OUT_JSON's folder/check_<cam>.jpg: green labels, red added boxes.
"""

import argparse
import collections
import json
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLOWorld

PROMPTS = {  # prompt -> is it an amber vial
    "amber glass bottle": True,
    "brown glass bottle": True,
    "small brown bottle": True,
    "white plastic bottle": False,
    "plastic bottle": False,
}

parser = argparse.ArgumentParser()
parser.add_argument("dataset", type=Path)
parser.add_argument("out", type=Path)
parser.add_argument("--frame", default="rgb_0000.png")
parser.add_argument("--weights", default="../yolov8l-worldv2.pt")
parser.add_argument("--conf", type=float, default=0.15)
parser.add_argument(
    "--max-iou", type=float, default=0.25, help="max IoU with an existing label"
)
parser.add_argument(
    "--min-amber", type=float, default=0.15, help="min share of amber pixels"
)
parser.add_argument(
    "--min-sat",
    type=int,
    default=140,
    help="HSV saturation an amber pixel needs; metal beakers reflect brown at low S",
)
args = parser.parse_args()

coco = json.loads((args.dataset / "annotations" / "instances.json").read_text())
camera_of = {im["id"]: im["camera"] for im in coco["images"]}
parts = collections.defaultdict(list)
for a in coco["annotations"]:
    x, y, w, h = a["bbox"]
    parts[a["image_id"], a["category_id"]].append((x, y, x + w, y + h))
merged = {
    k: (
        min(p[0] for p in v),
        min(p[1] for p in v),
        max(p[2] for p in v),
        max(p[3] for p in v),
    )
    for k, v in parts.items()
}

boxes_by_cam_cat = collections.defaultdict(list)
for (iid, cid), b in merged.items():
    boxes_by_cam_cat[camera_of[iid], cid].append(b)
shift = collections.defaultdict(float)
for (cam, _), bs in boxes_by_cam_cat.items():
    arr = np.array(bs)
    shift[cam] = max(shift[cam], float((arr.max(0) - arr.min(0)).max()))

first = {
    cam: next(
        im["id"]
        for im in coco["images"]
        if im["camera"] == cam and im["file_name"].endswith(args.frame)
    )
    for cam in sorted(set(camera_of.values()))
}


def area(boxes):
    """Area of xyxy boxes along the last axis"""
    return (boxes[..., 2] - boxes[..., 0]) * (boxes[..., 3] - boxes[..., 1])


def iou(box, boxes):
    """IoU of one xyxy box against an (N, 4) array of xyxy boxes"""
    x0 = np.maximum(box[0], boxes[:, 0])
    y0 = np.maximum(box[1], boxes[:, 1])
    x1 = np.minimum(box[2], boxes[:, 2])
    y1 = np.minimum(box[3], boxes[:, 3])
    inter = np.clip(x1 - x0, 0, None) * np.clip(y1 - y0, 0, None)
    return inter / (area(box) + area(boxes) - inter)


def amber_share(img, b):
    """Share of amber pixels in the central 60 % of box `b` of a BGR image"""
    x0, y0, x1, y1 = (int(round(v)) for v in b)
    dx, dy = (x1 - x0) // 5, (y1 - y0) // 5
    patch = img[y0 + dy : y1 - dy, x0 + dx : x1 - dx]
    if patch.size == 0:
        return 0.0
    hsv = cv2.cvtColor(patch, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    return float(
        ((h >= 5) & (h <= 30) & (s >= args.min_sat) & (v >= 30) & (v <= 230)).mean()
    )


model = YOLOWorld(args.weights)
model.set_classes(list(PROMPTS))
is_amber = list(PROMPTS.values())

out = {
    "source": f"{Path(args.weights).name}, conf >= {args.conf}, amber prompts, "
    f"IoU < {args.max_iou} with labels, "
    f"amber share >= {args.min_amber} at S >= {args.min_sat}",
    "class": "SMP",
    "static_shift_px": {},
    "cameras": {},
}
for cam, iid in first.items():
    path = args.dataset / "images" / cam / args.frame
    img = cv2.imread(str(path))
    labels = np.array([b for (i, _), b in merged.items() if i == iid])
    r = model.predict(
        str(path), imgsz=1600, conf=args.conf, iou=0.5, agnostic_nms=True, verbose=False
    )[0]
    added = []
    xyxy = r.boxes.xyxy.cpu().numpy()
    for b, c in zip(xyxy, r.boxes.cls.cpu().numpy().astype(int), strict=True):
        w, h = b[2] - b[0], b[3] - b[1]
        if not is_amber[c] or h < 1.1 * w or min(w, h) < 4:
            continue
        if len(labels) and iou(b, labels).max() >= args.max_iou:
            continue
        if amber_share(img, b) < args.min_amber:
            continue
        added.append([round(float(v), 1) for v in b])
    out["static_shift_px"][cam] = round(shift[cam], 2)
    out["cameras"][cam] = added
    print(
        f"{cam}: {len(labels)} labels, +{len(added)} amber vials, "
        f"max label shift across frames {shift[cam]:.2f} px"
    )

    for b in labels:
        cv2.rectangle(
            img, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 200, 0), 1
        )
    for b in added:
        cv2.rectangle(
            img, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), (0, 0, 255), 2
        )
    cv2.imwrite(
        str(args.out.parent / f"check_{cam}.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 85]
    )

args.out.write_text(json.dumps(out, indent=1))
print(f"-> {args.out}")
