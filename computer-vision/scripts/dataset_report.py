"""Check a rendered fixedcam dataset and build what its review page shows

Reads every split's ``gt.json`` under SRC and every frame's PNG, and writes to
OUT:

``data.json``
    Totals per split and family, per-frame rows (camera angle, distance, field
    of view, labelled vials, flags), histograms, the camera-angle coverage grid
    and the list of flagged frames.
``sprites/sNNN.jpg``
    Every frame as a 192 x 108 thumbnail, 100 to a sheet in frame order, a
    green dot on every labelled vial and, in orange, the bench crop the model is
    trained and run on (``bench_crop.py``).
``samples/*.jpg``
    A seeded random sample of training frames, cropped and labelled exactly as
    training will see them, at a size where labels can be checked: a
    fixed-camera band at full resolution, anything taller at 1280 px wide.
    Every flagged frame is added to it.

A vial is labelled when at least ``MIN_VISIBLE`` of it shows, as in
``fixedcam_to_yolo.py``. Flags: no labelled vial left in the crop; a flat
frame (the lens inside something); an orbit frame that fell back to the wall
camera; a bench vial the crop cuts below ``bench_crop.KEEP`` of its box.

    python dataset_report.py /workspace/fixedcam /root/out/report [--workers 16]
"""

import argparse
import json
import math
import random
import sys
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bench_crop import bench_crop, crop_labels  # noqa: E402
from fixedcam_crops import MIN_VISIBLE  # noqa: E402

THUMB_W, THUMB_H, SHEET_COLS, SHEET = 192, 108, 10, 100
HEIGHT_BINS = (0, 12, 20, 32, 64, 96, 160, 100_000)
ELEV_BANDS = (10, 20, 30, 40, 50, 60, 70, 80, 90)
AZ_SECTORS = 12
SAMPLES = {"rail": 40, "orbit": 50, "close": 30, "low": 20}
STYLES = ("scatter", "cluster", "as built", "clusters", "rows", "crowd")
"""Bench layouts a frame can carry in ``randomisation.layout.style``: the
renderer's own first, then ``bottle_patterns``'; a row stores the index."""
FLAT_STD = 6.0


def family(split: str) -> str:
    """rail, orbit or close: which camera a split's frames come from

    ``dark_test`` is the wall camera dimmed and ``overhead_test`` the orbit
    camera from above, so they go with the camera, not their first word.
    """
    named = {"pattern_test": "rail", "pattern_orbit_test": "orbit",
             "lab_test": "orbit", "lab_rail_test": "rail"}  # fmt: skip
    head = split.split("_")[0]
    return named.get(split, {"dark": "rail", "overhead": "orbit"}.get(head, head))


def camera(frame: dict) -> tuple[np.ndarray, np.ndarray]:
    """World position and rotation (columns: right, up, back) of a frame's camera"""
    return np.array(frame["cam_pos"], float), np.array(
        frame["cam_xmat"], float
    ).reshape(3, 3)


def view_angles(frame: dict) -> tuple[float, float, float]:
    """Elevation above the bench, bearing of the camera from what it looks at, range

    Elevation and bearing come from the viewing direction, so they mean the
    same for the wall camera and the orbit camera. Range is to where the
    optical axis meets the bench top.
    """
    pos, rot = camera(frame)
    look = -rot[:, 2]
    elevation = math.degrees(math.asin(max(-1.0, min(1.0, -look[2]))))
    azimuth = math.degrees(math.atan2(-look[1], -look[0])) % 360
    reach = (pos[2] - 0.90) / max(-look[2], 1e-6)
    return elevation, azimuth, reach


def labelled(frame: dict) -> list[dict]:
    """The vials a frame teaches: at least MIN_VISIBLE of them in view"""
    return [
        b for b in frame["bottles"] if b["visible_frac"] >= MIN_VISIBLE and b["pixels"]
    ]


def sheet_job(args: tuple) -> list[tuple[str, float]]:
    """Build one sprite sheet; return each frame's grey-level spread"""
    index, items, out = args
    sheet = np.zeros((THUMB_H * SHEET // SHEET_COLS, THUMB_W * SHEET_COLS, 3), np.uint8)
    spread = []
    for slot, (folder, frame, crop) in enumerate(items):
        image = cv2.imread(str(Path(folder) / frame["file"]))
        spread.append(
            (frame["file"], float(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).std()))
        )
        sx, sy = THUMB_W / frame["width"], THUMB_H / frame["height"]
        thumb = cv2.resize(image, (THUMB_W, THUMB_H), interpolation=cv2.INTER_AREA)
        if tuple(crop) != (0, 0, frame["width"], frame["height"]):
            x0, y0, x1, y1 = crop
            cv2.rectangle(
                thumb,
                (int(x0 * sx), int(y0 * sy)),
                (min(THUMB_W - 1, int(x1 * sx)), min(THUMB_H - 1, int(y1 * sy))),
                (40, 140, 255),
                1,
            )
        for b in labelled(frame):
            x0, y0, x1, y1 = b["xyxy"]
            centre = (int((x0 + x1) / 2 * sx), int((y0 + y1) / 2 * sy))
            radius = max(2, int(max(x1 - x0, y1 - y0) * sx / 2))
            cv2.circle(thumb, centre, radius, (40, 230, 60), -1 if radius <= 2 else 1)
        r, c = divmod(slot, SHEET_COLS)
        sheet[r * THUMB_H : (r + 1) * THUMB_H, c * THUMB_W : (c + 1) * THUMB_W] = thumb
    cv2.imwrite(
        str(Path(out) / f"s{index:03d}.jpg"), sheet, [cv2.IMWRITE_JPEG_QUALITY, 72]
    )
    return spread


def sample_job(args: tuple) -> str:
    """Write one sample frame with its labels drawn, at a checkable size"""
    folder, frame, crop, out = args
    image = cv2.imread(str(Path(folder) / frame["file"]))
    x0, y0, x1, y1 = crop
    image = np.ascontiguousarray(image[y0:y1, x0:x1])
    # Exactly the labels training will see: moved into the crop, slivers dropped.
    boxes = crop_labels([tuple(b["xyxy"]) for b in labelled(frame)], crop)
    thick = 2 if image.shape[1] <= 1280 * 1.2 and image.shape[0] < 600 else 3
    for bx0, by0, bx1, by1 in boxes:
        cv2.rectangle(
            image,
            (int(bx0) - 2, int(by0) - 2),
            (int(bx1) + 2, int(by1) + 2),
            (40, 230, 60),
            thick,
        )
    name = frame["file"][:-4] + ".jpg"
    # A fixed-camera band stays at full resolution, where a 14 px vial can be
    # checked; anything taller is brought down to 1280 px wide.
    if image.shape[0] > 600 and image.shape[1] > 1280:
        scale = 1280 / image.shape[1]
        image = cv2.resize(
            image, (1280, round(image.shape[0] * scale)), interpolation=cv2.INTER_AREA
        )
    cv2.imwrite(str(Path(out) / name), image, [cv2.IMWRITE_JPEG_QUALITY, 84])
    return name


def main() -> None:
    """Check every split and write the review data"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("src", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()
    (args.out / "sprites").mkdir(parents=True, exist_ok=True)
    (args.out / "samples").mkdir(parents=True, exist_ok=True)

    order = [
        "rail_train",
        "rail_val",
        "rail_test",
        "rail_test_shift",
        "orbit_train",
        "orbit_val",
        "orbit_test",
        "close_train",
        "close_val",
        "close_test",
    ]
    splits = [s for s in order if (args.src / s / "gt.json").exists()]
    splits += sorted(
        p.parent.name for p in args.src.glob("*/gt.json") if p.parent.name not in splits
    )
    frames, rows, flagged = [], [], []
    summary: dict = {"splits": {}, "families": {}}
    heights: dict[str, list[int]] = {}
    for split_id, split in enumerate(splits):
        gt = json.loads((args.src / split / "gt.json").read_text())
        fam = family(split)
        heights.setdefault(fam, [])
        boxes = empty = fallback = cut = lost = pixels = 0
        for frame in gt["frames"]:
            vials = labelled(frame)
            crop = bench_crop(frame)
            kept = crop_labels([tuple(b["xyxy"]) for b in vials], crop)
            elevation, azimuth, reach = view_angles(frame)
            orbit = frame["randomisation"].get("orbit")
            flags = []
            if not kept:
                flags.append("empty")
                empty += 1
            if fam != "rail" and not orbit:
                flags.append("fallback")
                fallback += 1
            x0, y0, x1, y1 = crop
            bench = [b for b in vials if b["where"] == "bench"]
            outside = [
                b
                for b in bench
                if not (
                    x0 <= b["xyxy"][0]
                    and y0 <= b["xyxy"][1]
                    and b["xyxy"][2] <= x1
                    and b["xyxy"][3] <= y1
                )
            ]
            dropped = len(bench) - len(
                crop_labels([tuple(b["xyxy"]) for b in bench], crop)
            )
            cut += len(outside)
            lost += dropped
            if dropped:
                flags.append("lost")
            boxes += len(kept)
            pixels += (x1 - x0) * (y1 - y0) / (frame["width"] * frame["height"])
            heights[fam] += [round(b[3] - b[1]) for b in kept]
            frames.append((str(args.src / split), frame, crop))
            layout = frame["randomisation"].get("layout", {})
            rows.append(
                [
                    split_id,
                    int(frame["file"].rsplit("_", 1)[1][:-4]),
                    round(elevation, 1),
                    round(azimuth, 1),
                    round(reach, 2),
                    round(frame["fovy_deg"], 1),
                    len(kept),
                    int(frame["as_built"]),
                    int("degrade" in frame["randomisation"]),
                    int("dark" in frame["randomisation"]),
                    *crop,
                    STYLES.index(layout.get("style", "scatter")),
                    int("lab" in frame["randomisation"]),
                ]
            )
            if flags:
                flagged.append({"file": frame["file"], "flags": flags})
        count = len(gt["frames"])
        summary["splits"][split] = {
            "frames": count,
            "boxes": boxes,
            "empty": empty,
            "fallback": fallback,
            "cut": cut,
            "lost": lost,
            "crop_share": round(pixels / max(count, 1), 3),
        }
        print(
            f"{split}: {count} frames, {boxes} vials, {empty} empty, {fallback} "
            f"fallback, {cut} bench vials cut by the crop, {lost} lost, crop "
            f"{pixels / max(count, 1):.0%} of the frame",
            flush=True,
        )

    # Sprite sheets, in parallel; they also measure how flat each frame is.
    jobs = [
        (i // SHEET, frames[i : i + SHEET], str(args.out / "sprites"))
        for i in range(0, len(frames), SHEET)
    ]
    with Pool(args.workers) as pool:
        spread = dict(s for sheet in pool.imap(sheet_job, jobs) for s in sheet)
    flat = {f for f, s in spread.items() if s < FLAT_STD}
    for f in sorted(flat):
        entry = next((e for e in flagged if e["file"] == f), None)
        if entry:
            entry["flags"].append("flat")
        else:
            flagged.append({"file": f, "flags": ["flat"]})

    # A seeded sample per family, plus every flagged frame.
    rng = random.Random(7)
    picked = []
    for fam, count in SAMPLES.items():
        pool_frames = [
            f
            for f in frames
            if family(Path(f[0]).name) == fam and Path(f[0]).name.endswith("train")
        ]
        picked += rng.sample(pool_frames, min(count, len(pool_frames)))
    names = {e["file"] for e in flagged}
    picked += [f for f in frames if f[1]["file"] in names and f not in picked][:30]
    with Pool(args.workers) as pool:
        written = pool.map(
            sample_job, [(*f, str(args.out / "samples")) for f in picked]
        )

    for fam, values in heights.items():
        h = np.array(values)
        summary["families"][fam] = {
            "frames": sum(
                summary["splits"][s]["frames"] for s in splits if family(s) == fam
            ),
            "boxes": int(len(h)),
            "height_hist": [
                int(((h >= lo) & (h < hi)).sum())
                for lo, hi in zip(HEIGHT_BINS, HEIGHT_BINS[1:], strict=False)
            ],
            "height_p": [float(np.percentile(h, p)) for p in (5, 50, 95)]
            if len(h)
            else [],
        }
    # Camera-angle coverage of the training frames: elevation band x bearing sector.
    grid = {}
    for row in rows:
        split = splits[row[0]]
        if not split.endswith("train"):
            continue
        fam = family(split)
        if row[2] < ELEV_BANDS[0]:
            e = -1
        else:
            e = min(len(ELEV_BANDS) - 2, int((row[2] - ELEV_BANDS[0]) // 10))
            e = max(e, 0)
        a = int(row[3] // (360 / AZ_SECTORS)) % AZ_SECTORS
        grid.setdefault(fam, np.zeros((len(ELEV_BANDS) - 1, AZ_SECTORS), int))
        if e >= 0:
            grid[fam][e, a] += 1
    summary["coverage"] = {k: v.tolist() for k, v in grid.items()}
    summary["flat"] = len(flat)
    data = {
        "summary": summary,
        "splits": splits,
        "columns": [
            "split",
            "k",
            "elev",
            "az",
            "range",
            "fovy",
            "vials",
            "as_built",
            "degraded",
            "dark",
            "crop_x0",
            "crop_y0",
            "crop_x1",
            "crop_y1",
            "style",
            "lab",
        ],
        "styles": STYLES,
        "rows": rows,
        "flagged": flagged,
        "samples": sorted(written),
        "sheet": {"w": THUMB_W, "h": THUMB_H, "cols": SHEET_COLS, "per": SHEET},
        "height_bins": list(HEIGHT_BINS),
        "elev_bands": list(ELEV_BANDS),
        "az_sectors": AZ_SECTORS,
    }
    (args.out / "data.json").write_text(json.dumps(data, separators=(",", ":")))
    print(
        f"{len(frames)} frames, {len(jobs)} sheets, {len(written)} samples, "
        f"{len(flagged)} flagged ({len(flat)} flat)"
    )


if __name__ == "__main__":
    main()
