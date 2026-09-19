"""Measure how often the wrist camera names the bottles it sees, and how

Takes wrist frames rendered by ``render_perfumery.py`` (every sample bottle
carries its ArUco ring) and, for every bench bottle a detector should find ---
at least half visible, not cut by the frame border --- asks whether its
``marker_id`` was read *on that bottle* by:

``whole``
    :func:`labvision.identify.identify_frame` on the whole frame, no detector.
    The read counts for a bottle when the markers of its id lie on it.
``<backend>``
    A detector's boxes (above its threshold) and :func:`labvision.identify.identify`
    in each. The read counts when a box matching the bottle (IoU 0.5 with its
    visible box) names it.
``oracle`` / ``oracle_x1``
    :func:`labvision.identify.identify` in the true visible boxes: the ceiling a
    perfect detector would give, with the enlargement ladder and without it.

It also counts what goes wrong: a box or a whole-frame read naming a sample
that is not the bottle under it (**wrong**), and an id no bottle in view
carries (**phantom**). A wrong id is a wrong bottle in the gripper, so it
matters more than a miss.

Detections are cached next to the frames, the way ``perfumery_eval.py`` and
``world_prompts.py`` cache them, so rerunning only rescores.

    python scripts/wrist_identify_bench.py ../simulation/out/wrist_v1
    python scripts/wrist_identify_bench.py ../simulation/out/wrist_v1 --backends coco

Writes ``wrist_identify.json`` and ``wrist_identify.md`` next to the frames.
"""

import argparse
import json
import math
import sys
import time
from collections import defaultdict
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from perfumery_eval import iou, is_required, kind  # noqa: E402

from labvision import registry  # noqa: E402
from labvision.identify import (  # noqa: E402
    DEFAULT_TABLE,
    MarkerReader,
    identify,
    identify_frame,
    rows_by_marker,
)
from labvision.perception import ring_geometry  # noqa: E402
from labvision.scene import BBox  # noqa: E402

WORLD_THRESHOLD = 0.11
"""YOLO-World's threshold in the detector; its cached boxes go down to 0.03."""
BACKENDS = {
    "world-b": ("world_prompts", "bottles"),
    "world": ("world_prompts", "current"),
    "coco": ("detect_all", "coco"),
}
"""Name: how its boxes are made. ``world-b`` is YOLO-World with the bottle
prompts that won the vocabulary experiment; ``world`` its current prompts."""
DISTANCE_EDGES_M = (0.4, 0.6, 0.8)


def distance_bucket(metres: float) -> str:
    """Label a camera-to-bottle distance by :data:`DISTANCE_EDGES_M`"""
    lo = None
    for edge in DISTANCE_EDGES_M:
        if metres < edge:
            return f"< {edge:.1f} m" if lo is None else f"{lo:.1f}-{edge:.1f} m"
        lo = edge
    return f">= {lo:.1f} m"


def distance_labels() -> list[str]:
    """Every distance bucket, nearest first"""
    edges = DISTANCE_EDGES_M
    middle = [f"{a:.1f}-{b:.1f} m" for a, b in zip(edges, edges[1:], strict=False)]
    return [f"< {edges[0]:.1f} m", *middle, f">= {edges[-1]:.1f} m"]


ELEVATION_EDGES_DEG = (15, 30, 45, 60)
"""The ring is read from its side: how high above it the camera is matters more
than how far, so reads are also tallied by the camera's elevation over it."""


def elevation_deg(camera_position, ring_centre) -> float:
    """Degrees the camera stands above the horizontal through the ring's centre"""
    dx, dy, dz = (
        float(c) - float(r) for c, r in zip(camera_position, ring_centre, strict=True)
    )
    return math.degrees(math.atan2(dz, math.hypot(dx, dy)))


def elevation_bucket(degrees: float) -> str:
    """Label an elevation by :data:`ELEVATION_EDGES_DEG`"""
    lo = None
    for edge in ELEVATION_EDGES_DEG:
        if degrees < edge:
            return f"< {edge} deg" if lo is None else f"{lo}-{edge} deg"
        lo = edge
    return f">= {lo} deg"


def elevation_labels() -> list[str]:
    """Every elevation bucket, lowest first"""
    edges = ELEVATION_EDGES_DEG
    middle = [f"{a}-{b} deg" for a, b in zip(edges, edges[1:], strict=False)]
    return [f"< {edges[0]} deg", *middle, f">= {edges[-1]} deg"]


def boxes_of(backend: str, folder: Path, frames: list[dict], device) -> dict:
    """Every frame's detector boxes for a backend, from cache or by running it"""
    how, name = BACKENDS[backend]
    if how == "world_prompts":
        import perfumery_eval
        import world_prompts

        # run_variant trusts any cache it finds; frames re-rendered into the
        # same folder would be scored against the old boxes, so the frames a
        # cache was made for are stamped beside it and checked here.
        cache = folder / "world_prompts" / f"{world_prompts.slug(name)}.json"
        stamp_file = cache.with_suffix(".frames.json")
        stamp = perfumery_eval.frame_stamp(folder, frames)
        if cache.exists() and (
            not stamp_file.exists()
            or json.loads(stamp_file.read_text(encoding="utf-8")) != stamp
        ):
            print(f"{cache.name} is from other frames, running {backend} again")
            cache.unlink()
        found = world_prompts.run_variant(
            name, folder, frames, folder / "world_prompts", device
        )
        stamp_file.write_text(json.dumps(stamp), encoding="utf-8")
        return {
            f: [b for b in v["boxes"] if b["score"] > WORLD_THRESHOLD]
            for f, v in found.items()
            if isinstance(v, dict) and "boxes" in v
        }
    import perfumery_eval

    class Args:
        redo = False

    Args.device = device
    found = perfumery_eval.detect_all(name, folder, frames, Args)
    return {
        f: v["boxes"] for f, v in found.items() if isinstance(v, dict) and "boxes" in v
    }


def on_bottle(identity_box: BBox, bottle: dict) -> bool:
    """Whether a whole-frame read's markers lie on a bottle's silhouette"""
    u0, v0, u1, v1 = bottle["full_xyxy"]
    cu = (identity_box.u_min + identity_box.u_max) / 2
    cv = (identity_box.v_min + identity_box.v_max) / 2
    return u0 <= cu <= u1 and v0 <= cv <= v1


def score_frame(frame: dict, identities: list, marker_of: dict, whole: bool) -> dict:
    """Which required bottles were named, and how many reads were wrong or phantom

    Args:
        frame: One ``gt.json`` frame.
        identities: What one method read in it.
        marker_of: Marker id by sample id.
        whole: True if the identities come from a whole-frame read, whose boxes
            are marker bounds rather than bottle boxes.
    """
    bottles = frame["bottles"]
    in_view = {marker_of[b["sample_id"]] for b in bottles}
    named: set[int] = set()
    wrong = phantom = 0
    for identity in identities:
        if identity.marker_id is None:
            continue
        if identity.marker_id not in in_view:
            phantom += 1
            continue
        if whole:
            under = [b for b in bottles if on_bottle(identity.bbox, b)]
        else:
            box = identity.bbox.as_tuple()
            best = max(bottles, key=lambda b: iou(box, b["xyxy"]), default=None)
            under = [best] if best and iou(box, best["xyxy"]) >= 0.5 else []
        right = [
            i
            for i, b in enumerate(bottles)
            if any(b is u for u in under)
            and marker_of[b["sample_id"]] == identity.marker_id
        ]
        named.update(right)
        if under and not right:
            wrong += 1
    required = [
        i for i, b in enumerate(bottles) if b.get("where") == "bench" and is_required(b)
    ]
    return {
        "required": required,
        "named": [i for i in required if i in named],
        "wrong": wrong,
        "phantom": phantom,
    }


def run(folder: Path, backends: list[str], device) -> dict:
    """Read every frame every way, then tally per method, distance, elevation, bottle"""
    gt = json.loads((folder / "gt.json").read_text(encoding="utf-8"))
    frames = gt["frames"]
    table = registry.load_table(DEFAULT_TABLE)
    rows = rows_by_marker(table)
    marker_of = {row["sample_id"]: int(row["marker_id"]) for row in table.values()}
    vessel_of = {row["sample_id"]: row["vessel_class"] for row in table.values()}
    detections = {b: boxes_of(b, folder, frames, device) for b in backends}
    reader = MarkerReader()

    methods = ["whole", *backends, "oracle", "oracle_x1"]
    tally = {
        m: {
            "required": 0,
            "named": 0,
            "wrong": 0,
            "phantom": 0,
            "seconds": 0.0,
            "by_distance": defaultdict(lambda: [0, 0]),
            "by_elevation": defaultdict(lambda: [0, 0]),
            "by_kind": defaultdict(lambda: [0, 0]),
        }
        for m in methods
    }
    for k, frame in enumerate(frames):
        image = cv2.imread(str(folder / frame["file"]))
        truth_boxes = [BBox(*b["xyxy"]) for b in frame["bottles"] if is_required(b)]
        for method in methods:
            start = time.perf_counter()
            if method == "whole":
                found = identify_frame(image, rows, reader=reader)
            elif method == "oracle":
                found = identify(image, truth_boxes, rows, reader=reader)
            elif method == "oracle_x1":
                found = identify(image, truth_boxes, rows, reader=reader, scales=(1.0,))
            else:
                boxes = [BBox(*b["xyxy"]) for b in detections[method][frame["file"]]]
                found = identify(image, boxes, rows, reader=reader)
            seconds = time.perf_counter() - start
            result = score_frame(frame, found, marker_of, method == "whole")
            t = tally[method]
            t["seconds"] += seconds
            t["wrong"] += result["wrong"]
            t["phantom"] += result["phantom"]
            for i in result["required"]:
                bottle = frame["bottles"][i]
                hit = i in result["named"]
                t["required"] += 1
                t["named"] += hit
                t["by_distance"][distance_bucket(bottle["distance_m"])][0] += hit
                t["by_distance"][distance_bucket(bottle["distance_m"])][1] += 1
                _, ring_height = ring_geometry(vessel_of[bottle["sample_id"]])
                x, y, z = bottle["position"]
                up = elevation_deg(frame["cam_pos"], (x, y, z + ring_height))
                t["by_elevation"][elevation_bucket(up)][0] += hit
                t["by_elevation"][elevation_bucket(up)][1] += 1
                t["by_kind"][kind(bottle)][0] += hit
                t["by_kind"][kind(bottle)][1] += 1
        print(f"{k + 1}/{len(frames)} {frame['file']}", flush=True)
    for t in tally.values():
        t["seconds_per_frame"] = t.pop("seconds") / max(len(frames), 1)
        t["by_distance"] = dict(t["by_distance"])
        t["by_elevation"] = dict(t["by_elevation"])
        t["by_kind"] = dict(t["by_kind"])
    return {"frames": len(frames), "methods": tally}


def to_markdown(result: dict) -> str:
    """Tables per method: overall, by distance, by elevation, by bottle"""

    def pct(pair):
        named, required = pair
        return (
            f"{100 * named / required:.0f} % ({named}/{required})" if required else "-"
        )

    methods = result["methods"]
    names = list(methods)
    lines = [
        f"# Wrist identification, {result['frames']} frames",
        "",
        "| method | named | wrong ids | phantom ids | ms/frame (reading only) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for name, t in methods.items():
        lines.append(
            f"| {name} | {pct((t['named'], t['required']))} | {t['wrong']} | "
            f"{t['phantom']} | {1000 * t['seconds_per_frame']:.0f} |"
        )
    lines += ["", "| distance | " + " | ".join(names) + " |"]
    lines.append("| --- |" + " --- |" * len(names))
    for label in distance_labels():
        cells = [pct(methods[n]["by_distance"].get(label, (0, 0))) for n in names]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    lines += ["", "| elevation over the ring | " + " | ".join(names) + " |"]
    lines.append("| --- |" + " --- |" * len(names))
    for label in elevation_labels():
        cells = [
            pct(methods[n].get("by_elevation", {}).get(label, (0, 0))) for n in names
        ]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    kinds = sorted({k for t in methods.values() for k in t["by_kind"]})
    lines += ["", "| bottle | " + " | ".join(names) + " |"]
    lines.append("| --- |" + " --- |" * len(names))
    for label in kinds:
        cells = [pct(methods[n]["by_kind"].get(label, (0, 0))) for n in names]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    """Read, score and report"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("folder", type=Path)
    parser.add_argument(
        "--backends", nargs="*", default=list(BACKENDS), choices=list(BACKENDS)
    )
    parser.add_argument("--device", default=None)
    args = parser.parse_args()
    result = run(args.folder, args.backends, args.device)
    report = to_markdown(result)
    (args.folder / "wrist_identify.json").write_text(
        json.dumps(result, indent=1), encoding="utf-8"
    )
    (args.folder / "wrist_identify.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
