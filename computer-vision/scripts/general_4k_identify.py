"""Can the fixed camera name bottles by their ring, at 1080p or at 4K?

The ring was measured to read from 0.4 m (10 ml flask) to 2.5 m (2 L bottle)
at 1080p (``scripts/ring_experiment.py``), and the fixed ``general`` GoPro is
3 to 4 m from the bench. At 4K each marker covers twice the pixels, so the
largest bottles might be named from the wall without the arm moving at all.

Per layout the same bottles are rendered from the ``general`` camera at 1080p
and at 3840 x 2160, and every bench bottle at least half visible is asked for
by :func:`labvision.identify.identify_frame` (whole frame, the ring's markers
lying on the bottle) and by :func:`labvision.identify.identify` in its true
visible box, the ceiling a perfect detector would give. No detector runs: at
4K a CPU would take most of a minute per frame, and the question is about the
ring, not the box.

    python scripts/general_4k_identify.py --layouts 8

Writes ``general_4k_identify.json`` and ``.md`` in ``--out``.
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from perfumery_eval import is_required, kind  # noqa: E402
from render_perfumery import BENCH_X, Lab  # noqa: E402

from labvision import registry  # noqa: E402
from labvision.identify import (  # noqa: E402
    DEFAULT_TABLE,
    MarkerReader,
    identify,
    identify_frame,
    rows_by_marker,
)
from labvision.scene import BBox  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
SIZES = {"1080p": (1920, 1080), "4K": (3840, 2160)}


def named(frame, bottles, rows, marker_of, reader) -> dict[str, list[bool]]:
    """Per bench bottle required, whether each method named it, or named it wrong

    A whole-frame read names a bottle wrong when an id other than its own lies
    on it and its own does not; a true-box read, when the box votes for
    another id. A wrong name sends the arm to the wrong sample, so it is
    counted apart from a miss.
    """
    required = [b for b in bottles if b.get("where") == "bench" and is_required(b)]
    whole = identify_frame(frame, rows, reader=reader)
    boxes = identify(frame, [BBox(*b["xyxy"]) for b in required], rows, reader=reader)
    result = {"whole": [], "true box": [], "whole wrong": [], "true box wrong": []}
    for bottle, in_box in zip(required, boxes, strict=True):
        marker = marker_of[bottle["sample_id"]]
        u0, v0, u1, v1 = bottle["full_xyxy"]
        on_it = {
            i.marker_id
            for i in whole
            if i.marker_id is not None
            and u0 <= (i.bbox.u_min + i.bbox.u_max) / 2 <= u1
            and v0 <= (i.bbox.v_min + i.bbox.v_max) / 2 <= v1
        }
        result["whole"].append(marker in on_it)
        result["whole wrong"].append(bool(on_it) and marker not in on_it)
        result["true box"].append(in_box.marker_id == marker)
        result["true box wrong"].append(in_box.marker_id not in (None, marker))
    return {"kinds": [kind(b) for b in required], **result}


def main() -> None:
    """Render, read and tally"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--layouts", type=int, default=8)
    parser.add_argument("--seed", type=int, default=4)
    parser.add_argument(
        "--out", type=Path, default=REPO / "simulation" / "out" / "general_4k"
    )
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    table = registry.load_table(DEFAULT_TABLE)
    rows = rows_by_marker(table)
    marker_of = {row["sample_id"]: int(row["marker_id"]) for row in table.values()}
    reader = MarkerReader()
    lab = Lab(*SIZES["4K"])
    general = lab.cameras["general"]
    tally = {
        size: {m: defaultdict(lambda: [0, 0]) for m in ("whole", "true box")}
        for size in SIZES
    }
    wrong = {size: {"whole": 0, "true box": 0} for size in SIZES}
    for k in range(args.layouts):
        x0 = float(rng.uniform(BENCH_X[0] + 0.8, BENCH_X[1] - 0.8))
        lab.scatter(rng, int(rng.integers(10, 16)), (x0 - 0.9, x0 + 0.9), (-1,))
        for size, (width, height) in SIZES.items():
            rgb, bottles, _ = lab.render(general, width, height)
            result = named(rgb[:, :, ::-1].copy(), bottles, rows, marker_of, reader)
            for method in ("whole", "true box"):
                for label, hit in zip(result["kinds"], result[method], strict=True):
                    tally[size][method][label][0] += hit
                    tally[size][method][label][1] += 1
                wrong[size][method] += sum(result[f"{method} wrong"])
        print(f"layout {k} done", flush=True)

    kinds = sorted({k for s in tally.values() for m in s.values() for k in m})
    columns = [(size, m) for size in SIZES for m in ("whole", "true box")]
    lines = [
        f"# Naming bottles from the general camera, {args.layouts} layouts",
        "",
        "| bottle | " + " | ".join(f"{s} {m}" for s, m in columns) + " |",
        "| --- |" + " --- |" * len(columns),
    ]
    for label in kinds:
        cells = []
        for size, method in columns:
            hit, total = tally[size][method].get(label, (0, 0))
            cells.append(f"{hit}/{total}" if total else "-")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    totals = []
    for size, method in columns:
        hit = sum(v[0] for v in tally[size][method].values())
        total = sum(v[1] for v in tally[size][method].values())
        totals.append(f"{100 * hit / total:.0f} % ({hit}/{total})" if total else "-")
    lines.append("| **all** | " + " | ".join(totals) + " |")
    lines.append(
        "| named wrong | "
        + " | ".join(str(wrong[size][method]) for size, method in columns)
        + " |"
    )
    report = "\n".join(lines) + "\n"
    serialisable = {
        s: {m: dict(v) for m, v in methods.items()} for s, methods in tally.items()
    }
    serialisable["wrong"] = wrong
    (args.out / "general_4k_identify.json").write_text(
        json.dumps(serialisable, indent=1), encoding="utf-8"
    )
    (args.out / "general_4k_identify.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
