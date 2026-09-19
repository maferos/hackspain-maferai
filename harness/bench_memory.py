#!/usr/bin/env python3
"""Revise a lookup table as more looks arrive, instead of rebuilding it from scratch

A scan writes what the bench looked like once. The bench then moves: the arm puts
a flask down 30 mm from where it took it, someone slides one along, and a bottle
the detector missed is read perfectly on the next pass. This is the memory that
lets the table follow that, one reading at a time, and it is the update policy
``SCANNING_PLAN.md`` specifies and leaves open.

**Identity is the key; position is an attribute of it.** Entries are matched by
``sample_id``, never by where they are, and an accepted identity is never
rewritten --- a ring read wrong would send the arm for the wrong compound, which
is worse than any stale coordinate. What a new look may change is where the
bottle is, and whether it is still believed to be there.

**A distance gate decides between refining and replacing.** Within ``GATE_M`` the
two readings are of the same bottle standing still, and averaging them is worth
doing; beyond it the bottle has moved, and averaging would put it where nothing
is. That is the difference between the first two rows of the rule table below,
and it is the whole reason this is not a running mean.

**The average is inverse-variance, not equal-weight.** Each reading carries the
spread of the views behind it, and weighting by 1/spread^2 makes a wrist read
from 0.30 m (about 3 mm) outweigh a room camera's box (about 30 mm) a hundred to
one. That reproduces ``build_lookup_table``'s rule --- "a ring read from 0.30 m
and a box seen from across the room are not worth averaging" --- without a hard
rule about which camera wins, and it degrades gracefully when two looks are of
similar quality.

**Nothing is deleted.** A bottle that is not seen where it was is marked
``missing``, because a flask behind a neighbour is not a flask that left.
Deleting on a single miss is how a memory loses what it already knew.

The rules, one per row, each with a test in ``tests/test_bench_memory.py``:

named, known, within GATE_M      refine the position, sightings++
named, known, beyond GATE_M      moved: replace the position, flag it
named, unknown                   insert
unnamed, near a known entry       touch it: do not rename, do not move
unnamed, far from everything      a new UNK-* entry, to be retried
known, not seen, its area scanned  status missing --- never deleted

Plain dictionaries throughout: no mujoco, no scene, no detector. The hard part is
the policy, and it is testable without any of them.

    simulation/.venv/bin/python harness/tests/test_bench_memory.py
"""

import math

#: Beyond this, two readings of one sample are not the same bottle standing
#: still: it has been moved. SCANNING_PLAN.md's merge table uses 5 cm, and
#: vision.MATCH_M uses the same figure for "a point this close to a label is
#: that label".
GATE_M = 0.05

#: Readings nearer than this to an existing entry are taken to be about it.
#: Wider than GATE_M because an unnamed box carries the room camera's error,
#: which vision-pick.md measures at about 3 cm nine times in ten.
NEAR_M = 0.08

#: No reading is treated as better than this, however small its spread. Without
#: a floor one lucky view with a spread of zero would take infinite weight and
#: pin the position forever.
SPREAD_FLOOR_M = 0.001

#: What a reading with no spread of its own is assumed to carry. A single view
#: has nothing to disagree with, so it cannot report a spread; the room camera's
#: typical error stands in.
SPREAD_DEFAULT_M = 0.03


def distance(a, b) -> float:
    """Metres between two positions, in the plane the bench lives in.

    Height is ignored on purpose: a flask's label height is a property of its
    vessel class, not of where it stands, and letting it into the distance would
    make a 10 ml flask and a 100 ml one look far apart when they are side by
    side.
    """
    return math.dist(a[:2], b[:2])


def blend(old, old_spread, new, new_spread):
    """Inverse-variance mean of two positions, and the spread of the result.

    Returns:
        The blended position and its spread, which is always smaller than
        either input's: two looks that agree are worth more than either alone.
        The spread keeps a decimal more than the position, because four is
        where the tightening stops being visible and the tightening is the
        whole point of keeping it.
    """
    wo = 1.0 / max(old_spread or SPREAD_DEFAULT_M, SPREAD_FLOOR_M) ** 2
    wn = 1.0 / max(new_spread or SPREAD_DEFAULT_M, SPREAD_FLOOR_M) ** 2
    pos = [(wo * o + wn * n) / (wo + wn) for o, n in zip(old, new)]
    return [round(v, 4) for v in pos], round(1.0 / math.sqrt(wo + wn), 5)


def nearest(labels, position, *, within=NEAR_M):
    """The entry closest to a position, or None if nothing is within `within`."""
    near = [(distance(e["position"], position), e) for e in labels if e.get("position")]
    near = [pair for pair in near if pair[0] < within]
    return min(near, key=lambda pair: pair[0])[1] if near else None


def _record(rule, entry, **fields):
    return {"rule": rule, "sample_id": entry.get("sample_id"), **fields}


def observe(labels, readings, *, cycle=0, t=0.0, gate=GATE_M):
    """Fold new readings into a table's labels, in place.

    Args:
        labels: The scene's ``labels`` list, revised in place. One entry per
            sample id --- entries are replaced, never appended to, so the
            uniqueness `verify_lookup_table` gates on survives.
        readings: Dicts with ``position`` and, where a ring was read,
            ``sample_id``. ``position_spread_m`` and ``probability`` are used
            when present.
        cycle: Perception cycle this batch came from, stamped on every revision.
        t: Simulated seconds, likewise.
        gate: Distance past which a reading is taken to be a moved bottle.

    Returns:
        One log record per revision, in the order they were applied. Empty when
        nothing changed, which is the common case once the bench settles.
    """
    by_id = {e["sample_id"]: e for e in labels if e.get("sample_id")}
    log = []
    for reading in readings:
        stamp = {"cycle": cycle, "t": round(t, 3)}
        sample, position = reading.get("sample_id"), reading["position"]
        spread = reading.get("position_spread_m")

        if sample is None:
            entry = nearest(labels, position)
            if entry is not None:
                # Touched, not moved: an unnamed box near a known bottle is
                # evidence it is still there and nothing more. Letting it move
                # the position would trade a ring's millimetres for a box's
                # centimetres.
                entry["last_seen"] = cycle
                entry["status"] = "present"
                log.append(_record("touch", entry, **stamp))
                continue
            unknown = f"UNK-{1 + sum(1 for e in labels if not e.get('sample_id')):04d}"
            entry = {"sample_id": None, "unknown_id": unknown, "position": position,
                     "position_spread_m": spread, "status": "unidentified",
                     "sightings": 1, "first_seen": cycle, "last_seen": cycle}
            labels.append(entry)
            log.append(_record("unknown", entry, unknown_id=unknown, to=position, **stamp))
            continue

        entry = by_id.get(sample)
        if entry is None:
            entry = {"sample_id": sample, "position": position,
                     "position_spread_m": spread, "status": "present",
                     "sightings": 1, "first_seen": cycle, "last_seen": cycle}
            for key in ("probability", "decision", "material", "cas", "container_ml",
                        "ean13", "aruco_marker_id", "vessel_class"):
                if key in reading:
                    entry[key] = reading[key]
            labels.append(entry)
            by_id[sample] = entry
            log.append(_record("insert", entry, to=position, **stamp))
            continue

        was = list(entry["position"])
        moved = distance(was, position)
        entry["sightings"] = entry.get("sightings", 1) + 1
        entry["last_seen"] = cycle
        entry["status"] = "present"
        if moved >= gate:
            entry["position"] = [round(v, 4) for v in position]
            entry["position_spread_m"] = spread
            entry["moved"] = True
            log.append(_record("moved", entry, was=was, to=entry["position"],
                               moved_m=round(moved, 4), **stamp))
        else:
            entry["position"], entry["position_spread_m"] = blend(
                was, entry.get("position_spread_m"), position, spread)
            log.append(_record("refine", entry, was=was, to=entry["position"],
                               moved_m=round(moved, 4),
                               spread_m=entry["position_spread_m"], **stamp))
    return log


def mark_missing(labels, seen, *, scanned=None, cycle=0):
    """Degrade to `missing` the entries a pass looked for and did not find.

    Args:
        labels: The scene's labels, revised in place.
        seen: Sample ids this pass did see.
        scanned: Sample ids this pass actually looked for. Entries outside it
            are left alone: not looking is not the same as looking and finding
            nothing, and a table that forgets the far end of the bench every
            time the arm works at the near end is worse than useless.
        cycle: Stamped on the revision.

    Returns:
        One log record per entry degraded.
    """
    log = []
    for entry in labels:
        sample = entry.get("sample_id")
        if sample is None or sample in seen:
            continue
        if scanned is not None and sample not in scanned:
            continue
        if entry.get("status") == "missing":
            continue
        entry["status"] = "missing"
        log.append(_record("missing", entry, cycle=cycle,
                           last_seen=entry.get("last_seen")))
    return log
