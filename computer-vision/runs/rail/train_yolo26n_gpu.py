"""Fine-tune YOLO26n on the rail scene's fixed camera, whole frames at 1920 px

The amber bottles are 9 to 36 px from the ``general`` camera (median 17), so
the model takes the frame at its native resolution and random scale is held
to +-25 %. Sized for the GPU ../../../propuesta_gpu.md justifies (Ampere/Ada,
>= 24 GB VRAM). Build DATA_YAML with ``scripts/fixedcam_to_yolo.py`` first.

    python runs/rail/train_yolo26n_gpu.py DATA_YAML [--weights ../yolo26n.pt]
        [--epochs 80] [--imgsz 1920] [--batch 8]
"""

import argparse

import torch
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument("data")
parser.add_argument("--weights", default="../yolo26n.pt")
parser.add_argument("--epochs", type=int, default=80)
parser.add_argument("--imgsz", type=int, default=1920)
parser.add_argument("--batch", type=int, default=8)
parser.add_argument("--workers", type=int, default=8)
parser.add_argument("--patience", type=int, default=20)
parser.add_argument("--name", default="yolo26n_rail_general")
args = parser.parse_args()

assert torch.cuda.is_available(), (
    "no CUDA GPU visible - provision one per ../../../propuesta_gpu.md "
    "(Ampere/Ada, >= 24 GB VRAM, driver 570/580) before running this"
)

model = YOLO(args.weights)
model.train(
    data=args.data,
    imgsz=args.imgsz,
    epochs=args.epochs,
    patience=args.patience,
    batch=args.batch,
    workers=args.workers,
    device=0,
    cache="ram",
    scale=0.25,
    plots=True,
    project="runs/rail",
    name=args.name,
    exist_ok=True,
)
