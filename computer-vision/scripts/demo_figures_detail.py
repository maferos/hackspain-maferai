"""Draw the detailed figures of ``docs/demo`` from its per-frame and per-vial tables

:mod:`demo_figures` draws the headline figures from summary numbers. This module
draws what needs every frame or every vial:

    python scripts/demo_figures_detail.py     # docs/demo/numbers -> docs/demo/*/

``numbers/frames.csv`` has one row a rendered frame (camera pose, vials, bench
layout, lab, light), ``vials.json`` the vials' heights and where they stand on the
worktop, ``test_vials.csv`` one row for every vial a detector had to find in the
twelve tests with the score each detector found it at (empty when it found none),
and ``test_false_boxes.csv`` every box that matched no vial. A vial is found when
its score reaches the detector's threshold in ``scores.json``.
"""

import csv
import json
import textwrap

import matplotlib

matplotlib.use("Agg")
import demo_figures  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from demo_figures import (  # noqa: E402
    DATA,
    DEMO,
    GRID,
    INK,
    INK_2,
    MODELS,
    MUTED,
    SURFACE,
    end_labels,
    fitness,
    log,
    save,
    style,
)
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

BLUES = LinearSegmentedColormap.from_list(
    "blues", ["#d9e7f8", "#86b6ef", "#2a78d6", "#0d366b"]
)
CAMERAS = {
    "rail": ("robot's wall camera", "#eb6834"),
    "orbit": ("any angle, 1–3.5 m", "#2a78d6"),
    "low": ("low, 15–30°", "#eda100"),
    "close": ("close, under 1 m", "#1baf7a"),
}
"""Name and colour of each camera family, in stacking order."""
DIM = ("dark_test", "orbit_dark_test")
MOVING = (
    "orbit_test",
    "close_test",
    "low_test",
    "overhead_test",
    "pattern_orbit_test",
    "lab_test",
)


def figure(width: float, height: float, title: str, note: str = "") -> plt.Figure:
    """:func:`demo_figures.figure`, with the note wrapped to the figure's width"""
    return demo_figures.figure(
        width, height, title, textwrap.fill(note, int(width * 12.5))
    )


def table(name: str) -> dict[str, np.ndarray]:
    """One CSV of ``numbers`` as columns; numeric columns as floats, empty as NaN"""
    with (DATA / name).open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    out = {}
    for key in rows[0]:
        column = [r[key] for r in rows]
        try:
            out[key] = np.array([float(v) if v else np.nan for v in column])
        except ValueError:
            out[key] = np.array(column)
    return out


def found_by(vials: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Whether each detector found each vial, at its own threshold"""
    thresholds = json.loads((DATA / "scores.json").read_text())["thresholds"]
    return {m: np.nan_to_num(vials[f"score_{m}"]) >= thresholds[m] for m in MODELS}


def span(edges: list[float], unit: str = "", digits: int = 0) -> list[str]:
    """Names of the bins between ``edges``"""
    return [
        f"{a:.{digits}f}–{b:.{digits}f}{unit}"
        for a, b in zip(edges[:-1], edges[1:], strict=False)
    ]


def recall_lines(
    ax: plt.Axes,
    values: np.ndarray,
    edges: list[float],
    names: list[str],
    found: dict[str, np.ndarray],
    mask: np.ndarray,
    floor: int = 25,
    reverse: bool = False,
) -> None:
    """Each detector's recall in every bin of ``values``, with the vials in the bin"""
    inside = [
        mask & (values > a) & (values <= b)
        for a, b in zip(edges[:-1], edges[1:], strict=False)
    ]
    keep = [i for i, m in enumerate(inside) if m.sum() >= floor][
        :: -1 if reverse else 1
    ]
    ends = {}
    for model, (name, colour) in MODELS.items():
        y = [found[model][inside[i]].mean() for i in keep]
        ax.plot(
            range(len(keep)),
            y,
            "-o",
            color=colour,
            linewidth=2.2,
            markersize=6,
            markeredgecolor=SURFACE,
            markeredgewidth=1.3,
            label=name,
        )
        ends.setdefault(f"{y[-1]:.2f}", y[-1])
        worst = int(np.argmin(y))
        if model == "rail" and worst != len(y) - 1:
            ax.annotate(
                f"{y[worst]:.2f}",
                (worst, y[worst]),
                xytext=(7, -4),
                textcoords="offset points",
                fontsize=9,
                color=INK_2,
            )
    ax.set_ylim(-0.04, 1.08)
    ax.set_xlim(-0.4, len(keep) - 0.6)
    end_labels(ax, len(keep) - 1, [(y, text) for text, y in ends.items()])
    ax.set_xticks(range(len(keep)))
    ax.set_xticklabels(
        [f"{names[i]}\n{inside[i].sum():,}" for i in keep], fontsize=8.5, color=INK_2
    )


def legend(fig: plt.Figure, ax: plt.Axes, height: float, ncols: int = 3) -> None:
    """The detectors' legend under the figure's title"""
    fig.legend(
        *ax.get_legend_handles_labels(),
        loc="upper left",
        frameon=False,
        fontsize=10,
        ncols=ncols,
        labelcolor=INK_2,
        bbox_to_anchor=(0.03, 1 - 0.62 / height),
    )


def polar(ax: plt.Axes, title: str, rim: float = 8) -> None:
    """The bench seen from above: bearing round it, straight down at the centre"""
    ax.set_facecolor(SURFACE)
    ax.set_ylim(0, 90 - rim)
    rings = (75, 60, 45, 30, 15)
    ax.set_yticks([90 - e for e in rings])
    ax.set_yticklabels([f"{e}°" for e in rings], fontsize=7.5, color=MUTED)
    ax.set_rlabel_position(22)
    ax.set_xticks(np.radians(range(0, 360, 45)))
    ax.set_xticklabels([f"{a}°" for a in range(0, 360, 45)], color=MUTED, fontsize=8)
    ax.grid(color=GRID, linewidth=0.8)
    ax.spines["polar"].set_color(GRID)
    ax.set_title(title, fontsize=11.5, color=INK, pad=12)


# The dataset ---------------------------------------------------------------------


def pose_maps(frames: dict) -> None:
    """Where the camera stood, one map a camera family, every rendered frame"""
    fig = figure(
        16,
        5.6,
        "Where the camera stood in all 10,300 frames, by camera",
        "The bench from above. A dot's angle is the side the camera looks from; "
        "its distance from the centre is how steeply it looks down (centre = "
        "straight down, rim = level with the bench); its shade is how far it "
        "stands.",
    )
    dots = None
    for i, (camera, (name, _)) in enumerate(CAMERAS.items()):
        m = frames["camera"] == camera
        ax = fig.add_axes([0.04 + i * 0.232, 0.17, 0.17, 0.56], projection="polar")
        polar(ax, f"{name}\n{m.sum():,} frames")
        order = np.argsort(-frames["range_m"][m])
        dots = ax.scatter(
            np.radians(frames["bearing_deg"][m][order]),
            90 - frames["elevation_deg"][m][order],
            c=frames["range_m"][m][order],
            cmap=BLUES,
            vmin=0.35,
            vmax=3.5,
            s=5,
            linewidths=0,
        )
    bar = fig.colorbar(dots, cax=fig.add_axes([0.955, 0.25, 0.008, 0.45]))
    bar.set_label("distance, m", color=INK_2, fontsize=9)
    bar.ax.tick_params(length=0, colors=INK_2, labelsize=8)
    bar.outline.set_visible(False)
    save(fig, DEMO / "1_dataset" / "pose_maps_by_camera.png")


def pose_histograms(frames: dict) -> None:
    """Elevation, distance and bearing of the training frames, stacked by camera"""
    m = frames["selected_for_training"] == 1
    panels = (
        (
            "elevation_deg",
            np.arange(15, 91, 5),
            "Elevation above the bench, degrees",
            "How steeply the camera looks down",
        ),
        (
            "range_m",
            np.arange(0.25, 3.76, 0.25),
            "Distance to the bench, m",
            "How far it stands",
        ),
        (
            "bearing_deg",
            np.arange(0, 361, 30),
            "Bearing round the bench, degrees",
            "Which side it looks from",
        ),
    )
    fig = figure(
        16,
        5.4,
        f"The {m.sum():,} training frames by camera pose",
        "The wall camera is one pose: 40° up, 3.2 m away, one bearing. Everything "
        "else in the bars is what the previous detector never saw. A cap of 200 "
        "frames a pose cell keeps any one view from dominating.",
    )
    for i, (column, edges, xlabel, title) in enumerate(panels):
        ax = fig.add_axes([0.045 + i * 0.325, 0.2, 0.27, 0.56])
        style(ax, title)
        base = np.zeros(len(edges) - 1)
        for camera, (name, colour) in CAMERAS.items():
            counts, _ = np.histogram(
                frames[column][m & (frames["camera"] == camera)], edges
            )
            ax.bar(
                edges[:-1],
                counts,
                width=np.diff(edges) * 0.88,
                bottom=base,
                align="edge",
                color=colour,
                label=name,
                edgecolor=SURFACE,
                linewidth=0.8,
            )
            base += counts
        ax.set_xlabel(xlabel, color=INK_2, fontsize=9)
        ax.set_ylabel("frames", color=INK_2, fontsize=9)
        if not i:
            legend(fig, ax, 5.4, ncols=4)
    save(fig, DEMO / "1_dataset" / "training_frames_by_camera_pose.png")


def vial_sizes() -> None:
    """How tall a vial is in the image, a row a camera family"""
    data = json.loads((DATA / "vials.json").read_text())
    edges = data["height_edges_px"]
    names = span(edges)
    names[-1] = f"{edges[-2]}+"
    fig = figure(
        11,
        8.2,
        "How tall a vial is in the image, by camera",
        "Share of each camera's labelled vials, by the height in pixels of the "
        "whole vial in the 1920 × 1080 frame. The previous detector trained on "
        "the top row only.",
    )
    for i, (camera, (name, colour)) in enumerate(CAMERAS.items()):
        counts = np.array(data["heights_by_camera"][camera])
        ax = fig.add_axes([0.08, 0.76 - i * 0.2, 0.89, 0.125])
        style(ax, f"{name}: {counts.sum():,} vials")
        share = counts / counts.sum()
        ax.bar(range(len(share)), share, width=0.86, color=colour)
        for x, v in enumerate(share):
            if v >= 0.005:
                ax.annotate(
                    f"{v:.0%}",
                    (x, v),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                    color=INK_2,
                )
        ax.set_ylim(0, 0.36)
        ax.set_yticks([])
        ax.grid(False)
        ax.set_xlim(-0.6, len(share) - 0.4)
        ax.set_xticks(range(len(share)))
        ax.set_xticklabels(names if i == 3 else [], fontsize=8.5, color=INK_2)
    ax.set_xlabel("vial height, px", color=INK_2, fontsize=9)
    save(fig, DEMO / "1_dataset" / "vial_size_by_camera.png")


def benches(frames: dict) -> None:
    """How many vials a frame shows, and where on the worktop they stand"""
    data = json.loads((DATA / "vials.json").read_text())["bench_positions_training"]
    m = frames["use"] == "train"
    fig = figure(
        16,
        5.2,
        "The benches: from a handful of vials to eighty, all along the worktop",
        "Training frames. Left: labelled vials a frame, by bench layout. Right: "
        "the worktop from above, 10 cm cells; darker means more vials stood "
        "there. The scattered layouts use the whole 6 × 2 m worktop, the seeded "
        "patterns the strip the robot reaches; the dark cells are the scene's "
        "own fixed vials.",
    )
    ax = fig.add_axes([0.045, 0.19, 0.4, 0.57])
    style(ax, "Vials in a frame")
    edges = np.arange(0, 85, 5)
    layouts = (
        ("scatter", "scattered", "#2a78d6"),
        ("cluster", "one cluster", "#1baf7a"),
        ("as built", "as the scene is built", "#eda100"),
        ("patterns", "seeded patterns: rows, clusters, crowds", "#eb6834"),
    )
    base = np.zeros(len(edges) - 1)
    for key, name, colour in layouts:
        which = (
            np.isin(frames["bench"], ["rows", "clusters", "crowd"])
            if key == "patterns"
            else frames["bench"] == key
        )
        counts, _ = np.histogram(frames["vials"][m & which], edges)
        ax.bar(
            edges[:-1],
            counts,
            width=4.4,
            bottom=base,
            align="edge",
            color=colour,
            label=name,
            edgecolor=SURFACE,
            linewidth=0.8,
        )
        base += counts
    ax.set_xlabel("labelled vials in the frame", color=INK_2, fontsize=9)
    ax.set_ylabel("frames", color=INK_2, fontsize=9)
    ax.legend(loc="upper right", frameon=False, fontsize=8.5, labelcolor=INK_2)

    counts = np.array(data["counts"]).T
    xs, ys = np.array(data["x_edges"]), np.array(data["y_edges"])
    cols, rows = np.nonzero(counts.sum(0))[0], np.nonzero(counts.sum(1))[0]
    counts = counts[rows[0] : rows[-1] + 1, cols[0] : cols[-1] + 1]
    ax = fig.add_axes([0.52, 0.19, 0.42, 0.57])
    style(ax, "Where the vials stand on the worktop")
    ax.grid(False)
    image = ax.imshow(
        np.ma.masked_equal(counts, 0),
        cmap=BLUES,
        origin="lower",
        aspect="equal",
        vmin=0,
        vmax=np.percentile(counts, 99),
        extent=(xs[cols[0]], xs[cols[-1] + 1], ys[rows[0]], ys[rows[-1] + 1]),
    )
    ax.set_xlabel("along the bench, m", color=INK_2, fontsize=9)
    ax.set_ylabel("across, m", color=INK_2, fontsize=9)
    bar = fig.colorbar(image, cax=fig.add_axes([0.952, 0.3, 0.008, 0.35]))
    bar.set_label("vials", color=INK_2, fontsize=9)
    bar.ax.tick_params(length=0, colors=INK_2, labelsize=8)
    bar.outline.set_visible(False)
    save(fig, DEMO / "1_dataset" / "benches_vials_per_frame_and_positions.png")


def light_levels(frames: dict) -> None:
    """The light the training frames were rendered at, against the dim tests"""
    light = frames["light"]
    train = frames["selected_for_training"] == 1
    dim = frames["dark"] == 1
    edges = np.arange(0, 1.61, 0.05)
    fig = figure(
        12,
        5.0,
        "How bright the room is: what was trained on, what was tested",
        f"Light as a multiple of the scene's own. Training never goes under "
        f"{light[train].min():.0%}: no dark frame was trained on, by decision. "
        f"The two dim tests run from {light[dim].min():.0%} to "
        f"{light[dim].max():.0%}.",
    )
    ax = fig.add_axes([0.07, 0.2, 0.88, 0.56])
    style(ax, "Frames by room light")
    for mask, name, colour in (
        (train, f"training, {train.sum():,} frames", "#2a78d6"),
        (dim, f"dim tests, {dim.sum():,} frames", "#52514e"),
    ):
        counts, _ = np.histogram(light[mask], edges)
        ax.bar(
            edges[:-1],
            counts / mask.sum(),
            width=0.044,
            align="edge",
            color=colour,
            label=name,
        )
    ax.set_xticks(np.arange(0, 1.61, 0.2))
    ax.set_xticklabels([f"{v:.0%}" for v in np.arange(0, 1.61, 0.2)])
    ax.set_yticks([0, 0.05, 0.1, 0.15])
    ax.set_yticklabels(["0", "5 %", "10 %", "15 %"])
    ax.set_ylabel("share of the set's frames", color=INK_2, fontsize=9)
    ax.set_xlabel("room light", color=INK_2, fontsize=9)
    ax.legend(loc="upper right", frameon=False, fontsize=9.5, labelcolor=INK_2)
    save(fig, DEMO / "1_dataset" / "light_levels_trained_and_tested.png")


def splits(frames: dict) -> None:
    """Every rendered set, by what it is used for"""
    names = {
        "rail_train": "wall camera",
        "orbit_train": "any angle, 1–3.5 m",
        "close_train": "close, under 1 m",
        "low_train": "low, 15–30°",
        "rail_val": "wall camera",
        "orbit_val": "any angle",
        "close_val": "close",
        "low_val": "low",
        "rail_test": "wall camera",
        "rail_test_shift": "degraded camera",
        "pattern_test": "demo benches, wall camera",
        "lab_rail_test": "another lab, wall camera",
        "orbit_test": "any angle",
        "close_test": "close",
        "low_test": "low",
        "overhead_test": "straight down",
        "pattern_orbit_test": "demo benches, any angle",
        "lab_test": "another lab, any angle",
        "dark_test": "dim room, wall camera",
        "orbit_dark_test": "dim room, any angle",
    }
    uses = (
        ("train", "Rendered for training", "#2a78d6"),
        ("val", "Validation", "#1baf7a"),
        ("test", "Tests: never trained on, never used to pick anything", "#eda100"),
    )
    fig = figure(
        13,
        8.2,
        "Twenty sets, three uses, no frame seed shared between them",
        "Frames rendered a set. Of the 7,800 rendered for training, 5,844 are "
        "kept by the pose cap, and 750 of the 800 for validation. The ten demo "
        "benches appear only in tests.",
    )
    top = 0.9
    for use, title, colour in uses:
        keys = [
            k
            for k in names
            if (frames["split"] == k).any()
            and frames["use"][frames["split"] == k][0] == use
        ]
        height = 0.029 * len(keys)
        ax = fig.add_axes([0.27, top - height - 0.045, 0.66, height])
        style(ax, title)
        ax.grid(False)
        counts = [int((frames["split"] == k).sum()) for k in keys]
        ax.barh(range(len(keys)), counts, height=0.62, color=colour)
        for i, v in enumerate(counts):
            ax.annotate(
                f"{v:,}",
                (v, i),
                xytext=(7, 0),
                textcoords="offset points",
                va="center",
                fontsize=9,
                color=INK_2,
            )
        ax.set_yticks(range(len(keys)))
        ax.set_yticklabels([names[k] for k in keys], fontsize=9.5, color=INK_2)
        ax.invert_yaxis()
        ax.set_xlim(0, 3300)
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        top -= height + 0.08
    save(fig, DEMO / "1_dataset" / "sets_train_validation_test.png")


# The training --------------------------------------------------------------------


def schedule() -> None:
    """Learning rate, wall-clock time, and what an hour of training bought"""
    runs = {run: log(run) for run in ("25_epochs", "100_epochs")}
    fig = figure(
        16,
        5.2,
        "The two runs: same recipe, a learning rate that decays over the whole run",
        "One RTX 4090, batch 8, bench crop at 1920 px, AdamW, fine-tuned from "
        "the previous detector. The 25-epoch run is not the first quarter of "
        "the 100-epoch run: its rate falls four times as fast.",
    )
    panels = (
        (
            "Learning rate",
            "epoch",
            lambda r: r["epoch"],
            lambda r: r["lr/pg0"] * 1e3,
            "× 0.001",
        ),
        (
            "Time on the GPU",
            "epoch",
            lambda r: r["epoch"],
            lambda r: r["time"] / 3600,
            "hours",
        ),
        (
            "Validation AP50–95 against time spent",
            "hours of training",
            lambda r: r["time"] / 3600,
            lambda r: r["metrics/mAP50-95(B)"],
            "",
        ),
    )
    for i, (title, xlabel, fx, fy, unit) in enumerate(panels):
        ax = fig.add_axes([0.045 + i * 0.325, 0.2, 0.245, 0.56])
        style(ax, title)
        ends = []
        for run, rows in runs.items():
            name, colour = MODELS[run]
            x, y = np.array([fx(r) for r in rows]), np.array([fy(r) for r in rows])
            ax.plot(x, y, color=colour, linewidth=2.2, label=name)
            best = int(np.argmax([fitness(r) for r in rows]))
            if i == 2:
                ax.plot(
                    x[best],
                    y[best],
                    "o",
                    color=colour,
                    markersize=7,
                    markeredgecolor=SURFACE,
                    markeredgewidth=1.6,
                )
                ends.append((y[best], f"{y[best]:.3f}, {x[best] * 60:.0f} min"))
            elif i == 1:
                ends.append((y[-1], f"{int(y[-1])} h {round(y[-1] % 1 * 60):02d} min"))
        ax.set_xlabel(xlabel, color=INK_2, fontsize=9)
        if unit:
            ax.set_ylabel(unit, color=INK_2, fontsize=9)
        if i == 2:
            ax.set_ylim(0.85, 0.915)
            for (y, text), rows in zip(ends, runs.values(), strict=True):
                best = int(np.argmax([fitness(r) for r in rows]))
                ax.annotate(
                    text,
                    (rows[best]["time"] / 3600, y),
                    xytext=(0, 10),
                    textcoords="offset points",
                    fontsize=9,
                    color=INK_2,
                    ha="center",
                )
        elif ends:
            end_labels(ax, 100, ends[1:])
            ax.annotate(
                ends[0][1],
                (25, ends[0][0]),
                xytext=(6, 6),
                textcoords="offset points",
                fontsize=9,
                color=INK_2,
            )
        if i < 2:
            ax.set_xlim(1, 100)
            ax.set_xticks([1, 25, 50, 75, 100])
        if not i:
            legend(fig, ax, 5.2)
    save(fig, DEMO / "2_training" / "learning_rate_and_time.png")


def last_epochs() -> None:
    """The validation scores' last stretch, where the curves look flat at full scale"""
    rows = log("100_epochs")
    epoch = np.array([r["epoch"] for r in rows])
    best = int(np.argmax([fitness(r) for r in rows]))
    panels = (
        ("AP50–95", "metrics/mAP50-95(B)", "#eda100"),
        ("recall", "metrics/recall(B)", "#2a78d6"),
        ("precision", "metrics/precision(B)", "#eb6834"),
        ("AP50", "metrics/mAP50(B)", "#1baf7a"),
    )
    fig = figure(
        16,
        4.6,
        "The 100-epoch run up close: still improving after epoch 25, flat after 85",
        "Each panel on its own scale; on a 0-to-1 axis these curves are flat "
        f"from the third epoch. Dotted line: epoch {int(epoch[best])}, the "
        "checkpoint that is kept. Grey line: epoch 25.",
    )
    for i, (title, column, colour) in enumerate(panels):
        ax = fig.add_axes([0.04 + i * 0.245, 0.2, 0.2, 0.53])
        values = np.array([r[column] for r in rows])
        style(ax, f"Validation {title}: {values[best]:.4f}")
        ax.plot(epoch, values, color=colour, linewidth=2)
        ax.plot(
            epoch[best],
            values[best],
            "o",
            color=colour,
            markersize=7,
            markeredgecolor=SURFACE,
            markeredgewidth=1.6,
        )
        ax.axvline(epoch[best], color=MUTED, linewidth=0.9, linestyle=(0, (3, 3)))
        ax.axvline(25, color=GRID, linewidth=1.4)
        low = np.percentile(values, 4)
        ax.set_ylim(low, values.max() + 0.12 * (values.max() - low))
        ax.set_xlim(1, 100)
        ax.set_xticks([1, 25, 50, 75, 100])
        ax.set_xlabel("epoch", color=INK_2, fontsize=9)
    save(fig, DEMO / "2_training" / "validation_scores_up_close.png")


# The results ---------------------------------------------------------------------


def scoreboard(vials: dict, false_boxes: dict, found: dict) -> None:
    """All twelve tests pooled: vials missed and boxes that are not vials"""
    thresholds = json.loads((DATA / "scores.json").read_text())["thresholds"]
    frames = sum(
        json.loads((DATA / "tests.json").read_text())["frames_per_test"].values()
    )
    total = len(vials["test"])
    missed = {m: int((~found[m]).sum()) for m in MODELS}
    false = {
        m: int(
            (
                (false_boxes["model"] == m) & (false_boxes["score"] >= thresholds[m])
            ).sum()
        )
        for m in MODELS
    }
    fig = figure(
        13,
        4.6,
        f"All twelve tests together: {total:,} vials in {frames:,} frames",
        "Each detector at its own validation threshold. The dim-room tests are "
        "included; without them the retrained detectors miss about 120 "
        "vials.",
    )
    for k, (title, values) in enumerate(
        (("Vials missed", missed), ("Boxes that are not vials", false))
    ):
        ax = fig.add_axes([0.2 + k * 0.49, 0.2, 0.26, 0.55])
        style(ax, title)
        ax.grid(False)
        for i, (model, (_name, colour)) in enumerate(MODELS.items()):
            ax.barh(i, values[model], height=0.58, color=colour)
            share = f"  ({values[model] / total:.1%})" if not k else ""
            ax.annotate(
                f"{values[model]:,}{share}",
                (values[model], i),
                xytext=(8, 0),
                textcoords="offset points",
                va="center",
                fontsize=13,
                color=INK,
                weight="bold",
            )
        ax.set_yticks(range(3))
        ax.set_yticklabels(
            [name for name, _ in MODELS.values()] if not k else [],
            fontsize=10,
            color=INK_2,
        )
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        ax.set_xlim(0, max(values.values()) * 1.05)
    save(fig, DEMO / "3_results" / "scoreboard_missed_and_false.png")


def by_size(vials: dict, found: dict) -> None:
    """Recall against the vial's height in the image"""
    edges = [0, 12, 16, 20, 24, 32, 48, 64, 96, 160, 400]
    names = span(edges)
    names[0], names[-1] = "under 12", "160+"
    bright = ~np.isin(vials["test"], DIM)
    wall = np.percentile(vials["height_px"][vials["test"] == "rail_test"], [1, 99])
    fig = figure(
        13,
        5.8,
        "The previous detector only knew vials the size the wall camera shows them",
        f"Recall by the vial's height in the 1920 × 1080 frame; under each bin, "
        f"the test vials in it. Ten bright tests. From the wall camera a vial is "
        f"{wall[0]:.0f} to {wall[1]:.0f} px tall: past that the previous detector "
        f"had never seen one.",
    )
    ax = fig.add_axes([0.06, 0.22, 0.87, 0.52])
    style(ax, "Recall by vial height, px")
    recall_lines(ax, vials["height_px"], edges, names, found, bright)
    legend(fig, ax, 5.8)
    save(fig, DEMO / "3_results" / "recall_by_vial_size.png")


def by_pose(vials: dict, found: dict) -> None:
    """Recall against the camera's elevation and distance, moving-camera tests"""
    moving = np.isin(vials["test"], MOVING)
    fig = figure(
        15,
        5.8,
        "Recall as the camera tilts and nears",
        "The six bright tests with a moving camera; under each bin, the test "
        "vials in it. The previous detector was trained at 40° and 3.2 m "
        "only.",
    )
    for i, (column, edges, unit, digits, title) in enumerate(
        (
            (
                "elevation_deg",
                [14, 20, 30, 45, 60, 75, 90],
                "°",
                0,
                "By elevation above the bench",
            ),
            (
                "range_m",
                [0.3, 0.5, 0.75, 1, 1.5, 2, 2.5, 3, 3.6],
                " m",
                2,
                "By distance to the bench",
            ),
        )
    ):
        ax = fig.add_axes([0.05 + i * 0.49, 0.22, 0.41, 0.52])
        style(ax, title)
        names = [
            n.replace(".00", "").replace("0 m", " m") if digits else n
            for n in span(edges, unit, digits)
        ]
        recall_lines(ax, vials[column], edges, names, found, moving)
        if not i:
            legend(fig, ax, 5.8)
    save(fig, DEMO / "3_results" / "recall_by_elevation_and_distance.png")


def pose_grid(vials: dict, found: dict) -> None:
    """Recall in every elevation by distance cell, before and after"""
    elevation, distance = [15, 30, 45, 60, 75, 90], [0.35, 0.6, 1, 1.75, 2.5, 3.5]
    moving = np.isin(vials["test"], MOVING)
    fig = figure(
        14,
        6.2,
        "Recall in every camera pose: before and after",
        "The six bright tests with a moving camera. Each cell is an elevation by "
        "distance band with at least 40 test vials; the number is the share "
        "found. Blank cells are poses the room does not allow: the ceiling, the "
        "walls.",
    )
    for k, model in enumerate(("rail", "100_epochs")):
        ax = fig.add_axes([0.07 + k * 0.46, 0.2, 0.36, 0.56])
        style(ax, MODELS[model][0])
        ax.grid(False)
        cells = np.full((len(elevation) - 1, len(distance) - 1), np.nan)
        for i in range(len(elevation) - 1):
            for j in range(len(distance) - 1):
                m = (
                    moving
                    & (vials["elevation_deg"] >= elevation[i])
                    & (vials["elevation_deg"] < elevation[i + 1] + (i == 4))
                    & (vials["range_m"] >= distance[j])
                    & (vials["range_m"] < distance[j + 1] + (j == 4))
                )
                if m.sum() >= 40:
                    cells[i, j] = found[model][m].mean()
        image = ax.imshow(
            np.ma.masked_invalid(cells),
            cmap=BLUES,
            vmin=0,
            vmax=1,
            origin="lower",
            aspect="auto",
        )
        for (i, j), v in np.ndenumerate(cells):
            if not np.isnan(v):
                ax.text(
                    j,
                    i,
                    f"{v:.2f}",
                    ha="center",
                    va="center",
                    fontsize=11,
                    color="#ffffff" if v > 0.55 else INK,
                )
        ax.set_xticks(range(len(distance) - 1))
        ax.set_xticklabels(
            [f"{a:g}–{b:g}" for a, b in zip(distance[:-1], distance[1:], strict=False)],
            fontsize=9,
            color=INK_2,
        )
        ax.set_yticks(range(len(elevation) - 1))
        ax.set_yticklabels(
            [f"{a}–{b}°" for a, b in zip(elevation[:-1], elevation[1:], strict=False)],
            fontsize=9,
            color=INK_2,
        )
        ax.set_xlabel("distance to the bench, m", color=INK_2, fontsize=9)
        if not k:
            ax.set_ylabel("elevation above the bench", color=INK_2, fontsize=9)
        ax.spines["bottom"].set_visible(False)
    bar = fig.colorbar(image, cax=fig.add_axes([0.925, 0.27, 0.009, 0.42]))
    bar.set_label("recall", color=INK_2, fontsize=9)
    bar.ax.tick_params(length=0, colors=INK_2, labelsize=8)
    bar.outline.set_visible(False)
    save(fig, DEMO / "3_results" / "recall_by_pose_cell_before_and_after.png")


def misses_on_the_map(vials: dict, found: dict) -> None:
    """Every bright test frame on the pose map, shaded by the share of vials missed"""
    bright = ~np.isin(vials["test"], DIM)
    names, first, index = np.unique(
        vials["frame"][bright], return_index=True, return_inverse=True
    )
    count = np.bincount(index)
    bearing = vials["bearing_deg"][bright][first]
    elevation = vials["elevation_deg"][bright][first]
    fig = figure(
        13,
        6.6,
        "Where vials were missed: every bright test frame on the pose map",
        f"{len(names):,} test frames, each a dot where its camera stood (centre = "
        "straight down, rim = level with the bench). The darker and larger the "
        "dot, the larger the share of that frame's vials the detector "
        "missed.",
    )
    dots = None
    for k, model in enumerate(("rail", "100_epochs")):
        missed = np.bincount(index, weights=~found[model][bright]) / count
        order = np.argsort(missed)
        ax = fig.add_axes([0.04 + k * 0.45, 0.13, 0.4, 0.62], projection="polar")
        whole = int((missed == 0).sum())
        polar(
            ax,
            f"{MODELS[model][0]}\n"
            f"every vial found in {whole:,} of {len(names):,} frames",
        )
        dots = ax.scatter(
            np.radians(bearing[order]),
            90 - elevation[order],
            c=missed[order],
            cmap=BLUES,
            vmin=0,
            vmax=1,
            s=7 + 60 * missed[order],
            linewidths=0,
        )
    bar = fig.colorbar(dots, cax=fig.add_axes([0.935, 0.25, 0.009, 0.4]))
    bar.set_label("share of the frame's vials missed", color=INK_2, fontsize=9)
    bar.ax.tick_params(length=0, colors=INK_2, labelsize=8)
    bar.outline.set_visible(False)
    save(fig, DEMO / "3_results" / "missed_vials_on_the_pose_map.png")


def by_darkness(vials: dict, found: dict, frames: dict) -> None:
    """Recall against the room's light: the dim tests binned, and the light sweep"""
    dim = np.isin(vials["test"], DIM)
    edges = [0.07, 0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]
    names = [
        f"{a:.3g}–{b:.3g} %"
        for a, b in zip(
            np.array(edges[:-1]) * 100, np.array(edges[1:]) * 100, strict=False
        )
    ]
    floor = frames["light"][frames["selected_for_training"] == 1].min()
    fig = figure(
        16,
        6.0,
        "How dark can the room get",
        f"No frame under {floor:.0%} light was trained on, by decision, yet the "
        "retrained detector holds to 15 %. Under about 12 % every detector goes "
        "blind, the previous one and the retrained one alike.",
    )
    ax = fig.add_axes([0.045, 0.22, 0.5, 0.5])
    style(ax, "The two dim-room tests, by the light each frame was rendered at")
    recall_lines(ax, vials["light"], edges, names, found, dim, reverse=True)
    ax.set_xlabel(
        "room light left; under it, the test vials in the bin", color=INK_2, fontsize=9
    )
    legend(fig, ax, 6.0)

    sweeps = json.loads((DATA / "limits.json").read_text())
    ax = fig.add_axes([0.63, 0.22, 0.3, 0.5])
    style(ax, "The same 12 benches as the light goes")
    series = (
        ("rail_at_0.10", "#eb6834", "-", "previous, threshold 0.10"),
        ("100_epochs_at_0.10", "#2a78d6", (0, (4, 2)), "retrained, threshold 0.10"),
        ("100_epochs_at_0.52", "#2a78d6", "-", "retrained, threshold 0.52"),
    )
    for key, colour, dash, name in series:
        rows = sweeps[key]["light"]
        ax.plot(
            [r["level"] for r in rows],
            [r["recall"] for r in rows],
            marker="o",
            color=colour,
            linestyle=dash,
            linewidth=2.2,
            markersize=5.5,
            markeredgecolor=SURFACE,
            markeredgewidth=1.2,
            label=name,
        )
    ax.axvspan(floor, 1.0, color=GRID, alpha=0.6, linewidth=0)
    ax.annotate("trained on", (0.74, 0.62), fontsize=9, color=INK_2, ha="center")
    ax.set_xscale("log")
    ax.set_xticks([0.03, 0.06, 0.1, 0.15, 0.3, 1.0])
    ax.set_xticklabels(["3 %", "6 %", "10 %", "15 %", "30 %", "100 %"])
    ax.minorticks_off()
    ax.invert_xaxis()
    ax.set_ylim(-0.04, 1.08)
    ax.set_xlabel("room light left", color=INK_2, fontsize=9)
    ax.legend(loc="lower left", frameon=False, fontsize=8.5, labelcolor=INK_2)
    save(fig, DEMO / "3_results" / "recall_by_darkness.png")


def by_difficulty(vials: dict, found: dict) -> None:
    """Recall against occlusion, crowding and position in the frame"""
    bright = ~np.isin(vials["test"], DIM)
    moving = np.isin(vials["test"], MOVING)
    fig = figure(
        16,
        5.8,
        "What makes a vial hard: hidden, crowded, or off to the side",
        "Bright tests; under each bin, the test vials in it. What is left for the "
        "retrained detector is occlusion: a vial half hidden behind another. "
        "Those are the wrist camera's to read.",
    )
    panels = (
        (
            "visible",
            [0.49, 0.7, 0.9, 0.999, 1.0],
            ["50–70 %", "70–90 %", "90–99 %", "fully\nvisible"],
            bright,
            "By how much of the vial shows",
        ),
        (
            "vials_in_frame",
            [0, 10, 20, 30, 45, 60, 100],
            ["1–10", "11–20", "21–30", "31–45", "46–60", "61+"],
            bright,
            "By vials in the frame",
        ),
        (
            "off_centre",
            [-0.01, 0.2, 0.4, 0.6, 0.8, 1.1],
            ["centre", "", "half way", "", "corner"],
            moving,
            "By position in the frame, moving camera",
        ),
    )
    for i, (column, edges, names, mask, title) in enumerate(panels):
        ax = fig.add_axes([0.04 + i * 0.325, 0.22, 0.265, 0.52])
        style(ax, title)
        recall_lines(ax, vials[column], edges, names, found, mask)
        if not i:
            legend(fig, ax, 5.8)
    save(fig, DEMO / "3_results" / "recall_by_occlusion_crowding_position.png")


def by_bench_and_lab(vials: dict, found: dict) -> None:
    """Recall on each bench layout and in the lab as it is and varied"""
    bright = ~np.isin(vials["test"], DIM)
    rows = [
        ("scattered", vials["bench"] == "scatter"),
        ("one cluster", vials["bench"] == "cluster"),
        ("as the scene is built", vials["bench"] == "as built"),
        ("rows (pattern)", vials["bench"] == "rows"),
        ("several clusters (pattern)", vials["bench"] == "clusters"),
        ("crowded (pattern)", vials["bench"] == "crowd"),
        None,
        ("the lab as it is", vials["lab_varied"] == 0),
        ("the lab varied", vials["lab_varied"] == 1),
    ]
    fig = figure(
        11.5,
        6.4,
        "No bench layout and no lab is left behind",
        "Bright tests; right of each row, the test vials in it. Dots, not bars: "
        "the axis starts at 0.80.",
    )
    ax = fig.add_axes([0.24, 0.16, 0.62, 0.6])
    style(ax, "Recall by bench layout, and by lab")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    for y, row in enumerate(rows):
        if row is None:
            continue
        m = bright & row[1]
        values = [found[model][m].mean() for model in MODELS]
        ax.plot([min(values), max(values)], [y, y], color=GRID, linewidth=2.4, zorder=1)
        for value, (name, colour) in zip(values, MODELS.values(), strict=True):
            ax.plot(
                value,
                y,
                "o",
                color=colour,
                markersize=10,
                markeredgecolor=SURFACE,
                markeredgewidth=1.6,
                label=name if not y else None,
                zorder=2,
            )
        ax.annotate(
            f"{values[0]:.2f}",
            (values[0], y),
            xytext=(-11, 0),
            textcoords="offset points",
            ha="right",
            va="center",
            fontsize=9,
            color=INK_2,
        )
        ax.annotate(
            f"{values[2]:.3f}   {m.sum():,} vials",
            (1.0, y),
            xytext=(14, 0),
            textcoords="offset points",
            va="center",
            fontsize=9,
            color=INK_2,
            annotation_clip=False,
        )
    ax.set_yticks([y for y, row in enumerate(rows) if row])
    ax.set_yticklabels([row[0] for row in rows if row], fontsize=10, color=INK_2)
    ax.invert_yaxis()
    ax.set_xlim(0.8, 1.004)
    ax.set_xticks([0.8, 0.85, 0.9, 0.95, 1.0])
    ax.spines["bottom"].set_visible(False)
    legend(fig, ax, 6.4)
    save(fig, DEMO / "3_results" / "recall_by_bench_layout_and_lab.png")


def by_threshold(vials: dict, false_boxes: dict) -> None:
    """Recall and false boxes as the threshold moves, all twelve tests pooled"""
    thresholds = json.loads((DATA / "scores.json").read_text())["thresholds"]
    frames = sum(
        json.loads((DATA / "tests.json").read_text())["frames_per_test"].values()
    )
    steps = np.arange(0.05, 0.96, 0.01)
    fig = figure(
        15,
        5.6,
        "How much the threshold matters",
        "All twelve tests pooled. Markers: the threshold each detector runs at, "
        "picked for best F1 on validation frames. The retrained detector's "
        "curves are flat round its marker: the exact value is not "
        "critical.",
    )
    for k, title in enumerate(
        ("Recall: share of the vials found", "False boxes a frame (log scale)")
    ):
        ax = fig.add_axes([0.05 + k * 0.49, 0.2, 0.41, 0.55])
        style(ax, title)
        for model, (name, colour) in MODELS.items():
            scores = (
                np.nan_to_num(vials[f"score_{model}"])
                if not k
                else false_boxes["score"][false_boxes["model"] == model]
            )
            counts = np.array([(scores >= t).sum() for t in steps])
            y = counts / (len(scores) if not k else frames)
            y = np.where(y > 0, y, np.nan)
            ax.plot(steps, y, color=colour, linewidth=2.2, label=name)
            at = int(np.argmin(abs(steps - thresholds[model])))
            ax.plot(
                steps[at],
                y[at],
                "o",
                color=colour,
                markersize=8,
                markeredgecolor=SURFACE,
                markeredgewidth=1.6,
            )
            ax.annotate(
                f"{y[at]:.3f}" if not k else f"{y[at]:.2f}",
                (steps[at], y[at]),
                xytext=(0, 9 if model != "rail" or k else -17),
                textcoords="offset points",
                ha="center",
                fontsize=9,
                color=INK_2,
            )
        if k:
            ax.set_yscale("log")
            ax.set_yticks([0.01, 0.1, 1, 10])
            ax.set_yticklabels(["0.01", "0.1", "1", "10"])
            ax.set_ylim(0.004, 14)
            ax.minorticks_off()
        else:
            ax.set_ylim(0.6, 1.02)
            legend(fig, ax, 5.6)
        ax.set_xlim(0.05, 0.95)
        ax.set_xlabel("confidence threshold", color=INK_2, fontsize=9)
    save(fig, DEMO / "3_results" / "threshold_sensitivity.png")


def main() -> None:
    """Draw every detailed figure"""
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK})
    frames, vials = table("frames.csv"), table("test_vials.csv")
    false_boxes = table("test_false_boxes.csv")
    found = found_by(vials)
    pose_maps(frames)
    pose_histograms(frames)
    vial_sizes()
    benches(frames)
    light_levels(frames)
    splits(frames)
    schedule()
    last_epochs()
    scoreboard(vials, false_boxes, found)
    by_size(vials, found)
    by_pose(vials, found)
    pose_grid(vials, found)
    misses_on_the_map(vials, found)
    by_darkness(vials, found, frames)
    by_difficulty(vials, found)
    by_bench_and_lab(vials, found)
    by_threshold(vials, false_boxes)


if __name__ == "__main__":
    main()
