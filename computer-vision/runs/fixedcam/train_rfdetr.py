"""Fine-tune RF-DETR on the fixed-camera crops (COCO layout from fixedcam_crops.py)

python runs/fixedcam/train_rfdetr.py DATASET OUTPUT [--size nano] [--epochs 8]
[--threads 4] [--resolution 384] [--freeze-encoder]
"""
import argparse

import torch

parser = argparse.ArgumentParser()
parser.add_argument("dataset")
parser.add_argument("output")
parser.add_argument("--size", default="nano")
parser.add_argument("--epochs", type=int, default=8)
parser.add_argument("--threads", type=int, default=4)
parser.add_argument("--resolution", type=int, default=384)
parser.add_argument("--batch", type=int, default=4)
parser.add_argument("--accum", type=int, default=4)
parser.add_argument("--freeze-encoder", action="store_true")
args = parser.parse_args()
torch.set_num_threads(args.threads)

import rfdetr  # noqa: E402

cls = {"nano": rfdetr.RFDETRNano, "small": rfdetr.RFDETRSmall}[args.size]
model = cls(resolution=args.resolution, freeze_encoder=args.freeze_encoder)
model.train(
    dataset_dir=args.dataset,
    output_dir=args.output,
    epochs=args.epochs,
    batch_size=args.batch,
    grad_accum_steps=args.accum,
    lr=1e-4,
    resolution=args.resolution,
    multi_scale=False,
    expanded_scales=False,
    num_workers=0,
    device="cuda" if torch.cuda.is_available() else "cpu",
    early_stopping=True,
    early_stopping_patience=3,
    checkpoint_interval=1,
)
