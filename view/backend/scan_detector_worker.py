"""Run the scan's original YOLO detector outside the camera server process."""
import contextlib
import json
from pathlib import Path
import sys
import time

import numpy as np


def main():
    output, source = sys.stdout, sys.stdin.buffer
    with contextlib.redirect_stdout(sys.stderr):
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'simulation/scripts'))
        import torch
        import vision_pick as vp

        torch.set_num_threads(2)
        torch.set_num_interop_threads(1)
        detector = vp.Detector(Path(sys.argv[1]), float(sys.argv[2]), None)
        for header in source:
            shape = json.loads(header)
            raw = source.read(int(np.prod(shape)))
            if len(raw) != int(np.prod(shape)):
                break
            try:
                frame = np.frombuffer(raw, dtype=np.uint8).reshape(shape)
                started = time.monotonic()
                result = {'boxes': [[*box.as_tuple(), score, label]
                                    for box, score, label in detector.detect(frame)]}
                result['inference_ms'] = round((time.monotonic() - started) * 1000)
            except Exception as exc:
                result = {'error': str(exc)}
            output.write(json.dumps(result) + '\n')
            output.flush()


if __name__ == '__main__':
    main()
