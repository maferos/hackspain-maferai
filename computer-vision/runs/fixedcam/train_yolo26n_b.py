"""YOLO26n fine-tuning, continued from the epoch-1 checkpoint without a RAM cache

The first run lost most of its speed to paging when other jobs filled the
laptop's memory, so this one reads the 384 px crops from disk each time.
"""
from ultralytics import YOLO

model = YOLO("runs/fixedcam/snapshots/yolo26n_ep1_last.pt")
model.train(
    data="../simulation/out/fixedcam/crops384/yolo/data.yaml",
    imgsz=384, epochs=7, close_mosaic=3, batch=16, workers=0, device="cpu",
    scale=0.25, cache=False, patience=4, plots=True,
    project="runs/fixedcam", name="yolo26n_384_b", exist_ok=True,
)
