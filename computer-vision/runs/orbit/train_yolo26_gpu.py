"""Fine-tune a YOLO26 of any size on the rail scene seen from anywhere

One run of the study in ``docs/YOLO26_STUDY.md``. ``runs/rail`` trained the
nano on the wall mount alone, where a bottle is 9 to 36 px; with the ``orbit_*``
and ``close_*`` splits a bottle is 10 to 300 px, so random scale goes back to
Ultralytics' +-50 % and the question becomes whether the nano still holds it
all. The input size is the other half of the question: the detector has 100 ms
a frame, which on a laptop CPU is the nano at 1280 px or the small at 960, so
the model is trained at the size it will run at rather than at the frames'
1920. Build DATA_YAML with ``scripts/fixedcam_to_yolo.py`` first.

    python runs/orbit/train_yolo26_gpu.py DATA_YAML --size n --imgsz 1280
        --name n_all_1280 [--fraction 0.33] [--epochs 50] [--batch 16]
    python runs/orbit/train_yolo26_gpu.py DATA_YAML --size n --imgsz 1920
        --weights weights/yolo26n_rail_general.pt --name n_sel_1920
"""

import argparse

import torch
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument("data")
parser.add_argument("--size", default="s", choices=["n", "s", "m", "l"])
parser.add_argument("--weights", default=None, help="start here, not from COCO")
parser.add_argument("--name", required=True)
parser.add_argument("--epochs", type=int, default=50)
parser.add_argument("--imgsz", type=int, default=1280)
parser.add_argument("--batch", type=int, default=None, help="default: by size, imgsz")
parser.add_argument("--fraction", type=float, default=1.0, help="share of train used")
parser.add_argument("--scale", type=float, default=0.5)
parser.add_argument("--workers", type=int, default=8)
parser.add_argument("--patience", type=int, default=12)
parser.add_argument("--cache", default="", choices=["", "ram", "disk"],
                    help="ram when the decoded frames fit: about 4 MB a bench crop")
args = parser.parse_args()

assert torch.cuda.is_available(), (
    "no CUDA GPU visible - provision one per ../../../propuesta_gpu.md "
    "(Ampere/Ada, >= 24 GB VRAM, driver 570/580) before running this"
)

model = YOLO(args.weights or f"yolo26{args.size}.pt")
model.train(
    data=args.data,
    imgsz=args.imgsz,
    epochs=args.epochs,
    patience=args.patience,
    # 8 whole frames at 1920 px fit 24 GB for n and s; scale with the pixels.
    batch=args.batch
    or max(2, int((8 if args.size in "ns" else 4) * (1920 / args.imgsz) ** 2)),
    fraction=args.fraction,
    workers=args.workers,
    device=0,
    cache=args.cache or False,
    scale=args.scale,
    plots=True,
    project="runs/orbit",
    name=args.name,
    exist_ok=True,
)
