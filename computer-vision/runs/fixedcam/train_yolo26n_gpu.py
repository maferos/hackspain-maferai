"""Full GPU fine-tune of YOLO26n from COCO weights on the 384 px crops

The laptop only had budget for one real epoch before CPU throttling made
further ones cost ~5 hours each (see docs/FIXED_CAMERA_BENCHMARK.md, "Training
on this laptop"), so `train_yolo26n.py` and its `_b`/`_c`/`_ep2`/`_more`
follow-ups each squeezed in a few more epochs from the last checkpoint between
throttling windows. On the GPU that ../../../propuesta_gpu.md justifies
(Ampere or Ada, >= 24 GB VRAM), that chunking is unnecessary: this restarts
from the COCO weights for one proper run with mosaic and a full worker pool,
rather than continuing the choppy checkpoint lineage.

Run from computer-vision/, matching the other runs/fixedcam/*.py scripts:

    python runs/fixedcam/train_yolo26n_gpu.py
"""
import torch
from ultralytics import YOLO

assert torch.cuda.is_available(), (
    "no CUDA GPU visible - provision one per ../../../propuesta_gpu.md "
    "(Ampere/Ada, >= 24 GB VRAM, driver 570/580) before running this"
)

model = YOLO("../yolo26n.pt")
model.train(
    data="../simulation/out/fixedcam/crops384/yolo/data.yaml",
    imgsz=384, epochs=100, close_mosaic=10, batch=128, workers=8, device=0,
    scale=0.25, cache="ram", patience=15, plots=True,
    project="runs/fixedcam", name="yolo26n_384_gpu", exist_ok=True,
)
