r"""Plot wrist-camera scans of the same bottles against each other

Takes the output folders of several ``wrist_scan.py`` runs over the same
bottles --- the one-sided EAN-13 label and the ArUco ring, say --- and draws how
many bottles each run read, from how far, and two bottles as each run saw them.

    python scripts/wrist_compare.py \
        "EAN-13, square to the label=../simulation/out/wrist_compare/ean_label" \
        "EAN-13, from the aisle=../simulation/out/wrist_compare/ean_aisle" \
        "ArUco ring, from the aisle=../simulation/out/wrist_compare/ring_aisle"

Output: ``comparison.png`` next to the first run. Needs ``matplotlib``.
"""

import argparse
import json
from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

STEPS = [
    (0.30, "0.30 m, a GoPro's near focus"),
    (0.20, "0.20 m"),
    (0.15, "0.15 m"),
    (0.10, "0.10 m"),
]
SHADES = ["#188038", "#81c995", "#fdd663", "#f29900"]
MISSED = "#d93025"
EXAMPLES = ("SMP-0021", "PWD-0012")


def main() -> None:
    """Read the runs and draw the figure"""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("runs", nargs="+", help="'title=folder' of a wrist_scan.py run")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    runs = []
    for item in args.runs:
        title, folder = item.split("=", 1)
        rows = json.loads((Path(folder) / "results.json").read_text())
        runs.append((title, Path(folder), rows))
    ids = [r["sample_id"] for r in runs[0][2]]
    for title, _, rows in runs:
        if [r["sample_id"] for r in rows] != ids:
            raise SystemExit(f"{title}: not the same bottles as the first run")

    figure = plt.figure(figsize=(15, 4.2 + 3.4 * len(EXAMPLES)))
    grid = figure.add_gridspec(
        1 + len(EXAMPLES),
        len(runs),
        hspace=0.7,
        height_ratios=[1.3] + [1.0] * len(EXAMPLES),
    )
    axis = figure.add_subplot(grid[0, :])
    y = np.arange(len(runs))[::-1]
    left = np.zeros(len(runs))
    for (standoff, label), shade in zip(STEPS, SHADES, strict=True):
        counts = np.array(
            [
                sum(
                    r["verdict"] == "ok" and abs(r["standoff_m"] - standoff) < 1e-6
                    for r in rows
                )
                for _, _, rows in runs
            ]
        )
        axis.barh(y, counts, left=left, color=shade, label=f"read from {label}")
        for yi, c, l0 in zip(y, counts, left, strict=True):
            if c:
                axis.text(l0 + c / 2, yi, str(c), ha="center", va="center", fontsize=11)
        left += counts
    missed = np.array([sum(r["verdict"] != "ok" for r in rows) for _, _, rows in runs])
    axis.barh(y, missed, left=left, color=MISSED, label="not read at all")
    for yi, c, l0 in zip(y, missed, left, strict=True):
        if c:
            axis.text(
                l0 + c / 2,
                yi,
                str(c),
                ha="center",
                va="center",
                color="white",
                fontsize=11,
            )
    axis.set_yticks(y)
    axis.set_yticklabels([t for t, _, _ in runs], fontsize=11)
    axis.set_xlim(0, len(ids))
    axis.set_xlabel(f"bottles, of the same {len(ids)} in the minihannover scene")
    axis.set_title(
        "Wrist camera (GoPro Linear 1080p): how close it had to come to read "
        "each bottle",
        loc="left",
        fontsize=13,
    )
    axis.legend(
        ncols=5,
        fontsize=9,
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
    )
    axis.spines[["top", "right"]].set_visible(False)

    for row, sample_id in enumerate(EXAMPLES, start=1):
        for column, (_, folder, rows) in enumerate(runs):
            cell = figure.add_subplot(grid[row, column])
            image = cv2.imread(str(folder / f"{sample_id}.png"))
            if image is not None:
                cell.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            scan = next(r for r in rows if r["sample_id"] == sample_id)
            verdict = (
                f"read from {scan['standoff_m']:.2f} m"
                if scan["verdict"] == "ok"
                else "not read"
            )
            cell.set_title(
                f"{sample_id}, {scan['material']} {scan['container_ml']:g} ml: "
                f"{verdict}",
                fontsize=10,
            )
            cell.set_xticks([])
            cell.set_yticks([])
    out = args.out or runs[0][1].parent / "comparison.png"
    figure.savefig(out, dpi=100, bbox_inches="tight")
    print("figure ->", out)


if __name__ == "__main__":
    main()
