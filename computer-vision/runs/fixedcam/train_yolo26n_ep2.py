"""A second YOLO26n epoch from the epoch-1 checkpoint: no mosaic, no warm-up

The learning rate falls linearly to 1 % over this one epoch, so it anneals the
epoch-1 weights on whole crops rather than restarting the schedule.
"""
import torch
from ultralytics import YOLO

torch.set_num_threads(6)
model = YOLO("runs/fixedcam/snapshots/yolo26n_ep1_last.pt")
model.train(
    data="../simulation/out/fixedcam/crops384/yolo/data.yaml",
    imgsz=384, epochs=1, close_mosaic=1, warmup_epochs=0, batch=16, workers=0,
    device="cpu", scale=0.25, cache=False, plots=False,
    project="runs/fixedcam", name="yolo26n_384_ep2", exist_ok=True,
)
