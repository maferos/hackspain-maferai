"""Check a lookup table written by build_lookup_table.py against the scenes it names

The table's own ``check`` fields and ``metrics`` are written by the same pass
that made the readings, so nothing here trusts them: every scene is compiled
again, its ground-truth labels are read from the model
(``build_lookup_table.scan_scene``), and each entry is scored from scratch.

Checks, each PASS, FAIL or INFO; any FAIL makes the exit status 1:

registry      the table's registry version is the current catalogue's, and every
              entry's catalogue fields (EAN-13, marker, material, ...) match its row
scenes        every scene file exists and compiles
unique        no sample id is listed twice in one scene (vision)
decisions     accept entries have p >= markers.ACCEPT_P, rescan entries
              REJECT_P <= p < ACCEPT_P, unidentified ones are reject (vision)
accept        every accept entry names the label nearest its position, within
              MATCH_M: the table never states a wrong identity it is sure of
rescan        wrong rescan entries (INFO: rescan means look again, not trust)
error         for correct identities, median position error <= --median-m and
              the worst <= --max-m
recall        correct identities over ground-truth labels > 0 and >= --min-recall
detected      labels with any bottle, named or not, within DETECT_M of them (INFO:
              separates what the detector missed from what the ring decoder did)
metrics       the stored metrics agree with the recount
weights       the detector weights named in the header are on disk and hash to
              the recorded sha256 (vision)
gt            for a --method gt table, every position is the recomputed one

    simulation/.venv-act/bin/python harness/verify_lookup_table.py
    ... verify_lookup_table.py path/to/table.json --min-recall 0.5
"""

import argparse
import hashlib
import json
import statistics
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_lookup_table import OUT, ROOT, load_registry, load_scene, scan_scene  # noqa: E402

sys.path.insert(0, str(ROOT / "computer-vision"))

MATCH_M = 0.05     # as in vision.py: a point this close to a label is that label
DETECT_M = 0.08    # an unnamed bottle's surface point is up to a radius off the label
REGISTRY_FIELDS = ("ean13", "aruco_marker_id", "material", "cas", "phase",
                   "container_ml", "lot", "vessel_class")


class Report:
    def __init__(self):
        self.failed = False

    def __call__(self, status: str, scene: str, check: str, message: str) -> None:
        self.failed |= status == "FAIL"
        print(f"{status:4s}  {scene:32s} {check:10s} {message}")

    def gate(self, ok: bool, scene: str, check: str, message: str) -> None:
        self("PASS" if ok else "FAIL", scene, check, message)


def nearest(gt_ids, gt_pos, position):
    if not len(gt_pos):
        return None, float("inf")
    distance = np.linalg.norm(gt_pos - np.asarray(position), axis=1)
    i = int(np.argmin(distance))
    return gt_ids[i], float(distance[i])


def check_registry_fields(report, scene, entries, registry):
    bad = []
    for e in entries:
        row = registry.get(e.get("sample_id"))
        if row is None:
            bad.append(f"{e.get('sample_id')}: not in the catalogue")
            continue
        for field in REGISTRY_FIELDS:
            if e.get(field) != row[field]:
                bad.append(f"{e['sample_id']}.{field}: {e.get(field)!r} != {row[field]!r}")
    report.gate(not bad, scene, "registry",
                f"{len(entries)} entries match the catalogue" if not bad
                else f"{len(bad)} mismatches, first: {bad[0]}")


def check_weights(report, table):
    weights = table.get("detector_weights")
    if not weights:
        report("FAIL", "-", "weights", "no detector_weights block in the header")
        return
    from labvision.detector import _find_weights

    path = ROOT / weights.get("path", weights["file"])
    if not path.exists():
        path = Path(_find_weights(weights["file"]))
    if not path.exists():
        report("INFO", "-", "weights", f"{weights['file']} not on disk here, hash not checked")
        return
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    report.gate(digest == weights.get("sha256"), "-", "weights",
                f"{weights['backend']}: {path.name} sha256 {digest[:12]}"
                + ("" if digest == weights.get("sha256")
                   else f" != recorded {str(weights.get('sha256'))[:12]}"))


def verify_vision_scene(report, name, record, truth, registry, args):
    from labvision import markers

    labels, unidentified = record["labels"], record.get("unidentified", [])
    gt_ids = [e["sample_id"] for e in truth]
    gt_pos = np.array([e["position"] for e in truth]) if truth else np.zeros((0, 3))

    check_registry_fields(report, name, labels, registry)

    ids = [e["sample_id"] for e in labels]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    report.gate(not dupes, name, "unique",
                f"{len(ids)} distinct ids" if not dupes else f"listed twice: {dupes[:5]}")

    bad = []
    for e in labels:
        p, d = e["probability"], e["decision"]
        if d == "accept" and p < markers.ACCEPT_P:
            bad.append(f"{e['sample_id']} accept at p={p}")
        elif d == "rescan" and not markers.REJECT_P <= p < markers.ACCEPT_P:
            bad.append(f"{e['sample_id']} rescan at p={p}")
        elif d not in ("accept", "rescan"):
            bad.append(f"{e['sample_id']} listed with decision {d}")
    bad += [f"unidentified entry with decision {e['decision']}"
            for e in unidentified if e["decision"] != "reject"]
    report.gate(not bad, name, "decisions",
                f"accept >= {markers.ACCEPT_P}, rescan >= {markers.REJECT_P}" if not bad
                else f"{len(bad)} inconsistent, first: {bad[0]}")

    wrong = {"accept": [], "rescan": []}
    errors, correct = [], set()
    for e in labels:
        seen, distance = nearest(gt_ids, gt_pos, e["position"])
        if distance < MATCH_M and seen == e["sample_id"]:
            correct.add(e["sample_id"])
            errors.append(float(np.linalg.norm(
                np.asarray(e["position"]) - gt_pos[gt_ids.index(seen)])))
        else:
            where = f"{seen} at {distance:.3f} m" if seen else "nothing"
            wrong.setdefault(e["decision"], []).append(f"{e['sample_id']} (nearest label: {where})")
    accepted = sum(e["decision"] == "accept" for e in labels)
    report.gate(not wrong["accept"], name, "accept",
                f"{accepted - len(wrong['accept'])}/{accepted} accept entries correct"
                + (f"; wrong: {wrong['accept'][:3]}" if wrong["accept"] else ""))
    rescans = sum(e["decision"] == "rescan" for e in labels)
    report("INFO", name, "rescan",
           f"{rescans - len(wrong['rescan'])}/{rescans} rescan entries correct"
           + (f"; wrong: {wrong['rescan'][:3]}" if wrong["rescan"] else ""))

    if errors:
        median, worst = statistics.median(errors), max(errors)
        report.gate(median <= args.median_m and worst <= args.max_m, name, "error",
                    f"median {median * 1000:.1f} mm (<= {args.median_m * 1000:.0f}), "
                    f"worst {worst * 1000:.1f} mm (<= {args.max_m * 1000:.0f})")
    else:
        report("INFO", name, "error", "no correct identity to measure")

    recall = len(correct) / len(set(gt_ids)) if gt_ids else 0.0
    report.gate(correct and recall >= args.min_recall, name, "recall",
                f"{len(correct)}/{len(set(gt_ids))} labels found and named = {recall:.2f} "
                f"(>= {args.min_recall:.2f})")

    found = [e["position"] for e in labels] + [e["position"] for e in unidentified]
    located = sum(1 for p in gt_pos if found and np.min(
        np.linalg.norm(np.asarray(found) - p, axis=1)) < DETECT_M)
    report("INFO", name, "detected",
           f"{located}/{len(gt_pos)} labels have a bottle within {DETECT_M * 100:.0f} cm, "
           f"{len(correct)} of them named right")

    metrics = record.get("metrics", {})
    stored = (metrics.get("gt_labels"), metrics.get("identified"))
    recount = (len(truth), len(labels))
    report.gate(stored == recount, name, "metrics",
                f"gt_labels, identified = {recount}" if stored == recount
                else f"stored {stored} != recount {recount}")


def verify_gt_scene(report, name, record, truth, registry):
    check_registry_fields(report, name, record["labels"], registry)
    key = lambda e: (e["sample_id"], e["geom"])  # noqa: E731
    want = {key(e): e["position"] for e in truth}
    have = {key(e): e["position"] for e in record["labels"]}
    moved = [k for k in want if k in have and np.linalg.norm(
        np.subtract(want[k], have[k])) > 1e-4]
    same = want.keys() == have.keys() and not moved
    report.gate(same, name, "gt",
                f"{len(have)} labels at their recomputed positions" if same
                else f"{len(want.keys() ^ have.keys())} labels differ, {len(moved)} moved")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("table", nargs="?", type=Path, default=OUT)
    parser.add_argument("--min-recall", type=float, default=0.0,
                        help="labels found and named over ground-truth labels (default 0: report)")
    parser.add_argument("--median-m", type=float, default=0.02)
    parser.add_argument("--max-m", type=float, default=MATCH_M)
    args = parser.parse_args()

    table = json.loads(args.table.read_text())
    version, registry = load_registry()
    report = Report()
    report.gate(table.get("registry_version") == version, "-", "registry",
                f"table v{table.get('registry_version')}, catalogue v{version}")
    if table["method"] == "vision":
        check_weights(report, table)

    for name, record in table["scenes"].items():
        path = ROOT / record["file"]
        if not path.exists():
            report("FAIL", name, "scenes", f"{record['file']} does not exist")
            continue
        model, data = load_scene(path)
        truth = scan_scene(model, data, registry)
        phases = {e.get("phase") for e in record["labels"]}
        if len(phases) == 1 and len({e.get("phase") for e in truth}) > 1:
            truth = [e for e in truth if e.get("phase") in phases]  # built with --phase
        report("PASS", name, "scenes", f"{record['file']}: {len(truth)} ground-truth labels")
        if table["method"] == "vision":
            verify_vision_scene(report, name, record, truth, registry, args)
        else:
            verify_gt_scene(report, name, record, truth, registry)

    print("FAILED" if report.failed else "all checks passed")
    sys.exit(1 if report.failed else 0)


if __name__ == "__main__":
    main()
