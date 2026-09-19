"""YOLO26n fine-tuning, three more epochs from the epoch-1 checkpoint

The laptop's CPU is held at a fifth of its speed, so the run is short, uses six
threads and reads the 384 px crops from disk (no RAM cache to be paged out).
"""
import torch
from ultralytics import YOLO

torch.set_num_threads(6)
model = YOLO("runs/fixedcam/snapshots/yolo26n_ep1_last.pt")
model.train(
    data="../simulation/out/fixedcam/crops384/yolo/data.yaml",
    imgsz=384, epochs=3, close_mosaic=1, batch=16, workers=0, device="cpu",
    scale=0.25, cache=False, patience=3, plots=True,
    project="runs/fixedcam", name="yolo26n_384_c", exist_ok=True,
)
