"""Select the training set from the rendered splits: even over camera poses

The render holds 7,500 training frames; training on all of them spends most of
its time on poses it has many of. This keeps every camera pose the render
covers and caps the crowded ones (``docs/YOLO26_TRAINING.md``):

- no dark frames: they stay in ``dark_test`` and ``orbit_dark_test``;
- wall mount: the first ``RAIL_TRAIN`` frames of ``rail_train`` by seed, and the
  first ``RAIL_VAL`` of ``rail_val``;
- orbit, close and low views together, on a grid of :data:`ELEVATION_DEG` by
  :data:`RANGE_M`: at most ``CELL_CAP`` frames a cell, taken round-robin over
  twelve 30-degree bearings, by seed within a bearing, so a capped cell still
  looks at the bench from all round;
- validation: every frame of ``orbit_val``, ``close_val`` and ``low_val`` that is
  not dark.

    python scripts/select_frames.py --src DIR [--out DIR] [--no-link]

Writes ``<out>/sel_train`` and ``<out>/sel_val``, each a ``gt.json`` in the
renderer's format and hard links to the frames it lists, so
``fixedcam_to_yolo.py sel_train:train sel_val:val --crop`` runs unchanged, and
``<out>/selection.json`` with the count of every cell. The same render always
gives the same selection. ``--no-link`` writes the lists alone, for a machine
that holds the labels and not the images.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixedcam_dataset import DEFAULT_OUT  # noqa: E402

ELEVATION_DEG = (15.0, 30.0, 45.0, 60.0, 75.0, 88.0)
RANGE_M = (0.35, 0.6, 1.0, 1.75, 2.5, 3.5)
BEARINGS = 12
CELL_CAP = 200
RAIL_TRAIN = 2000
RAIL_VAL = 200
VIEW_SPLITS = ("orbit", "close", "low")
"""The splits whose camera stands anywhere; ``low`` only where it was rendered."""


def band(value: float, edges: tuple[float, ...]) -> int:
    """Index of the band of ``edges`` holding ``value``; the ends are closed"""
    for i in range(len(edges) - 2):
        if value < edges[i + 1]:
            return i
    return len(edges) - 2


def lit(frames: list[dict]) -> list[dict]:
    """The frames that are not dark, by seed"""
    keep = [f for f in frames if "dark" not in f["randomisation"]]
    return sorted(keep, key=lambda f: f["seed"])


def grid(frames: list[dict], cap: int) -> tuple[list[dict], list[list[list[int]]]]:
    """Cap every elevation by range cell, round-robin over the bearings

    Returns:
        The frames kept, by seed, and ``[rendered, kept]`` for every cell.
    """
    rows, cols = len(ELEVATION_DEG) - 1, len(RANGE_M) - 1
    cells: dict[tuple[int, int], list[list[dict]]] = {}
    for frame in frames:
        orbit = frame["randomisation"].get("orbit")
        if not orbit:  # no clear pose was found and the wall mount was kept
            continue
        key = (band(orbit["elevation_deg"], ELEVATION_DEG),
               band(orbit["range_m"], RANGE_M))  # fmt: skip
        sectors = cells.setdefault(key, [[] for _ in range(BEARINGS)])
        sectors[int(orbit["azimuth_deg"] % 360 // (360 / BEARINGS))].append(frame)
    kept: list[dict] = []
    counts = [[[0, 0] for _ in range(cols)] for _ in range(rows)]
    for (row, col), sectors in cells.items():
        counts[row][col][0] = sum(len(s) for s in sectors)
        turn = 0
        while counts[row][col][1] < cap and any(sectors):
            sector = sectors[turn % BEARINGS]
            if sector:
                kept.append(sector.pop(0))
                counts[row][col][1] += 1
            turn += 1
    return sorted(kept, key=lambda f: f["seed"]), counts


def write(out: Path, name: str, src: Path, header: dict, frames: list[dict],
          link: bool) -> None:  # fmt: skip
    """Write one selected split: its ``gt.json`` and links to its frames"""
    folder = out / name
    folder.mkdir(parents=True, exist_ok=True)
    gt = {**header, "split": name, "frames": frames}
    (folder / "gt.json").write_text(json.dumps(gt), encoding="utf-8")
    if not link:
        return
    for frame in frames:
        for key in ("file", "categories"):
            source, target = src / frame["split"] / frame[key], folder / frame[key]
            if target.exists():
                continue
            # A hard link where the file system has them, else a symbolic one; a
            # copy is the last resort: it doubles the frames on a volume with a
            # quota, which is how a run died on the pod's network volume.
            for place in (os.link, os.symlink, shutil.copy2):
                try:
                    place(source.resolve(), target)
                    break
                except OSError:
                    continue
            else:
                raise OSError(f"cannot link or copy {source} to {target}")


def main() -> None:
    """Select, report and write"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--src", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--out", type=Path, default=None, help="default: --src")
    parser.add_argument("--cap", type=int, default=CELL_CAP)
    parser.add_argument("--no-link", action="store_true")
    args = parser.parse_args()
    out = args.out or args.src

    def present(split: str) -> bool:
        return (args.src / split / "gt.json").exists()

    def load(split: str) -> dict:
        path = args.src / split / "gt.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def views_of(role: str) -> list[dict]:
        names = [f"{s}_{role}" for s in VIEW_SPLITS if present(f"{s}_{role}")]
        return [frame for name in names for frame in load(name)["frames"]]

    rail = load("rail_train")
    header = {k: v for k, v in rail.items() if k not in ("frames", "split")}
    views = lit(views_of("train"))
    picked, counts = grid(views, args.cap)
    train = lit(rail["frames"])[:RAIL_TRAIN] + picked
    val = (
        lit(load("rail_val")["frames"])[:RAIL_VAL]
        + lit(views_of("val"))
    )
    write(out, "sel_train", args.src, header, train, not args.no_link)
    write(out, "sel_val", args.src, header, val, not args.no_link)

    report = {
        "elevation_deg": ELEVATION_DEG,
        "range_m": RANGE_M,
        "cap": args.cap,
        "cells_rendered_kept": counts,
        "train": {"rail": len(train) - len(picked), "views": len(picked)},
        "val": len(val),
    }
    (out / "selection.json").write_text(json.dumps(report, indent=1))
    print("elevation \\ range m  " + "  ".join(
        f"{a:g}-{b:g}".rjust(9) for a, b in zip(RANGE_M, RANGE_M[1:], strict=False)))
    for i, row in enumerate(counts):
        label = f"{ELEVATION_DEG[i]:g}-{ELEVATION_DEG[i + 1]:g} deg".ljust(19)
        print(label + "  ".join(f"{k}/{n}".rjust(9) for n, k in row))
    print(f"sel_train: {len(train)} frames ({len(train) - len(picked)} wall mount, "
          f"{len(picked)} orbit and close); sel_val: {len(val)}")  # fmt: skip


if __name__ == "__main__":
    main()
