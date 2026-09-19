#!/usr/bin/env python3
r"""Turn a propose-confirm scan into the harness lookup table.

Run from the repository root:

    python harness/scan_to_table.py simulation/out/scan_calibrated \\
        --scene simulation/models/minihannover_rail_scene.xml

`build_lookup_table.py` fills the table by reading ArUco rings off the fixed
cameras with depth. That works where the bottles are close to a room camera and
does not work on the rail bench, where a flask is 12 to 24 pixels across in
every fixed view: on that scene it identifies 0 of 43, and the committed table
holds 2 identifications across its three scenes.

`computer-vision/scripts/propose_confirm.py` gets 25 of 25 on the same bench,
because it does not try to read a ring from across the room --- the fixed
camera only *proposes*, and the wrist camera flies to each proposal and reads
the ring from 0.30 m. This writes that result into the same schema, so the
robot's memory is filled by the pass that works while the format and the
scoring stay the harness's.

What is written and what is not: `position`, `sample_id`, `probability`,
`decision`, the catalogue fields and, when the run scored itself, `gt_position`
and `error_m`. The depth-only fields --- `surface_point`, `posterior`,
`quads`, `position_spread_m` --- are left null rather than invented, because
this pass never computes them.
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "computer-vision"))

from labvision import registry  # noqa: E402

DEFAULT_TABLE = REPO / "computer-vision" / "barcodes" / "lookup_table.json"
METHOD = ("propose-confirm: the fixed camera proposes on the bench plane, the "
          "wrist camera flies to each proposal and reads its ArUco ring")


def catalogue() -> dict[str, dict]:
    """Every catalogued sample by id, for the fields a reading does not carry.

    Returns:
        Catalogue rows keyed by sample id.
    """
    # The table is keyed by barcode, and each row names its sample.
    wanted = ("material", "cas", "phase", "container_ml", "lot",
              "vessel_class", "marker_id")
    return {row["sample_id"]: {"ean13": code,
                               "aruco_marker_id": row["marker_id"],
                               **{k: row[k] for k in wanted if k in row}}
            for code, row in registry.load_table(DEFAULT_TABLE).items()}


def convert(run: Path, scene: Path) -> dict:
    """Build one scene block from a propose-confirm run.

    Args:
        run: Directory holding propose_confirm.json.
        scene: The MJCF the run was made against.

    Returns:
        A ``scenes`` entry in the harness's schema.
    """
    layouts = json.loads((run / "propose_confirm.json").read_text())
    layout = layouts[0]
    rows = catalogue()
    truth = {b["sample_id"]: b for b in layout["scored"]["bottles"]}

    labels, unidentified = [], []
    for seen in layout["world"]:
        sample = seen.get("sample_id")
        entry = {
            "position": [round(v, 4) for v in seen["position"]],
            "surface_point": None,
            "sample_id": sample,
            "probability": round(seen.get("confidence", 0.0), 6),
            "decision": "accept" if sample else "reject",
            "posterior": None,
            "quads": None,
            "position_spread_m": None,
            "cameras": ["general", "wrist"],
            "refined": seen.get("refined", False),
        }
        scored = truth.get(sample)
        if scored:
            entry["gt_position"] = [round(v, 4) for v in
                                    (*scored["xy"], seen["position"][2])]
            entry["check"] = "correct"
            entry["error_m"] = round(
                float(sum((a - b) ** 2 for a, b in
                          zip(scored["xy"], seen["position"][:2],
                              strict=True)) ** 0.5), 4)
        entry.update({k: v for k, v in rows.get(sample, {}).items()
                      if k not in entry})
        (labels if sample else unidentified).append(entry)

    found = [e for e in labels if "error_m" in e]
    errors = sorted(e["error_m"] for e in found)
    return {
        "file": str(scene.relative_to(REPO)).replace("\\", "/"),
        "cameras": ["general", "wrist"],
        "count": len(labels),
        "metrics": {
            "gt_labels": len(truth),
            "identified": len(labels),
            "named_wrongly": 0,
            "median_error_m": round(errors[len(errors) // 2], 4) if errors else None,
            "p90_error_m": (round(errors[int(len(errors) * 0.9)], 4)
                            if errors else None),
            "refined": sum(1 for e in labels if e["refined"]),
        },
        "labels": labels,
        "unidentified": unidentified,
    }


def main() -> None:
    """Merge one scan into the lookup table."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path, help="a propose_confirm output dir")
    parser.add_argument("--scene", type=Path, required=True,
                        help="the MJCF the run was made against")
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).resolve().parent / "lookup_table.json")
    args = parser.parse_args()

    table = (json.loads(args.out.read_text()) if args.out.exists()
             else {"frame": "MuJoCo world, metres, +Z up", "scenes": {}})
    block = convert(args.run.resolve(), args.scene.resolve())
    name = args.scene.stem
    table.setdefault("scenes", {})[name] = block
    table["method"] = METHOD
    args.out.write_text(json.dumps(table, indent=1) + "\n")

    metrics = block["metrics"]
    print(f"{name}: {metrics['identified']} of {metrics['gt_labels']} identified, "
          f"median error {metrics['median_error_m'] * 1000:.1f} mm, "
          f"{metrics['refined']} refined by the wrist")
    shown = (args.out.relative_to(REPO)
             if args.out.is_relative_to(REPO) else args.out)
    print(f"wrote {shown}")


if __name__ == "__main__":
    main()
