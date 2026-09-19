"""Locate sample labels the way the robot would: propose from the room, confirm up close

Two passes. The first proposes, from the cameras bolted to the room; the second
confirms, from the camera the arm carries. Neither is enough on its own: a fixed
camera sees the whole bench but resolves a flask at 12 to 24 pixels, which
cannot carry a 4x4 marker, and the wrist camera reads any ring it is put in
front of but has to be told where to go.

**Propose.** For every fixed camera in a scene the frame is rendered with its depth buffer.
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

**Confirm.** A bottle the fixed cameras did not accept is looked at again from
``STANDOFF_M`` by the scene's wrist camera (:mod:`wrist`), at each of its
azimuths in turn until the ring reads. Those quads are decoded by the same
decoder and fused into the same posterior, so a bottle named from the wrist is
named on the same evidence and the same thresholds as one named from the room:
the wrist buys pixels on the marker, not a second set of rules.

Which quads in a wrist frame belong to the bottle looked at is decided by where
they stand, never by what they decode to: the depth under a quad places it, the
nearest one to the aim point anchors the ring, and everything within RING_M of
that anchor joins it. A neighbour on a packed shelf projects close by in the
image but stands further away, and keeping the copies by position rather than
by agreement means a ring read badly still fuses its own disagreement, which is
what eight copies are for. A quad also has to measure what the marker it
decodes to would measure --- see :meth:`VisionScanner._right_size`.

Where a bottle was confirmed, its position comes from the wrist's views alone:
a reading from 0.30 m and one from across the room are not worth averaging.

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

import wrist

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "computer-vision"))
from labvision import markers  # noqa: E402
from labvision.camera import Camera, Intrinsics  # noqa: E402
from labvision.detector import Box, Detector, attach_barcodes, draw  # noqa: E402
from labvision.perception import PROPOSAL_RADIUS_M, marker_side  # noqa: E402

DEFAULT_SIZE = (1920, 1080)   # for cameras whose MJCF gives no resolution
INNER = 0.5                   # fraction of a box whose depth is trusted
MERGE_M = 0.03                # boxes from any camera closer than this are one bottle
SAME_ID_M = 0.10              # two bottles read as one id this close are one bottle seen twice
MATCH_M = 0.05                # a point this close to a ground-truth label is that label
CONFIRM_M = 0.08              # a ring further than this from the aim point is a neighbour's
RING_M = 0.05                 # quads further apart than this are on different bottles
SIDE_RANGE = (0.6, 1.6)       # a quad this far off its claimed marker's size is not that marker


@dataclass
class Sighting:
    """One look at a bottle: a YOLO box with the quads inside it, or a wrist view"""

    camera: str
    camera_position: np.ndarray
    box: Box | None                                # None for a wrist view: it was aimed, not detected
    point: np.ndarray                              # world point on the bottle surface
    readings: list[markers.MarkerReading] = field(default_factory=list)
    confirmed: bool = False                        # read from the wrist camera up close

    def to_json(self, by_marker: dict[int, dict]) -> dict:
        record = {"camera": self.camera, **(self.box.to_json() if self.box else {}),
                  "surface_point": _round(self.point), "confirmed": self.confirmed}
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
    refused: bool = False          # its id was claimed by a likelier bottle
    reached: bool = False          # something could be put in front of it to look

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
    def confirmed(self) -> bool:
        return any(s.confirmed for s in self.sightings)

    @property
    def views(self) -> list[Sighting]:
        """The sightings worth placing the bottle by

        The wrist's, if it got any, and of those only the ones that read the
        ring the bottle was finally named from. A cluster on a packed shelf can
        gather two bottles --- greedy clustering chains through sightings a
        few centimetres apart --- and its wrist views then read whichever
        neighbour each azimuth happened to face. Averaging all of them puts the
        bottle between the two: it is how the one confident wrong identity in
        200 came about, 76 mm from its own label and 7 mm from its
        neighbour's.
        """
        named = [s for s in self.sightings if s.confirmed
                 and any(r.marker_id == self.marker_id for r in s.readings)]
        return named or [s for s in self.sightings if s.confirmed] or self.sightings

    @property
    def marker_id(self) -> int | None:
        return self.posterior[0][0] if self.posterior else None

    @property
    def decision(self) -> str:
        if self.refused or not self.posterior:
            return "reject"
        return markers.decide(self.probability)

    def fuse(self) -> None:
        self.posterior = markers.fuse(self.readings)


@dataclass
class SceneScan:
    """Everything the cameras made of one scene"""

    bottles: list[Bottle]
    per_camera: dict[str, dict]
    confirm: dict


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


def one_per_id(bottles: list[Bottle]) -> list[Bottle]:
    """Refuse an id already claimed by a likelier bottle

    A catalogue id names one physical sample, so it cannot stand in two
    places. Two bottles that are really one have already been joined by
    :func:`merge_same_id`; what is left reading the same id is a
    misidentification, and writing both down would have the table assert
    something it knows to be impossible. The loser keeps its position --- there
    is something there --- and loses its name.

    Returns:
        The same bottles, with the losers marked refused.
    """
    claimed: set[int] = set()
    for bottle in sorted(bottles, key=lambda b: -b.probability):
        if bottle.decision == "reject":
            continue
        if bottle.marker_id in claimed:
            bottle.refused = True
        else:
            claimed.add(bottle.marker_id)
    return bottles


class VisionScanner:
    """Detector and ring decoder, loaded once and used across scenes"""

    def __init__(self, table: dict, *, backend="rail", weights=None, score=None,
                 device=None, read_ean=False, frames_dir: Path | None = None,
                 confirm="auto"):
        self.detector = Detector(backend, score=score, weights=weights, device=device)
        self.marker_detector = markers.make_detector()
        self.by_marker = {int(row["marker_id"]): row for row in table.values()}
        self.candidates = np.array(sorted(self.by_marker), int)
        self.read_ean = read_ean
        self.frames_dir = frames_dir
        self.confirm = confirm

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
        # Merged before the wrist flies, so one bottle both halves of the room
        # saw is not looked at twice, and again after, since two proposals the
        # wrist reads as the same id are the same bottle.
        bottles = merge_same_id(bottles)
        confirmed = self._confirm(model, data, name, bottles)
        return SceneScan(one_per_id(merge_same_id(bottles)), per_camera, confirmed)

    def _confirm(self, model, data, name: str, bottles: list[Bottle]) -> dict:
        """Look again, up close, at every bottle the fixed cameras could not name

        A bottle they already accepted is left alone: the flight costs a render
        per view and buys nothing where the identity is settled. The rest are
        aimed at in turn, azimuth by azimuth, and the loop stops on the first
        view that carries the posterior over the accept threshold --- which is
        what makes this affordable, since most bottles read on the first look.

        Returns:
            What the pass did, for the scene's ``metrics``.
        """
        eye = (wrist.mover(model, data, self.confirm,
                           lambda cam: camera_size(model, cam))
               if self.confirm != "off" else None)
        if eye is None:
            return {"camera": None, "views": 0, "confirmed": 0,
                    "skipped": "not asked for" if self.confirm == "off"
                               else "this scene has no camera that can be taken "
                                    "to a bottle"}
        tried = 0
        try:
            for bottle in bottles:
                if bottle.decision == "accept":
                    bottle.reached = True
                    continue
                tried += 1
                # The bottle is not identified yet, so there is no radius to
                # push its surface point back by: the calibrated generic one
                # gets the aim within a few millimetres of the axis, which at
                # 0.30 m is well inside the frame.
                aim = to_axis(bottle.sightings[0].camera_position, bottle.point,
                              2 * PROPOSAL_RADIUS_M)
                for k, (frame, depth, _pose) in enumerate(eye.look(data, aim)):
                    bottle.reached = True
                    # From where the camera really is, which the arm decides.
                    # It lands within 1.5 mm and 15 mrad of what it was asked
                    # for, and reading the request instead would put that error
                    # into every position the frame produces.
                    sighting = self._read(
                        eye.name,
                        camera_model(model, data, eye.cam, *camera_size(model, eye.cam)),
                        frame, depth, aim)
                    if self.frames_dir is not None:
                        self._save_view(name, tried, k, frame, sighting)
                    if sighting is None:
                        continue
                    bottle.sightings.append(sighting)
                    bottle.fuse()
                    if bottle.decision == "accept":
                        break
        finally:
            eye.park(data)
            eye.close()
        return {**eye.report(), "bottles_looked_at": tried,
                "confirmed": sum(b.confirmed for b in bottles)}

    def _read(self, name, camera, frame, depth, aim) -> Sighting | None:
        """The ring in one wrist frame, if it is the ring of the bottle aimed at

        Every quad is soft-decoded by the same decoder the fixed pass uses and
        placed by the depth under it. Which bottle a quad belongs to is settled
        by where it stands, not by where it falls in the image: from the aisle
        a neighbour behind or in front projects right beside the one looked at.
        """
        seen = []
        for reading in markers.read_markers(frame, self.candidates,
                                            self.marker_detector):
            range_m = _quad_depth(depth, reading.corners)
            point = back_project(camera, reading.corners.mean(axis=0), range_m)
            offset = float(np.linalg.norm(point - aim))
            if offset < CONFIRM_M and self._right_size(camera, reading, range_m):
                seen.append((offset, point, reading))
        if not seen:
            return None
        # One bottle's ring, not every ring in shot. On a shelf the bottles
        # stand centimetres apart, so a neighbour's ring passes the CONFIRM_M
        # test too, and fusing both into one posterior lets it outvote the
        # bottle actually looked at --- 18 confident wrong identities on the
        # open scene before this. The quads are kept by where they are and not
        # by what they decode to, so that a ring read badly still fuses its own
        # copies, which is what the ring is eight copies for: they sit on one
        # circumference, at most a diameter apart.
        seen.sort(key=lambda q: q[0])
        anchor = seen[0][1]
        quads = [q for q in seen if np.linalg.norm(q[1] - anchor) < RING_M]
        return Sighting(name, camera.position, None,
                        np.median([point for _, point, _ in quads], axis=0),
                        [reading for _, _, reading in quads], confirmed=True)

    def _right_size(self, camera, reading, range_m: float) -> bool:
        """Whether a quad measures what the marker it decodes to would measure

        The decoder answers with the likeliest id in the catalogue whatever it
        is shown, and on a featureless square --- a tile, a window pane, the
        corner of an instrument --- it answers confidently and always with the
        same one. Those squares are not the size of a ring's marker: the ring
        carries eight of them round the circumference, so one is 7 mm on a
        10 ml flask and 11 mm on a 50 ml. Back-projected at the depth under
        it, a quad's longest edge is its marker's side, foreshortening only
        ever making an edge shorter, so the side is checked against the one
        the claimed bottle prints.

        Without this the wrist adds five confident bottles to the rail scene
        that are not there, all of them the same sample, standing on the
        bench, the wall and a shelf 1.6 m up.
        """
        vessel = self.by_marker.get(reading.marker_id, {}).get("vessel_class")
        if not vessel:
            return False
        try:
            expected = marker_side(vessel)
        except OSError:
            return True     # no mesh to measure against: leave it to the decoder
        corners = back_project(camera, reading.corners, range_m)
        side = float(np.max(np.linalg.norm(
            corners - np.roll(corners, -1, axis=0), axis=1)))
        return SIDE_RANGE[0] * expected <= side <= SIDE_RANGE[1] * expected

    def _save_view(self, scene, bottle, view, frame, sighting: "Sighting | None"):
        out = frame.copy()
        for r in (sighting.readings if sighting else []):
            cv2.polylines(out, [np.round(r.corners).astype(np.int32)], True,
                          (0, 200, 0) if r.accepted else (0, 200, 255), 1)
        path = self.frames_dir / scene / f"wrist_{bottle:03d}_{view}.png"
        path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(path), out)

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
