"""Bounded latest-frame JPEG encoding, independent of the GL render thread."""
import threading

import cv2

PREVIEW_SIZE = (640, 360)


class JpegEncoder:
    def __init__(self, quality=80):
        self.quality = quality
        self.pending = {}
        self.latest = {}
        self.condition = threading.Condition()

    def submit(self, camera, rgb):
        # Renderer returns a new owned array for each frame. Never mutate it.
        with self.condition:
            self.pending[camera] = rgb
            self.condition.notify()

    def run_forever(self):
        while True:
            with self.condition:
                self.condition.wait_for(lambda: bool(self.pending))
                camera = next(iter(self.pending))
                rgb = self.pending.pop(camera)
            bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            ok, data = cv2.imencode(".jpg", bgr, [cv2.IMWRITE_JPEG_QUALITY, self.quality])
            if not ok:
                continue
            full = data.tobytes()
            if (bgr.shape[1], bgr.shape[0]) == PREVIEW_SIZE:
                preview = full
            else:
                small = cv2.resize(bgr, PREVIEW_SIZE, interpolation=cv2.INTER_AREA)
                ok, data = cv2.imencode(".jpg", small, [cv2.IMWRITE_JPEG_QUALITY, self.quality])
                if not ok:
                    continue
                preview = data.tobytes()
            # Only publication takes the lock; neither rendering nor inference
            # ever waits for compression. Each camera has at most one pending RGB.
            with self.condition:
                self.latest[camera, False] = full
                self.latest[camera, True] = preview
                self.condition.notify_all()
