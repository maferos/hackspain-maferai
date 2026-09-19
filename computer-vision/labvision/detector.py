"""Find vessels in a frame with a pretrained detector, no training needed

The barcode is the identity and :mod:`labvision.scene` is the geometry. What sits
between them is a box: *there is a bottle in these pixels*. This module produces
that box. Two backends were kept out of a benchmark of ten pretrained detectors
on real lab photographs (``docs/BENCHMARK.md``, next to this package):

``"world"``
    YOLO-World large with everyday prompts. The best quality: reliable down to
    24 px of vessel side at a 960 px input. About 1.9 s per frame on a CPU,
    real time on a GPU.
``"coco"``
    YOLO11 small with its fixed COCO vocabulary filtered to bottle, cup, wine
    glass, vase and bowl. No prompts, the most robust on small empty vessels,
    about 0.7 s per frame on a CPU at 960 px.

Both return the same :class:`Box`, which carries a :class:`labvision.scene.BBox`
ready for :func:`labvision.scene.locate` and a slot for the barcode read inside
it by :func:`attach_barcodes`. The label the detector gives is not the identity:
a beaker labelled ``cup`` is normal and correct enough.

The size floor matters more than the model. A vessel needs about **48 px of
side at the network input** to be found reliably; between 24 and 48 px it is a
coin toss; below 24 px it is lost. Check a camera against that before trusting
it with :func:`apparent_size_px`. The scene's camera in :mod:`labvision.scene`,
a GoPro in Linear mode at 1080p 3.23 m from the bench, puts a 1 L bottle at
25 x 62 px (a side of 40 px, coin-toss territory) and a 100 ml bottle at a side
of 19 px, which is lost. That is at the frame's own resolution: inference at
the usual 640 or 960 halves it or worse, which is why the default input here is
the native frame. At 4K the 1 L bottle has a side of 79 px and the 250 ml one
51 px, so 4K, or the Narrow lens at 1080p, is what makes that camera usable.

Command line, over a folder of frames, a single image or a video::

    python -m labvision.detector ../simulation/out/minihannover_scene
    python -m labvision.detector frames/ --backend both --barcodes
    python -m labvision.detector capture.mp4 --backend coco --max 200 --device cuda:0

Overlays go to ``results/detect/<backend>/`` and one JSON line per frame to
``results/detect/<backend>.jsonl``.
"""

import argparse
import json
import math
import statistics
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from labvision import reader
from labvision.camera import Intrinsics
from labvision.scene import BBox, Vessel, default_intrinsics

PROMPTS: tuple[str, ...] = (
    "bottle",
    "plastic bottle",
    "cup",
    "drinking glass",
    "glass",
    "jar",
    "beaker",
    "glass flask",
    "vial",
)
"""Class names for the open-vocabulary backend. Everyday words first: the
benchmark showed "cup" and "glass" are what make empty glassware appear, while
laboratory vocabulary on its own loses half of it."""

BOTTLE_PROMPTS: tuple[str, ...] = (
    "bottle",
    "plastic bottle",
    "amber glass bottle",
    "brown glass bottle",
    "small brown bottle",
    "white plastic bottle",
    "reagent bottle",
    "medicine bottle",
    "bottle with a white label",
)
"""Class names that describe the sample bottles themselves. On the fixed
camera's renders they beat :data:`PROMPTS` by about 0.3 AP50 with YOLO-World L
(``docs/FIXED_CAMERA_BENCHMARK.md``): naming what the samples are works,
naming other vessels only adds false boxes."""

COCO_KEEP: frozenset[str] = frozenset({"bottle", "cup", "wine glass", "vase", "bowl"})
"""COCO classes that stand for a vessel; everything else the model says is dropped."""

SIDE_PX_RELIABLE = 48
"""Vessel side, in network-input pixels, above which detection is reliable."""

SIDE_PX_MARGINAL = 24
"""Below this side the vessel is lost; between this and reliable it is a coin toss."""

DEFAULT_INPUT_PX: int | None = None
"""Long side the frame is resized to before inference. None keeps the frame's own
size, rounded up to a multiple of 32. Downscaling a 1080p frame to 960 halves
every vessel and pushes the whole bottle kit under the floor at 3.2 m."""


def input_size_for(image: np.ndarray, input_px: int | None) -> int:
    """Return the network input size for a frame: the override, or its own long side"""
    if input_px is not None:
        return input_px
    return int(math.ceil(max(image.shape[:2]) / 32.0) * 32)


@dataclass(frozen=True)
class Backend:
    """One pretrained detector configuration

    Attributes:
        weights: Ultralytics weights file; downloaded on first use if absent.
        score: Confidence threshold, the best-F1 point measured in the benchmark.
        prompts: Class names for an open-vocabulary model, or None for a fixed one.
        keep: Fixed-vocabulary classes that count as a vessel, or None for all.
    """

    weights: str
    score: float
    prompts: tuple[str, ...] | None = None
    keep: frozenset[str] | None = None


BACKENDS: dict[str, Backend] = {
    "world": Backend("yolov8l-worldv2.pt", 0.11, prompts=PROMPTS),
    "coco": Backend("yolo11s.pt", 0.08, keep=COCO_KEEP),
    "world-s": Backend("yolov8s-worldv2.pt", 0.17, prompts=PROMPTS),
    "world-bottles": Backend("yolov8l-worldv2.pt", 0.12, prompts=BOTTLE_PROMPTS),
    "coco26": Backend("yolo26s.pt", 0.13, keep=COCO_KEEP),
    "fixedcam": Backend("yolo26n_fixedcam.pt", 0.07),
    "rail": Backend("yolo26n_rail_general.pt", 0.10),
    # The harness names this one `mujoco`; same weights, same threshold.
    "mujoco": Backend("yolo26n_rail_general.pt", 0.10),
}
"""The two backends chosen on real photographs, the small YOLO-World as a fast
variant that loses distant vessels, and three chosen on the fixed camera's
renders (``docs/FIXED_CAMERA_BENCHMARK.md``): YOLO-World L with bottle prompts,
YOLO26s on COCO, and ``fixedcam``, a YOLO26n fine-tuned on simulator-labelled
crops whose classes are ``amber_bottle`` and ``hdpe_bottle``.

``rail`` is the one trained on the rail scene's own general-camera
renders. Neither trained
backend's weights are in git: drop the file in ``computer-vision/weights/``
and the name works. Adding another model is one entry here, and every script
that takes ``--weights`` accepts a backend name as well as a path, so nothing
else has to change.

The three fixed-camera thresholds are the best-F1 points on the validation
frames for the whole frame with no filter, which is what :class:`Detector`
sees. On the fixed camera, pass the boxes through
:func:`labvision.evaluation.on_worktop` as well: every sample bottle is a
bottle, the gantry's included, and only the camera's geometry tells the bench
from the shelf (0.64 to 0.80 AP50 for ``fixedcam`` on validation)."""

FIXEDCAM_HELP = (
    "the fine-tuned fixed-camera weights are made by training, not downloaded: "
    "render with scripts/fixedcam_dataset.py, cut crops with "
    "scripts/fixedcam_crops.py, train YOLO26n on them (see "
    "docs/FIXED_CAMERA_BENCHMARK.md), and copy best.pt to "
    "computer-vision/runs/fixedcam/yolo26n_fixedcam.pt, or pass weights=..."
)

IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".bmp"})
VIDEO_SUFFIXES = frozenset({".mp4", ".avi", ".mov", ".mkv"})


@dataclass
class Box:
    """One detected vessel

    Attributes:
        label: The detector's class name. Not the identity; see the barcode.
        score: Detector confidence in [0, 1].
        bbox: The box in pixels, ready for :func:`labvision.scene.locate`.
        barcode: The EAN-13 read inside the box, or None if none decoded.
    """

    label: str
    score: float
    bbox: BBox
    barcode: str | None = None

    @property
    def side_px(self) -> float:
        """Geometric mean of width and height, the size the floor is stated in"""
        return math.sqrt(self.bbox.width * self.bbox.height)

    @property
    def centre(self) -> tuple[float, float]:
        """Box centre as (u, v)"""
        return (
            (self.bbox.u_min + self.bbox.u_max) / 2.0,
            (self.bbox.v_min + self.bbox.v_max) / 2.0,
        )

    def to_json(self) -> dict[str, object]:
        """Return a JSON-serialisable record of this box"""
        return {
            "label": self.label,
            "score": round(self.score, 3),
            "xyxy": [round(v, 1) for v in self.bbox.as_tuple()],
            "side_px": round(self.side_px, 1),
            "barcode": self.barcode,
        }


WEIGHTS_DIR = Path(__file__).resolve().parents[1] / "weights"
"""Where trained weights are kept. Nothing in it is in git except its README;
dropping a ``.pt`` there is all it takes to make a backend usable."""


def _find_weights(name: str) -> str:
    """Return a local path for the weights if one exists, else the bare name

    Looks in the weights folder first, then the places a download or an older
    benchmark run may have left a file, and finally hands the bare name back to
    Ultralytics, which downloads its own published models.

    Args:
        name: File name or path.

    Returns:
        A path that exists, or the name unchanged.
    """
    here = Path(__file__).resolve()
    if Path(name).is_absolute() and Path(name).exists():
        return name
    for folder in (WEIGHTS_DIR, Path.cwd(), here.parents[1], here.parents[2],
                   here.parents[1] / "runs/fixedcam"):
        candidate = folder / name
        if candidate.exists():
            return str(candidate)
    return name


def resolve(weights: str | None) -> tuple[str, float | None]:
    """Turn what a caller typed into a weights path and a threshold.

    ``--weights`` takes a backend name or a path, so a new model is usable the
    moment its file is in the weights folder and its name is in BACKENDS ---
    no script has to change.

    Args:
        weights: A key of BACKENDS, a path, or None.

    Returns:
        The weights path and the backend's own threshold, or None for a path
        with no backend behind it.

    Raises:
        FileNotFoundError: If a named backend's file is not on disk.
    """
    if weights is None:
        return "", None
    spec = BACKENDS.get(weights)
    if spec is None:
        return _find_weights(weights), None
    path = _find_weights(spec.weights)
    if not Path(path).exists():
        raise FileNotFoundError(
            f"backend {weights!r} wants {spec.weights}, which is not in "
            f"{WEIGHTS_DIR}. Trained weights are not in git --- see "
            f"{WEIGHTS_DIR / 'README.md'}.")
    return path, spec.score


class Detector:
    """A pretrained vessel detector behind one ``detect`` call

    Args:
        backend: Key in :data:`BACKENDS`.
        input_px: Long side the frame is resized to before inference, or None
            for the frame's own size. See :data:`DEFAULT_INPUT_PX`.
        score: Confidence threshold, overriding the backend's measured optimum.
        device: Torch device such as ``"cuda:0"``; None picks a GPU if present.
        weights: Weights file, overriding the backend's.

    Raises:
        ValueError: If the backend name is unknown.
    """

    def __init__(
        self,
        backend: str = "world",
        *,
        input_px: int | None = DEFAULT_INPUT_PX,
        score: float | None = None,
        device: str | None = None,
        weights: str | None = None,
    ) -> None:
        """Load the backend's weights and, for an open-vocabulary model, its prompts"""
        if backend not in BACKENDS:
            raise ValueError(f"unknown backend {backend!r}; one of {sorted(BACKENDS)}")
        from ultralytics import YOLO, YOLOWorld

        spec = BACKENDS[backend]
        self.backend = backend
        self.input_px = input_px
        self.score = spec.score if score is None else score
        self.device = device
        self.keep = spec.keep
        path = _find_weights(weights or spec.weights)
        if spec.prompts is None and not Path(path).exists():
            raise FileNotFoundError(
                f"{path} is not on disk. Trained weights are not in git; put "
                f"the file in {WEIGHTS_DIR} --- see its README. "
                + (FIXEDCAM_HELP if backend == "fixedcam" else ""))
        if spec.prompts is not None:
            self.model = YOLOWorld(path)
            self.model.set_classes(list(spec.prompts))  # downloads CLIP the first time
        else:
            self.model = YOLO(path)

    def detect(self, image: np.ndarray) -> list[Box]:
        """Find every vessel in a BGR frame

        Args:
            image: (H, W, 3) uint8 BGR frame, as OpenCV reads it.

        Returns:
            One box per vessel, in no particular order, barcode unset.
        """
        result = self.model.predict(
            image,
            imgsz=input_size_for(image, self.input_px),
            conf=self.score,
            iou=0.6,
            agnostic_nms=True,
            max_det=300,
            device=self.device,
            verbose=False,
        )[0]
        boxes: list[Box] = []
        for hit in result.boxes:
            label = result.names[int(hit.cls)]
            if self.keep is not None and label not in self.keep:
                continue
            u_min, v_min, u_max, v_max = (float(v) for v in hit.xyxy[0])
            if u_max <= u_min or v_max <= v_min:
                continue
            boxes.append(Box(label, float(hit.conf), BBox(u_min, v_min, u_max, v_max)))
        return boxes

    def warmup(self, shape: tuple[int, int, int] = (1080, 1920, 3)) -> None:
        """Run one blank frame so the first real one is not slowed by lazy setup

        Pass the shape of the frames to come: the backend sizes its input for
        the first shape it sees, and a frame of another shape is cold again.
        """
        self.detect(np.zeros(shape, np.uint8))


def attach_barcodes(
    image: np.ndarray, boxes: list[Box], *, margin: float = 0.15
) -> list[Box]:
    """Read the barcode inside each box and record it on the box

    Each box is cropped with a margin, so the label's quiet zones survive, and
    handed to :func:`labvision.reader.decode_image`. A crop narrower than the
    reader's floor of about 190 px will not decode; that is expected at range,
    and is why the fixed camera proposes and the wrist camera confirms.

    Args:
        image: The full-resolution BGR frame the boxes were detected in.
        boxes: Boxes to read, mutated in place.
        margin: Crop padding as a fraction of the box size.

    Returns:
        The same boxes, for chaining.
    """
    height, width = image.shape[:2]
    detector = reader.make_detector()
    for box in boxes:
        pad_u = margin * box.bbox.width
        pad_v = margin * box.bbox.height
        u0 = max(0, int(box.bbox.u_min - pad_u))
        v0 = max(0, int(box.bbox.v_min - pad_v))
        u1 = min(width, int(math.ceil(box.bbox.u_max + pad_u)))
        v1 = min(height, int(math.ceil(box.bbox.v_max + pad_v)))
        if u1 - u0 < 8 or v1 - v0 < 8:
            continue
        hits = reader.decode_image(image[v0:v1, u0:u1], detector)
        if hits:
            box.barcode = hits[0].code
    return boxes


def apparent_size_px(
    vessel: Vessel,
    range_m: float,
    intrinsics: Intrinsics | None = None,
    *,
    input_px: int | None = None,
) -> tuple[float, float]:
    """Predict how many pixels a vessel covers at a given range

    A pinhole approximation, good to a few percent for a vessel small next to
    its range. Use it to check a camera placement against the size floor
    before rendering anything.

    Args:
        vessel: The vessel, for its diameter and height.
        range_m: Distance from the camera centre to the vessel.
        intrinsics: The camera, defaulting to the scene's GoPro at 1080p.
        input_px: If given, scale to the network input of that long side.

    Returns:
        (width_px, height_px) in the frame, or at the network input.

    Example:
        >>> from labvision.scene import VESSELS
        >>> w, h = apparent_size_px(VESSELS["bottle_1000ml"], 3.23)
        >>> round(w), round(h)
        (25, 62)
    """
    cam = intrinsics or default_intrinsics()
    width_px = cam.fx * vessel.diameter_m / range_m
    height_px = cam.fy * vessel.height_m / range_m
    if input_px is not None:
        scale = input_px / max(cam.width, cam.height)
        width_px *= scale
        height_px *= scale
    return width_px, height_px


def draw(image: np.ndarray, boxes: list[Box]) -> np.ndarray:
    """Return a copy of the frame with the boxes drawn on it"""
    out = image.copy()
    for box in boxes:
        u0, v0, u1, v1 = (int(round(v)) for v in box.bbox.as_tuple())
        cv2.rectangle(out, (u0, v0), (u1, v1), (0, 140, 255), 2)
        text = f"{box.label} {box.score:.2f}"
        if box.barcode:
            text += f" [{box.barcode}]"
        cv2.putText(
            out,
            text,
            (u0, max(14, v0 - 5)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 140, 255),
            2,
        )
    return out


def iter_frames(
    source: Path, limit: int | None = None
) -> Iterator[tuple[str, np.ndarray]]:
    """Yield (name, BGR frame) from a folder of images, a video or one image

    Args:
        source: Folder, video file or image file.
        limit: Stop after this many frames.

    Raises:
        SystemExit: If nothing readable is found.
    """
    if source.is_dir():
        paths = sorted(
            p for p in source.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES
        )
        if not paths:
            raise SystemExit(f"no images in {source}")
        for path in paths[:limit]:
            image = cv2.imread(str(path))
            if image is not None:
                yield path.stem, image
    elif source.suffix.lower() in VIDEO_SUFFIXES:
        capture = cv2.VideoCapture(str(source))
        index = 0
        while capture.isOpened() and (limit is None or index < limit):
            ok, image = capture.read()
            if not ok:
                break
            yield f"{source.stem}_{index:05d}", image
            index += 1
        capture.release()
    else:
        image = cv2.imread(str(source))
        if image is None:
            raise SystemExit(f"cannot read {source}")
        yield source.stem, image


def main(argv: list[str] | None = None) -> None:
    """Run one or both backends over frames and report boxes and timing"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("source", help="folder of frames, an image or a video")
    parser.add_argument(
        "--backend",
        default="world",
        choices=[*BACKENDS, "both"],
        help="'both' = world and coco",
    )
    parser.add_argument(
        "--input-px",
        type=int,
        default=DEFAULT_INPUT_PX,
        help="network input long side; default: the frame's own size",
    )
    parser.add_argument(
        "--score", type=float, default=None, help="override the threshold"
    )
    parser.add_argument(
        "--device", default=None, help="e.g. cuda:0; default GPU if present"
    )
    parser.add_argument(
        "--barcodes", action="store_true", help="read the EAN-13 inside each box"
    )
    parser.add_argument(
        "--max", type=int, default=None, help="stop after this many frames"
    )
    parser.add_argument("--out", default="results/detect")
    parser.add_argument("--no-overlay", action="store_true")
    args = parser.parse_args(argv)

    backends = ["world", "coco"] if args.backend == "both" else [args.backend]
    source = Path(args.source)
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    for name in backends:
        detector = Detector(
            name, input_px=args.input_px, score=args.score, device=args.device
        )
        out_dir = out_root / name
        out_dir.mkdir(parents=True, exist_ok=True)
        times_ms: list[float] = []
        counts: list[int] = []
        sides: list[float] = []
        with (out_root / f"{name}.jsonl").open("w", encoding="utf-8") as log:
            for stem, image in iter_frames(source, args.max):
                if not times_ms:
                    detector.warmup(image.shape)
                start = time.perf_counter()
                boxes = detector.detect(image)
                elapsed_ms = 1000.0 * (time.perf_counter() - start)
                if args.barcodes:
                    attach_barcodes(image, boxes)
                times_ms.append(elapsed_ms)
                counts.append(len(boxes))
                sides.extend(b.side_px for b in boxes)
                record = {
                    "frame": stem,
                    "ms": round(elapsed_ms),
                    "boxes": [b.to_json() for b in boxes],
                }
                log.write(json.dumps(record) + "\n")
                if not args.no_overlay:
                    cv2.imwrite(str(out_dir / f"{stem}.png"), draw(image, boxes))
                print(
                    f"[{name}] {stem}: {len(boxes)} boxes, {elapsed_ms:.0f} ms",
                    flush=True,
                )
        if times_ms:
            median_ms = statistics.median(times_ms)
            side_note = (
                f", median box side {statistics.median(sides):.0f} px in the frame"
                if sides
                else ""
            )
            print(
                f"\n[{name}] {len(times_ms)} frames, median {median_ms:.0f} ms/frame "
                f"({1000.0 / median_ms:.1f} fps), "
                f"{statistics.mean(counts):.1f} boxes/frame"
                f"{side_note}; overlays in {out_dir}\n"
            )


if __name__ == "__main__":
    main()
