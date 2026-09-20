"""The viewer's deliberately pinned detector versions."""
from pathlib import Path

WEIGHTS_DIR = Path(__file__).resolve().parents[2] / 'computer-vision/weights'

# Intentionally hardcoded: upgrading the viewer's model or threshold requires
# changing this code. Environment variables must not override these values.
DETECTOR_SPEC = 'full'
DETECTOR_WEIGHTS = WEIGHTS_DIR / 'yolo26n_full_1920_e25.pt'
DETECTOR_CONF = 0.41

# Isaac Replay retains its separately selected model; upgrades also require code.
REPLAY_WEIGHTS = WEIGHTS_DIR / 'yolo26n_isaac_v2.pt'
REPLAY_INPUT_PX = 1600
# Initial inference cutoff, not a calibrated best-F1 score for these replay videos.
REPLAY_CONF = 0.25
