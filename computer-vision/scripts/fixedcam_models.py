"""Every detector the fixed-camera benchmark compares, behind one ``predict`` call

A predictor takes a BGR frame and returns :class:`labvision.evaluation.Detection`
boxes, each tagged with a kit (``0`` amber, ``1`` HDPE) when the model can
tell, or ``-1`` when it only says *bottle*. Scoring, thresholds and reports
live in ``fixedcam_bench.py``; this module only runs models.

Families:

- **Ultralytics** (:class:`UltralyticsPredictor`): YOLO-World v2 and YOLOE with
  text prompts, YOLOE with visual prompts (example boxes from one reference
  frame), COCO-pretrained YOLO11 / YOLO26 filtered to vessel classes, and any
  fine-tuned YOLO weights.
- **Transformers** (:class:`GroundingDinoPredictor`): Grounding DINO with the
  same bottle prompts.
- **RF-DETR** (:class:`RfDetrPredictor`): fine-tuned weights.
- **Tiling** (:class:`TiledPredictor`): wraps any of the above and runs it over
  overlapping tiles of the worktop's image region, optionally upsampled, then
  merges with non-maximum suppression. This is how a model trained on native
  crops, or one that downsizes its input, sees 8 px wide bottles.

The worktop region is computed from the camera's calibrated pose and the
bench outline (:func:`worktop_roi`), never from where the bottles are.
"""

import math
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision import evaluation as ev  # noqa: E402

REPO = Path(__file__).resolve().parents[2]

GENERIC_PROMPTS: dict[str, int | None] = {
    p: -1
    for p in (
        "bottle", "plastic bottle", "cup", "drinking glass", "glass", "jar",
        "beaker", "glass flask", "vial",
    )
}  # fmt: skip
"""``labvision.detector.PROMPTS``, the vocabulary chosen on real photographs."""

BOTTLE_PROMPTS: dict[str, int | None] = {
    "bottle": -1,
    "plastic bottle": 1,
    "amber glass bottle": 0,
    "brown glass bottle": 0,
    "small brown bottle": 0,
    "white plastic bottle": 1,
    "reagent bottle": -1,
    "medicine bottle": -1,
    "bottle with a white label": -1,
}
"""The winning vocabulary of ``world_prompts.py`` (bottles only), each prompt
mapped to the kit it names, or -1 when it names neither."""

COCO_VESSELS: dict[str, int | None] = {
    "bottle": -1,
    "cup": -1,
    "wine glass": -1,
    "vase": -1,
    "bowl": -1,
}
"""COCO classes that stand for a vessel, as in ``labvision.detector.COCO_KEEP``."""


def find_weights(name: str) -> str:
    """Return a local path for a weights file if one exists, else the name"""
    for folder in (Path.cwd(), REPO, REPO / "computer-vision"):
        candidate = folder / name
        if candidate.exists():
            return str(candidate)
    return name


def native_size(image: np.ndarray) -> int:
    """Return the frame's long side rounded up to a multiple of 32"""
    return int(math.ceil(max(image.shape[:2]) / 32.0) * 32)


class UltralyticsPredictor:
    """An Ultralytics detector with its class names mapped to the two kits

    Args:
        weights: Weights file or name.
        family: ``yolo`` (fixed classes or fine-tuned), ``world`` (YOLO-World)
            or ``yoloe``.
        classes: Map from the model's class name to a kit index, -1 for "a
            bottle of either kit", None to drop that class. For ``world`` and
            ``yoloe`` the keys are the text prompts. None keeps every class,
            mapped by index (a fine-tuned model on :data:`ev.CLASS_NAMES`).
        imgsz: Network input long side; None for the frame's own size.
        conf: Lowest score kept; low, so the benchmark sees the whole curve.
        visual: For ``yoloe`` with visual prompts, ``(reference image, boxes,
            kits)``: the example boxes that stand for each kit.
    """

    def __init__(
        self,
        weights: str,
        family: str = "yolo",
        classes: dict[str, int | None] | None = None,
        imgsz: int | None = None,
        conf: float = 0.02,
        visual: tuple[np.ndarray, np.ndarray, np.ndarray] | None = None,
    ) -> None:
        """Load the weights and set the prompts"""
        from ultralytics import YOLO, YOLOE, YOLOWorld

        path = find_weights(weights)
        self.imgsz = imgsz
        self.conf = conf
        self.classes = classes
        if family == "world":
            self.model = YOLOWorld(path)
            self.model.set_classes(list(classes))
        elif family == "yoloe" and visual is None:
            self.model = YOLOE(path)
            names = list(classes)
            self.model.set_classes(names, self.model.get_text_pe(names))
        elif family == "yoloe":
            from ultralytics.models.yolo.yoloe import YOLOEVPSegPredictor

            self.model = YOLOE(path)
            reference, boxes, kits = visual
            # The first call turns the example boxes into class embeddings and
            # keeps them; later calls are plain predictions with those classes.
            self.model.predict(
                reference,
                refer_image=reference,
                visual_prompts={"bboxes": boxes, "cls": kits},
                predictor=YOLOEVPSegPredictor,
                verbose=False,
            )
            self.classes = {name: int(k) for k, name in self.model.names.items()}
        else:
            self.model = YOLO(path)

    def predict(self, image: np.ndarray) -> list[ev.Detection]:
        """Detect bottles in a BGR frame"""
        result = self.model.predict(
            image,
            imgsz=self.imgsz or native_size(image),
            conf=self.conf,
            iou=0.6,
            agnostic_nms=True,
            max_det=300,
            verbose=False,
        )[0]
        out = []
        names = result.names
        for box, score, cls in zip(
            result.boxes.xyxy.tolist(),
            result.boxes.conf.tolist(),
            result.boxes.cls.tolist(),
            strict=True,
        ):
            if self.classes is None:
                kit = int(cls)
            else:
                kit = self.classes.get(names[int(cls)])
                if kit is None:
                    continue
            if box[2] > box[0] and box[3] > box[1]:
                out.append(ev.Detection(tuple(box), float(score), kit))
        return out


class GroundingDinoPredictor:
    """Grounding DINO from Hugging Face transformers, prompted with bottle names

    Args:
        model_id: Hugging Face model id; tiny is the one cached locally.
        prompts: Prompt to kit map, as for :class:`UltralyticsPredictor`.
        threshold: Lowest box score kept.
    """

    def __init__(
        self,
        model_id: str = "IDEA-Research/grounding-dino-tiny",
        prompts: dict[str, int | None] | None = None,
        threshold: float = 0.1,
    ) -> None:
        """Load the processor and the model on the CPU"""
        import torch
        from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

        self.torch = torch
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id)
        self.model.eval()
        self.prompts = prompts or BOTTLE_PROMPTS
        self.labels = [p for p, k in self.prompts.items() if k is not None]
        self.threshold = threshold

    def predict(self, image: np.ndarray) -> list[ev.Detection]:
        """Detect bottles in a BGR frame"""
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        inputs = self.processor(images=rgb, text=[self.labels], return_tensors="pt")
        with self.torch.no_grad():
            outputs = self.model(**inputs)
        result = self.processor.post_process_grounded_object_detection(
            outputs,
            inputs.input_ids,
            threshold=self.threshold,
            text_threshold=self.threshold,
            target_sizes=[rgb.shape[:2]],
        )[0]
        labels = result.get("text_labels", result.get("labels"))
        out = []
        for box, score, label in zip(
            result["boxes"].tolist(), result["scores"].tolist(), labels, strict=True
        ):
            kit = self.prompts.get(label, -1) if isinstance(label, str) else -1
            out.append(
                ev.Detection(tuple(box), float(score), -1 if kit is None else kit)
            )
        return out


class RfDetrPredictor:
    """A fine-tuned RF-DETR checkpoint

    Args:
        weights: The ``checkpoint_best_*.pth`` written by training.
        size: ``nano``, ``small``, ``medium`` or ``base``.
        conf: Lowest score kept.
        resolution: Input side the model was trained at.
    """

    def __init__(
        self,
        weights: str,
        size: str = "nano",
        conf: float = 0.02,
        resolution: int = 384,
    ) -> None:
        """Load the checkpoint"""
        import rfdetr

        cls = {
            "nano": "RFDETRNano",
            "small": "RFDETRSmall",
            "medium": "RFDETRMedium",
            "base": "RFDETRBase",
        }[size]
        self.model = getattr(rfdetr, cls)(
            pretrain_weights=weights, resolution=resolution
        )
        self.conf = conf

    def predict(self, image: np.ndarray) -> list[ev.Detection]:
        """Detect bottles in a BGR frame"""
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        found = self.model.predict(rgb, threshold=self.conf)
        out = []
        for box, score, cls in zip(
            found.xyxy.tolist(), found.confidence.tolist(), found.class_id.tolist(),
            strict=True,
        ):  # fmt: skip
            out.append(ev.Detection(tuple(box), float(score), int(cls) % 2))
        return out


def worktop_roi(
    frame: dict, worktop: ev.Worktop, margin_px: int = 24
) -> tuple[int, int, int, int]:
    """Return the image rectangle the worktop and anything on it can occupy

    Projects the corners of the worktop outline, at the worktop height and at
    the tallest bottle's height above it, and pads the box they span. Uses the
    camera's calibrated pose only.
    """
    cx, cy = worktop.centre
    hx, hy = worktop.half
    points = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for dz in (0.0, worktop.height_range[1]):
                p = ev.project(frame, (cx + sx * hx, cy + sy * hy, worktop.z + dz))
                if p is not None:
                    points.append(p)
    width, height = frame["width"], frame["height"]
    if not points:
        return 0, 0, width, height
    us, vs = zip(*points, strict=True)
    return (
        max(0, int(min(us)) - margin_px),
        max(0, int(min(vs)) - margin_px),
        min(width, int(max(us)) + margin_px),
        min(height, int(max(vs)) + margin_px),
    )


def nms(detections: list[ev.Detection], iou_max: float = 0.5) -> list[ev.Detection]:
    """Keep the highest-scoring box of every group overlapping above ``iou_max``"""
    if not detections:
        return []
    import torch
    from torchvision.ops import nms as torch_nms

    boxes = torch.tensor([d.box for d in detections], dtype=torch.float32)
    scores = torch.tensor([d.score for d in detections], dtype=torch.float32)
    keep = torch_nms(boxes, scores, iou_max).tolist()
    return [detections[i] for i in keep]


@dataclass
class TiledPredictor:
    """Run a predictor over overlapping tiles of a region and merge the boxes

    Attributes:
        inner: The predictor run on every tile.
        tile: Tile side in frame pixels.
        overlap: Fraction of a tile shared with its neighbour.
        upscale: Factor each tile is resized by before ``inner`` sees it.
        roi: Function from a frame record to the region to tile, or None for
            the whole frame.
        edge_px: A box within this many pixels of a tile side that is inside
            the region is dropped; the neighbouring tile holds it whole.
    """

    inner: object
    tile: int = 640
    overlap: float = 0.25
    upscale: float = 1.0
    roi: Callable[[dict], tuple[int, int, int, int]] | None = None
    edge_px: int = 3
    frame: dict | None = None

    def region(self, width: int, height: int) -> tuple[int, int, int, int]:
        """Return the rectangle to tile: the ROI of the current frame, or all of it"""
        if self.roi is not None and self.frame is not None:
            return self.roi(self.frame)
        return 0, 0, width, height

    def tiles(self, width: int, height: int) -> list[tuple[int, int, int, int]]:
        """Return the tile rectangles covering the region"""
        u0, v0, u1, v1 = self.region(width, height)
        step = max(1, int(self.tile * (1 - self.overlap)))

        def starts(lo: int, hi: int, size: int) -> list[int]:
            if hi - lo <= self.tile:
                return [max(0, min(lo, size - self.tile))]
            out = list(range(lo, hi - self.tile, step))
            return [*out, hi - self.tile]

        return [
            (u, v, min(u + self.tile, width), min(v + self.tile, height))
            for v in starts(v0, v1, height)
            for u in starts(u0, u1, width)
        ]

    def predict(self, image: np.ndarray) -> list[ev.Detection]:
        """Detect over every tile, shift the boxes back and merge them"""
        height, width = image.shape[:2]
        rects = self.tiles(width, height)
        # A box touching a tile side that another tile overlaps is dropped: the
        # overlap is wider than any bottle, so the neighbour holds it whole.
        low_u = min(r[0] for r in rects)
        low_v = min(r[1] for r in rects)
        high_u = max(r[2] for r in rects)
        high_v = max(r[3] for r in rects)
        found: list[ev.Detection] = []
        for u0, v0, u1, v1 in rects:
            crop = image[v0:v1, u0:u1]
            if self.upscale != 1.0:
                crop = cv2.resize(
                    crop, None, fx=self.upscale, fy=self.upscale,
                    interpolation=cv2.INTER_LINEAR,
                )  # fmt: skip
            for d in self.inner.predict(crop):
                b = [c / self.upscale for c in d.box]
                cut = (
                    (b[0] < self.edge_px and u0 > low_u)
                    or (b[1] < self.edge_px and v0 > low_v)
                    or (b[2] > (u1 - u0) - self.edge_px and u1 < high_u)
                    or (b[3] > (v1 - v0) - self.edge_px and v1 < high_v)
                )
                if cut:
                    continue
                box = (b[0] + u0, b[1] + v0, b[2] + u0, b[3] + v0)
                found.append(ev.Detection(box, d.score, d.cls))
        return nms(found)


@dataclass
class RoiPredictor:
    """Run a predictor on the worktop's image region only, optionally enlarged

    The fixed camera never moves, so the worktop covers the same band of the
    frame every time. Cropping to it skips floor and ceiling, and enlarging it
    before the network gives small bottles more pixels at the model's input.

    Attributes:
        inner: The predictor run on the region; it should size its input to
            the image it is given.
        roi: Function from a frame record to the region, as for tiling.
        upscale: Factor the region is resized by before ``inner`` sees it.
    """

    inner: object
    roi: Callable[[dict], tuple[int, int, int, int]] | None = None
    upscale: float = 1.0
    frame: dict | None = None

    def predict(self, image: np.ndarray) -> list[ev.Detection]:
        """Detect in the region and map the boxes back to the frame"""
        height, width = image.shape[:2]
        if self.roi is not None and self.frame is not None:
            u0, v0, u1, v1 = self.roi(self.frame)
        else:
            u0, v0, u1, v1 = 0, 0, width, height
        crop = image[v0:v1, u0:u1]
        if self.upscale != 1.0:
            crop = cv2.resize(
                crop, None, fx=self.upscale, fy=self.upscale,
                interpolation=cv2.INTER_LINEAR,
            )  # fmt: skip
        out = []
        for d in self.inner.predict(crop):
            b = [c / self.upscale for c in d.box]
            out.append(ev.Detection((b[0] + u0, b[1] + v0, b[2] + u0, b[3] + v0),
                                    d.score, d.cls))  # fmt: skip
        return out
