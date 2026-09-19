"""Crop a frame to where the rail scene's bench can appear in it

The detector only has to find vials standing on the bench, so the model is
trained and run on the part of the frame the bench occupies, not the whole
frame. From the wall-mounted ``general`` camera that is a 1920 x 448 band
(rows 352 to 800), 41 % of the pixels, which is what brings the nano under
100 ms on the laptop's CPU; from an orbit camera it is wherever the bench
falls.

The crop is the projection of the worktop and the height its vials stand to,
padded and snapped to multiples of 32 px (the network's stride), clipped to
the frame. It needs only the camera's pose and field of view, so the same
function serves a rendered frame (its ``gt.json`` record) and the real camera
(its calibration).

    from bench_crop import bench_crop, crop_labels
    x0, y0, x1, y1 = bench_crop(frame)
"""

import math

import numpy as np

WORKTOP = ((-4.5, 1.5), (-1.4, 0.6))
"""The rail scene's worktop, x and y in metres (``fixedcam_dataset.SCENES``)."""
HEIGHTS = (0.90, 1.10)
"""From the bench top to above the tallest vial, metres."""
PAD = 8
STEP = 32
KEEP = 0.6
"""Share of a vial's box that must be inside the crop for it to stay labelled."""


def project(
    frame: dict, points: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Pixel columns, rows and depths of world points in a frame's camera

    Args:
        frame: A ``gt.json`` frame record: ``cam_pos``, ``cam_xmat`` (MuJoCo's
            row-major rotation, columns right, up, back), ``fovy_deg``,
            ``width``, ``height``.
        points: World points, shape (n, 3).
    """
    pos = np.asarray(frame["cam_pos"], float)
    rot = np.asarray(frame["cam_xmat"], float).reshape(3, 3)
    focal = frame["height"] / 2 / math.tan(math.radians(frame["fovy_deg"]) / 2)
    rel = (np.asarray(points, float) - pos) @ rot
    depth = -rel[:, 2]
    safe = np.maximum(depth, 1e-6)
    cols = frame["width"] / 2 + focal * rel[:, 0] / safe
    rows = frame["height"] / 2 - focal * rel[:, 1] / safe
    return cols, rows, depth


def bench_crop(frame: dict) -> tuple[int, int, int, int]:
    """The crop, x0, y0, x1, y1 in pixels, that holds every place a bench vial can be

    A bench corner behind the camera means the bench runs out of the frame on
    that side, so the crop keeps the whole frame along both axes there.
    """
    w, h = frame["width"], frame["height"]
    corners = np.array(
        [[x, y, z] for x in WORKTOP[0] for y in WORKTOP[1] for z in HEIGHTS]
    )
    cols, rows, depth = project(frame, corners)
    if (depth <= 0).any():
        return 0, 0, w, h

    def span(values: np.ndarray, size: int) -> tuple[int, int]:
        low = max(0, math.floor((values.min() - PAD) / STEP) * STEP)
        high = min(size, math.ceil((values.max() + PAD) / STEP) * STEP)
        return int(low), int(high)

    x0, x1 = span(cols, w)
    y0, y1 = span(rows, h)
    return x0, y0, x1, y1


def crop_labels(
    boxes: list[tuple[float, float, float, float]], crop: tuple[int, int, int, int]
) -> list[tuple[float, float, float, float]]:
    """Move boxes into a crop, dropping those left with under ``KEEP`` of their area

    Returns:
        The kept boxes, clipped to the crop, in the crop's pixel coordinates.
    """
    cx0, cy0, cx1, cy1 = crop
    kept = []
    for x0, y0, x1, y1 in boxes:
        area = max(0.0, x1 - x0) * max(0.0, y1 - y0)
        ix0, iy0 = max(x0, cx0), max(y0, cy0)
        ix1, iy1 = min(x1, cx1), min(y1, cy1)
        inside = max(0.0, ix1 - ix0) * max(0.0, iy1 - iy0)
        if area > 0 and inside / area >= KEEP:
            kept.append((ix0 - cx0, iy0 - cy0, ix1 - cx0, iy1 - cy0))
    return kept
