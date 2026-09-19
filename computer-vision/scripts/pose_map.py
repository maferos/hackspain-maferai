"""Draw where the camera stood in every frame of a dataset: the pose map

One figure for the presentation and for checking a training set before paying
for its training. Left, the bench seen from above: every frame is a dot at its
camera's bearing round the bench, overhead views at the centre and low ones at
the rim, shaded by the camera's distance. Right, the same frames counted on the
elevation by distance grid ``select_frames.py`` caps, so an empty or thin cell
shows as one. Reads only ``gt.json``, so it works on Isaac frames converted by
``isaac_replicator_to_gt.py`` as well as on MuJoCo's.

    python scripts/pose_map.py sel_train --src DIR --out pose_map.png
    python scripts/pose_map.py rail_train orbit_train close_train --title "All"

An orbit or close frame carries its pose as drawn (``randomisation.orbit``).
Any other frame's elevation, bearing and distance are taken from its camera
position towards the centre of the bench.
"""

import argparse
import json
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixedcam_dataset import DEFAULT_OUT  # noqa: E402
from select_frames import ELEVATION_DEG, RANGE_M, band  # noqa: E402

SURFACE, INK, INK_2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e4e3df"
BLUES = LinearSegmentedColormap.from_list(
    "blues", ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]
)
"""One hue, light to dark, for distance and for counts; its lightest step still
clears 2:1 on the surface."""
WALL = "#eb6834"
"""The wall mount's own colour: it is one place, not a distance."""
RIM_DEG = 10.0


def pose(frame: dict, gt: dict) -> tuple[float, float, float, bool]:
    """Elevation and bearing in degrees, distance in metres, and whether drawn"""
    orbit = frame["randomisation"].get("orbit")
    if orbit:
        return orbit["elevation_deg"], orbit["azimuth_deg"], orbit["range_m"], True
    x, y, z = frame["cam_pos"]
    dx, dy = x - gt["bench_centre"][0], y - gt["bench_centre"][1]
    dz = z - gt["worktop_z"]
    flat = math.hypot(dx, dy)
    return (math.degrees(math.atan2(dz, flat)), math.degrees(math.atan2(dy, dx)) % 360,
            math.hypot(flat, dz), False)  # fmt: skip


def main() -> None:
    """Read the splits and draw the figure"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("splits", nargs="+")
    parser.add_argument("--src", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--out", type=Path, default=Path("pose_map.png"))
    parser.add_argument("--title", default=None)
    args = parser.parse_args()

    poses = []
    for split in args.splits:
        gt = json.loads((args.src / split / "gt.json").read_text(encoding="utf-8"))
        poses += [pose(frame, gt) for frame in gt["frames"]]
    elevation, bearing, reach, drawn = (np.array(v) for v in zip(*poses, strict=True))
    fixed = ~drawn.astype(bool)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "text.color": INK, "axes.labelcolor": INK_2})  # fmt: skip
    fig = plt.figure(figsize=(13, 6.4), facecolor=SURFACE)
    title = args.title or " + ".join(args.splits)
    fig.suptitle(f"Where the camera stood: {title}, {len(poses):,} frames",
                 x=0.035, y=0.965, ha="left", fontsize=14, weight="bold")  # fmt: skip

    polar = fig.add_axes([0.03, 0.06, 0.46, 0.78], projection="polar",
                         facecolor=SURFACE)  # fmt: skip
    radius = 90 - elevation
    order = np.argsort(-reach[~fixed])  # near views drawn last, on top
    dots = polar.scatter(np.radians(bearing[~fixed][order]), radius[~fixed][order],
                         c=reach[~fixed][order], cmap=BLUES, vmin=RANGE_M[0],
                         vmax=RANGE_M[-1], s=9, linewidths=0)  # fmt: skip
    if fixed.any():
        polar.scatter(np.radians(bearing[fixed]), radius[fixed], s=9, color=WALL,
                      linewidths=0)  # fmt: skip
        polar.annotate(
            f"wall mount\n{int(fixed.sum()):,} frames",
            (np.radians(np.median(bearing[fixed])), np.median(radius[fixed])),
            xytext=(34, -44), textcoords="offset points", color=INK, fontsize=9,
            arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.8},
        )  # fmt: skip
    rim = max(RIM_DEG, math.floor(elevation.min() / 5) * 5 - 5)
    polar.set_ylim(0, 90 - rim)
    rings = [e for e in (75, 60, 45, 30, 15) if e > rim]
    polar.set_yticks([90 - e for e in rings])
    polar.set_yticklabels(
        [f"{e}°" for e in rings], color=INK, fontsize=8,
        bbox={"facecolor": SURFACE, "edgecolor": "none", "pad": 1.5, "alpha": 0.85},
    )
    polar.set_rlabel_position(22)
    polar.set_xticks(np.radians(range(0, 360, 30)))
    polar.set_xticklabels([f"{a}°" for a in range(0, 360, 30)], color=MUTED,
                          fontsize=8)  # fmt: skip
    polar.grid(color=GRID, linewidth=0.8)
    polar.spines["polar"].set_color(GRID)
    polar.set_title("Bearing round the bench; centre = straight down, rim = low",
                    loc="left", fontsize=10, color=INK_2, pad=14)  # fmt: skip
    bar = fig.colorbar(dots, ax=polar, orientation="horizontal", fraction=0.04,
                       pad=0.09, shrink=0.55)  # fmt: skip
    bar.set_label("distance from the camera to its aim point, m", fontsize=9)
    bar.outline.set_visible(False)
    bar.ax.tick_params(colors=INK_2, labelsize=8, length=0)

    rows, cols = len(ELEVATION_DEG) - 1, len(RANGE_M) - 1
    counts = np.zeros((rows, cols), int)
    for e, r in zip(elevation[~fixed], reach[~fixed], strict=True):
        if ELEVATION_DEG[0] <= e <= ELEVATION_DEG[-1]:
            counts[band(e, ELEVATION_DEG), band(r, RANGE_M)] += 1
    outside = int((~fixed).sum() - counts.sum())
    grid = fig.add_axes([0.57, 0.2, 0.4, 0.56], facecolor=SURFACE)
    shown = np.ma.masked_equal(counts, 0)
    grid.imshow(shown, cmap=BLUES, vmin=0, vmax=max(counts.max(), 1), aspect="auto",
                origin="lower")  # fmt: skip
    for (i, j), n in np.ndenumerate(counts):
        dark = n > 0.45 * counts.max()
        ink = "#ffffff" if dark else (INK if n else MUTED)
        grid.text(j, i, f"{n:,}" if n else "none", ha="center", va="center",
                  fontsize=11, color=ink)  # fmt: skip
    grid.set_xticks(range(cols))
    grid.set_xticklabels([f"{a:g}–{b:g} m" for a, b in zip(RANGE_M, RANGE_M[1:],
                                                           strict=False)])  # fmt: skip
    grid.set_yticks(range(rows))
    grid.set_yticklabels([f"{a:g}–{b:g}°" for a, b in zip(ELEVATION_DEG,
                                                          ELEVATION_DEG[1:],
                                                          strict=False)])  # fmt: skip
    grid.set_xticks(np.arange(-0.5, cols), minor=True)
    grid.set_yticks(np.arange(-0.5, rows), minor=True)
    grid.grid(which="minor", color=SURFACE, linewidth=3)
    grid.tick_params(which="both", length=0, colors=INK_2, labelsize=9)
    for side in grid.spines.values():
        side.set_visible(False)
    grid.set_xlabel("distance to the aim point")
    grid.set_ylabel("elevation above the bench")
    grid.set_title("Frames in every elevation by distance cell (orbit and close views)",
                   loc="left", fontsize=10, color=INK_2, pad=10)  # fmt: skip
    note = ("“none”: the 2.85 m ceiling leaves no room for a steep view from that far."
            if (counts == 0).any() else "")  # fmt: skip
    if outside:
        note += f"  {outside:,} frames fall outside the grid's elevations."
    fig.text(0.57, 0.085, note.strip(), fontsize=8.5, color=INK_2, ha="left", va="top",
             wrap=True)  # fmt: skip

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=160, facecolor=SURFACE)
    print(f"{args.out}: {len(poses)} frames, {int(fixed.sum())} from the wall mount, "
          f"grid total {int(counts.sum())}")  # fmt: skip


if __name__ == "__main__":
    main()
