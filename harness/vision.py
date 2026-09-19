"""Locate sample labels the way the robot would: camera, detector, ring, depth

For every fixed camera in a scene the frame is rendered with its depth buffer.
Martí's YOLO26n trained on the rail scene's general-camera renders
(``labvision.detector`` backend ``rail``) proposes bottle boxes. Every box counts, the shelves'
included, since the lookup table wants every sample: no worktop filter
(``labvision.evaluation.on_worktop``) is applied. Every candidate ArUco
quad in the frame, the ones OpenCV rejected included, is soft-decoded by
``labvision.markers`` into a likelihood over the catalogue's ids, and handed to
the smallest box around it. The depth under the quads puts the box in the world:

    pixel (u, v) + depth d  ->  X = C + d / (r . f) * r

where C is the camera centre, r the unit ray through the pixel and f the
optical axis: MuJoCo's depth buffer is distance along the axis, not along the ray.

Boxes from every camera whose points fall within MERGE_M of each other are one
bottle. All of its quads, from all views, are fused by ``markers.fuse`` into
one posterior, and ``markers.decide`` turns that into accept, rescan or reject.
That posterior is the probability the lookup table reports for the reading.

The point under a quad lies on the bottle's surface. The ground truth
(``build_lookup_table.scan_scene``) is the centre of a label that wraps the
whole bottle, which sits on its axis, so once the bottle is identified the
surface point is pushed back along the horizontal view direction by its radius
(from the bottle kit's manifest).
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import mujoco
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "computer-vision"))
from labvision import markers  # noqa: E402
from labvision.camera import Camera, Intrinsics  # noqa: E402
from labvision.detector import Box, Detector, attach_barcodes, draw  # noqa: E402

DEFAULT_SIZE = (1920, 1080)   # for cameras whose MJCF gives no resolution
INNER = 0.5                   # fraction of a box whose depth is trusted
MERGE_M = 0.03                # boxes from any camera closer than this are one bottle
SAME_ID_M = 0.10              # two bottles read as one id this close are one bottle seen twice
MATCH_M = 0.05                # a point this close to a ground-truth label is that label


@dataclass
class Sighting:
    """One YOLO box in one camera, with the ring quads that fell inside it"""

    camera: str
    camera_position: np.ndarray
    box: Box
    point: np.ndarray                              # world point on the bottle surface
    readings: list[markers.MarkerReading] = field(default_factory=list)

    def to_json(self, by_marker: dict[int, dict]) -> dict:
        record = {"camera": self.camera, **self.box.to_json(),
                  "surface_point": _round(self.point)}
        if self.readings:
            record["quads"] = [{
                "sample_id": by_marker.get(r.marker_id, {}).get("sample_id"),
                "marker_id": r.marker_id,
                "probability": _p(r.probability),
                "bit_errors": r.bit_errors,
                "accepted_by_opencv": r.accepted,
                "centre_px": _round(r.corners.mean(axis=0), 1),
            } for r in self.readings]
        return record


@dataclass
class Bottle:
    """A cluster of sightings of one physical bottle and what its ring says"""

    sightings: list[Sighting]
    posterior: list[tuple[int, float]] = field(default_factory=list)

    @property
    def readings(self) -> list[markers.MarkerReading]:
        return [r for s in self.sightings for r in s.readings]

    @property
    def point(self) -> np.ndarray:
        return np.median([s.point for s in self.sightings], axis=0)

    @property
    def probability(self) -> float:
        return self.posterior[0][1] if self.posterior else 0.0

    @property
    def marker_id(self) -> int | None:
        return self.posterior[0][0] if self.posterior else None

    @property
    def decision(self) -> str:
        return markers.decide(self.probability) if self.posterior else "reject"

    def fuse(self) -> None:
        self.posterior = markers.fuse(self.readings)


@dataclass
class SceneScan:
    """Everything the cameras made of one scene"""

    bottles: list[Bottle]
    per_camera: dict[str, dict]


def _round(values, nd=4):
    return [round(float(v), nd) for v in values]


def _p(value: float) -> float:
    """A probability rounded without collapsing 0.9999 into 1.0"""
    return float(f"{value:.6g}")


def fixed_cameras(model: mujoco.MjModel) -> list[str]:
    """Cameras that cannot move: not on a mocap body and with no joint above them"""
    names = []
    for cam in range(model.ncam):
        body = model.cam_bodyid[cam]
        moving = False
        while body > 0:
            if model.body_mocapid[body] >= 0 or model.body_jntnum[body] > 0:
                moving = True
                break
            body = model.body_parentid[body]
        if not moving:
            names.append(mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_CAMERA, cam))
    return names


def camera_size(model: mujoco.MjModel, cam: int) -> tuple[int, int]:
    width, height = (int(v) for v in model.cam_resolution[cam])
    return (width, height) if width > 1 and height > 1 else DEFAULT_SIZE


def camera_model(model, data, cam: int, width: int, height: int) -> Camera:
    intrinsics = Intrinsics.from_fov(width, height, fovy_deg=float(model.cam_fovy[cam]))
    return Camera.from_mujoco(intrinsics, cam_pos=data.cam_xpos[cam], cam_xmat=data.cam_xmat[cam])


def back_project(camera: Camera, uv, depth) -> np.ndarray:
    """World points for pixels (..., 2) at MuJoCo z-depths (...)"""
    rays = camera.pixel_ray(np.asarray(uv, float))
    along = rays @ camera.rotation[:, 2]
    return camera.position + (np.asarray(depth, float) / along)[..., None] * rays


def to_axis(camera_position: np.ndarray, surface: np.ndarray, diameter_m: float) -> np.ndarray:
    """Push a surface point back by the bottle radius, horizontally, away from the camera"""
    away = surface - camera_position
    away[2] = 0.0
    norm = np.linalg.norm(away)
    if norm < 1e-9:
        return surface.copy()
    return surface + away / norm * (diameter_m / 2)


def _inner_depth(depth: np.ndarray, box: Box) -> float:
    height, width = depth.shape
    b = box.bbox
    du, dv = (1 - INNER) / 2 * b.width, (1 - INNER) / 2 * b.height
    u0, v0 = max(0, int(b.u_min + du)), max(0, int(b.v_min + dv))
    u1, v1 = min(width, int(np.ceil(b.u_max - du))), min(height, int(np.ceil(b.v_max - dv)))
    return float(np.median(depth[v0:max(v1, v0 + 1), u0:max(u1, u0 + 1)]))


def _quad_depth(depth: np.ndarray, quad: np.ndarray) -> float:
    mask = np.zeros(depth.shape, np.uint8)
    cv2.fillPoly(mask, [np.round(quad).astype(np.int32)], 1)
    values = depth[mask.astype(bool)]
    if values.size:
        return float(np.median(values))
    u, v = quad.mean(axis=0)
    return float(depth[int(v), int(u)])


def _contains(box: Box, uv) -> bool:
    b = box.bbox
    return b.u_min <= uv[0] <= b.u_max and b.v_min <= uv[1] <= b.v_max


def cluster(sightings: list[Sighting], radius: float = MERGE_M) -> list[Bottle]:
    """Greedy: a sighting joins the first bottle whose centre is within radius"""
    bottles: list[Bottle] = []
    for sighting in sightings:
        for bottle in bottles:
            if np.linalg.norm(sighting.point - bottle.point) < radius:
                bottle.sightings.append(sighting)
                break
        else:
            bottles.append(Bottle([sighting]))
    return bottles


def merge_same_id(bottles: list[Bottle]) -> list[Bottle]:
    """Join bottles read as the same id that are close enough to be one bottle

    Two cameras on opposite sides see surface points up to a diameter apart,
    more than MERGE_M, so one bottle can come out of :func:`cluster` twice.
    Catalogue ids are unique, so the same id twice within SAME_ID_M is that.
    """
    merged: list[Bottle] = []
    for bottle in sorted(bottles, key=lambda b: -b.probability):
        if bottle.decision != "reject":
            for kept in merged:
                if (kept.marker_id == bottle.marker_id and kept.decision != "reject"
                        and np.linalg.norm(kept.point - bottle.point) < SAME_ID_M):
                    kept.sightings.extend(bottle.sightings)
                    kept.fuse()
                    break
            else:
                merged.append(bottle)
        else:
            merged.append(bottle)
    return merged


class VisionScanner:
    """Detector and ring decoder, loaded once and used across scenes"""

    def __init__(self, table: dict, *, backend="rail", weights=None, score=None,
                 device=None, read_ean=False, frames_dir: Path | None = None):
        self.detector = Detector(backend, score=score, weights=weights, device=device)
        self.marker_detector = markers.make_detector()
        self.by_marker = {int(row["marker_id"]): row for row in table.values()}
        self.candidates = np.array(sorted(self.by_marker), int)
        self.read_ean = read_ean
        self.frames_dir = frames_dir

    def scan(self, model, data, name: str, cameras: list[str]) -> SceneScan:
        sightings: list[Sighting] = []
        per_camera: dict[str, dict] = {}
        renderers: dict[tuple[int, int], mujoco.Renderer] = {}
        for cam_name in cameras:
            cam = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, cam_name)
            if cam < 0:
                raise SystemExit(f"{name}: no camera {cam_name!r}")
            width, height = camera_size(model, cam)
            model.vis.global_.offwidth = max(model.vis.global_.offwidth, width)
            model.vis.global_.offheight = max(model.vis.global_.offheight, height)
            if (width, height) not in renderers:
                renderers[(width, height)] = mujoco.Renderer(model, height=height, width=width)
            renderer = renderers[(width, height)]

            renderer.update_scene(data, camera=cam)
            renderer.disable_depth_rendering()
            bgr = cv2.cvtColor(renderer.render(), cv2.COLOR_RGB2BGR)
            renderer.enable_depth_rendering()
            depth = renderer.render().copy()
            renderer.disable_depth_rendering()

            camera = camera_model(model, data, cam, width, height)
            found, stats = self._scan_frame(cam_name, camera, bgr, depth)
            sightings += found
            per_camera[cam_name] = stats
            if self.frames_dir is not None:
                self._save(name, cam_name, bgr, found)
        for r in renderers.values():
            r.close()

        bottles = cluster(sightings)
        for bottle in bottles:
            bottle.fuse()
        return SceneScan(merge_same_id(bottles), per_camera)

    def _scan_frame(self, cam_name, camera, bgr, depth):
        boxes = self.detector.detect(bgr)
        if self.read_ean:
            attach_barcodes(bgr, boxes)
        readings = markers.read_markers(bgr, self.candidates, self.marker_detector)
        stats = {"boxes": len(boxes), "quads": len(readings),
                 "quads_accepted_by_opencv": sum(r.accepted for r in readings),
                 "quads_in_box": 0}

        # The smallest box around a quad is the bottle it is printed on. Quads
        # outside every box are the room's own squares and say nothing.
        per_box: dict[int, list[markers.MarkerReading]] = {}
        for reading in readings:
            centre = reading.corners.mean(axis=0)
            inside = [i for i, b in enumerate(boxes) if _contains(b, centre)]
            if inside:
                stats["quads_in_box"] += 1
                best = min(inside, key=lambda i: boxes[i].bbox.width * boxes[i].bbox.height)
                per_box.setdefault(best, []).append(reading)

        found = []
        for i, box in enumerate(boxes):
            quads = per_box.get(i, [])
            if quads:
                point = np.median([back_project(camera, q.corners.mean(axis=0),
                                                _quad_depth(depth, q.corners)) for q in quads], axis=0)
            else:
                point = back_project(camera, box.centre, _inner_depth(depth, box))
            found.append(Sighting(cam_name, camera.position, box, point, quads))
        return found, stats

    def _save(self, scene, cam_name, bgr, found: list[Sighting]):
        out = draw(bgr, [s.box for s in found])
        for s in found:
            if not s.readings:
                continue
            for r in s.readings:
                colour = (0, 200, 0) if r.accepted else (0, 200, 255)
                cv2.polylines(out, [np.round(r.corners).astype(np.int32)], True, colour, 1)
            posterior = markers.fuse(s.readings)
            sid = self.by_marker.get(posterior[0][0], {}).get("sample_id", "?")
            u0, v1 = int(s.box.bbox.u_min), int(s.box.bbox.v_max)
            cv2.putText(out, f"{sid} p={posterior[0][1]:.3f}", (u0, v1 + 14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 160, 0), 2)
        path = self.frames_dir / scene / f"{cam_name}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(path), out)
