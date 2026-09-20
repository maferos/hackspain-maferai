"""Draw the figures of ``docs/demo`` about the rest of the vision pipeline

:mod:`demo_figures` and :mod:`demo_figures_detail` cover the trained bench
detector. This module draws what surrounds it: how the detector was chosen, how a
bottle is named from its label, and how a box becomes a point on the bench.

    python scripts/demo_figures_pipeline.py   # vision_pipeline.json -> docs/demo/*/

Every number is copied from the document named in its block's ``source`` in
``numbers/vision_pipeline.json``; nothing is measured here.
"""

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from demo_figures import (  # noqa: E402
    DATA,
    DEMO,
    GRID,
    INK,
    INK_2,
    MUTED,
    SURFACE,
    save,
    style,
)
from demo_figures_detail import figure  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

ORANGE, VIOLET, TEAL, YELLOW = "#eb6834", "#7b61d9", "#0e9fa8", "#eda100"
TRAINED, WORLD, COCO = ORANGE, VIOLET, TEAL
"""Ours, the open-vocabulary detector and the fixed-class one, on every figure."""
EAN, ARUCO = VIOLET, TEAL
CHOICE, IDENTITY, POSITION = (
    DEMO / "4_detector_choice",
    DEMO / "5_identity",
    DEMO / "6_position",
)


def label_bars(
    ax: plt.Axes, xs, values, fmt: str = "{:.2f}", size: float = 8.5, at=None
) -> None:
    """The value over each bar, or over ``at`` when the bar's top is elsewhere"""
    for x, v, y in zip(xs, values, at or values, strict=True):
        if v is not None:
            ax.annotate(
                fmt.format(v),
                (x, y),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                fontsize=size,
                color=INK_2,
            )


def top_legend(fig: plt.Figure, ax: plt.Axes, height: float, ncols: int = 3) -> None:
    """The legend under the figure's title"""
    fig.legend(
        *ax.get_legend_handles_labels(),
        loc="upper left",
        frameon=False,
        fontsize=10,
        ncols=ncols,
        labelcolor=INK_2,
        bbox_to_anchor=(0.03, 1 - 0.62 / height),
    )


# Choosing the detector -----------------------------------------------------------


def accuracy_against_speed(d: dict) -> None:
    """Fourteen pretrained detectors on real lab photographs: AP against time"""
    rows = d["zero_shot_real_photos"]["rows"]
    colours = {"open vocabulary": VIOLET, "fixed classes": TEAL, "no prompts": YELLOW}
    fig = figure(
        13,
        7.2,
        "Step one, nothing trained: fourteen pretrained detectors on real lab "
        "photographs",
        "5 photographs, 11 hand-annotated flasks, a 12-thread CPU, 640 px unless "
        "stated. Up and to the left is better. The large models that read a text "
        "prompt (Grounding DINO, OWLv2) take 9 to 13 s a frame; YOLO-World L scores "
        "higher in about one. With 11 flasks, each moves recall by 9 %.",
    )
    ax = fig.add_axes([0.07, 0.17, 0.88, 0.62])
    style(ax, "Average precision against time a frame on a CPU")
    nudge = {
        "YOLO-World S|everyday": (8, 6),
        "YOLO-World S|laboratory": (6, -15),
        "YOLO-World S @960|laboratory": (4, 9),
        "YOLOE-11 S @960|laboratory": (10, -3),
        "YOLOE-11 S|everyday": (-9, -3),
        "YOLO11 S COCO|": (-8, 8),
        "YOLO11 S COCO @960|": (8, -12),
        "FastSAM S|": (8, -4),
        "YOLO-World L|laboratory": (8, -12),
    }
    seen = set()
    for r in rows:
        family = r["family"]
        ax.plot(
            r["ms"] / 1000,
            r["ap"],
            "o",
            color=colours[family],
            markersize=10,
            markeredgecolor=SURFACE,
            markeredgewidth=1.6,
            label=None if family in seen else family,
        )
        seen.add(family)
        dx, dy = nudge.get(f"{r['model']}|{r['prompts']}", (8, 6))
        text = r["model"] + (f", {r['prompts']} words" if r["prompts"] else "")
        ax.annotate(
            text,
            (r["ms"] / 1000, r["ap"]),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=8.5,
            color=INK_2,
            ha="left" if dx > 0 else "right",
        )
    ax.set_xscale("log")
    ax.set_xticks([0.4, 1, 2, 5, 10])
    ax.set_xticklabels(["0.4 s", "1 s", "2 s", "5 s", "10 s"])
    ax.minorticks_off()
    ax.set_xlim(0.16, 40)
    ax.set_ylim(0.3, 1.0)
    ax.set_xlabel("time a frame, log scale", color=INK_2, fontsize=9)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, labelcolor=INK_2)
    save(fig, CHOICE / "pretrained_accuracy_against_speed.png")


def prompts(d: dict) -> None:
    """The same open-vocabulary model with two vocabularies, on two image sets"""
    p = d["prompts"]
    fig = figure(
        13,
        5.0,
        "With an open-vocabulary detector, the words matter more than the model",
        "The same YOLO-World L both times. On real photographs, everyday words beat "
        "laboratory words: “cup” has millions of training examples, “beaker” a few "
        "dozen. On our renders, naming the samples beats naming vessels.",
    )
    for k, (key, title, unit) in enumerate(
        (
            ("real_photo_recall", "Real lab photographs: recall", "recall"),
            ("fixed_camera_ap50", "Our wall camera's renders: AP50", "AP50"),
        )
    ):
        ax = fig.add_axes([0.3 + k * 0.4, 0.26, 0.2, 0.5])
        style(ax, title)
        names, values = list(p[key]), list(p[key].values())
        ax.bar(range(2), values, width=0.55, color=[MUTED, VIOLET])
        label_bars(ax, range(2), values, size=11)
        ax.set_xticks(range(2))
        ax.set_xticklabels(
            [n.replace(": ", ":\n").replace(", ", ",\n", 1) for n in names],
            fontsize=8.5,
            color=INK_2,
        )
        ax.set_ylim(0, 1.15)
        ax.set_ylabel(unit, color=INK_2, fontsize=9)
    save(fig, CHOICE / "prompts_matter.png")


def size_floor(d: dict) -> None:
    """Recall against the flask's side in pixels, and the kit's side from the wall"""
    sides, kit = d["recall_by_side_real_photos"], d["kit_side_from_the_wall"]
    fig = figure(
        15,
        5.8,
        "The size floor: a pretrained detector needs about 48 px, and our camera gives "
        "19 to 48",
        "Left: real photographs shrunk to seven scales. Right: the side (square root "
        "of width × height) of each bottle of the kit from the wall camera, 3.23 m "
        "away. At 1080p only the 2 L bottle reaches the floor. That is why a detector "
        "was trained.",
    )
    ax = fig.add_axes([0.05, 0.2, 0.42, 0.52])
    style(ax, "Share of the flasks found, by their side at the network input")
    for (name, values), colour in zip(
        sides["models"].items(), (VIOLET, YELLOW, TEAL, ORANGE), strict=True
    ):
        ax.plot(
            range(4),
            values,
            "-o",
            color=colour,
            linewidth=2.2,
            markersize=6,
            markeredgecolor=SURFACE,
            markeredgewidth=1.3,
            label=name,
        )
    ax.set_xticks(range(4))
    ax.set_xticklabels(sides["bins"], color=INK_2)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right", frameon=False, fontsize=8.5, labelcolor=INK_2)

    ax = fig.add_axes([0.58, 0.2, 0.37, 0.52])
    style(ax, "Side of the kit's bottles from the wall camera, px")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ys = range(len(kit["bottles"]))
    ax.axvspan(0, kit["reliable_from_px"], color=GRID, alpha=0.55, linewidth=0)
    ax.annotate(
        "under 48 px:\na coin toss, then lost",
        (2, 4.4),
        fontsize=9,
        color=INK_2,
        va="top",
    )
    for y, a, b in zip(ys, kit["side_px_1080p"], kit["side_px_4k"], strict=True):
        ax.plot([a, b], [y, y], color=MUTED, linewidth=1.6, zorder=1)
    ax.plot(
        kit["side_px_1080p"],
        ys,
        "o",
        color=ORANGE,
        markersize=10,
        label="1080p",
        markeredgecolor=SURFACE,
        markeredgewidth=1.6,
    )
    ax.plot(
        kit["side_px_4k"],
        ys,
        "o",
        color=TEAL,
        markersize=10,
        label="4K",
        markeredgecolor=SURFACE,
        markeredgewidth=1.6,
    )
    ax.set_yticks(list(ys))
    ax.set_yticklabels(kit["bottles"], color=INK_2, fontsize=10)
    ax.set_xlim(0, 105)
    ax.set_ylim(-0.6, 4.6)
    ax.spines["bottom"].set_visible(False)
    ax.legend(loc="lower right", frameon=False, fontsize=9.5, labelcolor=INK_2)
    save(fig, CHOICE / "size_floor.png")


def distance(d: dict) -> None:
    """Bottles found by distance to the wall camera, renders at 1080p"""
    data = d["found_by_distance_renders"]
    fig = figure(
        11,
        5.2,
        "Past 3.5 m a pretrained detector loses the small bottles",
        "347 rendered bottles on a 6 m bench, 1080p, nothing trained; under each "
        "band, the bottles in it. Whenever a bottle was found its size class could be "
        "told by geometry (82 to 100 %): what fails at a distance is finding it.",
    )
    ax = fig.add_axes([0.08, 0.24, 0.8, 0.5])
    style(ax, "Share of the bottles found")
    for (name, values), colour in zip(
        data["found"].items(), (WORLD, COCO), strict=True
    ):
        ax.plot(
            range(4),
            values,
            "-o",
            color=colour,
            linewidth=2.2,
            markersize=7,
            markeredgecolor=SURFACE,
            markeredgewidth=1.4,
            label=name,
        )
        ax.annotate(
            f"{values[-1]:.0%}",
            (3, values[-1]),
            xytext=(9, -3),
            textcoords="offset points",
            fontsize=9.5,
            color=INK_2,
        )
    ax.set_xticks(range(4))
    ax.set_xticklabels(
        [f"{b}\n{n}" for b, n in zip(data["bins"], data["n"], strict=True)], color=INK_2
    )
    ax.set_ylim(0, 1.05)
    ax.set_xlim(-0.3, 3.4)
    top_legend(fig, ax, 5.2)
    save(fig, CHOICE / "found_by_distance.png")


def three_models(d: dict) -> None:
    """One epoch of fine-tuning against the best pretrained detectors, three splits"""
    data = d["fixed_camera_three_models"]
    colours = (TRAINED, WORLD, COCO)
    splits = list(data["splits"])
    fig = figure(
        16,
        6.0,
        "Step two: one epoch of fine-tuning on a laptop CPU already matches the best "
        "pretrained detector",
        "The same 30 frames a split for the three models, each at the threshold it "
        "chose on validation; whiskers are 95 % intervals. Fine-tuned on "
        "simulator-labelled crops of one scene: level on that scene, the most robust "
        "to a degraded camera, a little behind on a scene it never saw.",
    )
    width = 0.26
    for k, (field, title) in enumerate(
        (("ap50", "AP50"), ("recall", "Recall"), ("false", "False boxes a frame"))
    ):
        ax = fig.add_axes([0.045 + k * 0.325, 0.2, 0.28, 0.52])
        style(ax, title)
        for j, (name, colour) in enumerate(zip(data["models"], colours, strict=True)):
            values = [data["splits"][s][field][j] for s in splits]
            xs = np.arange(len(splits)) + (j - 1) * width
            ax.bar(xs, values, width=width - 0.035, color=colour, label=name)
            if field == "ap50":
                low = [data["splits"][s]["low"][j] for s in splits]
                high = [data["splits"][s]["high"][j] for s in splits]
                ax.errorbar(
                    xs,
                    values,
                    yerr=[np.subtract(values, low), np.subtract(high, values)],
                    fmt="none",
                    ecolor=INK,
                    elinewidth=1.1,
                    capsize=2.5,
                )
                label_bars(ax, xs, values, size=8, at=high)
            else:
                label_bars(
                    ax, xs, values, "{:.2f}" if field == "recall" else "{:.1f}", 8
                )
        ax.set_xticks(range(len(splits)))
        ax.set_xticklabels(
            [s.replace(", ", ",\n") for s in splits], color=INK_2, fontsize=9
        )
        ax.margins(y=0.15)
        if not k:
            top_legend(fig, ax, 6.0)
    save(fig, CHOICE / "fine_tuned_against_pretrained.png")


def by_bottle_and_size(d: dict) -> None:
    """Recall of the three models by bottle of the kit and by apparent size"""
    data = d["fixed_camera_three_models"]
    colours = (TRAINED, WORLD, COCO)
    fig = figure(
        16,
        5.8,
        "Where training pays: the smallest bottles",
        "The robot's scene, 30 frames, 334 bottles; under each group, the bottles in "
        "it. The gap is under 24 px of side, which is the whole amber kit up to 50 ml. "
        "The 10 ml flask, 8 × 15 px from the wall, is still missed one time in four: a "
        "camera limit, not a model one.",
    )
    for k, (key, labels, title) in enumerate(
        (
            ("recall_by_bottle", "bottles", "Recall by bottle of the kit"),
            ("recall_by_side", "bins", "Recall by side of the bottle in the frame"),
        )
    ):
        block = data[key]
        ax = fig.add_axes([0.045 + k * 0.56, 0.22, 0.5 if not k else 0.36, 0.5])
        style(ax, title)
        for name, values, colour in zip(
            data["models"], block["recall"], colours, strict=True
        ):
            ax.plot(
                range(len(values)),
                values,
                "-o",
                color=colour,
                linewidth=2.2,
                markersize=6,
                markeredgecolor=SURFACE,
                markeredgewidth=1.3,
                label=name,
            )
        ax.set_xticks(range(len(block[labels])))
        ax.set_xticklabels(
            [
                f"{b.replace(' ', chr(10), 1) if not k else b}\n{n}"
                for b, n in zip(block[labels], block["n"], strict=True)
            ],
            fontsize=8.5,
            color=INK_2,
        )
        ax.set_ylim(0, 1.05)
        if not k:
            top_legend(fig, ax, 5.8)
    save(fig, CHOICE / "recall_by_bottle_and_size.png")


def worktop_filter(d: dict) -> None:
    """False boxes a frame before and after the worktop filter"""
    data = d["worktop_filter"]
    fig = figure(
        11,
        5.0,
        "A calibrated camera removes nine false boxes in ten without losing a bottle",
        "The worktop filter back-projects the bottom edge of each box onto the bench "
        "plane and drops what does not stand on the bench: the shelf library, "
        "glassware, the balance. On the fixed camera precision goes from 33 % to 82 %.",
    )
    ax = fig.add_axes([0.1, 0.24, 0.8, 0.5])
    style(ax, "False boxes a frame, YOLO-World L")
    xs = np.arange(2)
    ax.bar(xs - 0.17, data["before"], width=0.3, color=MUTED, label="every box")
    ax.bar(
        xs + 0.17,
        data["after"],
        width=0.3,
        color=TRAINED,
        label="boxes standing on the bench",
    )
    label_bars(ax, xs - 0.17, data["before"], "{:g}", 10.5)
    label_bars(ax, xs + 0.17, data["after"], "{:g}", 10.5)
    ax.set_xticks(xs)
    ax.set_xticklabels(data["cameras"], color=INK_2, fontsize=10)
    ax.margins(y=0.15)
    ax.legend(loc="upper right", frameon=False, fontsize=9.5, labelcolor=INK_2)
    save(fig, CHOICE / "worktop_filter.png")


# Naming the bottle ---------------------------------------------------------------


def dumbbell(ax: plt.Axes, names: list[str], a: list, b: list, fmt: str) -> None:
    """EAN-13 against ArUco, a row a vessel"""
    ys = range(len(names))
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    for y, u, v in zip(ys, a, b, strict=True):
        ax.plot([u, v], [y, y], color=GRID, linewidth=2.4, zorder=1)
        for value, side in ((u, -1 if u < v else 1), (v, 1 if u < v else -1)):
            ax.annotate(
                fmt.format(value),
                (value, y),
                xytext=(10 * side, 0),
                textcoords="offset points",
                va="center",
                fontsize=8.5,
                ha="left" if side > 0 else "right",
                color=INK_2,
            )
    ax.plot(
        a,
        ys,
        "o",
        color=EAN,
        markersize=9,
        markeredgecolor=SURFACE,
        markeredgewidth=1.5,
        label="EAN-13 barcode label",
        zorder=2,
    )
    ax.plot(
        b,
        ys,
        "o",
        color=ARUCO,
        markersize=9,
        markeredgecolor=SURFACE,
        markeredgewidth=1.5,
        label="one ArUco marker",
        zorder=2,
    )
    ax.set_yticks(list(ys))
    ax.set_yticklabels(names, color=INK_2, fontsize=9.5)
    ax.invert_yaxis()
    ax.spines["bottom"].set_visible(False)


def ean_against_aruco(d: dict) -> None:
    """Module size, reach and tolerated turn of the two symbologies"""
    data = d["ean_against_aruco"]
    fig = figure(
        16,
        6.6,
        "Why the bottles carry ArUco markers: ten times the module, four to twelve "
        "times the reach",
        "The same 1080p wrist camera, square on, in MuJoCo; no code was ever read as "
        "another. A GoPro focuses from 0.30 m: a barcode on a small flask needs "
        "0.15 m. What a single marker cannot take is a turned bottle, which is why "
        "the label became a ring of eight, one every 45°.",
    )
    ax = fig.add_axes([0.075, 0.17, 0.24, 0.58])
    style(ax, "Size of one module, mm")
    dumbbell(
        ax, data["vessels"], data["ean_module_mm"], data["aruco_module_mm"], "{:g}"
    )
    ax.set_xscale("log")
    ax.set_xticks([0.2, 0.5, 1, 2, 5, 10])
    ax.set_xticklabels(["0.2", "0.5", "1", "2", "5", "10"])
    ax.minorticks_off()
    ax.set_xlim(0.1, 22)
    top_legend(fig, ax, 6.6)

    ax = fig.add_axes([0.4, 0.17, 0.24, 0.58])
    style(ax, "Reads from, m")
    dumbbell(ax, data["vessels"], data["ean_reach_m"], data["aruco_reach_m"], "{:g}")
    ax.set_xscale("log")
    ax.set_xticks([0.1, 0.3, 1, 4])
    ax.set_xticklabels(["0.1", "0.3", "1", "4"])
    ax.minorticks_off()
    ax.set_xlim(0.07, 9)
    ax.axvline(0.3, color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.annotate(
        "GoPro near focus",
        (0.3, 9.85),
        fontsize=8.5,
        color=INK_2,
        ha="center",
        annotation_clip=False,
    )
    ax.set_yticklabels([])

    ax = fig.add_axes([0.72, 0.17, 0.24, 0.58])
    style(ax, "Bottle can be turned by, degrees")
    dumbbell(
        ax,
        data["vessels"],
        data["ean_max_turn_deg"],
        data["aruco_max_turn_deg"],
        "{:g}°",
    )
    ax.set_xlim(-8, 95)
    ax.set_xticks([0, 20, 40, 60, 80])
    ax.set_yticklabels([])
    save(fig, IDENTITY / "ean13_against_aruco.png")


def wrist_scan(d: dict) -> None:
    """The same forty bottles read with each label"""
    data = d["wrist_scan_40_bottles"]
    parts = (
        ("from_030_m", "read from 0.30 m, where a GoPro focuses", TEAL),
        ("had_to_come_closer", "had to come closer, down to 0.10 m", YELLOW),
        ("not_read", "not read", ORANGE),
    )
    fig = figure(
        13,
        5.0,
        "The same forty bottles, read by the wrist camera: the ring reads 38 from "
        "where the lens focuses",
        "Whole 1080p frame decoded, nothing tells the reader where the label is. From "
        "the aisle the arm does not know which way a bottle is turned. No label was "
        "ever misread. With the ring, 107 neighbouring bottles were also named in "
        "passing, against 38.",
    )
    ax = fig.add_axes([0.27, 0.22, 0.66, 0.46])
    style(ax, "Bottles of 40")
    ax.grid(False)
    left = np.zeros(3)
    for key, name, colour in parts:
        values = np.array(data[key])
        ax.barh(
            range(3),
            values,
            left=left + 0.25 * (left > 0),
            height=0.58,
            color=colour,
            label=name,
        )
        for y, (v, x0) in enumerate(zip(values, left, strict=True)):
            if v:
                ax.annotate(
                    str(v),
                    (x0 + v / 2, y),
                    ha="center",
                    va="center",
                    fontsize=11,
                    color="#ffffff" if v > 2 else INK,
                    weight="bold",
                    xytext=(0, 0) if v > 2 else (24, 0),
                    textcoords="offset points",
                )
        left += values
    ax.set_yticks(range(3))
    ax.set_yticklabels(data["labels"], color=INK_2, fontsize=10)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_xlim(0, 43)
    ax.spines["bottom"].set_visible(False)
    top_legend(fig, ax, 5.0)
    save(fig, IDENTITY / "wrist_scan_forty_bottles.png")


def separation(d: dict) -> None:
    """How far apart the marker ids are, and what bit correction costs"""
    data = d["marker_separation"]
    fig = figure(
        14,
        5.6,
        "The failure that matters is the silent one: a wrong id that still names a "
        "real sample",
        "DICT_4X4_250: some pairs of markers differ in only 3 of 16 cells (637 such "
        "pairs among our 200 ids). Left: asking for more separation leaves too few "
        "ids for a 200-sample catalogue. Right: OpenCV's default corrects no bits, "
        "which is the safe setting; correcting more buys read rate and pays in "
        "silent misreads. In every run measured, no id was read as another.",
    )
    ax = fig.add_axes([0.06, 0.26, 0.36, 0.46])
    style(ax, "Marker ids left, by minimum distance between any two")
    ax.bar(range(5), data["ids_available"], width=0.6, color=ARUCO)
    label_bars(ax, range(5), data["ids_available"], "{:d}", 10)
    ax.axhline(data["catalogue"], color=INK_2, linewidth=1, linestyle=(0, (3, 3)))
    ax.annotate(
        "the catalogue: 200 samples",
        (4.4, data["catalogue"]),
        xytext=(0, 5),
        textcoords="offset points",
        ha="right",
        fontsize=9,
        color=INK_2,
    )
    ax.set_xticks(range(5))
    ax.set_xticklabels([f"{v} cells" for v in data["min_distance"]], color=INK_2)
    ax.margins(y=0.15)

    ax = fig.add_axes([0.5, 0.26, 0.46, 0.46])
    style(ax, "A clean marker with cells flipped: what the reader reports")
    ax.grid(False)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2)
    rows = (
        ("default: corrects 0 bits", data["outcome_default"]),
        ("set to correct up to 2 bits", data["outcome_rate_2"]),
    )
    fill = {
        "right id": "#d5efe6",
        "rejected": "#ecebe7",
        "WRONG id, silently": "#f8d3c4",
    }
    for y, (_, outcomes) in enumerate(rows):
        for x, outcome in enumerate(outcomes):
            ax.add_patch(
                plt.Rectangle(
                    (x + 0.04, 1 - y + 0.06),
                    0.92,
                    0.88,
                    facecolor=fill[outcome],
                    edgecolor="none",
                )
            )
            ax.text(
                x + 0.5,
                1 - y + 0.5,
                outcome.replace(", ", ",\n"),
                ha="center",
                va="center",
                fontsize=10,
                color=INK,
                weight="bold" if "WRONG" in outcome else "normal",
            )
    ax.set_xticks([0.5, 1.5, 2.5, 3.5])
    ax.set_xticklabels([f"{n} flipped" for n in data["flipped_bits"]], color=INK_2)
    ax.set_yticks([1.5, 0.5])
    ax.set_yticklabels(
        [r[0].replace(": ", ":\n").replace("up to", "up\nto") for r in rows],
        color=INK_2,
        fontsize=9,
    )
    ax.spines["bottom"].set_visible(False)
    save(fig, IDENTITY / "marker_separation_and_silent_misreads.png")


# From a box to a point on the bench ----------------------------------------------


def anchors(d: dict) -> None:
    """Position error of each way of turning a box into a bench point"""
    data = d["anchor_error_mm"]
    series = (
        ("base_no_radius_correction", "bottom of the box, as is", MUTED),
        ("base", "bottom of the box, moved back by the bottle's radius", YELLOW),
        ("centre", "centre of the box", VIOLET),
        ("fit", "fit the bottle's known silhouette to the box", TEAL),
    )
    fig = figure(
        14,
        5.6,
        "One camera is enough: which pixel of the box says where the bottle stands",
        "Exact boxes, 25 positions over a 1.6 m square of bench, mean error. The "
        "bottles stand on a known plane, so a ray through the right pixel lands on "
        "the bench. These errors are geometry: they do not change with resolution.",
    )
    ax = fig.add_axes([0.06, 0.2, 0.9, 0.5])
    style(ax, "Mean position error, mm")
    width = 0.2
    xs = np.arange(len(data["vessels"]))
    for j, (key, name, colour) in enumerate(series):
        values = data[key]
        ax.bar(
            xs + (j - 1.5) * width,
            [max(v, 0.25) for v in values],
            width=width - 0.03,
            color=colour,
            label=name,
        )
        label_bars(
            ax,
            xs + (j - 1.5) * width,
            values,
            "{:g}",
            8.5,
            at=[max(v, 0.25) for v in values],
        )
    ax.set_xticks(xs)
    ax.set_xticklabels(data["vessels"], color=INK_2, fontsize=10)
    ax.margins(y=0.12)
    top_legend(fig, ax, 5.6, ncols=2)
    save(fig, POSITION / "which_pixel_of_the_box.png")


def resolution(d: dict) -> None:
    """Millimetres of bench a pixel covers, and what box noise costs"""
    data = d["mm_per_pixel"]
    fig = figure(
        15,
        5.6,
        "The real limit is resolution: from 3.2 m, a pixel is 5.5 mm of bench",
        "Wall camera, GoPro Linear lens. Right: a 1 L bottle at 1080p, whose box is "
        "about 26 × 72 px. A detector good to a pixel or two lands within a "
        "centimetre: enough to aim the wrist camera, not enough to pick blind.",
    )
    ax = fig.add_axes([0.05, 0.2, 0.4, 0.52])
    style(ax, "Bench covered by one pixel, mm")
    for (name, values), colour in zip(
        data["resolutions"].items(), (ORANGE, VIOLET, TEAL), strict=True
    ):
        ax.plot(
            range(3),
            values,
            "-o",
            color=colour,
            linewidth=2.2,
            markersize=7,
            markeredgecolor=SURFACE,
            markeredgewidth=1.4,
            label=name,
        )
        ax.annotate(
            f"{name}: {values[-1]:g}",
            (2, values[-1]),
            xytext=(9, -3),
            textcoords="offset points",
            fontsize=9,
            color=INK_2,
        )
        ax.annotate(
            f"{values[1]:g}",
            (1, values[1]),
            xytext=(0, 8) if colour == ORANGE else (0, -16),
            textcoords="offset points",
            fontsize=9,
            color=INK_2,
            ha="center",
        )
    ax.set_xticks(range(3))
    ax.set_xticklabels(data["where"], color=INK_2, fontsize=10)
    ax.set_xlim(-0.25, 2.75)
    ax.set_ylim(0, 9.5)

    ax = fig.add_axes([0.57, 0.2, 0.36, 0.52])
    style(ax, "Position error against how many pixels the box is off, mm")
    for key, name, colour in (
        ("p95_error_mm", "95th percentile", MUTED),
        ("mean_error_mm", "mean", ORANGE),
    ):
        ax.plot(
            data["box_noise_px"],
            data[key],
            "-o",
            color=colour,
            linewidth=2.2,
            markersize=7,
            markeredgecolor=SURFACE,
            markeredgewidth=1.4,
            label=name,
        )
        for x, v in zip(data["box_noise_px"], data[key], strict=True):
            ax.annotate(
                f"{v:g}",
                (x, v),
                textcoords="offset points",
                xytext=(0, 8) if key.startswith("p95") else (0, -16),
                fontsize=9,
                color=INK_2,
                ha="center",
            )
    ax.set_xticks(data["box_noise_px"])
    ax.set_xticklabels([f"{v:g} px" for v in data["box_noise_px"]], color=INK_2)
    ax.set_ylim(-4, 58)
    ax.legend(loc="upper left", frameon=False, fontsize=9.5, labelcolor=INK_2)
    save(fig, POSITION / "millimetres_per_pixel.png")


def end_to_end(d: dict) -> None:
    """Frame to named, placed bottle: the funnel and the two position errors"""
    data = d["end_to_end"]
    rnd, p05 = data["random_layouts"], data["p05"]["rail"]
    fig = figure(
        16,
        5.8,
        "End to end in the scene: every bottle proposed was named, none wrongly, "
        "and placed to a tenth of a millimetre",
        "Wall camera → detector → worktop filter → point on the bench → wrist camera "
        "flown to that point → ring read → position refined from the marker. Nothing "
        "the pipeline decides reads the simulator. The 11 stray proposals read no "
        "ring from any of five views: nothing to pick, which is the right answer.",
    )
    ax = fig.add_axes([0.2, 0.2, 0.22, 0.52])
    style(ax, "12 random benches, YOLO-World L")
    ax.grid(False)
    rows = (
        ("bench bottles in view", rnd["bottles"], MUTED),
        ("proposed by the wall camera", rnd["proposed"], VIOLET),
        ("named correctly by the wrist", rnd["named_correctly"], TEAL),
        ("named wrongly", rnd["named_wrongly"], ORANGE),
    )
    for y, (_, value, colour) in enumerate(rows):
        ax.barh(y, value, height=0.58, color=colour)
        ax.annotate(
            f"{value}" + (f"  ({value / rnd['bottles']:.0%})" if 0 < y < 3 else ""),
            (value, y),
            xytext=(8, 0),
            textcoords="offset points",
            va="center",
            fontsize=11,
            color=INK,
            weight="bold",
        )
    ax.set_yticks(range(4))
    ax.set_yticklabels([r[0] for r in rows], color=INK_2, fontsize=10)
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_xlim(0, 105)
    ax.spines["bottom"].set_visible(False)

    ax = fig.add_axes([0.62, 0.2, 0.33, 0.52])
    style(ax, "Position error, mm (log scale): median, and 90th percentile")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.grid(axis="y", visible=False)
    pairs = (
        ("12 random benches\nwall camera alone", rnd["general_mm"], VIOLET),
        ("after the wrist camera", rnd["wrist_mm"], TEAL),
        (
            "catalogue bench p05, 41 flasks\nwall camera alone",
            p05["general_mm"],
            VIOLET,
        ),
        ("after the wrist camera", p05["wrist_mm"], TEAL),
    )
    for y, (_, (median, p90), colour) in enumerate(pairs):
        ax.plot([median, p90], [y, y], color=colour, linewidth=2.4, alpha=0.45)
        ax.plot(
            median,
            y,
            "o",
            color=colour,
            markersize=11,
            markeredgecolor=SURFACE,
            markeredgewidth=1.6,
        )
        ax.plot(p90, y, "|", color=colour, markersize=16, markeredgewidth=2.4)
        ax.annotate(
            f"{median:g}  ·  {p90:g}",
            (p90, y),
            xytext=(10, 0),
            textcoords="offset points",
            va="center",
            fontsize=10,
            color=INK_2,
        )
    ax.set_xscale("log")
    ax.set_xticks([0.1, 1, 10])
    ax.set_xticklabels(["0.1 mm", "1 mm", "10 mm"])
    ax.minorticks_off()
    ax.set_xlim(0.05, 130)
    ax.set_yticks(range(4))
    ax.set_yticklabels([p[0] for p in pairs], color=INK_2, fontsize=9.5)
    ax.invert_yaxis()
    ax.set_ylim(3.6, -0.6)
    ax.spines["bottom"].set_visible(False)
    save(fig, POSITION / "end_to_end.png")


def radius_bias(d: dict) -> None:
    """The wall camera's error is the assumed radius, flask by flask"""
    data = d["end_to_end"]["radius_bias"]
    fig = figure(
        13,
        6.0,
        "The wall camera's error is bias, not noise: the radius assumed before the "
        "bottle is named",
        "Catalogue bench p05. Before the ring is read the pipeline assumes an 18 mm "
        "radius for every flask. Each class is off by what that assumption costs it; "
        "with its own radius the bias goes to +0.1 mm. Replacing detector boxes with "
        "the true silhouettes leaves the error where it was.",
    )
    ax = fig.add_axes([0.2, 0.27, 0.6, 0.45])
    style(ax, "Each flask class is off by its own radius error")
    ax.set_xlabel("assumed radius − true radius, mm", color=INK_2, fontsize=9)
    ax.set_ylabel("mean error along the bench's depth, mm", color=INK_2, fontsize=9)
    ax.grid(axis="both", color=GRID, linewidth=0.8)
    ax.plot([-8, 8], [-8, 8], color=MUTED, linewidth=1, linestyle=(0, (3, 3)))
    ax.annotate("error = radius error", (-4.6, -3.2), fontsize=9, color=INK_2)
    ax.scatter(
        data["assumed_minus_true_mm"],
        data["mean_error_y_mm"],
        s=[60 + 14 * n for n in data["n"]],
        color=ORANGE,
        edgecolor=SURFACE,
        linewidth=1.6,
        zorder=3,
    )
    for name, x, y, n in zip(
        data["flasks"],
        data["assumed_minus_true_mm"],
        data["mean_error_y_mm"],
        data["n"],
        strict=True,
    ):
        ax.annotate(
            f"{name} flask, {n} on the bench",
            (x, y),
            xytext=(14, -12),
            textcoords="offset points",
            fontsize=9.5,
            color=INK_2,
        )
    ax.axhline(0, color=GRID, linewidth=1.2)
    ax.axvline(0, color=GRID, linewidth=1.2)
    ax.set_xlim(-8, 12)
    ax.set_ylim(-8, 8)
    ax.spines["bottom"].set_visible(False)
    save(fig, POSITION / "radius_bias.png")


# The whole thing -----------------------------------------------------------------


def overview(d: dict) -> None:
    """The pipeline on one slide, each stage with the number that backs it"""
    p05 = d["end_to_end"]["p05"]["rail"]
    scan = d["wrist_scan_40_bottles"]
    stages = (
        (
            "Wall camera",
            "one 1080p frame\nof the bench, 3.2 m away",
            "a 10 ml flask is\n8 × 15 px",
            MUTED,
        ),
        (
            "Detector",
            "YOLO26n trained on\nMuJoCo renders",
            "99.9 % of the vials\n0.05 false boxes a frame",
            ORANGE,
        ),
        (
            "Worktop filter",
            "keep what stands\non the bench plane",
            "false boxes\n17.5 → 1.8 a frame",
            YELLOW,
        ),
        (
            "Point on the bench",
            "a ray through the box,\none calibrated camera",
            f"median {p05['general_mm'][0]} mm off",
            VIOLET,
        ),
        (
            "Wrist camera",
            "flown to that point,\nreads the ArUco ring",
            f"{scan['from_030_m'][2] + scan['had_to_come_closer'][2]} of 40 read\n"
            "0 misread",
            TEAL,
        ),
        (
            "Bench memory",
            "sample → compound\n→ 3D position",
            f"median {p05['wrist_mm'][0]} mm off",
            "#2a78d6",
        ),
    )
    fig = figure(
        16,
        5.4,
        "From one frame to a bench where every bottle has a name and a position",
        "Every number is measured in simulation (MuJoCo); nothing has been scored on a "
        "real photograph. The two position errors are the catalogue bench p05, 41 "
        "flasks, all 41 proposed and named, scanned with the previous detector.",
    )
    ax = fig.add_axes([0.02, 0.14, 0.96, 0.66])
    ax.set_facecolor(SURFACE)
    ax.axis("off")
    ax.set_xlim(0, len(stages))
    ax.set_ylim(0, 1)
    for i, (name, what, number, colour) in enumerate(stages):
        ax.add_patch(
            FancyBboxPatch(
                (i + 0.07, 0.42),
                0.8,
                0.5,
                boxstyle="round,pad=0,rounding_size=0.035",
                facecolor=SURFACE,
                edgecolor=colour,
                linewidth=2.2,
            )
        )
        ax.add_patch(
            plt.Rectangle(
                (i + 0.07, 0.86), 0.8, 0.06, facecolor=colour, edgecolor="none"
            )
        )
        ax.text(
            i + 0.47,
            0.76,
            name,
            ha="center",
            va="center",
            fontsize=12.5,
            weight="bold",
            color=INK,
        )
        ax.text(
            i + 0.47,
            0.57,
            what,
            ha="center",
            va="center",
            fontsize=9.5,
            color=INK_2,
            linespacing=1.35,
        )
        ax.text(
            i + 0.47,
            0.2,
            number,
            ha="center",
            va="center",
            fontsize=11.5,
            color=INK,
            weight="bold",
            linespacing=1.35,
        )
        if i < len(stages) - 1:
            ax.add_patch(
                FancyArrowPatch(
                    (i + 0.89, 0.67),
                    (i + 1.05, 0.67),
                    arrowstyle="-|>",
                    mutation_scale=16,
                    color=INK_2,
                    linewidth=1.6,
                )
            )
    save(fig, DEMO / "0_overview" / "pipeline_on_one_slide.png")


def main() -> None:
    """Draw every pipeline figure"""
    plt.rcParams.update({"font.family": "DejaVu Sans", "text.color": INK})
    d = json.loads((DATA / "vision_pipeline.json").read_text(encoding="utf-8"))
    overview(d)
    accuracy_against_speed(d)
    prompts(d)
    size_floor(d)
    distance(d)
    three_models(d)
    by_bottle_and_size(d)
    worktop_filter(d)
    ean_against_aruco(d)
    wrist_scan(d)
    separation(d)
    anchors(d)
    resolution(d)
    end_to_end(d)
    radius_bias(d)


if __name__ == "__main__":
    main()
