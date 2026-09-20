"""Draw the figures of ``docs/demo`` from the numbers in ``docs/demo/numbers``

Everything the demo folder shows about the detector's dataset, training and
results is drawn here from the files beside it, so a figure can be redrawn,
restyled or checked without a GPU or the rendered frames:

    python scripts/demo_figures.py            # docs/demo/numbers -> docs/demo/*/

``numbers/results_<run>.csv`` are Ultralytics' per-epoch logs, ``scores.json`` the
twelve tests of ``viewpoint_study.py`` for the three detectors, ``limits.json``
``limits_sweep.py``'s sweeps, ``demo_benches.json`` the ten viewer benches and
``dataset.json`` the render's counts. One colour means one detector on every
figure: the previous one orange, the 25-epoch run green, the 100-epoch run blue.
"""

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

DEMO = Path(__file__).resolve().parents[1] / "docs" / "demo"
DATA = DEMO / "numbers"

SURFACE, INK, INK_2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e4e3df"
MODELS = {
    "rail": ("previous detector (rail)", "#eb6834"),
    "25_epochs": ("retrained, 25 epochs", "#1baf7a"),
    "100_epochs": ("retrained, 100 epochs", "#2a78d6"),
}
"""Name and colour of each detector, the same on every figure."""
TRAIN, VAL = "#2a78d6", "#eb6834"
TESTS = (
    ("rail_test", "robot's\nwall camera"),
    ("pattern_test", "demo benches\nwall camera"),
    ("lab_rail_test", "another lab\nwall camera"),
    ("rail_test_shift", "degraded\ncamera"),
    ("orbit_test", "any angle\n1–3.5 m"),
    ("close_test", "close\nunder 1 m"),
    ("overhead_test", "straight\ndown"),
    ("low_test", "low camera\n15–30°"),
    ("pattern_orbit_test", "demo benches\nany angle"),
    ("lab_test", "another lab\nany angle"),
    ("dark_test", "dim room\nwall camera"),
    ("orbit_dark_test", "dim room\nany angle"),
)


def style(ax: plt.Axes, title: str) -> None:
    """Recessive axes and grid; the title names the panel"""
    ax.set_facecolor(SURFACE)
    ax.set_title(title, loc="left", fontsize=11.5, color=INK, pad=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, colors=INK_2, labelsize=9)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)


def figure(width: float, height: float, title: str, note: str = "") -> plt.Figure:
    """A figure on the chart surface with its title top left"""
    fig = plt.figure(figsize=(width, height), facecolor=SURFACE)
    fig.text(0.035, 1 - 0.28 / height, title, fontsize=15, weight="bold", color=INK,
             va="top")  # fmt: skip
    if note:
        fig.text(0.035, 0.18 / height, note, fontsize=9, color=INK_2, va="bottom")
    return fig


def save(fig: plt.Figure, path: Path) -> None:
    """Write one figure and say so"""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=170, facecolor=SURFACE)
    plt.close(fig)
    print(path.relative_to(DEMO))


def end_labels(ax: plt.Axes, x: float, ends: list[tuple[float, str]]) -> None:
    """Direct labels right of the lines' ends, pushed apart where they meet"""
    low, high = ax.get_ylim()
    gap = 0.06 * (high - low)
    ceiling = high
    for y, text in sorted(ends, reverse=True):
        y = min(y, ceiling)
        ceiling = y - gap
        ax.annotate(text, (x, y), xytext=(7, 0), textcoords="offset points",
                    va="center", fontsize=9, color=INK_2,
                    annotation_clip=False)  # fmt: skip


def log(run: str) -> list[dict]:
    """One run's per-epoch rows"""
    with (DATA / f"results_{run}.csv").open(newline="") as handle:
        return [{k.strip(): float(v) for k, v in row.items()}
                for row in csv.DictReader(handle)]  # fmt: skip


def fitness(row: dict) -> float:
    """What Ultralytics keeps the best epoch by"""
    return 0.1 * row["metrics/mAP50(B)"] + 0.9 * row["metrics/mAP50-95(B)"]


def curves(run: str) -> None:
    """One run: losses, training against validation, and the validation scores"""
    rows = log(run)
    epoch = np.array([r["epoch"] for r in rows])
    best = int(np.argmax([fitness(r) for r in rows]))
    panels = (
        ("Box loss: how far the boxes are off", (("training", "train/box_loss", TRAIN),
                                                  ("validation", "val/box_loss", VAL))),
        ("Class loss: vial or not", (("training", "train/cls_loss", TRAIN),
                                     ("validation", "val/cls_loss", VAL))),
        ("On validation frames it never trains on",
         (("recall", "metrics/recall(B)", "#2a78d6"),
          ("precision", "metrics/precision(B)", "#eb6834"),
          ("AP50", "metrics/mAP50(B)", "#1baf7a"),
          ("AP50–95", "metrics/mAP50-95(B)", "#eda100"))),
    )  # fmt: skip
    fig = figure(15, 5.2, f"The training run of {len(rows)} epochs",
                 f"Dotted line: epoch {int(epoch[best])}, the checkpoint that is kept; "
                 "labels give each curve's value there. The step in the training "
                 "losses ten epochs from the end is mosaic augmentation switching off. "
                 "5,844 training frames, 750 validation frames.")  # fmt: skip
    for i, (title, series) in enumerate(panels):
        ax = fig.add_axes([0.035 + i * 0.325, 0.15, 0.215, 0.64])
        style(ax, title)
        ends = []
        for label, column, colour in series:
            values = np.array([r[column] for r in rows])
            ax.plot(epoch, values, color=colour, linewidth=2.2, label=label)
            ax.plot(epoch[best], values[best], "o", color=colour, markersize=6.5,
                    markeredgecolor=SURFACE, markeredgewidth=1.6)  # fmt: skip
            ends.append((values[-1], f"{label} {values[best]:.3f}"))
        ax.axvline(epoch[best], color=MUTED, linewidth=0.9, linestyle=(0, (3, 3)))
        ax.set_xlim(1, epoch[-1])
        end_labels(ax, epoch[-1], ends)
        ax.set_xticks([1, *range(max(5, len(rows) // 5), len(rows) + 1,
                                 max(5, len(rows) // 5))])  # fmt: skip
        ax.set_xlabel("epoch", color=INK_2, fontsize=9)
        ax.legend(loc="upper right" if "loss" in title else "lower right",
                  frameon=False, fontsize=8.5, labelcolor=INK_2)  # fmt: skip
    save(fig, DEMO / "2_training" / f"curves_{run}.png")


def both_runs() -> None:
    """The two runs on the same axes: what 75 more epochs bought"""
    runs = {run: log(run) for run in ("25_epochs", "100_epochs")}
    panels = (("Validation AP50–95: how tight the boxes are", "metrics/mAP50-95(B)"),
              ("Validation recall: share of the vials found", "metrics/recall(B)"),
              ("Training box loss", "train/box_loss"))  # fmt: skip
    fig = figure(15, 5.2, "The same training, stopped at 25 epochs and run to 100",
                 "Same frames, same recipe, same seed. The runs start together and "
                 "part, because the learning rate decays over the whole run. "
                 "Markers: the checkpoint each run keeps.")  # fmt: skip
    for i, (title, column) in enumerate(panels):
        ax = fig.add_axes([0.035 + i * 0.325, 0.15, 0.215, 0.64])
        style(ax, title)
        ends = []
        for run, rows in runs.items():
            name, colour = MODELS[run]
            epoch = np.array([r["epoch"] for r in rows])
            values = np.array([r[column] for r in rows])
            best = int(np.argmax([fitness(r) for r in rows]))
            ax.plot(epoch, values, color=colour, linewidth=2.2, label=name)
            ax.plot(epoch[best], values[best], "o", color=colour, markersize=7,
                    markeredgecolor=SURFACE, markeredgewidth=1.6)  # fmt: skip
            ends.append((values[best], f"{name.split(', ')[-1]}: {values[best]:.3f}"))
        ax.set_xlim(1, 100)
        end_labels(ax, 100, ends)
        ax.set_xticks([1, 25, 50, 75, 100])
        ax.set_xlabel("epoch", color=INK_2, fontsize=9)
        ax.legend(loc="lower right" if "loss" not in title else "upper right",
                  frameon=False, fontsize=8.5, labelcolor=INK_2)  # fmt: skip
    save(fig, DEMO / "2_training" / "curves_25_vs_100_epochs.png")


def all_tests() -> None:
    """Recall and false boxes of the three detectors on every test set"""
    scores = json.loads((DATA / "scores.json").read_text())
    tests = [t for t in TESTS if t[0] in scores["tests"]]
    thresholds = ", ".join(f"{MODELS[m][0]} {v:.2f}"
                           for m, v in scores["thresholds"].items())  # fmt: skip
    fig = figure(16.5, 8.6, "Twelve tests no model trained on: vials found, and "
                 "boxes that are not vials",
                 f"1,700 MuJoCo frames, 37,261 vials. Each detector at its own "
                 f"validation threshold: {thresholds}.")  # fmt: skip
    width = 0.26
    for k, (field, title, fmt, top) in enumerate((
        ("recall", "Recall: share of the vials found", "{:.2f}", 0.53),
        ("false_per_frame", "False boxes a frame", "{:.2f}", 0.12),
    )):  # fmt: skip
        ax = fig.add_axes([0.045, top, 0.94, 0.31])
        style(ax, title)
        for j, (model, (name, colour)) in enumerate(MODELS.items()):
            for i, (key, _) in enumerate(tests):
                value = scores["tests"][key][model][field]
                x = i + (j - 1) * width
                ax.bar(x, value, width=width - 0.035, color=colour,
                       label=name if i == 0 else None)  # fmt: skip
                ax.annotate(fmt.format(value), (x, value), xytext=(0, 3),
                            textcoords="offset points", ha="center", fontsize=7.8,
                            color=INK_2)  # fmt: skip
        ax.set_xticks(range(len(tests)))
        ax.set_xticklabels([label for _, label in tests] if k else [], color=INK_2,
                           fontsize=9)  # fmt: skip
        ax.set_xlim(-0.6, len(tests) - 0.4)
        ax.margins(y=0.18)
        if not k:
            ax.set_ylim(0, 1.16)
            fig.legend(*ax.get_legend_handles_labels(), loc="upper left",
                       frameon=False, fontsize=10, ncols=3, labelcolor=INK_2,
                       bbox_to_anchor=(0.03, 0.935))  # fmt: skip
    save(fig, DEMO / "3_results" / "all_tests_three_models.png")


def limits() -> None:
    """Where a detector breaks as the camera nears, tilts, or the light goes"""
    data = json.loads((DATA / "limits.json").read_text())
    series = (("rail_at_0.10", "rail"), ("100_epochs_at_0.52", "100_epochs"))
    panels = (("range", "Distance to the bench, m", "Camera distance"),
              ("elevation", "Elevation above the bench, degrees", "Camera elevation"),
              ("light", "Share of the room's light left", "Room light"))  # fmt: skip
    fig = figure(15, 5.4, "How far each detector goes: recall as one condition moves",
                 "The same 12 benches of 24 vials rendered at every step. Previous "
                 "detector at its threshold 0.10, retrained at 0.52. No dark frame was "
                 "trained on, by decision: the dark is the one limit that did not "
                 "move.")  # fmt: skip
    for i, (sweep, xlabel, title) in enumerate(panels):
        ax = fig.add_axes([0.04 + i * 0.325, 0.2, 0.25, 0.59])
        style(ax, title)
        ends = []
        for key, model in series:
            name, colour = MODELS[model]
            rows = data[key][sweep]
            x = [r["level"] for r in rows]
            y = [r["recall"] for r in rows]
            ax.plot(x, y, "-o", color=colour, linewidth=2.2, markersize=5.5,
                    markeredgecolor=SURFACE, markeredgewidth=1.2,
                    label=name)  # fmt: skip
            worst = min(range(len(y)), key=y.__getitem__)
            if sweep != "light":
                ax.annotate(f"{y[worst]:.2f}", (x[worst], y[worst]), xytext=(6, -11),
                            textcoords="offset points", fontsize=9,
                            color=INK_2)  # fmt: skip
            ends.append((y[-1], name))
        if sweep == "light":
            ax.set_xscale("log")
            ax.set_xticks([0.03, 0.06, 0.1, 0.15, 0.3, 1.0])
            ax.set_xticklabels(["3 %", "6 %", "10 %", "15 %", "30 %", "100 %"])
            ax.minorticks_off()
            ax.invert_xaxis()
        ax.set_ylim(-0.04, 1.08)
        ax.set_xlabel(xlabel, color=INK_2, fontsize=9)
        ax.legend(loc="lower right" if sweep != "light" else "lower left",
                  frameon=False, fontsize=8.5, labelcolor=INK_2)  # fmt: skip
    save(fig, DEMO / "3_results" / "limits_before_and_after.png")


def demo_benches() -> None:
    """The ten catalogued benches, seed by seed, from any angle"""
    benches = json.loads((DATA / "demo_benches.json").read_text())
    patterns = benches["per_pattern_tests"]
    fig = figure(15, 5.6, "The ten benches the viewer shows, seed by seed, seen from "
                 "any angle",
                 "None of the ten was trained on. 10 frames a bench. From the wall "
                 "camera all three detectors find 0.97 to 1.00 of every bench; the "
                 "difference is here, when the camera moves. Axis starts at "
                 "0.8.")  # fmt: skip
    ax = fig.add_axes([0.045, 0.24, 0.94, 0.56])
    style(ax, "Recall from any angle")
    width = 0.26
    for j, (model, (name, colour)) in enumerate(MODELS.items()):
        for i, p in enumerate(patterns):
            value = p["scores"][model]["any_angle"]["recall"]
            x = i + (j - 1) * width
            ax.bar(x, value - 0.8, bottom=0.8, width=width - 0.035, color=colour,
                   label=name if i == 0 else None)  # fmt: skip
            ax.annotate(f"{value:.2f}", (x, value), xytext=(0, 3),
                        textcoords="offset points", ha="center", fontsize=8,
                        color=INK_2)  # fmt: skip
    names = {"scatter": "scattered", "crowd": "crowded", "rows": "rows",
             "clusters": "clusters"}  # fmt: skip
    ax.set_xticks(range(len(patterns)))
    ax.set_xticklabels([f"{p['pattern']} · seed {p['seed']}\n{names[p['style']]}, "
                        f"{p['count']} flasks" for p in patterns], color=INK_2,
                       fontsize=9)  # fmt: skip
    ax.set_ylim(0.8, 1.03)
    ax.set_xlim(-0.6, len(patterns) - 0.4)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, ncols=3,
              labelcolor=INK_2, bbox_to_anchor=(1, 1.02))  # fmt: skip
    save(fig, DEMO / "3_results" / "demo_benches_by_seed.png")


def dataset() -> None:
    """What the 10,300 frames are made of"""
    d = json.loads((DATA / "dataset.json").read_text())
    cameras = (("rail", "wall camera"), ("orbit", "any angle, 1–3.5 m"),
               ("close", "close, under 1 m"), ("low", "low, 15–30°"))  # fmt: skip
    styles = (("scatter", "scattered"), ("cluster", "one cluster"),
              ("as built", "as the scene is built"), ("rows", "rows (pattern)"),
              ("clusters", "several clusters (pattern)"),
              ("crowd", "crowded (pattern)"))  # fmt: skip
    fig = figure(15, 5.0, f"What the dataset is made of: {d['frames']:,} frames, "
                 f"{d['vials']:,} labelled vials",
                 "Light, worktop tint and camera degradation are drawn in every frame "
                 "and cost no frames; what the count covers is camera poses, benches "
                 "and labs.")  # fmt: skip
    ax = fig.add_axes([0.13, 0.17, 0.2, 0.6])
    style(ax, "Frames by camera")
    ax.grid(False)
    left = np.zeros(len(cameras))
    uses = (("train", "#2a78d6"), ("val", "#1baf7a"), ("test", "#eda100"))
    for use, colour in uses:
        values = np.array([d["by_camera_and_use"].get(f"{c}/{use}", 0)
                           for c, _ in cameras])  # fmt: skip
        ax.barh(range(len(cameras)), values, left=left + 12 * (left > 0), height=0.55,
                color=colour, label={"train": "training", "val": "validation",
                                     "test": "test"}[use])  # fmt: skip
        left += values
    for i, total in enumerate(left):
        ax.annotate(f"{int(total):,}", (total, i), xytext=(8, 0),
                    textcoords="offset points", va="center", fontsize=9,
                    color=INK_2)  # fmt: skip
    ax.set_yticks(range(len(cameras)))
    ax.set_yticklabels([label for _, label in cameras], color=INK_2, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax.set_xlim(0, max(left) * 1.22)
    ax.legend(loc="lower right", frameon=False, fontsize=8.5, labelcolor=INK_2)

    for k, (title, items, colour, x0) in enumerate((
        ("Frames by bench layout", [(label, d["by_bench_style"].get(key, 0))
                                    for key, label in styles], "#1baf7a", 0.52),
        ("The lab around the bench", [("as it is", d["lab"]["as it is"]),
                                      ("varied", d["lab"]["varied"])], "#eb6834", 0.83),
    )):  # fmt: skip
        ax = fig.add_axes([x0, 0.17 if not k else 0.45, 0.14, 0.6 if not k else 0.32])
        style(ax, title)
        ax.grid(False)
        values = [v for _, v in items]
        ax.barh(range(len(items)), values, height=0.55, color=colour)
        for i, v in enumerate(values):
            ax.annotate(f"{v:,}", (v, i), xytext=(8, 0), textcoords="offset points",
                        va="center", fontsize=9, color=INK_2)  # fmt: skip
        ax.set_yticks(range(len(items)))
        ax.set_yticklabels([label for label, _ in items], color=INK_2, fontsize=9.5)
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        ax.set_xlim(0, max(values) * 1.3)
    save(fig, DEMO / "1_dataset" / "dataset_composition.png")


def main() -> None:
    """Draw every figure"""
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK})
    dataset()
    for run in ("25_epochs", "100_epochs"):
        curves(run)
    both_runs()
    all_tests()
    limits()
    demo_benches()


if __name__ == "__main__":
    main()
