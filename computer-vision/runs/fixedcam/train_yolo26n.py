"""First fine-tuning run: YOLO26n from COCO weights on 384 px native crops"""
from ultralytics import YOLO

model = YOLO("../yolo26n.pt")
model.train(
    data="../simulation/out/fixedcam/crops384/yolo/data.yaml",
    imgsz=384, epochs=8, close_mosaic=3, batch=16, workers=2, device="cpu",
    scale=0.25, cache="ram", patience=4, plots=True,
    project="runs/fixedcam", name="yolo26n_384", exist_ok=True,
)
