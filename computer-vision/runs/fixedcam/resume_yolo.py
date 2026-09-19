"""Resume an Ultralytics training run from its last checkpoint"""
import sys

from ultralytics import YOLO

YOLO(sys.argv[1]).train(resume=True)
