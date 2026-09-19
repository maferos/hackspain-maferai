"""Sequential on-demand YOLO on the replay video, isolated from rendering."""
import contextlib
import json
import math
import sys
import time


def main():
    output = sys.stdout
    with contextlib.redirect_stdout(sys.stderr):
        import cv2
        import torch
        from ultralytics import YOLO

        cv2.setNumThreads(1)
        torch.set_num_threads(2)
        torch.set_num_interop_threads(1)
        model = YOLO(sys.argv[1])
        video = cv2.VideoCapture(sys.argv[2])
        fps = video.get(cv2.CAP_PROP_FPS)
        count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        if not video.isOpened() or fps <= 0 or count <= 0:
            raise RuntimeError("Replay video unavailable")
        output.write(json.dumps({"ready": True, "duration": count / fps}) + "\n")
        output.flush()
        for line in sys.stdin:
            request = json.loads(line)
            target = float(request["time"])
            if not math.isfinite(target):
                raise ValueError("Invalid replay time")
            frame_index = int((target % (count / fps)) * fps)
            start = time.monotonic()
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ok, frame = video.read()
            if not ok:
                raise RuntimeError("Cannot decode replay frame")
            result = model.predict(frame, imgsz=1920, conf=0.47, verbose=False)[0]
            boxes = [[round(float(v), 1) for v in xyxy] + [round(float(score), 3)]
                     for xyxy, score in zip(result.boxes.xyxy.cpu().numpy(),
                                           result.boxes.conf.cpu().numpy(), strict=True)]
            payload = {"time": target, "width": frame.shape[1], "height": frame.shape[0],
                       "boxes": boxes, "inference_ms": round(sum(result.speed.values()), 1),
                       "processing_ms": round((time.monotonic() - start) * 1000, 1)}
            output.write(json.dumps(payload) + "\n")
            output.flush()
        video.release()


if __name__ == "__main__":
    main()
