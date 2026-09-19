"""Draw a training run for the presentation: its curves, and before against after

Ultralytics writes its own ``results.png`` next to the weights; it is a grid of
ten small panels made for debugging. These are the two figures to show:

``<out>/training_curves.png``
    From the run's ``results.csv``: box loss and class loss, training against
    validation, and the four validation scores, epoch by epoch, with the best
    epoch marked.
``<out>/before_after.png``
    From ``viewpoint_study.py``'s results: recall and false boxes a frame on
    every test set, one bar per detector, so the old and the new model stand
    side by side. With one detector it is the "before" on its own.

    python scripts/training_plots.py --run runs/orbit/n_sel_1920 --out OUT \
        --scores "rail (before)=results/viewpoint/rail_now" \
                 "retrained=results/viewpoint/n_sel_1920"

Both read files only, so they can be redrawn on any machine from what the pod
leaves behind, and they work the same on a run trained on Isaac frames.
"""

import argparse
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

SURFACE, INK, INK_2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e4e3df"
SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100")
"""Categorical slots in fixed order; validated as a set for colour-blind readers."""
TESTS = (
    ("rail_test", "wall mount"),
    ("orbit_test", "any angle\n1–3.5 m"),
    ("close_test", "close\n0.35–1 m"),
    ("overhead_test", "overhead\n70–88°"),
    ("low_test", "low\n15–30°"),
    ("dark_test", "dim room\nwall mount"),
    ("orbit_dark_test", "dim room\nany angle"),
    ("rail_test_shift", "degraded\ncamera"),
    ("pattern_test", "demo bench\npatterns"),
    ("lab_test", "other lab\nlayouts"),
)


def style(ax: plt.Axes, title: str) -> None:
    """Recessive axes and grid; the title names the panel"""
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", fontsize=11, color=INK, pad=8)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, colors=INK_2, labelsize=9)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)


def curves(run: Path, out: Path) -> None:
    """The run's losses and validation scores by epoch"""
    with (run / "results.csv").open(newline="") as handle:
        rows = [{k.strip(): float(v) for k, v in row.items()}
                for row in csv.DictReader(handle)]  # fmt: skip
    epoch = np.array([r["epoch"] for r in rows])
    best = int(np.argmax([r["metrics/mAP50-95(B)"] for r in rows]))
    panels = (
        ("Box loss", (("training", "train/box_loss"), ("validation", "val/box_loss"))),
        ("Class loss", (("training", "train/cls_loss"),
                        ("validation", "val/cls_loss"))),
        ("Validation scores", (("recall", "metrics/recall(B)"),
                               ("precision", "metrics/precision(B)"),
                               ("AP50", "metrics/mAP50(B)"),
                               ("AP50–95", "metrics/mAP50-95(B)"))),
    )  # fmt: skip
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6), facecolor=SURFACE)
    fig.suptitle(f"Training {run.name}: {len(rows)} epochs, best at epoch "
                 f"{int(epoch[best])}", x=0.04, y=0.98, ha="left", fontsize=14,
                 weight="bold", color=INK)  # fmt: skip
    for ax, (title, series) in zip(axes, panels, strict=True):
        style(ax, title)
        ends = []
        for colour, (name, column) in zip(SERIES, series, strict=False):
            values = np.array([r[column] for r in rows])
            ax.plot(epoch, values, color=colour, linewidth=2, label=name)
            ax.plot(epoch[best], values[best], "o", color=colour, markersize=6,
                    markeredgecolor=SURFACE, markeredgewidth=1.5)  # fmt: skip
            ends.append((values[-1], name, values[best]))
        ax.axvline(epoch[best], color=MUTED, linewidth=0.8, linestyle=(0, (3, 3)))
        # Direct labels at the line ends, pushed apart where the lines meet.
        low, high = ax.get_ylim()
        gap = 0.055 * (high - low)
        ceiling = high
        for last, name, at_best in sorted(ends, reverse=True):
            y = min(last, ceiling)
            ceiling = y - gap
            ax.annotate(f"{name} {at_best:.3g}", (epoch[-1], y), xytext=(6, 0),
                        textcoords="offset points", va="center", fontsize=9,
                        color=INK_2, annotation_clip=False)  # fmt: skip
        ax.set_xlim(epoch[0], epoch[-1] + 0.34 * (epoch[-1] - epoch[0]))
        ax.set_xticks([int(e) for e in np.linspace(epoch[0], epoch[-1], 5)])
        ax.set_xlabel("epoch", color=INK_2, fontsize=9)
        ax.legend(loc="upper right" if "loss" in title else "lower right",
                  frameon=False, fontsize=8.5, labelcolor=INK_2)  # fmt: skip
    fig.text(0.04, 0.015, "Labels give each line's value at the best epoch (dotted), "
             "the checkpoint that is kept.", fontsize=8.5, color=INK_2)  # fmt: skip
    fig.subplots_adjust(left=0.04, right=0.985, top=0.83, bottom=0.17, wspace=0.16)
    fig.savefig(out / "training_curves.png", dpi=160, facecolor=SURFACE)


def before_after(scores: list[tuple[str, Path]], out: Path) -> None:
    """Recall and false boxes a frame on every test set, one bar per detector"""
    tests = [
        (key, label)
        for key, label in TESTS
        if any((folder / f"{key}.json").exists() for _, folder in scores)
    ]
    fig, axes = plt.subplots(2, 1, figsize=(max(9, 1.55 * len(tests) + 2), 7.4),
                             facecolor=SURFACE, sharex=True)  # fmt: skip
    fig.suptitle("On every test set: bottles found, and boxes that are not bottles",
                 x=0.06, y=0.975, ha="left", fontsize=14, weight="bold")  # fmt: skip
    width = min(0.8 / len(scores), 0.42)
    for ax, (field, title, fmt) in zip(axes, (
        ("recall", "Recall: share of the bottles found", "{:.2f}"),
        ("false_per_frame", "False boxes a frame", "{:.1f}"),
    ), strict=True):  # fmt: skip
        style(ax, title)
        for k, (name, folder) in enumerate(scores):
            for i, (key, _) in enumerate(tests):
                path = folder / f"{key}.json"
                if not path.exists():
                    continue
                value = json.loads(path.read_text())["all"]["all"][field]
                x = i + width * (k + 0.5 - len(scores) / 2)
                ax.bar(x, value, width=width - 0.03, color=SERIES[k],
                       label=name if i == 0 else None)  # fmt: skip
                ax.annotate(fmt.format(value), (x, value), xytext=(0, 3),
                            textcoords="offset points", ha="center", fontsize=9,
                            color=INK_2)  # fmt: skip
        ax.set_xticks(range(len(tests)))
        ax.set_xticklabels([label for _, label in tests], color=INK_2, fontsize=9)
        ax.margins(y=0.16)
    axes[0].set_ylim(0, 1.12)
    if len(scores) > 1:
        axes[0].legend(loc="lower right", frameon=False, fontsize=9, labelcolor=INK_2)
    else:
        fig.text(0.06, 0.925, scores[0][0], fontsize=10, color=INK_2)
    fig.subplots_adjust(left=0.06, right=0.985, top=0.86, bottom=0.09, hspace=0.3)
    fig.savefig(out / "before_after.png", dpi=160, facecolor=SURFACE)


def main() -> None:
    """Draw whichever figures have their inputs"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--run", type=Path, default=None, help="holds results.csv")
    parser.add_argument("--scores", nargs="*", default=[], metavar="NAME=FOLDER",
                        help="viewpoint_study.py result folders, oldest first")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK})
    if args.run:
        curves(args.run, args.out)
        print(args.out / "training_curves.png")
    if args.scores:
        pairs = [(s.split("=", 1)[0], Path(s.split("=", 1)[1])) for s in args.scores]
        before_after(pairs, args.out)
        print(args.out / "before_after.png")


if __name__ == "__main__":
    main()
