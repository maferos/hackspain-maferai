"""Build the per-frame and per-vial tables ``demo_figures_detail.py`` draws from

Needs the rendered sets' ``gt.json`` and the boxes ``viewpoint_study.py`` cached for
the three detectors; writes ``docs/demo/numbers/{frames,test_vials,
test_false_boxes}.csv``, ``vials.json`` and ``tests.json``.
"""

import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from labvision import evaluation as ev  # noqa: E402

if len(sys.argv) != 5:
    sys.exit(
        "usage: demo_tables.py FRAMES RAIL_BOXES E25_BOXES E100_BOXES, where "
        "FRAMES holds one folder a rendered set and *_BOXES are "
        "viewpoint_study.py's result folders"
    )
GT = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1] / "docs" / "demo" / "numbers"
MODELS = dict(
    zip(("rail", "25_epochs", "100_epochs"), map(Path, sys.argv[2:5]), strict=True)
)
NAMED = {
    "pattern_test": "rail",
    "pattern_orbit_test": "orbit",
    "lab_test": "orbit",
    "lab_rail_test": "rail",
    "dark_test": "rail",
    "orbit_dark_test": "orbit",
    "overhead_test": "orbit",
}


def family(split):
    """The camera family a set belongs to"""
    return NAMED.get(split, split.split("_")[0])


def role(split):
    """What a set is used for"""
    return (
        "train"
        if split.endswith("_train")
        else "val"
        if split.endswith("_val")
        else "test"
    )


def pose(frame, gt):
    """Elevation, bearing and distance of a frame's camera from the bench centre"""
    orbit = frame["randomisation"].get("orbit")
    if orbit:
        return orbit["elevation_deg"], orbit["azimuth_deg"] % 360, orbit["range_m"]
    x, y, z = frame["cam_pos"]
    dx, dy = x - gt["bench_centre"][0], y - gt["bench_centre"][1]
    dz = z - gt["worktop_z"]
    flat = math.hypot(dx, dy)
    return (
        math.degrees(math.atan2(dz, flat)),
        math.degrees(math.atan2(dy, dx)) % 360,
        math.hypot(flat, dz),
    )


# select_frames.py leaves the frames it kept in sel_train.
selected = set()
for name in ("sel_train",):
    path = GT / name / "gt.json"
    if path.exists():
        selected = {
            f["file"] for f in json.loads(path.read_text(encoding="utf-8"))["frames"]
        }

frames_rows, heights, bench_xy = [], {}, []
HEIGHT_EDGES = [0, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 160, 200, 260, 400]
splits = sorted(
    p.parent.name for p in GT.glob("*/gt.json") if not p.parent.name.startswith("sel_")
)
for split in splits:
    gt = json.loads((GT / split / "gt.json").read_text(encoding="utf-8"))
    for frame in gt["frames"]:
        elevation, bearing, reach = pose(frame, gt)
        rnd = frame["randomisation"]
        light = (rnd.get("light") or [1.0])[0]
        dark = rnd.get("dark")
        labelled = [
            b for b in frame["bottles"] if b["visible_frac"] >= 0.3 and b["pixels"]
        ]
        frames_rows.append(
            [
                split,
                family(split),
                role(split),
                round(elevation, 1),
                round(bearing, 1),
                round(reach, 2),
                len(labelled),
                rnd.get("layout", {}).get("style", "scatter"),
                int("lab" in rnd),
                round(light * (dark or 1.0), 3),
                int(dark is not None),
                int("degrade" in rnd),
                int(frame["file"] in selected),
            ]
        )
        h = heights.setdefault(family(split), np.zeros(len(HEIGHT_EDGES) - 1, int))
        for b in labelled:
            x0, y0, x1, y1 = b["full_xyxy"]
            h[min(np.searchsorted(HEIGHT_EDGES, y1 - y0, "right") - 1, len(h) - 1)] += 1
            if b["where"] == "bench" and role(split) == "train":
                bench_xy.append(b["position"][:2])

with (OUT / "frames.csv").open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(
        [
            "split",
            "camera",
            "use",
            "elevation_deg",
            "bearing_deg",
            "range_m",
            "vials",
            "bench",
            "lab_varied",
            "light",
            "dark",
            "degraded",
            "selected_for_training",
        ]
    )
    writer.writerows(frames_rows)
xy = np.array(bench_xy)
grid, xe, ye = np.histogram2d(
    xy[:, 0], xy[:, 1], bins=[60, 20], range=[[-4.5, 1.5], [-1.4, 0.6]]
)
(OUT / "vials.json").write_text(
    json.dumps(
        {
            "height_edges_px": HEIGHT_EDGES,
            "heights_by_camera": {k: v.tolist() for k, v in heights.items()},
            "bench_positions_training": {
                "x_edges": xe.round(3).tolist(),
                "y_edges": ye.round(3).tolist(),
                "counts": grid.astype(int).tolist(),
            },
        }
    )
)

# Every required vial of every test, and the score each detector found it at.
tests = [s for s in splits if role(s) == "test"]
vial_rows, false_rows = [], []
for test in tests:
    gt = json.loads((GT / test / "gt.json").read_text(encoding="utf-8"))
    boxes = {
        m: json.loads((folder / f"{test}.boxes.json").read_text())
        for m, folder in MODELS.items()
    }
    for frame in gt["frames"]:
        truths = ev.truths_of(frame)
        required = [t for t in truths if t.required]
        bottles = [b for b in frame["bottles"] if ev.is_required(b)]
        assert len(bottles) == len(required), (test, frame["file"])
        found = {}
        for m in MODELS:
            dets = [ev.Detection(tuple(b[:4]), b[4]) for b in boxes[m][frame["file"]]]
            result = ev.match_frame(truths, dets)
            assert len(result.found) == len(required)
            found[m] = result.found
            false_rows += [
                [test, frame["file"], m, round(d.score, 4)]
                for d in result.false_boxes
                if d.score >= 0.05
            ]
        elevation, bearing, reach = pose(frame, gt)
        rnd = frame["randomisation"]
        light = (rnd.get("light") or [1.0])[0] * (rnd.get("dark") or 1.0)
        for i, (t, b) in enumerate(zip(required, bottles, strict=True)):
            w, h = frame["width"], frame["height"]
            cx, cy = (t.box[0] + t.box[2]) / 2, (t.box[1] + t.box[3]) / 2
            vial_rows.append(
                [
                    test,
                    frame["file"],
                    round(t.full_box[3] - t.full_box[1]),
                    round(b["visible_frac"], 3),
                    round(elevation, 1),
                    round(bearing, 1),
                    round(reach, 2),
                    round(light, 3),
                    rnd.get("layout", {}).get("style", "scatter"),
                    int("lab" in rnd),
                    len(required),
                    round(
                        math.hypot(cx - w / 2, cy - h / 2) / math.hypot(w / 2, h / 2), 3
                    ),
                    *(
                        "" if found[m][i] is None else round(found[m][i], 4)
                        for m in MODELS
                    ),
                ]
            )
with (OUT / "test_vials.csv").open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(
        [
            "test",
            "frame",
            "height_px",
            "visible",
            "elevation_deg",
            "bearing_deg",
            "range_m",
            "light",
            "bench",
            "lab_varied",
            "vials_in_frame",
            "off_centre",
            *(f"score_{m}" for m in MODELS),
        ]
    )
    writer.writerows(vial_rows)
with (OUT / "test_false_boxes.csv").open("w", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["test", "frame", "model", "score"])
    writer.writerows(false_rows)
frames_per_test = {
    t: len(json.loads((GT / t / "gt.json").read_text(encoding="utf-8"))["frames"])
    for t in tests
}
(OUT / "tests.json").write_text(
    json.dumps({"frames_per_test": frames_per_test}, indent=1)
)
print(
    len(frames_rows),
    "frames,",
    len(vial_rows),
    "test vials,",
    len(false_rows),
    "false boxes,",
    sum(r[-1] for r in frames_rows),
    "selected",
)
for p in sorted(OUT.iterdir()):
    print(f"  {p.name}: {p.stat().st_size // 1024} KB")
