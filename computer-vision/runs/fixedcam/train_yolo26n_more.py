"""Three more YOLO26n epochs from the epoch-1 checkpoint, once the CPU recovered

No warm-up (the weights are already trained), mosaic off for the last epoch,
crops read from disk (no RAM cache to be paged out).
"""
from ultralytics import YOLO

model = YOLO("runs/fixedcam/snapshots/yolo26n_ep1_last.pt")
model.train(
    data="../simulation/out/fixedcam/crops384/yolo/data.yaml",
    imgsz=384, epochs=3, close_mosaic=1, warmup_epochs=0, batch=16, workers=0,
    device="cpu", scale=0.25, cache=False, plots=True,
    project="runs/fixedcam", name="yolo26n_384_more", exist_ok=True,
)
