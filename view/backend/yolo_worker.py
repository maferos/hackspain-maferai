"""YOLO subprocess: raw RGB frames in, JSON detections out over private pipes.

Keeping torch and preprocessing out of the renderer's Python process prevents
inference from holding its GIL or changing its native thread-pool settings.
"""
import contextlib
import json
import sys
import time

from table_crop import table_region


def main():
    output = sys.stdout
    source = sys.stdin.buffer
    # Ultralytics logs must never enter the result protocol.
    with contextlib.redirect_stdout(sys.stderr):
        import cv2
        import numpy as np
        import torch
        from ultralytics import YOLO

        cv2.setNumThreads(1)
        torch.set_num_threads(int(sys.argv[3]))
        torch.set_num_interop_threads(1)
        model = YOLO(sys.argv[1])
        confidence = float(sys.argv[2])
        for header in source:
            shape = json.loads(header)
            size = int(np.prod(shape))
            raw = source.read(size)
            if len(raw) != size:
                break
            try:
                frame = np.frombuffer(raw, dtype=np.uint8).reshape(shape)
                start = time.monotonic()
                cropped, top = table_region(frame)
                result = model.predict(
                    np.ascontiguousarray(cropped[:, :, ::-1]),
                    imgsz=max(shape[:2]), conf=confidence, verbose=False,
                )[0]
                coordinates = result.boxes.xyxy.cpu().numpy().copy()
                coordinates[:, [1, 3]] += top
                boxes = [
                    [round(float(v), 1) for v in xyxy] + [round(float(score), 3)]
                    for xyxy, score in zip(coordinates,
                                          result.boxes.conf.cpu().numpy(), strict=True)
                ]
                payload = {"boxes": boxes, "inference_ms": round((time.monotonic() - start) * 1000)}
            except Exception as exc:
                payload = {"error": str(exc)}
            output.write(json.dumps(payload) + "\n")
            output.flush()


if __name__ == "__main__":
    main()
