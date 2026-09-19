"""The general camera proposes, the wrist camera confirms: find, place and name bottles

The vision system the team settled on, run end to end in the minihannover scene
with nothing read from the simulator but the cameras' own poses. The steps are
:mod:`labvision.perception`'s; this script supplies the scene, the detector and
the scoring:

1. **Propose.** The fixed ``general`` GoPro's frame goes through a detector
   (YOLO-World with the bottle prompts by default, or any Ultralytics weights,
   such as a model trained on the renders). Boxes whose base does not land on
   the worktop are dropped (:func:`perfumery_eval.on_worktop`) and the rest are
   placed on the bench (:func:`labvision.perception.propose`).
2. **Confirm.** For each proposal the wrist camera is flown to
   :data:`STANDOFF_M` from it, from the nearer aisle, and its frame's ArUco
   rings name the bottle and refine its position
   (:func:`labvision.perception.confirm`). If nothing is read the next of
   :data:`AZIMUTHS_DEG` is tried: the pipeline does not ask the simulator
   whether a view is blocked, it finds out by looking.

The truth --- where every bottle really is and which one it is --- is read
from the simulator only to score, never by the pipeline.

    python scripts/propose_confirm.py --layouts 12
    python scripts/propose_confirm.py --layouts 12 --weights runs/fixedcam/best.pt
    python scripts/propose_confirm.py --as-built --save-frames   # the scene as built

Writes ``propose_confirm.json`` and ``propose_confirm.md`` in ``--out``. Per
layout the JSON holds the proposals and what the wrist read at each, the world
state as :class:`labvision.world.PerceivedBottle` records, the same bottles as
the console's ``vessels`` (:func:`labvision.world.to_dashboard`), and the truth
they were scored against.
"""

import argparse
import json
import math
import statistics
import sys
import time
from dataclasses import asdict
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from perfumery_eval import WORKTOP_HALF, base_on_worktop, on_worktop  # noqa: E402
from render_perfumery import BENCH_X, WORKTOP_Z, Lab, where_is  # noqa: E402
from world_prompts import BOTTLES  # noqa: E402

from labvision import registry  # noqa: E402
from labvision.camera import Camera  # noqa: E402
from labvision.detector import _find_weights, input_size_for  # noqa: E402
from labvision.identify import DEFAULT_TABLE, MarkerReader, rows_by_marker  # noqa: E402
from labvision.perception import confirm, perceived, propose  # noqa: E402
from labvision.scene import BBox, gopro_intrinsics  # noqa: E402
from labvision.world import to_dashboard  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
STANDOFF_M = 0.30
"""Wrist camera to proposal: a GoPro's near focus, from where the ring reads on
every bottle size (``scripts/ring_experiment.py``)."""
WRIST_ELEVATION_DEG = 15.0
"""The wrist camera looks down at the proposal from this far above level, which
:func:`labvision.perception.refine` needs to cross the ring's height."""
LOOK_ABOVE_BENCH_M = 0.05
"""The wrist camera aims this far above the proposal's base."""
MATCH_M = 0.06
"""A proposal within this of a true bottle is scored as that bottle."""
GENERAL_THRESHOLD = 0.11
"""YOLO-World's threshold in :mod:`labvision.detector`."""


class GeneralDetector:
    """The detector the fixed camera runs: YOLO-World with bottle prompts, or weights

    Args:
        weights: Ultralytics weights to use instead of YOLO-World, or None.
        threshold: Confidence threshold; the detector's own if None.
    """

    def __init__(self, weights: str | None = None, threshold: float | None = None):
        """Load the model"""
        from ultralytics import YOLO, YOLOWorld

        if weights:
            self.model = YOLO(weights)
            self.threshold = 0.25 if threshold is None else threshold
            self.name = Path(weights).name
        else:
            self.model = YOLOWorld(_find_weights("yolov8l-worldv2.pt"))
            self.model.set_classes(list(BOTTLES))
            self.threshold = GENERAL_THRESHOLD if threshold is None else threshold
            self.name = "world-b"

    def detect(self, frame: np.ndarray) -> list[tuple[BBox, float, str]]:
        """Boxes above the threshold as ``(bbox, score, label)``"""
        result = self.model.predict(
            frame,
            imgsz=input_size_for(frame, None),
            conf=self.threshold,
            iou=0.6,
            agnostic_nms=True,
            max_det=300,
            verbose=False,
        )[0]
        return [
            (
                BBox(*(float(v) for v in hit.xyxy[0])),
                float(hit.conf),
                result.names[int(hit.cls)],
            )
            for hit in result.boxes
        ]


def frame_meta(lab: Lab, camera: int, width: int, height: int, name: str) -> dict:
    """The camera record :func:`perfumery_eval.on_worktop` expects"""
    return {
        "set": name,
        "width": width,
        "height": height,
        "fovy_deg": float(lab.model.cam_fovy[camera]),
        "cam_pos": [float(v) for v in lab.data.cam_xpos[camera]],
        "cam_xmat": [float(v) for v in lab.data.cam_xmat[camera]],
    }


def on_any_worktop(meta: dict, bbox: BBox) -> bool:
    """Whether a box's base lands anywhere on the worktop, either half

    Looser than :func:`perfumery_eval.on_worktop`, which keeps the fixed
    camera to its own half because the lowest shelf projects onto the far one.
    Here those shelf boxes get through, and the wrist camera's check that a
    ring's bottle stands on the proposal is what turns them away.
    """
    point = base_on_worktop(meta, bbox.as_tuple())
    return (
        point is not None
        and abs(point[0]) <= WORKTOP_HALF[0]
        and abs(point[1]) <= WORKTOP_HALF[1]
    )


def camera_of(lab: Lab, camera: int, width: int, height: int) -> Camera:
    """The pinhole model of a scene camera at its current pose"""
    intrinsics = gopro_intrinsics(width, height)
    return Camera.from_mujoco(
        intrinsics, lab.data.cam_xpos[camera], lab.data.cam_xmat[camera]
    )


AZIMUTHS_DEG = (0, 25, -25, 50, -50)
"""Wrist views tried in turn, from straight across the aisle to 50 degrees
either side, until one names the bottle."""


def wrist_pose(target: np.ndarray, azimuth_deg: float) -> np.ndarray:
    """The wrist camera position at the standoff from the aisle side of a proposal

    It uses nothing but the proposal: which aisle is the nearer, and the
    azimuth to try. A view blocked by something is found out by reading
    nothing there, and the next azimuth is tried, as an arm would.
    """
    side = -1.0 if target[1] < 0 else 1.0
    elevation = math.radians(WRIST_ELEVATION_DEG)
    azimuth = math.radians(azimuth_deg)
    return target + STANDOFF_M * np.array(
        [
            math.cos(elevation) * math.sin(azimuth),
            side * math.cos(elevation) * math.cos(azimuth),
            math.sin(elevation),
        ]
    )


def truth(lab: Lab) -> list[dict]:
    """Every bottle standing on the bench, with its identity: for scoring only"""
    return [
        {
            "sample_id": s["sample_id"],
            "xy": [float(v) for v in lab.data.xpos[s["body"]][:2]],
        }
        for s in lab.samples
        if s["movable"] and where_is(lab.data.xpos[s["body"]]) == "bench"
    ]


def score(bottles: list[dict], visible: set[str], found: list[dict]) -> dict:
    """Match proposals to bottles one to one by distance and grade each bottle"""
    pairs = sorted(
        (math.dist(b["xy"], f["xy"]), i, j)
        for i, b in enumerate(bottles)
        for j, f in enumerate(found)
    )
    bottle_of, used = {}, set()
    for distance, i, j in pairs:
        if distance > MATCH_M or i in bottle_of or j in used:
            continue
        bottle_of[i] = j
        used.add(j)
    graded = []
    for i, bottle in enumerate(bottles):
        j = bottle_of.get(i)
        f = found[j] if j is not None else None
        named = f["confirm"]["sample_id"] if f else None
        refined = f["confirm"]["refined_xy"] if f else None
        graded.append(
            {
                **bottle,
                "visible": bottle["sample_id"] in visible,
                "proposed": f is not None,
                "named": named,
                "correct": named == bottle["sample_id"],
                "wrong": named is not None and named != bottle["sample_id"],
                "error_m": math.dist(bottle["xy"], f["xy"]) if f else None,
                "refined_error_m": math.dist(bottle["xy"], refined)
                if refined
                else None,
            }
        )
    stray = [f for j, f in enumerate(found) if j not in used]
    return {"bottles": graded, "stray": stray}


def summarise(layouts: list[dict], detector: str) -> str:
    """Markdown summary over every layout"""
    graded = [b for layout in layouts for b in layout["scored"]["bottles"]]
    visible = [b for b in graded if b["visible"]]
    stray = [f for layout in layouts for f in layout["scored"]["stray"]]

    def pct(n, d):
        return f"{100 * n / d:.0f} % ({n}/{d})" if d else "-"

    def quant(values, q):
        values = sorted(values)
        return (
            values[min(len(values) - 1, int(q * len(values)))] if values else math.nan
        )

    errors = [b["error_m"] * 1000 for b in graded if b["error_m"] is not None]
    refined = [b["refined_error_m"] * 1000 for b in graded if b["refined_error_m"]]
    seconds = {
        k: statistics.median(layout["seconds"][k] for layout in layouts)
        for k in layouts[0]["seconds"]
    }
    lines = [
        f"# Propose (general) -> confirm (wrist), {len(layouts)} layouts, "
        f"detector {detector}",
        "",
        "| | all bench bottles | visible from the general camera |",
        "| --- | --- | --- |",
        f"| proposed | {pct(sum(b['proposed'] for b in graded), len(graded))} | "
        f"{pct(sum(b['proposed'] for b in visible), len(visible))} |",
        f"| named correctly | {pct(sum(b['correct'] for b in graded), len(graded))} | "
        f"{pct(sum(b['correct'] for b in visible), len(visible))} |",
        f"| named wrongly | {sum(b['wrong'] for b in graded)} | "
        f"{sum(b['wrong'] for b in visible)} |",
        "",
        f"Proposals that matched no bottle: {len(stray)} "
        f"({sum(1 for f in stray if f['confirm']['sample_id'])} of them read an id).",
        "",
        "| position error | median | p90 |",
        "| --- | --- | --- |",
        f"| general camera proposal | {quant(errors, 0.5):.0f} mm | "
        f"{quant(errors, 0.9):.0f} mm |",
        f"| after the wrist refines it | {quant(refined, 0.5):.0f} mm | "
        f"{quant(refined, 0.9):.0f} mm |",
        "",
        "Median seconds per layout: "
        + ", ".join(f"{k} {v:.1f}" for k, v in seconds.items()),
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    """Run the layouts and write the results"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--layouts", type=int, default=12)
    parser.add_argument(
        "--bottles", type=int, nargs=2, default=(6, 10), metavar=("MIN", "MAX")
    )
    parser.add_argument(
        "--weights", default=None, help="Ultralytics weights for the general camera"
    )
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--keep",
        choices=("half", "bench"),
        default="half",
        help="worktop filter: the camera's own half of the bench, or all of it",
    )
    parser.add_argument(
        "--as-built",
        action="store_true",
        help="one layout: the bottles where the scene file puts them",
    )
    parser.add_argument(
        "--save-frames",
        action="store_true",
        help="write every general and wrist frame as JPEG next to the results",
    )
    parser.add_argument(
        "--out", type=Path, default=REPO / "simulation" / "out" / "propose_confirm"
    )
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    detector = GeneralDetector(args.weights, args.threshold)
    rows = rows_by_marker(registry.load_table(DEFAULT_TABLE))
    reader = MarkerReader()
    lab = Lab()
    general, wrist = lab.cameras["general"], lab.cameras["wrist"]
    gw, gh = (int(v) for v in lab.model.cam_resolution[general])
    ww, wh = (int(v) for v in lab.model.cam_resolution[wrist])

    layouts = []
    for k in range(1 if args.as_built else args.layouts):
        if args.as_built:
            x0 = 0.0
            lab.reset()
        else:
            x0 = float(rng.uniform(BENCH_X[0] + 0.8, BENCH_X[1] - 0.8))
            count = int(rng.integers(args.bottles[0], args.bottles[1] + 1))
            lab.scatter(rng, count, (x0 - 0.8, x0 + 0.8), (-1,))
        t0 = time.perf_counter()
        rgb, in_view, _ = lab.render(general, gw, gh)
        visible = {
            b["sample_id"]
            for b in in_view
            if b.get("where") == "bench"
            and b["visible_frac"] >= 0.5
            and not b["clipped"]
        }
        frame = rgb[:, :, ::-1].copy()
        boxes_of = {
            b["sample_id"]: b["xyxy"] for b in in_view if b.get("where") == "bench"
        }
        if args.save_frames:
            cv2.imwrite(
                str(args.out / f"layout_{k:02d}_general.jpg"),
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, 85],
            )
        t1 = time.perf_counter()
        meta = frame_meta(lab, general, gw, gh, "general")
        proposals = propose(
            detector.detect(frame),
            camera_of(lab, general, gw, gh),
            keep=(
                (lambda bbox, meta=meta: on_worktop(meta, bbox.as_tuple()))
                if args.keep == "half"
                else (lambda bbox, meta=meta: on_any_worktop(meta, bbox))
            ),
            bench_z=WORKTOP_Z,
        )
        t2 = time.perf_counter()
        world, found = [], []
        for j, proposal in enumerate(proposals):
            target = np.array([*proposal.xy, WORKTOP_Z + LOOK_ABOVE_BENCH_M])
            views = 0
            for azimuth in AZIMUTHS_DEG:
                views += 1
                lab.fly_wrist(wrist_pose(target, azimuth), target)
                wrist_frame = lab.rgb(wrist, ww, wh)[:, :, ::-1].copy()
                confirmation = confirm(
                    wrist_frame,
                    camera_of(lab, wrist, ww, wh),
                    target,
                    rows,
                    reader=reader,
                    bench_z=WORKTOP_Z,
                )
                if confirmation.sample_id:
                    break
            if args.save_frames:
                small = cv2.resize(wrist_frame, (ww // 2, wh // 2))
                cv2.imwrite(
                    str(args.out / f"layout_{k:02d}_wrist_{j:02d}.jpg"),
                    small,
                    [cv2.IMWRITE_JPEG_QUALITY, 80],
                )
            world.append(perceived(proposal, confirmation, bench_z=WORKTOP_Z))
            found.append(
                {
                    "xy": list(proposal.xy),
                    "score": proposal.score,
                    "label": proposal.label,
                    "xyxy": [round(v, 1) for v in proposal.bbox.as_tuple()],
                    "confirm": asdict(confirmation),
                    "wrist_views": views,
                }
            )
        t3 = time.perf_counter()
        scored = score(truth(lab), visible, found)
        for bottle in scored["bottles"]:
            bottle["xyxy"] = boxes_of.get(bottle["sample_id"])
        layouts.append(
            {
                "layout": k,
                "x0": x0,
                "proposals": found,
                "world": [asdict(b) for b in world],
                "dashboard": to_dashboard(world),
                "scored": scored,
                "seconds": {"render": t1 - t0, "propose": t2 - t1, "confirm": t3 - t2},
            }
        )
        # Written after every layout, so a long run that dies keeps what it did.
        (args.out / "propose_confirm.json").write_text(
            json.dumps(layouts, indent=1, default=float), encoding="utf-8"
        )
        right = sum(b["correct"] for b in scored["bottles"])
        wrong = sum(b["wrong"] for b in scored["bottles"])
        print(
            f"layout {k}: {len(scored['bottles'])} bottles, {len(found)} proposals, "
            f"{right} named correctly, {wrong} wrongly",
            flush=True,
        )

    report = summarise(layouts, detector.name)
    (args.out / "propose_confirm.json").write_text(
        json.dumps(layouts, indent=1, default=float), encoding="utf-8"
    )
    (args.out / "propose_confirm.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
