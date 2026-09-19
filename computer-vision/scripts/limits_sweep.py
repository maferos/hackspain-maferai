"""Find where a bottle detector breaks: sweep one condition, hold the rest

``viewpoint_study.py`` scores random views. This renders the same bench
layouts again and again while one thing moves, and reports recall and false
boxes at every step, so the answer is a limit: how dark, how near, how far,
how flat a view a detector stands before it drops under a recall.

    python scripts/limits_sweep.py rail --sweeps light,range,elevation
    python scripts/limits_sweep.py runs/orbit/n_all_1280/weights/best.pt \
        --imgsz 1280 --threshold 0.3 --layouts 12

``light``
    The wall mount, the scene's lights at 100 % down to 2 %.
``range``
    The orbit camera 30 degrees above the bench, 0.25 to 3.5 m from its aim.
``elevation``
    The orbit camera 1.5 m from its aim, 10 to 88 degrees above the bench.

Frames are rendered once under ``<out>/sweep_<name>/<level>`` and reused, so
another detector only costs its inference. Output: a Markdown table on stdout
and ``results/limits/<detector>.json``.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import cv2
import mujoco
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fixedcam_dataset as fd  # noqa: E402

from labvision import detector as det  # noqa: E402
from labvision import evaluation as ev  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results" / "limits"
SEED = 2_000_000

SWEEPS: dict[str, tuple[float, ...]] = {
    "light": (1.0, 0.5, 0.3, 0.2, 0.15, 0.1, 0.06, 0.03),
    "range": (0.25, 0.35, 0.5, 0.75, 1.0, 1.5, 2.5, 3.5),
    "elevation": (10.0, 20.0, 30.0, 45.0, 60.0, 75.0, 88.0),
}
"""Levels of each sweep: share of the light, metres, degrees."""
SWEEP_ELEVATION_DEG = 30.0
SWEEP_RANGE_M = 1.5


def render(sweep: str, level: float, layouts: int, out: Path) -> list[dict]:
    """Render ``layouts`` frames at one level; the same layouts at every level"""
    gt_path = out / "gt.json"
    if gt_path.exists():
        frames = json.loads(gt_path.read_text(encoding="utf-8"))["frames"]
        if len(frames) >= layouts:
            return frames[:layouts]
    out.mkdir(parents=True, exist_ok=True)
    scene = fd.SCENES["rail"]
    lab = render.lab = getattr(render, "lab", None) or fd.load_lab(scene)
    m = lab.model
    camera = lab.cameras[fd.CAMERA]
    randomiser = fd.Randomiser(lab, camera)
    frames = []
    for k in range(layouts):
        # One generator for the layout, another for the pose: the bench is the
        # same at every level whatever the camera draws.
        rng = np.random.default_rng(SEED + k)
        randomiser.reset()
        fd.pose_arm(lab, rng, scene)
        fd.lay_out(lab, rng, scene, 24)
        mujoco.mj_kinematics(m, lab.data)
        drawn: dict = {"sweep": sweep, "level": level}
        pose_rng = np.random.default_rng(SEED + 1000 * k + 7)
        if sweep == "light":
            m.light_diffuse[:] *= level
            m.vis.headlight.diffuse[:] *= level
            m.vis.headlight.ambient[:] *= level
        else:
            elevation = level if sweep == "elevation" else SWEEP_ELEVATION_DEG
            reach = level if sweep == "range" else SWEEP_RANGE_M
            drawn["orbit"] = randomiser.orbit(
                pose_rng, scene, (reach, reach), 0.0, (elevation, elevation)
            )
            if drawn["orbit"] is None:
                print(f"  {sweep} {level:g}, layout {k}: no clear pose, skipped")
                continue
        rgb, bottles, _ = lab.render(camera, fd.WIDTH, fd.HEIGHT)
        name = f"{k:03d}.png"
        cv2.imwrite(str(out / name), rgb[:, :, ::-1])
        frames.append({"file": name, "width": fd.WIDTH, "height": fd.HEIGHT,
                       "randomisation": drawn, "bottles": bottles})  # fmt: skip
    randomiser.reset()
    gt_path.write_text(json.dumps({"frames": frames}), encoding="utf-8")
    return frames


def main() -> None:
    """Render the sweeps that are missing and score one detector on them"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("weights", help="backend name or path to weights")
    parser.add_argument("--sweeps", default="light,range,elevation")
    parser.add_argument("--layouts", type=int, default=12)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--imgsz", type=int, default=None, help="default: native")
    parser.add_argument("--out", type=Path, default=fd.DEFAULT_OUT)
    parser.add_argument("--name", default=None, help="results file name")
    args = parser.parse_args()
    from ultralytics import YOLO

    weights, backend_threshold = det.resolve(args.weights)
    threshold = args.threshold or backend_threshold or 0.25
    name = args.name or (
        args.weights if backend_threshold else Path(args.weights).parent.parent.name
    )
    model = YOLO(weights)
    report: dict[str, list[dict]] = {}
    for sweep in args.sweeps.split(","):
        report[sweep] = []
        for level in SWEEPS[sweep]:
            folder = args.out / f"sweep_{sweep}" / f"{level:g}"
            frames = render(sweep, level, args.layouts, folder)
            results, heights = [], []
            for frame in frames:
                image = cv2.imread(str(folder / frame["file"]))
                size = args.imgsz or math.ceil(max(image.shape[:2]) / 32) * 32
                out = model.predict(image, imgsz=size, conf=0.01, max_det=300,
                                    verbose=False)[0]  # fmt: skip
                dets = [
                    ev.Detection(tuple(box), score)
                    for box, score in zip(out.boxes.xyxy.tolist(),
                                          out.boxes.conf.tolist(), strict=True)
                ]  # fmt: skip
                result = ev.match_frame(ev.truths_of(frame), dets)
                results.append(result)
                heights += [t.full_box[3] - t.full_box[1] for t in result.truths]
            point = ev.operating_point(results, threshold)
            report[sweep].append({
                "level": level,
                "frames": len(frames),
                "bottles": point["required"],
                "median_height_px": float(np.median(heights)) if heights else None,
                "recall": point["recall"],
                "false_per_frame": point["false_per_frame"],
            })  # fmt: skip
            print(f"  {sweep} {level:g}: recall {point['recall']:.3f}", file=sys.stderr)

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{name}.json").write_text(json.dumps(report, indent=1))
    print(f"\n### {name}, threshold {threshold:g}, {args.layouts} layouts a level\n")
    print("| sweep | level | frames | bottles | median height | recall | false/frame |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for sweep, rows in report.items():
        for r in rows:
            height = f"{r['median_height_px']:.0f} px" if r["bottles"] else "-"
            recall = f"{r['recall']:.3f}" if r["bottles"] else "-"
            print(f"| {sweep} | {r['level']:g} | {r['frames']} | {r['bottles']} | "
                  f"{height} | {recall} | {r['false_per_frame']:.2f} |")  # fmt: skip


if __name__ == "__main__":
    main()
