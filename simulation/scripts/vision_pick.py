#!/usr/bin/env python3
"""The cameras find the bottles and direct the arm, live: the whole loop, closed.

Two things run at once and neither waits for the other.

**Perception**, on its own thread, never stops looking. Every cycle it copies
the simulation state, renders the fixed ``general`` camera, runs the fine-tuned
YOLO detector on the frame and lets ``labvision.perception.propose`` put every
box on the bench plane (a pixel is a ray, the bench is z = 0.90, where they meet
is where the bottle stands --- to about a centimetre). Those positions are
matched against the bottles it already knows, so the world model follows the
bench: a bottle that appears is a new track, one that goes missing is lost.

**Control**, in the physics loop, takes its directions from that world model.
It starts with the **initial scan**: the carriage parks at the end of the rail,
where the arm hides no bottle from the fixed camera, the fixed camera surveys
the whole bench, and the arm then sweeps the rail once from that end to the
other, reading every proposal's ring on the way. The wrist camera keeps every
ring in its frame, not only the one it went for: a neighbour's ring names a
track before the arm gets there, and a ring where the fixed camera boxed
nothing is a bottle it cannot see. What it read is written to
``out/bench_map.json``, one entry per sample with where it stands, before the
arm touches anything. After that:

1. A track nobody has looked at yet: the arm flies its eye-in-hand camera to
   0.36 m from it, 25 degrees above level, and ``confirm`` reads the ArUco ring.
   The ring names the sample and places the bottle's axis to a fraction of a
   millimetre. No ring from any bearing means it is not a sample, and the arm
   leaves it alone.
2. A named track: the ring's row says which vessel it is, the vessel's mesh
   says how tall, and the arm closes on it at the refined position on the
   gripper's own force feedback, lifts it, and puts it back.
3. If the track it is heading for is lost on the way --- somebody moved the
   bottle --- it backs off. The bottle turns up as a new track where it now
   stands, the ring names it again, and the world model records the move.

Move a bottle yourself to see it: press ``M`` in the MuJoCo window (or the
button on the page) to put a random one somewhere else, or double-click one and
Ctrl + right-drag it.

Nothing the arm decides reads the simulator's state. The truth is read in one
place, :func:`truth`, to score what the cameras said, and by the ``M`` key,
which plays the person moving a bottle.

Run from simulation/, with computer-vision's requirements installed as well
(ultralytics, opencv). Under mjpython on macOS:

    python scripts/vision_pick.py                     # viewer + page, picks everything
    python scripts/vision_pick.py --manual            # only looks; pick from the page
    python scripts/vision_pick.py --headless --video out/vision_pick.mp4 --perturb-at 40
    python scripts/vision_pick.py --headless --manual # the initial scan only, then stop

The page at http://localhost:8009 shows the fixed camera with the detector's
boxes, the wrist camera, the tracked bottles and the log of what happened. The
detector runs on CUDA or Apple's MPS when there is one; rendering wants a real
GPU too --- the scene draws a million triangles, which integrated graphics
manage at about two frames a second.
"""
import argparse
import http.server
import itertools
import json
import math
import sys
import threading
import time
import webbrowser
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import mujoco
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(REPO / 'computer-vision'))
import grasp_test as gt
import rail_kinematics as rk
from generate_rail_scene import BENCH_X, BENCH_Y
from labvision import registry
from labvision.camera import Camera, Intrinsics
from labvision.identify import (
    DEFAULT_TABLE,
    MarkerReader,
    identify_frame,
    rows_by_marker,
)
from labvision.perception import (
    KIT,
    Confirmation,
    Proposal,
    confirm,
    propose,
    refine,
    refine_marker,
    ring_geometry,
    vessel_height,
)
from labvision.scene import BBox

# The fixed camera's detectors, best first, each with its threshold; the first
# whose weights are on disk is used. ``rail`` was trained on this scene's own
# general-camera renders and runs at labvision's operating point: on this bench
# it finds the same bottles as ``fixedcam`` with no false box against ten. ``fixedcam`` runs lower than the 0.07 its benchmark settled on: there a
# false box was an error, here it costs the arm a look that reads no ring, while
# a missed bottle is never picked, and 0.03 finds 12 where 0.07 finds 9.
DETECTORS = (
    (REPO / 'computer-vision/runs/rail/yolo26n_rail_general.pt', 0.10),
    (REPO / 'computer-vision/weights/yolo26n_rail_general.pt', 0.10),
    (REPO / 'computer-vision/runs/fixedcam/yolo26n_fixedcam.pt', 0.03),
)
FPS = 30
# The worktop, taken from the generator so it cannot drift from the scene. It
# is not centred on the origin: x runs -4.5 to 1.5 and y -1.4 to 0.6. This was
# once written as +-3 by +-1, which silently threw away every detection on the
# left metre and a half and the aisle edge --- three real bottles on this bench.
WORKTOP = (BENCH_X, BENCH_Y)
# Where the wrist camera stands to read a ring. propose_confirm.py flies a bare
# camera at 0.30 m and 15 degrees; this one has a gripper on it, which reaches
# 0.2 m past the lens and at that pose stands 37 mm inside the worktop. Of the
# poses tried, 0.36 m and 25 degrees is the lowest that clears the bench for
# every bottle, and the ring still reads there (10 of 10, within 0.5 mm).
# Where the wrist camera stands to read a ring: (standoff, elevation) pairs, tried
# in turn. The gripper reaches 0.2 m past the lens, so with the camera aimed down
# at the elevation the hand's lowest point sits (standoff - 0.2) * sin(elevation)
# over what it looks at. The old single look, 0.36 m at 25 degrees, put that two
# centimetres *inside* a 14 cm flask: to read a ring the arm had to come into the
# bench, which is what let it knock bottles over. These are ordered by how far they
# keep the hand clear, and the ring decides which is used, so a bottle whose ring
# reads from the first never has the hand near it. The proven low look is kept last
# so that nothing which used to be named stops being named.
# Standing further out beats tilting further over: with 0.36 m at 55 degrees as the
# only look, the ring foreshortens and 8 of 19 would not read (seed 0, measured).
LOOKS = ((0.45, 40.0), (0.36, 55.0), (0.36, 25.0))
STANDOFF, ELEVATION = LOOKS[-1]     # the low look; the back-row test uses STANDOFF
LOOK_ABOVE_BENCH = 0.05     # the camera aims this far above the proposal's base
CLEARANCE = 0.25            # the look pose is entered and left from this far above
# During the initial scan the arm does not climb back to the carry pose between
# looks. It hops from one view to the next with its lowest point never nearer
# than HOVER_MARGIN to the top of the tallest flask on the bench (the floor),
# and it waits HUB_ABOVE over that floor: about 20 cm lower than the carry pose
# over a bench of 100 ml flasks, and lower still over smaller ones.
HOVER_MARGIN = 0.03
HUB_ABOVE = (0.03, 0.08)    # how far over the floor the low poses stand, tried in turn
SLIDE_STEP = 0.10           # waypoint spacing when the hand slides without turning
LIFTS = (0.12, 0.25)        # how high a slide may climb to clear what is in its way
MAX_LOOKS = 2               # bearings tried before a proposal is called empty
# Bearings the camera can stand at, from the bottle. The rail side first while
# the camera still clears the gantry beam at y = 0.30, the aisle side otherwise.
RAIL_SIDE = (90, 60, 120, 30, 150)
AISLE_SIDE = (-90, -60, -120, -30, -150)

# The world model. A proposal lands within 3 cm of its bottle nine times in ten,
# and the bench's vessels stand 28 cm apart or more, so 4 cm tells a bottle seen
# again from a different bottle.
ASSOCIATE = 0.04
LOST_AFTER = 3              # cycles a track may go unseen before it is lost
# A box has to come back this many cycles running before it is a track. The
# detector flickers at 0.03, and a flicker is not worth a trip along the rail.
CONFIRM_HITS = 3
# The arm is in the fixed camera's picture, and a gripper over a white bench
# looks enough like a flask to be boxed: the first live run made forty tracks
# out of it in twenty seconds. The arm knows where it is, so it can be taken out
# of the picture: a box within this of the arm's own projected links is the arm,
# and a track behind them is hidden rather than missing.
ARM_MASK_PX = 45
# The detector also boxes the funnel, the pot and the wash bottles, and each one
# costs the arm two looks before it reads no ring. Where a box stands on the
# bench says how big a flask would look there, so size tells them apart: the
# tallest sample is the 100 ml flask at 115 mm, and measured in the scene every
# real bottle's box is under 1.36 of that high and, over the ten seeded benches,
# 0.72 of it wide. The wash station measured 1.6 to 2.7 wide against the upright
# reference, which the width's own reference reads about three quarters of, so
# the limit still tells them apart. Each side is measured against 115 mm laid
# the way that side runs; measuring the width against the upright one is what
# the seeded benches broke, see flask_across.
FLASK_HEIGHT = 0.115
MAX_BOX = (1.5, 0.8)        # a box's height and width, in flask heights at its place
SURE = 0.5                  # tracks scoring this or better are looked at first
MATCH = 0.06                # scoring only: a bottle this near a track is it
# The initial scan waits this many perception cycles with the arm parked before
# it plans the sweep: enough for every box to be seen CONFIRM_HITS times running.
SURVEY_CYCLES = CONFIRM_HITS + 2
BENCH_MAP = rk.SIM / 'out/bench_map.json'
# The wrist camera reads every ring in its frame, not only the one it went for,
# and a neighbour's ring names a bottle nobody has visited yet. That is how the
# scan finds the flasks the fixed camera never boxes: from one look on this
# bench the wrist read five rings, two of them bottles with no box, each placed
# within 4 mm. A ring this near a track is that track's bottle: proposals land
# within 3 cm of their bottle nine times in ten, the worst seen was 6.3 cm, and
# no two vessels on the bench stand closer than 10 cm.
RING_ASSOCIATE = 0.08
# Rings are only placed from this close to the lens. Farther off they are a few
# pixels across, and a bottle on a shelf past the bench, placed as if it stood
# on the worktop, lands somewhere wrong.
RING_RANGE = 1.2
SAME_BOTTLE = 0.03          # two rings placed this close are on one bottle
CATALOGUE_FIELDS = ('material', 'cas', 'phase', 'container_ml', 'lot', 'vessel_class')


class Retarget(Exception):
    """The track being worked on was lost on the way; back off and think again."""


@dataclass
class Track:
    """One bottle the cameras believe in, and everything learnt about it.

    Attributes:
        id: Stable number for the page and the log.
        seen_xy: Where the fixed camera last put it; for a bottle only the
            wrist camera has seen, where its ring put it.
        score: The detector's latest confidence.
        bbox: The detector's latest box, for drawing; None if it never had one.
        state: ``tentative`` until seen :data:`CONFIRM_HITS` times running, then
            ``proposed``, ``named``, ``empty``, ``unreachable``, ``picked``,
            ``missed`` or ``lost``.
        confirmation: What the wrist camera read, once it has looked.
        hits: Cycles it has been seen in.
        misses: Cycles since the fixed camera last saw it.
        held: The gripper has it; the fixed camera is not expected to.
        wrist_only: Only the wrist camera has seen it, beside another bottle
            it went to look at. The fixed camera not seeing it says nothing.
        note: One line for the table.
        truth: Scoring only --- the true body nearest it and the error in mm.
    """

    id: int
    seen_xy: tuple[float, float]
    score: float
    bbox: BBox | None
    state: str = 'tentative'
    confirmation: Confirmation | None = None
    hits: int = 1
    misses: int = 0
    held: bool = False
    wrist_only: bool = False
    picks: int = 0
    note: str = 'seen by the fixed camera'
    truth: dict[str, object] = field(default_factory=dict)

    @property
    def xy(self) -> tuple[float, float]:
        """Best position known: the ring's if it was read, else the box's."""
        if self.confirmation and self.confirmation.refined_xy:
            return self.confirmation.refined_xy
        return self.seen_xy

    @property
    def sample(self) -> str | None:
        """The sample the ring named, if it has been read."""
        return self.confirmation.sample_id if self.confirmation else None


class World:
    """What the lab believes stands on the bench. Shared between the threads."""

    def __init__(self, auto: bool) -> None:
        self.lock = threading.Lock()
        self.tracks: dict[int, Track] = {}
        self.events: list[str] = []
        self.commands: list[dict] = []
        self.auto = auto
        self.cycles = 0
        self.cycle_seconds = 0.0
        self.caption = 'starting'
        self.scan: dict | None = None       # the initial scan's record, once it is done
        self.scene = GRIPPER_SCENE.relative_to(REPO).as_posix()    # for the bench map
        self._next = 1

    def log(self, clock: float, text: str) -> None:
        """Say what happened, on the terminal and on the page."""
        line = f'[{clock:6.1f} s] {text}'
        print(line, flush=True)
        self.events.append(line)
        del self.events[:-40]

    def update(self, proposals: list[Proposal], clock: float, hidden) -> None:
        """Fold one cycle of the fixed camera's proposals into the tracks.

        Args:
            proposals: This cycle's boxes on the bench, the arm's own removed.
            clock: Simulated time, for the log.
            hidden: Whether a bench position is behind the arm in this frame, so
                that not seeing a track there says nothing.
        """
        with self.lock:
            free = {t.id for t in self.tracks.values() if t.state != 'lost'}
            for proposal in proposals:
                # Box against box: a named track's ring position can stand a few
                # cm off where the fixed camera puts it, and is not what it sees.
                near = [(math.dist(proposal.xy, self.tracks[i].seen_xy), i) for i in free]
                near = [pair for pair in near if pair[0] < ASSOCIATE]
                if near:
                    track = self.tracks[min(near)[1]]
                    free.discard(track.id)
                    track.seen_xy, track.score = proposal.xy, proposal.score
                    track.bbox, track.misses = proposal.bbox, 0
                    track.hits, track.wrist_only = track.hits + 1, False
                    if track.state == 'tentative' and track.hits >= CONFIRM_HITS:
                        track.state = 'proposed'
                        self.log(clock, f'track {track.id}: new at ({track.xy[0]:+.2f}, '
                                        f'{track.xy[1]:+.2f}), score {track.score:.2f}')
                else:
                    track = Track(self._next, proposal.xy, proposal.score, proposal.bbox)
                    self.tracks[track.id] = track
                    self._next += 1
            for i in free:
                track = self.tracks[i]
                if track.held or track.wrist_only or hidden(track.xy):
                    continue
                track.misses += 1
                if track.state == 'tentative':
                    del self.tracks[i]          # a flicker; it never was a track
                elif track.misses >= LOST_AFTER:
                    track.state, track.note = 'lost', 'no longer where it was'
                    self.log(clock, f'track {track.id}'
                                    f'{" (" + track.sample + ")" if track.sample else ""}: '
                                    'lost, nothing stands there any more')
            self.cycles += 1

    def named(self, track: Track, clock: float) -> None:
        """A ring was read: if that sample was known elsewhere, it has moved."""
        with self.lock:
            for other in list(self.tracks.values()):
                if other.id != track.id and other.sample == track.sample:
                    moved = math.dist(other.xy, track.xy)
                    self.log(clock, f'{track.sample} moved {moved * 100:.0f} cm: was track '
                                    f'{other.id}, now track {track.id}')
                    del self.tracks[other.id]

    def sighted(self, rings: list[Confirmation], clock: float, beside: Track) -> None:
        """Fold in the rings a look read around the bottle it went for.

        A ring whose sample is known already adds nothing. One that lands near
        a track nobody has named names it, and saves that track a look of its
        own. One that lands near nothing is a bottle the fixed camera never
        boxed: it becomes a track only the wrist camera has seen.

        Args:
            rings: Every ring the look read on the worktop, placed by its own geometry.
            clock: Simulated time, for the log.
            beside: The track the look was for.
        """
        with self.lock:
            for ring in rings:
                if any(t.sample == ring.sample_id and t.state != 'lost'
                       for t in self.tracks.values()):
                    continue
                if any(t.sample and t.state != 'lost'
                       and math.dist(ring.refined_xy, t.xy) < SAME_BOTTLE
                       for t in self.tracks.values()):
                    continue        # that bottle has a name already: a misread
                near = [(math.dist(ring.refined_xy, t.seen_xy), t) for t in self.tracks.values()
                        if t.state in ('tentative', 'proposed', 'empty', 'unreachable')]
                near = [pair for pair in near if pair[0] < RING_ASSOCIATE]
                x, y = ring.refined_xy
                if near:
                    off, track = min(near, key=lambda pair: pair[0])
                    track.confirmation, track.state = ring, 'named'
                    source = ('its own look' if track is beside
                              else f'the look at track {beside.id}')
                    track.note = f'ring read from {source}, {off * 100:.1f} cm off its box'
                    self.log(clock, f'track {track.id} is {ring.sample_id}: its ring, read '
                                    f'from {source}, places it at ({x:+.4f}, {y:+.4f}), '
                                    f'{off * 100:.1f} cm off its box')
                else:
                    track = Track(self._next, ring.refined_xy, 0.0, None, state='named',
                                  confirmation=ring, wrist_only=True,
                                  note=f'no box; ring read beside track {beside.id}')
                    self.tracks[track.id] = track
                    self._next += 1
                    self.log(clock, f'{ring.sample_id}: a bottle the fixed camera never boxed, '
                                    f'its ring read beside track {beside.id}; track '
                                    f'{track.id} at ({x:+.4f}, {y:+.4f})')

    def snapshot(self) -> list[Track]:
        """The tracks as they stand, safe to iterate."""
        with self.lock:
            return list(self.tracks.values())


class Detector:
    """The fixed camera's detector: Ultralytics weights, boxes out."""

    def __init__(self, weights: Path, threshold: float, device: str | None) -> None:
        import torch
        from ultralytics import YOLO
        if not weights.exists():
            raise SystemExit(
                f'no detector weights at {weights}: they are not in git. Copy '
                'yolo26n_rail_general.pt there (or train it with computer-vision/'
                'runs/rail/train_yolo26n_gpu.py), or pass --weights')
        if device is None:
            device = ('cuda:0' if torch.cuda.is_available() else
                      'mps' if torch.backends.mps.is_available() else 'cpu')
        self.model, self.threshold, self.device = YOLO(str(weights)), threshold, device

    def detect(self, frame: np.ndarray) -> list[tuple[BBox, float, str]]:
        """Boxes above the threshold as ``(bbox, score, label)``, at native size."""
        size = int(math.ceil(max(frame.shape[:2]) / 32) * 32)
        result = self.model.predict(frame, imgsz=size, conf=self.threshold, iou=0.6,
                                    agnostic_nms=True, max_det=300, verbose=False,
                                    device=self.device)[0]
        return [(BBox(*(float(v) for v in hit.xyxy[0])), float(hit.conf),
                 result.names[int(hit.cls)]) for hit in result.boxes]


class Eyes:
    """Renders the scene's cameras and hands back frames with their calibration."""

    def __init__(self, model: mujoco.MjModel, data: mujoco.MjData) -> None:
        self.model, self.data = model, data
        self.renderers: dict[tuple[int, int], mujoco.Renderer] = {}

    def frame(self, name: str, size: tuple[int, int] | None = None) -> np.ndarray:
        """A BGR frame from a named camera, at its own resolution unless told."""
        cam = self.model.camera(name).id
        width, height = size or (int(v) for v in self.model.cam_resolution[cam])
        if (width, height) not in self.renderers:
            self.renderers[width, height] = mujoco.Renderer(
                self.model, height=height, width=width)
        renderer = self.renderers[width, height]
        renderer.update_scene(self.data, camera=name)
        return renderer.render()[:, :, ::-1].copy()

    def camera(self, name: str) -> Camera:
        """The pinhole model of a named camera where it is right now.

        On hardware this is the fixed camera's calibration, and for the wrist
        the arm's forward kinematics; neither is a peek at the scene.
        """
        return camera_at(self.model, self.data, name)

    def close(self) -> None:
        """Free the OpenGL contexts."""
        for renderer in self.renderers.values():
            renderer.close()


def lighten(model: mujoco.MjModel, data: mujoco.MjData) -> int:
    """Stop drawing the meshes that stand off the bench, for a slow GPU.

    The room draws a million triangles and the GC-MS by the door is a third of
    them. Nothing off the worktop is ever a proposal, so hiding those meshes
    changes no decision; it moves them to a geom group neither the viewer nor
    the offscreen renderer shows. They still collide.

    Returns:
        How many triangles are no longer drawn.
    """
    hidden = 0
    for geom in range(model.ngeom):
        x, y, _ = data.geom_xpos[geom]
        on_bench = (WORKTOP[0][0] - 0.3 <= x <= WORKTOP[0][1] + 0.3
                    and WORKTOP[1][0] - 0.3 <= y <= WORKTOP[1][1] + 0.3)
        body = model.body(model.geom_bodyid[geom]).name
        if model.geom_type[geom] != mujoco.mjtGeom.mjGEOM_MESH or on_bench \
                or body.startswith(('arm_', 'rail')):
            continue
        model.geom_group[geom] = 4
        hidden += int(model.mesh_facenum[model.geom_dataid[geom]])
    return hidden


def rings_in_view(frame: np.ndarray, camera: Camera, rows: dict[int, dict],
                  reader: MarkerReader) -> list[Confirmation]:
    """Every catalogue ring in a wrist frame, each placed on the bench by itself.

    ``confirm`` keeps only the ring at the target. This keeps them all, placed
    the same way: the ring's most frontal marker and the vessel's ring geometry
    give the bottle's axis. Rings off the worktop or beyond :data:`RING_RANGE`
    are dropped.

    Returns:
        One confirmation per ring, with ``refined_xy`` set.
    """
    out = []
    for identity in identify_frame(frame, rows, reader=reader):
        row = identity.row
        vessel = row.get('vessel_class') if row else None
        if not vessel or not (KIT / 'meshes' / f'{vessel}_label.obj').exists():
            continue
        radius, ring_height = ring_geometry(vessel)
        facing = identity.frontal
        xy = (refine_marker(camera, facing.corners, radius, ring_height,
                            bench_z=rk.BENCH_TOP) if facing else None)
        if xy is None:
            uv = facing.centre if facing else identity.bbox.centre
            xy = refine(camera, uv, radius, ring_height, bench_z=rk.BENCH_TOP)
        if xy is None or math.dist(xy, camera.position[:2]) > RING_RANGE:
            continue
        if not (WORKTOP[0][0] <= xy[0] <= WORKTOP[0][1]
                and WORKTOP[1][0] <= xy[1] <= WORKTOP[1][1]):
            continue
        out.append(Confirmation(sample_id=identity.sample_id, marker_id=identity.marker_id,
                                votes=identity.votes, phase=row.get('phase'),
                                refined_xy=xy))
    # Two identities placed on one spot are one bottle with a marker misread:
    # measured, a single bit error on SMP-0044's ring read as SMP-0018, 5 mm
    # away. The ring with more markers read wins; a tie names neither.
    return [ring for ring in out if all(
        ring.votes > other.votes for other in out
        if other.sample_id != ring.sample_id
        and math.dist(other.refined_xy, ring.refined_xy) < SAME_BOTTLE)]


def camera_at(model: mujoco.MjModel, data: mujoco.MjData, name: str) -> Camera:
    """The pinhole model of a named camera where it stands in ``data``.

    The optics are the ones the scene gives the camera, its resolution and
    vertical field of view, not an assumed lens.
    """
    cam = model.camera(name).id
    width, height = (int(v) for v in model.cam_resolution[cam])
    return Camera.from_mujoco(
        Intrinsics.from_fov(width, height, fovy_deg=float(model.cam_fovy[cam])),
        data.cam_xpos[cam], data.cam_xmat[cam])


def flask_pixels(xy: tuple[float, float], camera: Camera) -> float:
    """How many pixels tall the tallest sample flask looks standing at a place."""
    foot = np.array([*xy, rk.BENCH_TOP])
    ends = camera.project(np.array([foot, foot + (0.0, 0.0, FLASK_HEIGHT)]))
    return float(np.linalg.norm(ends[1] - ends[0]))


def flask_across(xy: tuple[float, float], camera: Camera) -> float:
    """How many pixels wide a flask's own height looks, laid across the sight line.

    The width test needs a reference stretched the way a box's width is. The
    scene camera is 92 degrees wide (60.44 vertical at 16:9), and off its axis
    it pulls a box sideways far more than it stretches an upright segment: over
    the ten seeded benches the same 100 ml flask measures 0.58 of
    :func:`flask_pixels` in the middle of the frame and 0.90 at its left edge,
    so ``MAX_BOX`` threw away every 100 ml flask standing at that end --- 19 of
    the 71 boxes on seed 15, and the detector had found all 71. A segment of
    the same length lying on the bench square to the sight line is pulled
    alike, and against it the widest flask of the ten measures 0.72.

    Args:
        xy: Where the flask stands on the bench.
        camera: The fixed camera, calibrated.

    Returns:
        The segment's length in pixels.
    """
    foot = np.array([*xy, rk.BENCH_TOP])
    across = np.cross((0.0, 0.0, 1.0), foot - camera.position)
    across *= FLASK_HEIGHT / 2 / np.linalg.norm(across)
    ends = camera.project(np.array([foot - across, foot + across]))
    return float(np.linalg.norm(ends[1] - ends[0]))


def flask_sized(proposal: Proposal, camera: Camera) -> bool:
    """Whether a box is no bigger than a sample flask would look where it stands."""
    box = proposal.bbox
    return (box.v_max - box.v_min <= MAX_BOX[0] * flask_pixels(proposal.xy, camera)
            and box.u_max - box.u_min <= MAX_BOX[1] * flask_across(proposal.xy, camera))


def box_height(track: Track, camera: Camera) -> float:
    """How tall the fixed camera's box says a flask is, in metres.

    The box's height against a 115 mm flask's at the same place. The box takes
    in the rim of the base and the top seen from above, so this comes out a
    little tall, which is the safe side for something the arm must pass over.
    """
    box = track.bbox
    return (box.v_max - box.v_min) / flask_pixels(track.seen_xy, camera) * FLASK_HEIGHT


GRIPPER_SCENE = rk.SIM /'models/minihannover_rail_gripper_scene.xml'
GRIPPER_ARM = rk.SIM / 'assets/ur10e_2f85_gripper'


def gripper_scene() -> Path:
    """The rail scene with the Robotiq on the flange, built if it is out of date.

    The scene as shipped carries the pipette, and a pipette cannot pick a bottle
    up. generate_rail_scene.py builds either tool but writes both to the same
    files, so this runs it with the tool switched and its outputs pointed
    elsewhere, leaving the pipetting scene as it was. Both outputs are
    gitignored: they are one command away and would only go stale.

    Which is exactly what they did. A build older than the generator or than the
    scene it is built from is rebuilt: editing the generator and seeing the old
    bench is a long way to debug, because the file is there and looks current.
    """
    sources = [Path(__file__).resolve(), rk.SIM / 'scripts/generate_rail_scene.py',
               rk.SCENE]
    if (GRIPPER_SCENE.exists() and (GRIPPER_ARM / 'ur10e_2f85.xml').exists()
            and all(s.exists() and s.stat().st_mtime <= GRIPPER_SCENE.stat().st_mtime
                    for s in sources)):
        return GRIPPER_SCENE
    import generate_rail_scene as gen
    shipped = f'../{gen.ARM_DIR.relative_to(rk.SIM).as_posix()}/'
    gen.TOOL, gen.ARM_DIR, gen.OUT_SCENE = 'gripper', GRIPPER_ARM, GRIPPER_SCENE
    gen.build_gripper()
    gen.build_arm()
    gen.build_scene()
    # The scene names the arm's file by its shipped path; point it at this one.
    GRIPPER_SCENE.write_text(GRIPPER_SCENE.read_text(encoding='utf-8').replace(
        shipped, f'../{GRIPPER_ARM.relative_to(rk.SIM).as_posix()}/'), encoding='utf-8')
    print(f'built {GRIPPER_SCENE.relative_to(rk.SIM)}')
    return GRIPPER_SCENE


def truth(model: mujoco.MjModel, data: mujoco.MjData) -> dict[str, np.ndarray]:
    """Where every free bottle really is. For scoring, never for deciding.

    Keyed by the name that carries the sample id: the free body's own for the
    ``dyn_*`` vessels, its child's for the ``loose_*`` ones.
    """
    out = {}
    for j in range(model.njnt):
        if model.jnt_type[j] != mujoco.mjtJoint.mjJNT_FREE:
            continue
        body = model.jnt_bodyid[j]
        names = [model.body(body).name] + [
            model.body(i).name for i in range(model.nbody)
            if model.body_parentid[i] == body]
        out[next((n for n in names if 'SMP-' in n), names[0])] = data.xpos[body].copy()
    return out


class Feed:
    """The latest JPEG of one camera, handed from the perception thread to the page.

    wrist_view.py has one of these too and this script used to borrow it, until
    that one grew a second view and the page's streams died with it. Twelve
    lines are cheaper than the coupling.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._jpeg: bytes | None = None
        self._tick = 0

    def publish(self, picture: bytes) -> None:
        """Replace the current frame."""
        with self._lock:
            self._jpeg, self._tick = picture, self._tick + 1

    def latest(self) -> tuple[bytes | None, int]:
        """The current frame and a counter that changes when it does."""
        with self._lock:
            return self._jpeg, self._tick


class Read:
    """A request for the wrist camera to read the ring at a target."""

    def __init__(self, target: np.ndarray) -> None:
        self.target = target
        self.result: Confirmation | None = None
        self.rings: list[Confirmation] = []     # every ring in the frame, the target's too
        self.done = threading.Event()


class Show:
    """What the run puts on the page: two streams, fed by the perception thread."""

    def __init__(self) -> None:
        self.general, self.wrist = Feed(), Feed()


class Perception(threading.Thread):
    """The vision system: it looks all the time, whatever the arm is doing.

    It owns a copy of the simulation state, refreshed under the physics lock at
    the top of every cycle, and renders from that copy, so a slow render never
    holds the physics up. Its own OpenGL context lives on this thread.
    """

    def __init__(self, model: mujoco.MjModel, live: mujoco.MjData,
                 physics: threading.Lock, world: World, detector: Detector,
                 show: Show | None, video: Path | None) -> None:
        super().__init__(daemon=True)
        self.model, self.live, self.physics = model, live, physics
        self.world, self.detector, self.show, self.video = world, detector, show, video
        self.data = mujoco.MjData(model)
        self.rows = rows_by_marker(registry.load_table(DEFAULT_TABLE))
        self.reader = MarkerReader()
        self.requests: list[Read] = []
        # The arm's links, and each one's parent: the skeleton whose projection
        # is masked out of the fixed camera's frame.
        self.links = [(b, int(model.body_parentid[b])) for b in range(model.nbody)
                      if model.body(b).name.startswith('arm_')]
        self.stop = threading.Event()
        self.finished = threading.Event()
        self.ready = threading.Event()

    def read(self, target: np.ndarray) -> Read:
        """Ask for the ring at a target to be read from where the wrist is now."""
        request = Read(target)
        self.requests.append(request)
        return request

    def run(self) -> None:
        eyes = Eyes(self.model, self.data)
        writer = None
        try:
            # Both OpenGL contexts are made here, before anyone else touches
            # GLFW. The viewer initialises it too, on its own thread, and two
            # initialisations at once fail on Windows with "Failed to register
            # helper window class": main() waits for `ready` before it opens
            # the window.
            with self.physics:
                mujoco.mj_copyData(self.data, self.model, self.live)
            eyes.frame('general')
            eyes.frame('arm_eih', (960, 540))
            self.ready.set()
            while not self.stop.is_set():
                started = time.time()
                with self.physics:
                    mujoco.mj_copyData(self.data, self.model, self.live)
                while self.requests:
                    request = self.requests.pop(0)
                    # The copy above can predate the request by a whole cycle, when
                    # the arm was still on its way to the view: a frame from it
                    # reads nothing and costs a second bearing. Look from now.
                    with self.physics:
                        mujoco.mj_copyData(self.data, self.model, self.live)
                    wrist, lens = eyes.frame('arm_eih'), eyes.camera('arm_eih')
                    request.result = confirm(wrist, lens, request.target, self.rows,
                                             reader=self.reader, bench_z=rk.BENCH_TOP)
                    request.rings = rings_in_view(wrist, lens, self.rows, self.reader)
                    request.done.set()
                general = eyes.frame('general')
                camera = eyes.camera('general')
                arm = self.arm_pixels(camera)

                def on_arm(uv, arm=arm) -> bool:
                    return bool((np.linalg.norm(arm - uv, axis=1) < ARM_MASK_PX).any())

                boxes = [b for b in self.detector.detect(general)
                         if not on_arm(np.array(b[0].centre))]
                proposals = [p for p in propose(boxes, camera)
                             if WORKTOP[0][0] <= p.xy[0] <= WORKTOP[0][1]
                             and WORKTOP[1][0] <= p.xy[1] <= WORKTOP[1][1]
                             and flask_sized(p, camera)]
                self.world.update(
                    proposals, float(self.data.time),
                    lambda xy, on_arm=on_arm, camera=camera: on_arm(camera.project(
                        np.array([xy[0], xy[1], rk.BENCH_TOP + 0.03]))))
                self.score()
                self.world.cycle_seconds = time.time() - started
                if self.show is None and not self.video:
                    continue            # someone else shows the cameras
                drawn = annotate(general, self.world.snapshot(), camera)
                small = eyes.frame('arm_eih', (960, 540))
                if self.show is not None:
                    self.show.general.publish(jpeg(drawn))
                    self.show.wrist.publish(jpeg(small))
                if self.video:
                    if writer is None:
                        self.video.parent.mkdir(parents=True, exist_ok=True)
                        writer = cv2.VideoWriter(str(self.video),
                                                 cv2.VideoWriter_fourcc(*'mp4v'),
                                                 2, (1920, 540))
                    left = cv2.resize(drawn, (960, 540))
                    cv2.putText(left, f'{self.data.time:6.1f} s  {self.world.caption}',
                                (14, 526), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20),
                                2, cv2.LINE_AA)
                    writer.write(np.hstack([left, small]))
        finally:
            if writer:
                writer.release()
            eyes.close()
            self.ready.set()            # never leave main() waiting on a thread that died
            self.finished.set()

    def arm_pixels(self, camera: Camera) -> np.ndarray:
        """Where the arm is in a camera's picture, from its own joint angles.

        Forward kinematics and the camera's calibration, nothing else: points
        along every link of the arm and the gripper, projected.
        """
        points = [self.data.site(rk.TCP_SITE).xpos.copy()]
        for body, parent in self.links:
            points.append(self.data.xpos[body].copy())
            if self.model.body(parent).name.startswith('arm_'):
                points += [self.data.xpos[parent] + f * (self.data.xpos[body]
                                                        - self.data.xpos[parent])
                           for f in (0.25, 0.5, 0.75)]
        pixels = camera.project(np.array(points))
        return pixels[np.all(np.isfinite(pixels), axis=1)]

    def score(self) -> None:
        """Pair every track with the true bottle nearest it. Scoring only."""
        bodies = truth(self.model, self.data)
        with self.world.lock:
            for track in self.world.tracks.values():
                if track.held or track.state == 'lost':
                    continue
                name, off = min(((n, math.dist(track.xy, p[:2]))
                                 for n, p in bodies.items()), key=lambda pair: pair[1])
                track.truth = ({'body': name, 'error_mm': round(off * 1000, 1)}
                               if off < MATCH else {'body': None, 'error_mm': None})


def unwrap(model: mujoco.MjModel, q: np.ndarray, ref: np.ndarray) -> np.ndarray:
    """The same arm pose with each joint a whole number of turns nearest ``ref``.

    The UR10e's joints turn through two full turns, so an angle and that angle
    plus 360 degrees put the hand in the same place. IK returns whichever it
    converges to, and a servo ramped to the other one spins the hand round a
    full turn to arrive where it almost was: measured, 341 degrees of hand
    rotation in a single move between two views that look the same way.
    """
    out = q.copy()
    for i, name in enumerate(rk.ARM_JOINTS):
        joint = model.joint(name)
        lo, hi = joint.range if model.jnt_limited[joint.id] else (-np.inf, np.inf)
        turns = round((ref[i] - q[i]) / (2 * math.pi))
        options = [q[i] + 2 * math.pi * k for k in (turns - 1, turns, turns + 1)]
        options = [v for v in options if lo <= v <= hi]
        if options:
            out[i] = min(options, key=lambda v, r=ref[i]: abs(v - r))
    return out


def ik(model: mujoco.MjModel, scratch: mujoco.MjData, target: np.ndarray,
       ref: np.ndarray, **kwargs) -> bool:
    """rail_kinematics.solve_ik, with the answer turned to lie nearest ``ref``.

    Args:
        model: Compiled scene.
        scratch: Data to solve in; its arm angles hold the answer.
        target: World target of the driven site.
        ref: The arm pose the move starts from.
        **kwargs: Forwarded to :func:`rail_kinematics.solve_ik`.

    Returns:
        Whether IK converged.
    """
    if not rk.solve_ik(model, scratch, target, **kwargs):
        return False
    arm = rk.arm_qpos(model)
    scratch.qpos[arm] = unwrap(model, scratch.qpos[arm], np.asarray(ref))
    return True


def blocked(model: mujoco.MjModel, data: mujoco.MjData) -> bool:
    """Whether the posed arm touches the room or itself.

    IK knows nothing of the bench, the gantry beam, the balances or the arm's own
    forearm, so a pose it is happy with can stand inside any of them. Contacts
    with the free bottles are left out on purpose: where those stand is the
    cameras' business, and the arm keeps clear of them by travelling high.
    """
    mujoco.mj_forward(model, data)
    for contact in data.contact[:data.ncon]:
        bodies = [model.geom_bodyid[g] for g in (contact.geom1, contact.geom2)]
        if contact.dist > -0.001 or not any(
                model.body(i).name.startswith('arm_') for i in bodies):
            continue
        if not any(model.body_dofnum[model.body_rootid[i]] == 6 for i in bodies):
            return True
    return False


_ARM_GEOMS: dict[int, np.ndarray] = {}


def lowest_point(model: mujoco.MjModel, data: mujoco.MjData) -> float:
    """Height of the lowest point of the arm and its tool, from their geoms' boxes."""
    arm = _ARM_GEOMS.get(id(model))
    if arm is None:
        bodies = [b for b in range(model.nbody) if model.body(b).name.startswith('arm_')]
        arm = _ARM_GEOMS[id(model)] = np.flatnonzero(np.isin(model.geom_bodyid, bodies))
    centre, half = model.geom_aabb[arm, :3], model.geom_aabb[arm, 3:]
    up = data.geom_xmat[arm].reshape(-1, 3, 3)[:, 2, :]   # each local axis' world z
    z = (data.geom_xpos[arm, 2] + np.einsum('ij,ij->i', up, centre)
         - np.einsum('ij,ij->i', np.abs(up), half))
    return float(z.min())


def path_clear(model: mujoco.MjModel, scratch: mujoco.MjData,
               start: tuple[float, np.ndarray], goal: tuple[float, np.ndarray],
               floor: float | None = None) -> bool:
    """Whether the straight joint-space move between two poses touches nothing.

    With ``floor``, the arm's lowest point must also stay above that height the
    whole way: the free flasks are not in :func:`blocked`, so passing over them
    is a matter of height.

    The servos are ramped from one pose to the other joint by joint, so this is
    the path the arm will take. It matters: the first live run solved a grasp
    from the pose it had just looked from, got a wrist-flipped answer that was
    fine in itself, and on the way there jammed the wrist camera against the
    wrist. The servos stalled 170 mm from the bottle and the gripper closed on
    air.
    """
    (x0, q0), (x1, q1) = start, goal
    span = max(abs(x1 - x0) / 0.10, float(np.abs(q1 - q0).max()) / 0.08, 1.0)
    for f in np.linspace(0.0, 1.0, math.ceil(span) + 1):
        rk.set_rail(model, scratch, x0 + f * (x1 - x0))
        scratch.qpos[rk.arm_qpos(model)] = q0 + f * (q1 - q0)
        if blocked(model, scratch) or (floor is not None
                                       and lowest_point(model, scratch) < floor):
            return False
    return True


# Where the hand is carried between jobs: pointing down, 0.40 m over the middle
# of the worktop, above every vessel and clear of the balances' draught shields.
CARRY = (-0.35, 1.30)       # world y and z of the tool; x is wherever the carriage is
# Hand down over the bench with the wrist unfolded (wrist 2 at +90 degrees), the
# branch every grasp that worked was in. rail_kinematics' own seeds have wrist 2
# at -90, which for targets this high converges on the fold the camera blocks.
HAND_DOWN = (1.3, -0.35, 1.63, 0.29, 1.57, -1.69)


def carry_pose(model: mujoco.MjModel, scratch: mujoco.MjData,
               start: np.ndarray) -> np.ndarray:
    """The arm pose for :data:`CARRY`. The rail only translates it, so one pose serves.

    It has to be a pose the arm can get to from where it starts, not merely one
    that is clear once there. IK's first answer had the wrist folded over, where
    the wrist camera meets the forearm before wrist 3 is two thirds of the way
    round: clear as posed, unreachable as driven, and every pose solved from it
    inherited the fold.

    Args:
        model: Compiled scene.
        scratch: A copy of the state to solve in.
        start: The arm's joint angles now.
    """
    station = rk.set_rail(model, scratch, float(model.body('rail_carriage').pos[0]))
    target = np.array([station, *CARRY])
    for seed in (HAND_DOWN, *rk.SEED_POSES):
        if not ik(model, scratch, target, start, seed=np.array(seed)) \
                or blocked(model, scratch):
            continue
        pose = scratch.qpos[rk.arm_qpos(model)].copy()
        if path_clear(model, scratch, (station, start), (station, pose)):
            return pose
    raise SystemExit('no carry pose the arm can reach: has the bench changed?')


def plan(model: mujoco.MjModel, scratch: mujoco.MjData, carry: np.ndarray,
         first: np.ndarray, second: np.ndarray, **kwargs
         ) -> tuple[float, np.ndarray, np.ndarray] | None:
    """A station and two arm poses, reached carry -> first -> second, all clear.

    Every job has this shape: a pose well above the work and the pose at the
    work. The first is solved from the carry pose and the library's seeds, the
    second from the first so the two stay in one branch, and both the poses and
    the joint-space moves between them are checked against the room and the arm.

    Args:
        model: Compiled scene.
        scratch: A copy of the state to solve in; solve_ik overwrites its qpos.
        carry: The carry pose the move starts from.
        first: World target of the driven site for the pose above the work.
        second: World target for the pose at the work.
        **kwargs: Forwarded to :func:`rail_kinematics.solve_ik`.

    Returns:
        The carriage station and the two arm poses, or None.
    """
    for offset in rk.STANDOFFS:
        station = rk.set_rail(model, scratch, float(first[0]) + offset)
        mujoco.mj_kinematics(model, scratch)
        reach = float(np.linalg.norm(second - scratch.body('arm_base').xpos))
        if not rk.ENVELOPE[0] <= reach <= rk.ENVELOPE[1]:
            continue
        for seed in (carry, *map(np.array, (HAND_DOWN, *rk.SEED_POSES))):
            if not ik(model, scratch, first, carry, seed=seed, **kwargs) \
                    or blocked(model, scratch):
                continue
            q_first = scratch.qpos[rk.arm_qpos(model)].copy()
            if not ik(model, scratch, second, q_first, seed=q_first, **kwargs) \
                    or blocked(model, scratch):
                continue
            q_second = scratch.qpos[rk.arm_qpos(model)].copy()
            if path_clear(model, scratch, (station, carry), (station, q_first)) and \
                    path_clear(model, scratch, (station, q_first), (station, q_second)):
                return station, q_first, q_second
    return None


def plan_look(model: mujoco.MjModel, scratch: mujoco.MjData, carry: np.ndarray,
              target: np.ndarray, bearing_deg: float, look: tuple | None = None
              ) -> tuple[float, np.ndarray, np.ndarray] | None:
    """Arm poses that put the wrist camera on a proposal from one bearing.

    Args:
        look: Which of :data:`LOOKS` to stand at; the low look when not given.

    Returns:
        The carriage station, the arm pose well above the view, and the arm pose
        at the view; or None when this bearing cannot be held.
    """
    eye, gaze = look_view(target, bearing_deg, look)
    return plan(model, scratch, carry, eye + (0.0, 0.0, CLEARANCE), eye,
                approach=gaze, site_name=rk.EIH_SITE, image_up=(0.0, 0.0, 1.0))


def look_view(target: np.ndarray, bearing_deg: float, look: tuple | None = None
              ) -> tuple[np.ndarray, tuple]:
    """Where the wrist camera stands to look at a target from a bearing, and its gaze.

    ``look`` is one of :data:`LOOKS`, a (standoff, elevation) pair; the low look
    is used when it is not given.
    """
    standoff, elevation = LOOKS[-1] if look is None else look
    rise, turn = math.radians(elevation), math.radians(bearing_deg)
    offset = standoff * np.array([math.cos(rise) * math.cos(turn),
                                  math.cos(rise) * math.sin(turn), math.sin(rise)])
    return target + offset, tuple(-offset / np.linalg.norm(offset))


def hover_pose(model: mujoco.MjModel, scratch: mujoco.MjData, station: float,
               q_look: np.ndarray, eye: np.ndarray, gaze: tuple, floor: float
               ) -> np.ndarray | None:
    """The view pose raised to clear ``floor``, camera aimed the same way.

    It stands a little over the floor, as the hub does, since moving between
    two poses sweeps the hand a centimetre or two below both.

    Returns:
        The arm pose, or None if it cannot be held or the way down to the view
        is not clear; the caller then uses the view's usual pose above.
    """
    rk.set_rail(model, scratch, station)
    scratch.qpos[rk.arm_qpos(model)] = q_look
    mujoco.mj_forward(model, scratch)
    rise = max(floor - lowest_point(model, scratch) + HUB_ABOVE[0], 0.03)
    if not ik(model, scratch, eye + (0.0, 0.0, rise), q_look, seed=q_look, approach=gaze,
              site_name=rk.EIH_SITE, image_up=(0.0, 0.0, 1.0)) \
            or blocked(model, scratch) or lowest_point(model, scratch) < floor:
        return None
    q = scratch.qpos[rk.arm_qpos(model)].copy()
    return q if path_clear(model, scratch, (station, q), (station, q_look)) else None


def hub_pose(model: mujoco.MjModel, scratch: mujoco.MjData, carry: np.ndarray,
             floor: float) -> np.ndarray | None:
    """The carry pose lowered until the arm's lowest point stands at ``floor``.

    Returns:
        The arm pose, or None if it is not lower than the carry pose or cannot
        be held.
    """
    station = rk.set_rail(model, scratch, float(model.body('rail_carriage').pos[0]))
    scratch.qpos[rk.arm_qpos(model)] = carry
    mujoco.mj_forward(model, scratch)
    drop = lowest_point(model, scratch) - floor
    if drop <= 0.02:
        return None
    target = np.array([station, CARRY[0], CARRY[1] - drop])
    if not ik(model, scratch, target, carry, seed=carry) or blocked(model, scratch) \
            or lowest_point(model, scratch) < floor:
        return None
    return scratch.qpos[rk.arm_qpos(model)].copy()


def plan_grasp(model: mujoco.MjModel, scratch: mujoco.MjData, carry: np.ndarray,
               xy: tuple[float, float], height: float
               ) -> tuple[float, np.ndarray, np.ndarray] | None:
    """Arm poses above and on a bottle of known height at a perceived position.

    Returns:
        The carriage station, the pose above and the pose at the grasp; or None.
    """
    on = np.array([xy[0], xy[1], rk.BENCH_TOP + height * gt.GRASP_FRACTION])
    return plan(model, scratch, carry, on + (0.0, 0.0, gt.APPROACH), on)


def controller(model: mujoco.MjModel, data: mujoco.MjData, world: World,
               perception: Perception, bench_map_to: Path | None = BENCH_MAP):
    """Work the bench from the world model, stepping physics throughout.

    A generator: it yields a caption after every simulation step, so the caller
    renders and syncs between steps and the perception thread gets its turn at
    the state. It never reads a bottle's pose; tracks are all it knows.

    Every job starts and ends in the carry pose, hand high over the middle of
    the bench, and the carriage only travels with the arm in it.

    Args:
        model: Compiled scene.
        data: The live state.
        world: The tracks, shared with the perception thread.
        perception: The perception thread, which reads rings on request.
        bench_map_to: Where the initial scan writes what it found; None skips
            the scan and the arm works the tracks as they come.

    Yields:
        A short line describing what is happening.
    """
    ids = gt.actuators(model)
    # The pipetting scene has no gripper: it can scan and look, not pick.
    grip_id = (model.actuator('arm_grip_fingers_actuator').id
               if mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR,
                                    'arm_grip_fingers_actuator') >= 0 else None)
    rail_id = model.actuator(rk.RAIL_JOINT).id
    home = model.body('rail_carriage').pos[0]
    steps_per_second = round(1 / model.opt.timestep)
    scratch = mujoco.MjData(model)
    carry = carry_pose(model, scratch, data.qpos[rk.arm_qpos(model)].copy())
    general = camera_at(model, data, 'general')     # fixed: its calibration, once
    open_hand = lambda *_: gt.OPEN

    def drive(station, pose, grip, seconds, caption, *, guard=None,
              stop_on_grip=False):
        # The same ramp-then-sit servo drive as wrist_view's pick programme: a
        # position servo lags, and reading anything before it has caught up is
        # what made the first grasps there close 20 to 47 mm off the vessel.
        start = np.array([data.ctrl[i] for i in ids])
        # The nearest way round: a pose planned against the carry pose can be a
        # whole turn off the angles the arm has drifted to since.
        goal = np.concatenate([[station - home], unwrap(model, pose, start[1:])])
        move = np.abs(goal - start)
        seconds = max(seconds, float(move[0]) / 0.6, float(move[1:].max()) / 0.9)
        total = max(int(seconds * steps_per_second), 1)
        ramp = max(int(total * 0.7), 1)
        for step in range(total):
            if guard is not None and guard.state == 'lost':
                raise Retarget
            alpha = 0.5 - 0.5 * np.cos(np.pi * min(step + 1, ramp) / ramp)
            for i, value in zip(ids, start + alpha * (goal - start)):
                data.ctrl[i] = value
            if grip_id is not None:
                data.ctrl[grip_id] = grip(step, total)
            mujoco.mj_step(model, data)
            yield caption
            if stop_on_grip and step > total * 0.25 and \
                    rk.read_grip(model, data).holding:
                return

    def still(seconds, caption):
        for _ in range(max(int(seconds * steps_per_second), 1)):
            mujoco.mj_step(model, data)
            yield caption

    def glide(path, caption, guard=None):
        """Drive through (station, pose) waypoints as one move, then settle.

        One ramp over the whole path rather than one per waypoint, so a line of
        close waypoints is a single smooth move and not a string of stops. Each
        stretch takes its share of the time by how far its slowest joint or the
        carriage has to go, at the same speed limits as :func:`drive`.
        """
        points = [np.array([data.ctrl[i] for i in ids])]
        for station, pose in path:
            points.append(np.concatenate([[station - home],
                                          unwrap(model, pose, points[-1][1:])]))
        spans = [max(abs(b[0] - a[0]) / 0.6, float(np.abs(b[1:] - a[1:]).max()) / 0.9, 1e-6)
                 for a, b in itertools.pairwise(points)]
        edges = np.concatenate([[0.0], np.cumsum(spans)]) / sum(spans)
        total = max(int(max(sum(spans) * 1.4, 1.0) * steps_per_second), 1)
        for step in range(total):
            if guard is not None and guard.state == 'lost':
                raise Retarget
            f = 0.5 - 0.5 * math.cos(math.pi * (step + 1) / total)
            i = min(int(np.searchsorted(edges, f, side='right')) - 1, len(spans) - 1)
            local = (f - edges[i]) / (edges[i + 1] - edges[i])
            for actuator, value in zip(ids, points[i] + local * (points[i + 1] - points[i]),
                                       strict=True):
                data.ctrl[actuator] = value
            if grip_id is not None:
                data.ctrl[grip_id] = gt.OPEN
            mujoco.mj_step(model, data)
            yield caption
        yield from still(0.3, caption)

    def straight(start, goal, gaze, floor):
        """Waypoints that carry the camera along a straight line, turned one way.

        Two views at one bearing look the same way, but a joint-space move
        between them still swings the hand on the way: measured, up to 458
        degrees across the back strip. Solving the camera's pose every
        :data:`SLIDE_STEP` along the line, each from the one before, keeps the
        hand's orientation fixed the whole way: it only translates.

        Returns:
            The waypoints after ``start``, or None if the line cannot be held,
            or the two ends do not look the same way.
        """
        arm = rk.arm_qpos(model)
        mujoco.mj_copyData(scratch, model, data)
        ends = []
        for station, pose in (start, goal):
            rk.set_rail(model, scratch, station)
            scratch.qpos[arm] = pose
            mujoco.mj_kinematics(model, scratch)
            mujoco.mj_camlight(model, scratch)
            ends.append(scratch.site(rk.EIH_SITE).xpos.copy())
            facing = -scratch.cam_xmat[model.camera(rk.EIH_CAMERA).id].reshape(3, 3)[:, 2]
            if float(facing @ np.asarray(gaze)) < math.cos(math.radians(3)):
                return None
        (x0, q), (x1, _) = start, goal
        steps = max(math.ceil(float(np.linalg.norm(ends[1] - ends[0])) / SLIDE_STEP), 1)
        path, last = [], start
        for k in range(1, steps + 1):
            f = k / steps
            station = rk.set_rail(model, scratch, x0 + f * (x1 - x0))
            if k == steps:
                point = goal
            else:
                if not ik(model, scratch, ends[0] + f * (ends[1] - ends[0]), q, seed=q,
                          approach=gaze, site_name=rk.EIH_SITE, image_up=(0.0, 0.0, 1.0)):
                    return None
                point = (station, scratch.qpos[arm].copy())
            if not path_clear(model, scratch, last, point, floor=floor):
                return None
            path.append(point)
            last, q = point, point[1]
        return path

    def here() -> float:
        return float(home + data.ctrl[rail_id])

    def travel(station, caption, guard):
        """To a station in the carry pose; on Retarget the arm is already safe."""
        yield from drive(station, carry, open_hand, 1.0, caption, guard=guard)

    def tallest() -> float:
        """Height of the tallest flask on the bench: the ring's vessel, else the box's."""
        heights = []
        for track in world.snapshot():
            if track.state == 'lost' or track.held:
                continue
            if track.sample:
                vessel = perception.rows[track.confirmation.marker_id]['vessel_class']
                heights.append(vessel_height(vessel))
            elif track.bbox is not None:
                heights.append(box_height(track, general))
        return max(heights, default=FLASK_HEIGHT)

    hubs: dict[float, np.ndarray | None] = {}

    def hop(start, goal, floor):
        """A way from one low pose to another that stays over ``floor``, or None.

        Straight across if that is clear. Otherwise through the carry pose
        lowered to just over the floor: the arm reshapes there, the carriage
        runs along the rail with it, and it reshapes again for the next view.
        Two views from opposite sides need that, since turning the wrist all
        the way round sweeps the camera low.

        Returns:
            The (station, pose) waypoints after ``start``.
        """
        mujoco.mj_copyData(scratch, model, data)
        if path_clear(model, scratch, start, goal, floor=floor):
            return [goal]
        # Reshaping between a view and the hub sweeps the hand a centimetre or
        # two below both, so the hub stands a little over the floor.
        for above in HUB_ABOVE:
            key = round(floor + above, 2)
            if key not in hubs:
                hubs[key] = hub_pose(model, scratch, carry, key)
            if hubs[key] is None:
                continue
            legs = [start, (start[0], hubs[key]), (goal[0], hubs[key]), goal]
            if all(path_clear(model, scratch, a, b, floor=floor)
                   for a, b in itertools.pairwise(legs)):
                return legs[1:]
        return None

    def lifted(pose, rise, gaze):
        """The same view pose with the camera ``rise`` higher, turned the same way."""
        station, q = pose
        mujoco.mj_copyData(scratch, model, data)
        rk.set_rail(model, scratch, station)
        scratch.qpos[rk.arm_qpos(model)] = q
        mujoco.mj_kinematics(model, scratch)
        eye = scratch.site(rk.EIH_SITE).xpos + (0.0, 0.0, rise)
        if not ik(model, scratch, eye, q, seed=q, approach=gaze,
                  site_name=rk.EIH_SITE, image_up=(0.0, 0.0, 1.0)) or blocked(model, scratch):
            return None
        return station, scratch.qpos[rk.arm_qpos(model)].copy()

    def over(start, goal, gaze, floor):
        """Straight across; else straight up, across and down. The hand never turns.

        Across the back strip a line at waiting height runs the tool into the
        balances there, and one along the aisle edge into the arm itself.
        Lifting the whole line clears both without giving up the orientation.

        Returns:
            The waypoints after ``start``, or None.
        """
        line = straight(start, goal, gaze, floor)
        for rise in LIFTS:
            if line is not None:
                return line
            up, across = lifted(start, rise, gaze), lifted(goal, rise, gaze)
            if up is None or across is None:
                continue
            legs = [straight(a, b, gaze, floor) for a, b in
                    itertools.pairwise((start, up, across, goal))]
            line = None if None in legs else [point for leg in legs for point in leg]
        return line

    def plan_slide(hover, target, bearing, floor, look=None):
        """A view the arm reaches from where it waits without turning the hand.

        From one view to the next at the same bearing the camera looks the same
        way, so the hand keeps its orientation. Solved from the waiting pose,
        with the carriage where it stood relative to the camera, the arm also
        keeps its shape: the rail does the travelling and the joints only take
        up the difference in depth. That is the least the arm can move between
        two views, and it is tried before anything else.

        Returns:
            (station, pose over the flasks, view pose, waypoints from where
            the arm waits to the pose over the flasks), or None.
        """
        station0, q0 = hover
        mujoco.mj_copyData(scratch, model, data)
        rk.set_rail(model, scratch, station0)
        scratch.qpos[rk.arm_qpos(model)] = q0
        mujoco.mj_kinematics(model, scratch)
        eye, gaze = look_view(target, bearing, look)
        offset = station0 - float(scratch.site(rk.EIH_SITE).xpos[0])
        for station_offset in (offset, *rk.STANDOFFS):
            mujoco.mj_copyData(scratch, model, data)
            station = rk.set_rail(model, scratch, float(eye[0]) + station_offset)
            if not ik(model, scratch, eye, q0, seed=q0, approach=gaze,
                      site_name=rk.EIH_SITE, image_up=(0.0, 0.0, 1.0)) \
                    or blocked(model, scratch):
                continue
            q_look = scratch.qpos[rk.arm_qpos(model)].copy()
            q_hover = hover_pose(model, scratch, station, q_look, eye, gaze, floor)
            if q_hover is None:
                continue
            line = over(hover, (station, q_hover), gaze, floor)
            if line is not None:
                return station, q_hover, q_look, line
            mujoco.mj_copyData(scratch, model, data)
            if path_clear(model, scratch, hover, (station, q_hover), floor=floor):
                return station, q_hover, q_look, [(station, q_hover)]
        return None

    def back_row(track: Track) -> bool:
        """Whether a flask stands on the back strip, seen from the aisle side."""
        return track.seen_xy[1] + STANDOFF >= 0.10

    def look(track: Track, low: bool = False, hover=None):
        """Put the wrist camera on a track from its bearings until a ring reads.

        Normally the arm comes from the carry pose and goes back to it. With
        ``low`` it waits over the flasks instead, :data:`HOVER_MARGIN` above the
        tallest, and ``hover`` is where it waits now: it hops from there to the
        next view when the way is clear, and climbs to the carry pose only when
        it is not.

        Returns:
            Where the arm waits afterwards, as (station, pose), or None if it
            is back in the carry pose.
        """
        x, y = track.seen_xy
        target = np.array([x, y, rk.BENCH_TOP + LOOK_ABOVE_BENCH])
        tag = f'track {track.id} at ({x:+.2f}, {y:+.2f})'
        sides = AISLE_SIDE + RAIL_SIDE if back_row(track) else RAIL_SIDE + AISLE_SIDE
        looks, result, rings = 0, None, []
        # The looks in turn, the clearest first: only a ring that will not read
        # from up there brings the hand down to the next one.
        for look_at in LOOKS:
            tried = 0
            if look_at != LOOKS[0]:
                world.log(data.time, f'{tag}: no ring from {looks} views, bringing the '
                                     f'hand down to {look_at[1]:.0f} deg at '
                                     f'{look_at[0] * 100:.0f} cm')
            for bearing in sides:
                floor = rk.BENCH_TOP + tallest() + HOVER_MARGIN
                slid = (plan_slide(hover, target, bearing, floor, look_at)
                        if hover is not None else None)
                if slid is not None:
                    station, q_hover, q_look, line = slid
                    q_high = None
                else:
                    mujoco.mj_copyData(scratch, model, data)
                    found = plan_look(model, scratch, carry, target, bearing, look_at)
                    if found is None:
                        continue
                    station, q_high, q_look = found
                    q_hover = q_high
                    if low:
                        q_low = hover_pose(model, scratch, station, q_look,
                                           *look_view(target, bearing, look_at), floor)
                        q_hover = q_high if q_low is None else q_low
                looks, tried = looks + 1, tried + 1
                track.note = (f'wrist camera looking from {bearing:+d} deg, '
                              f'{look_at[1]:.0f} deg up at {look_at[0] * 100:.0f} cm')
                try:
                    if slid is not None:
                        yield from glide(line, f'over the flasks to {tag}', guard=track)
                    elif hover is not None and (route := hop(hover, (station, q_hover), floor)):
                        for leg_station, leg_pose in route:
                            yield from drive(leg_station, leg_pose, open_hand, 1.2,
                                             f'over the flasks to {tag}', guard=track)
                    else:
                        # From the carry pose the way down was checked to q_high, not
                        # to the low pose: enter through q_high.
                        if hover is not None:
                            hover = None
                            yield from drive(here(), carry, open_hand, 1.5,
                                             f'climbing clear to reach {tag}', guard=track)
                        yield from travel(station, f'travelling to {tag}', track)
                        yield from drive(station, q_high, open_hand, 1.5,
                                         f'turning the camera to {tag}', guard=track)
                except Retarget:
                    yield from drive(here(), carry, open_hand, 1.5, f'{tag} is gone')
                    return None
                yield from drive(station, q_look, open_hand, 1.5, f'looking at {tag}')
                yield from still(0.3, f'reading the ring at {tag}')
                request = perception.read(target)
                while not request.done.is_set():
                    yield from still(0.05, f'reading the ring at {tag}')
                result = request.result
                rings += request.rings
                yield from drive(station, q_hover, open_hand, 1.2, f'backing off {tag}')
                if low:
                    hover = (station, q_hover)
                else:
                    yield from drive(station, carry, open_hand, 1.5, f'backing off {tag}')
                if result.sample_id or tried >= MAX_LOOKS:
                    break
            if (result is not None and result.sample_id) or track.state == 'lost':
                break
        if track.state == 'lost':
            return hover
        if result is None:
            track.state, track.note = 'unreachable', 'the wrist camera cannot get there'
        elif not result.sample_id:
            track.confirmation, track.state = result, 'empty'
            track.note = f'no ring from {looks} views: not a sample'
        else:
            track.confirmation, track.state = result, 'named'
            track.note = f'ring read, {result.votes} markers'
            world.named(track, data.time)
        world.log(data.time, f'{tag}: ' + (
            f'ring reads {track.sample}, placed at ({track.xy[0]:+.4f}, '
            f'{track.xy[1]:+.4f})' if track.sample else track.note))
        world.sighted(rings, data.time, track)
        return hover

    def pick(track: Track):
        if grip_id is None:
            world.log(data.time, f'{track.sample}: this arm carries no gripper')
            return
        if not track.confirmation.refined_xy:
            # Put down since the ring last placed it: read it again first.
            yield from look(track)
            if track.state != 'named':
                return
        sample = track.sample
        vessel =perception.rows[track.confirmation.marker_id]['vessel_class']
        mujoco.mj_copyData(scratch, model, data)
        found = plan_grasp(model, scratch, carry, track.xy, vessel_height(vessel))
        if found is None:
            track.state, track.note = 'unreachable', 'named, but the gripper cannot reach'
            world.log(data.time, f'{sample}: {track.note}')
            return
        station, q_above, q_on = found
        try:
            yield from travel(station, f'travelling to {sample}', track)
            yield from drive(station, q_above, open_hand, 1.5,
                             f'moving over {sample}', guard=track)
        except Retarget:
            yield from drive(here(), carry, open_hand, 1.5, f'{sample} is gone')
            return
        yield from drive(station, q_on, open_hand, 2.0, f'reaching down for {sample}')
        track.held = True
        yield from drive(station, q_on,
                         lambda i, n: gt.SHUT * min((i + 1) / (n * 0.5), 1.0),
                         1.5, f'closing on {sample}', stop_on_grip=True)
        settled = float(data.ctrl[grip_id])
        keep = lambda *_, g=settled: g
        yield from drive(station, q_above, keep, 1.5, f'lifting {sample}')
        yield from drive(station, q_above, keep, 1.5, f'holding {sample}')
        got = rk.read_grip(model, data).holding
        track.state = 'picked' if got else 'missed'
        track.note = ('gripper reported an object and lifted it' if got
                      else 'gripper closed on nothing')
        world.log(data.time, f'{sample}: {track.note}')
        yield from drive(station, q_on, keep, 1.5, f'putting {sample} back')
        yield from drive(station, q_on, open_hand, 0.8, f'releasing {sample}')
        yield from drive(station, q_above, open_hand, 1.2, f'clear of {sample}')
        yield from drive(station, carry, open_hand, 1.5, f'clear of {sample}')
        # A bottle let go of settles where it likes, up to 30 mm from where it
        # was taken. The ring's position is spent; the fixed camera's stands in
        # until the next pick reads the ring again.
        track.confirmation.refined_xy = None
        track.picks += 1
        track.held = False

    def prefixed(prefix, job):
        """Run a job with a prefix on its captions, and hand back what it returns."""
        try:
            while True:
                yield prefix + next(job)
        except StopIteration as done:
            return done.value

    def survey(cycles, caption):
        """Hold still while the fixed camera looks at the bench this many times."""
        since = world.cycles
        while world.cycles < since + cycles:
            yield from still(0.2, caption)

    def initial_scan():
        """Read every bottle on the bench once, in one sweep of the rail.

        The carriage parks at the end of the rail nearer to it. From there the
        arm stands past the end of the bench in the fixed camera's picture and
        hides no bottle, so the survey sees them all. The proposals are then
        looked at in order along the rail from that end, and the carriage
        crosses the bench once. A proposal that turns up during the sweep joins
        it, or waits for the way back if the carriage has already passed it.
        """
        lo, hi = (float(home + v) for v in model.joint(rk.RAIL_JOINT).range)
        start = hi if hi - here() <= here() - lo else lo
        sweep = -1.0 if start == hi else 1.0
        began = float(data.time)
        yield from travel(start, 'initial scan: parking the arm at the end of the rail',
                          None)
        yield from survey(SURVEY_CYCLES, 'initial scan: the fixed camera surveys the bench')
        frontier, looked, settled, hover, row = start, 0, False, None, False
        world.log(data.time, f'initial scan: the tallest flask stands {tallest() * 100:.0f} cm, '
                             f'so between looks the arm keeps {HOVER_MARGIN * 100:.0f} cm over it')
        while True:
            todo = [t for t in world.snapshot() if t.state == 'proposed']
            if not todo:
                if settled:
                    break
                # A box first seen during the last look needs CONFIRM_HITS cycles
                # to become a track: one more survey before calling it done.
                yield from survey(CONFIRM_HITS, 'initial scan: a last survey of the bench')
                settled = True
                continue
            settled = False
            # One row at a time: the front of the bench on the way out, the back
            # strip on the way back. The camera looks at the two rows from
            # opposite sides, so mixing them would turn the hand round each time.
            in_row = [t for t in todo if back_row(t) == row]
            if not in_row:
                row, sweep = not row, -sweep
                continue
            ahead = [t for t in in_row if sweep * (t.seen_xy[0] - frontier) >= 0]
            if not ahead:
                sweep = -sweep
                continue
            track = min(ahead, key=lambda t: sweep * t.seen_xy[0])
            frontier = track.seen_xy[0]
            looked += 1
            prefix = f'initial scan {looked}/{looked + len(todo) - 1}: '
            hover = yield from prefixed(prefix, look(track, low=True, hover=hover))
        if hover is not None:
            yield from drive(here(), carry, open_hand, 1.5, 'initial scan: back to carry')
        world.scan = bench_map(world, began, float(data.time))
        bench_map_to.parent.mkdir(parents=True, exist_ok=True)
        bench_map_to.write_text(json.dumps(world.scan, indent=1) + '\n', encoding='utf-8')
        summary = world.scan['scans'][0]
        world.log(data.time, f'initial scan done in {summary["seconds"]:.0f} s: '
                             f'{summary["named"]} named, {summary["unidentified"]} '
                             f'not samples, {summary["unreachable"]} out of reach; '
                             f'wrote {bench_map_to.name}')

    yield from still(0.5, 'settling')
    yield from drive(here(), carry, open_hand, 3.0, 'raising the hand to carry')
    if bench_map_to is not None:
        yield from initial_scan()
    while True:
        tracks = world.snapshot()
        by_id = {t.id: t for t in tracks}
        job = None
        with world.lock:
            asked = [c for c in world.commands if c.get('cmd') == 'pick']
            world.commands[:] = [c for c in world.commands if c not in asked]
        for command in asked:
            track = by_id.get(command.get('track'))
            if job is None and track and track.sample and track.state != 'lost':
                job = (pick, track)
        if job is None:
            # A bottle just named is picked before anything else is looked at: the
            # arm is already there, and its position is as fresh as it will be.
            todo = [(pick, t) for t in tracks
                    if t.state == 'named' and not t.picks] if world.auto else []
            todo = todo or [(look, t) for t in tracks if t.state == 'proposed']
            if todo:
                # What the detector is sure of first, nearest along the rail first.
                # A ring is surer than any box: a bottle it named goes with the
                # sure ones, even one the fixed camera never boxed at all.
                job = min(todo, key=lambda j: (j[1].score < SURE and not j[1].sample,
                                               abs(j[1].xy[0] - here())))
        if job is None:
            yield from still(0.2, 'idle: watching the bench')
            continue
        yield from job[0](job[1])


def annotate(frame: np.ndarray, tracks: list[Track], camera: Camera) -> np.ndarray:
    """The fixed camera's frame with every track it sees boxed and labelled.

    A bottle only the wrist camera has seen has no box; one is drawn where a
    flask standing at its position would be.
    """
    out = frame.copy()
    colours = {'proposed': (0, 190, 255), 'named': (80, 200, 120),
               'picked': (80, 200, 120), 'missed': (60, 60, 230)}
    for track in tracks:
        if track.state in ('lost', 'tentative') or track.misses:
            continue
        if track.bbox is None:
            foot = np.array([*track.xy, rk.BENCH_TOP])
            (u, v0), (_, v1) = camera.project(np.array([foot, foot + (0, 0, FLASK_HEIGHT)]))
            half = 0.25 * abs(v0 - v1)
            x0, y0, x1, y1 = (round(c) for c in (u - half, v1, u + half, v0))
        else:
            x0, y0, x1, y1 = (round(c) for c in track.bbox.as_tuple())
        colour = colours.get(track.state, (140, 140, 140))
        cv2.rectangle(out, (x0 - 3, y0 - 3), (x1 + 3, y1 + 3), colour, 2)
        cv2.putText(out, track.sample or f'#{track.id}', (x0 - 3, y0 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 1, cv2.LINE_AA)
    return out


def jpeg(frame: np.ndarray, quality: int = 80) -> bytes:
    """A BGR frame as JPEG bytes."""
    return cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])[1].tobytes()


def state_of(world: World) -> dict[str, object]:
    """The page's JSON: tracks, log, caption."""
    return {
        'caption': world.caption, 'auto': world.auto, 'cycles': world.cycles,
        'cycle_seconds': round(world.cycle_seconds, 2),
        'events': world.events[-12:][::-1],
        'tracks': [{
            'id': t.id, 'x': round(t.xy[0], 3), 'y': round(t.xy[1], 3),
            'score': round(t.score, 2), 'sample': t.sample, 'state': t.state,
            'note': t.note, 'refined': bool(t.confirmation and t.confirmation.refined_xy),
            'error_mm': t.truth.get('error_mm'),
        } for t in sorted(world.snapshot(), key=lambda t: t.xy[0])
            if t.state not in ('lost', 'tentative')],
    }


PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Vision pick</title>
<style>
  :root { color-scheme: dark; }
  body { margin: 0; background: #14161a; color: #e8e6e1;
         font: 14px/1.5 ui-sans-serif, system-ui, sans-serif; }
  header { padding: 12px 18px; border-bottom: 1px solid #2a2e35; display: flex;
           gap: 18px; align-items: baseline; flex-wrap: wrap; }
  h1 { margin: 0; font-size: 15px; font-weight: 600; }
  #caption { color: #ffbe4d; font-variant-numeric: tabular-nums; flex: 1; }
  button { background: #22262c; color: #e8e6e1; border: 1px solid #3a3f47;
           border-radius: 5px; padding: 3px 10px; font: inherit; cursor: pointer; }
  button:hover { border-color: #ffbe4d; }
  main { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; padding: 14px 18px; }
  @media (max-width: 900px) { main { grid-template-columns: 1fr; } }
  figure { margin: 0; } figcaption { color: #9aa0a8; font-size: 12px; margin: 0 0 4px; }
  img { width: 100%; border-radius: 6px; border: 1px solid #2a2e35; background: #000; }
  .wide { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 13px;
          font-variant-numeric: tabular-nums; }
  th { text-align: left; color: #6f757d; font-weight: 600; font-size: 11px;
       letter-spacing: .06em; text-transform: uppercase; }
  th, td { padding: 4px 10px 4px 0; border-bottom: 1px solid #22262c; }
  .ok { color: #7fd18b; } .dim { color: #6f757d; }
  pre { margin: 0; font-size: 12px; color: #9aa0a8; white-space: pre-wrap; }
</style></head>
<body>
  <header><h1>Cameras direct the arm</h1><span id="caption">&hellip;</span>
    <span class="dim" id="rate"></span>
    <button onclick="send({cmd:'mode'})" id="mode">auto</button>
    <button onclick="send({cmd:'perturb'})">move a bottle</button></header>
  <main>
    <figure><figcaption>general &middot; YOLO boxes placed on the bench plane</figcaption>
      <img src="/general.mjpg" alt="fixed camera"></figure>
    <figure><figcaption>arm_eih &middot; ArUco ring names and places the bottle</figcaption>
      <img src="/wrist.mjpg" alt="wrist camera"></figure>
    <div class="wide"><table><thead><tr><th>track</th><th>bench x, y (m)</th>
      <th>score</th><th>sample</th><th>state</th><th>note</th><th>vs truth</th><th></th>
      </tr></thead><tbody id="rows"></tbody></table></div>
    <pre id="events"></pre>
  </main>
  <script>
    const send = body => fetch('/command', {method: 'POST', body: JSON.stringify(body)});
    setInterval(async () => {
      try {
        const t = await (await fetch('/telemetry')).json();
        document.getElementById('caption').textContent = t.caption;
        document.getElementById('rate').textContent =
          `perception cycle ${t.cycle_seconds} s`;
        document.getElementById('mode').textContent =
          t.auto ? 'auto: picks everything' : 'manual: pick from the table';
        document.getElementById('events').textContent = t.events.join('\\n');
        document.getElementById('rows').innerHTML = t.tracks.map(f =>
          `<tr><td>${f.id}</td>` +
          `<td>${f.x.toFixed(3)}, ${f.y.toFixed(3)}${f.refined ? ' &#9679;' : ''}</td>` +
          `<td>${f.score.toFixed(2)}</td>` +
          `<td class="${f.sample ? 'ok' : 'dim'}">${f.sample || '-'}</td>` +
          `<td>${f.state}</td><td class="dim">${f.note}</td>` +
          `<td class="dim">${f.error_mm == null ? '-' : f.error_mm + ' mm'}</td>` +
          `<td>${f.sample ? `<button onclick="send({cmd:'pick',track:${f.id}})">pick</button>` : ''}</td></tr>`
        ).join('');
      } catch (e) { /* run ended; keep the last table */ }
    }, 300);
  </script>
</body></html>
"""


def serve(world: World, show: Show, port: int) -> http.server.ThreadingHTTPServer:
    """Serve the page, both MJPEG streams, the state and the commands."""

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            if self.path.startswith('/general.mjpg'):
                self._stream(show.general)
            elif self.path.startswith('/wrist.mjpg'):
                self._stream(show.wrist)
            elif self.path.startswith('/telemetry'):
                self._send(json.dumps(state_of(world)).encode(), 'application/json')
            else:
                self._send(PAGE.encode(), 'text/html; charset=utf-8')

        def do_POST(self) -> None:
            length = int(self.headers.get('Content-Length', 0))
            try:
                command = json.loads(self.rfile.read(length) or b'{}')
            except json.JSONDecodeError:
                command = {}
            if command.get('cmd') == 'mode':
                world.auto = not world.auto
            elif command.get('cmd') in ('pick', 'perturb'):
                with world.lock:
                    world.commands.append(command)
            self._send(b'{}', 'application/json')

        def _send(self, body: bytes, content_type: str) -> None:
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass          # the tab went away mid-answer

        def _stream(self, feed: Feed) -> None:
            self.send_response(200)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Type',
                             'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()
            seen = -1
            try:
                while True:
                    picture, tick = feed.latest()
                    if picture is None or tick == seen:
                        time.sleep(1 / 60)
                        continue
                    seen = tick
                    self.wfile.write(b'--frame\r\nContent-Type: image/jpeg\r\n'
                                     b'Content-Length: ' + str(len(picture)).encode()
                                     + b'\r\n\r\n' + picture + b'\r\n')
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                pass

        def log_message(self, *args) -> None:
            """Stay quiet; the interesting output is the run's."""

    server = http.server.ThreadingHTTPServer(('127.0.0.1', port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def move_a_bottle(model: mujoco.MjModel, data: mujoco.MjData, world: World,
                  rng: np.random.Generator) -> None:
    """Play the person who moves a bottle: put a random one somewhere else.

    This is the one actor allowed to know where things are. It picks a bottle
    the cameras have named, because moving one nobody knows shows nothing.
    """
    bodies = truth(model, data)
    known = [t for t in world.snapshot() if t.sample and not t.held and not t.wrist_only
             and t.state != 'lost' and t.truth.get('body') in bodies]
    if not known:
        world.log(data.time, 'move a bottle: none named yet')
        return
    body = str(rng.choice([t.truth['body'] for t in known]))
    spot = bodies[body][:2]
    for _ in range(200):
        spot = np.array([rng.uniform(-2.8, 0.2), rng.uniform(-0.75, -0.25)])
        if all(np.linalg.norm(spot - p[:2]) > 0.2 for p in bodies.values()):
            break
    joint = model.body_jntadr[model.body_rootid[model.body(body).id]]
    qpos, qvel = model.jnt_qposadr[joint], model.jnt_dofadr[joint]
    world.log(data.time, f'someone moves {body} to ({spot[0]:+.2f}, {spot[1]:+.2f})')
    data.qpos[qpos:qpos + 2] = spot
    data.qvel[qvel:qvel + 6] = 0.0


def bench_map(world: World, began: float, ended: float) -> dict[str, object]:
    """The initial scan as the bench memory of SCANNING_PLAN.md: what stands where.

    A named bottle is keyed by its sample id and carries the catalogue's row. A
    proposal no ring named is kept too, as ``UNK-*``: the arm has to know that
    something stands there even when it does not know what, so as not to hit it
    and to try again. A named bottle the fixed camera has since lost is kept as
    ``missing``, not dropped: in a crowd a box merges with its neighbour's or
    hides behind the arm, and losing it from the map would forget a flask that
    is still there. The truth only fills ``scored``, which grades the scan.

    Args:
        world: The tracks as the scan left them.
        began: Simulated time the scan started.
        ended: Simulated time it finished.

    Returns:
        The JSON-ready map.
    """
    table = registry.load_table(DEFAULT_TABLE)
    by_marker = {int(row['marker_id']): (code, row) for code, row in table.items()
                 if 'marker_id' in row}
    entries: dict[str, dict] = {}
    tracks = [t for t in world.snapshot() if t.state != 'tentative']
    present = {t.sample for t in tracks if t.sample and t.state != 'lost'}
    tracks = sorted((t for t in tracks if t.state != 'lost'
                     or (t.sample and t.sample not in present)), key=lambda t: t.xy[0])
    unknown, errors, right = 0, [], 0
    for track in tracks:
        entry = {
            'position': [round(track.xy[0], 4), round(track.xy[1], 4), rk.BENCH_TOP],
            'refined': bool(track.confirmation and track.confirmation.refined_xy),
            'detector_score': round(track.score, 3) if track.bbox is not None else None,
            'found_by': 'wrist camera' if track.bbox is None else 'fixed camera',
            'track': track.id,
        }
        body = track.truth.get('body')
        if track.sample:
            code, row = by_marker[track.confirmation.marker_id]
            key = track.sample
            entry = {'marker_id': track.confirmation.marker_id, 'barcode': code,
                     **{k: row[k] for k in CATALOGUE_FIELDS if k in row}, **entry,
                     'votes': track.confirmation.votes,
                     'status': 'missing' if track.state == 'lost' else 'present'}
            correct = body is not None and str(body).endswith(track.sample)
            entry['scored'] = {'check': 'correct' if correct else 'wrong',
                               'error_mm': track.truth.get('error_mm')}
            if correct and track.state != 'lost':
                right += 1
                errors.append(track.truth['error_mm'])
        else:
            unknown += 1
            key = f'UNK-{unknown:04d}'
            entry['status'] = 'unreachable' if track.state == 'unreachable' else 'unidentified'
            entry['note'] = track.note
            entry['scored'] = {'body': body, 'error_mm': track.truth.get('error_mm')}
        entries[key] = entry
    named = sum(1 for e in entries.values() if e['status'] == 'present')
    return {
        'version': 1,
        'scene': world.scene,
        'frame': f'MuJoCo world, metres, +Z up; bench top z = {rk.BENCH_TOP}',
        'method': 'initial scan: the fixed camera proposes, the arm sweeps the rail '
                  'once and its wrist camera reads each proposal\'s ArUco ring',
        'scans': [{
            'id': 0, 'started_s': round(began, 1), 'finished_s': round(ended, 1),
            'seconds': round(ended - began, 1), 'proposals': len(entries),
            'named': named,
            'missing': sum(1 for e in entries.values() if e['status'] == 'missing'),
            'unidentified': sum(1 for e in entries.values() if e['status'] == 'unidentified'),
            'unreachable': sum(1 for e in entries.values() if e['status'] == 'unreachable'),
            'found_by_wrist_only': sum(1 for e in entries.values()
                                       if e['found_by'] == 'wrist camera'),
            'scored': {'named_right': right, 'named_wrong': named - right,
                       'median_error_mm': (round(float(np.median(errors)), 1)
                                           if errors else None)},
        }],
        'entries': entries,
    }


def report(world: World) -> str:
    """The run in a few lines: the cameras' claims against the truth."""
    tracks = [t for t in world.snapshot() if t.state not in ('lost', 'tentative')]
    named = [t for t in tracks if t.sample]
    right = [t for t in named if str(t.truth.get('body', '')).endswith(t.sample)]
    errors = [t.truth['error_mm'] for t in named if t.truth.get('error_mm') is not None]
    lines = []
    if world.scan:
        scan = world.scan['scans'][0]
        lines.append(f'initial scan:             {scan["named"]} named of '
                     f'{scan["proposals"]} proposals in {scan["seconds"]:.0f} s '
                     f'({scan["scored"]["named_wrong"]} named wrong)')
    lines += [
        f'perception cycles:        {world.cycles} (last {world.cycle_seconds:.2f} s)',
        f'tracks on the bench:      {len(tracks)}',
        f'named by the ring:        {len(named)} ({len(right)} checked right against truth)',
        f'not samples, left alone:  {sum(1 for t in tracks if t.state == "empty")}',
        f'picked and lifted:        {sum(1 for t in tracks if t.state == "picked")}',
        f'gripper closed on air:    {sum(1 for t in tracks if t.state == "missed")}',
    ]
    if errors:
        lines.append(f'position error, named:    median {np.median(errors):.1f} mm, '
                     f'max {max(errors):.1f} mm')
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--weights', type=Path, default=None,
                        help='Ultralytics weights for the fixed camera; the best '
                             'of DETECTORS that is on disk when omitted')
    parser.add_argument('--threshold', type=float, default=None,
                        help='detector confidence; the chosen weights\' own when omitted')
    parser.add_argument('--device', default=None,
                        help='torch device for the detector; CUDA or MPS when present')
    parser.add_argument('--manual', action='store_true',
                        help='look at everything, pick only what the page asks for')
    parser.add_argument('--headless', action='store_true',
                        help='no MuJoCo window; stops once the bench is worked')
    parser.add_argument('--max-time', type=float, default=600.0,
                        help='headless: stop after this much simulated time')
    parser.add_argument('--perturb-at', type=float, nargs='*', default=[],
                        help='simulated times at which a bottle gets moved')
    parser.add_argument('--video', type=Path, default=None,
                        help='write what the cameras saw, one frame per perception cycle')
    parser.add_argument('--no-scan', action='store_true',
                        help='skip the initial scan: look at and pick each track as it comes')
    parser.add_argument('--bench-map', type=Path, default=BENCH_MAP,
                        help='where the initial scan writes what stands on the bench')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--port', type=int, default=8009)
    parser.add_argument('--no-browser', action='store_true')
    parser.add_argument('--light', action='store_true',
                        help='do not draw the meshes off the bench: for integrated '
                             'graphics, where the full room is a frame a second')
    args = parser.parse_args()

    model, data = rk.load(gripper_scene())
    if args.light:
        print(f'light: {lighten(model, data):,} triangles off the bench not drawn')
    rng = np.random.default_rng(args.seed)
    weights, threshold = next((d for d in DETECTORS if d[0].exists()), DETECTORS[0])
    if args.weights:
        weights, threshold = args.weights, 0.10
    detector = Detector(weights, args.threshold or threshold, args.device)
    detector.detect(np.zeros((1080, 1920, 3), np.uint8))     # warm up before the clock
    print(f'detector {weights.name} at {detector.threshold} on {detector.device}')
    world, show, physics = World(auto=not args.manual), Show(), threading.Lock()
    perception = Perception(model, data, physics, world, detector, show, args.video)
    run = controller(model, data, world, perception,
                     None if args.no_scan else args.bench_map)
    perturb_at = sorted(args.perturb_at)

    server = serve(world, show, args.port)
    print(f'page at http://localhost:{args.port}')
    if not (args.headless or args.no_browser):
        webbrowser.open(f'http://localhost:{args.port}')
    steps_per_frame = max(round(1 / FPS / model.opt.timestep), 1)
    idle_since = None

    def frame_once() -> None:
        nonlocal idle_since
        with physics:
            for _ in range(steps_per_frame):
                world.caption = next(run)
            with world.lock:
                asked = [c for c in world.commands if c.get('cmd') == 'perturb']
                world.commands[:] = [c for c in world.commands if c not in asked]
            while perturb_at and data.time >= perturb_at[0]:
                asked.append(perturb_at.pop(0))
            for _ in asked:
                move_a_bottle(model, data, world, rng)
        if not world.caption.startswith('idle') or perturb_at:
            idle_since = None
        elif idle_since is None:
            idle_since = world.cycles

    def key(code: int) -> None:
        if code == ord('M'):
            with world.lock:
                world.commands.append({'cmd': 'perturb'})

    perception.start()
    perception.ready.wait(timeout=180)
    if perception.finished.is_set():
        raise SystemExit('the perception thread could not start; see the error above')
    try:
        if args.headless:
            while data.time < args.max_time:
                started = time.time()
                frame_once()
                # Worked out: idle, and the cameras have had a few looks since.
                if idle_since is not None and world.cycles - idle_since >= LOST_AFTER + 2:
                    break
                time.sleep(max(1 / FPS - (time.time() - started), 0))
        else:
            import mujoco.viewer
            with mujoco.viewer.launch_passive(model, data, show_left_ui=False,
                                              show_right_ui=False,
                                              key_callback=key) as viewer:
                while viewer.is_running():
                    started = time.time()
                    with viewer.lock():
                        frame_once()
                    viewer.sync()
                    time.sleep(max(1 / FPS - (time.time() - started), 0))
    except KeyboardInterrupt:
        pass
    finally:
        perception.stop.set()
        perception.finished.wait(timeout=60)
        server.shutdown()
        print(report(world))


if __name__ == '__main__':
    main()
