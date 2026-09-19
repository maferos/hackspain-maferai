"""Fine-tune YOLO26n on the Isaac Sim lab dataset (PWD/SMP by default)

Sized for the GPU ../../../propuesta_gpu.md justifies (Ampere/Ada,
>= 24 GB VRAM): native 1600 px frames, full worker pool, RAM cache.
Random scale is held to +-25 % because 17 % of the bottles are under 16 px.
Run `scripts/isaac_dataset_to_yolo.py` first to build DATA_YAML.

    python runs/isaac/train_yolo26n_gpu.py DATA_YAML [--weights ../yolo26n.pt]
        [--epochs 100] [--imgsz 1600] [--batch 16]
"""

import argparse

import torch
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument("data")
parser.add_argument("--weights", default="../yolo26n.pt")
parser.add_argument("--epochs", type=int, default=100)
parser.add_argument("--imgsz", type=int, default=1600)
parser.add_argument("--batch", type=int, default=16)
parser.add_argument("--workers", type=int, default=8)
parser.add_argument("--patience", type=int, default=15)
parser.add_argument("--name", default="yolo26n_isaac_v2")
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
    project="runs/isaac",
    name=args.name,
    exist_ok=True,
)
