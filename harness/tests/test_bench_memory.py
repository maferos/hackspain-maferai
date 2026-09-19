"""One test per row of bench_memory's rule table, plus the invariants it must keep

Runs under pytest, and on its own for anyone whose venv has no pytest:

    simulation/.venv/bin/python harness/tests/test_bench_memory.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bench_memory as bm  # noqa: E402


def entry(sample, x, y, spread=0.004, **extra):
    return {"sample_id": sample, "position": [x, y, 0.93],
            "position_spread_m": spread, "status": "present",
            "sightings": 1, "first_seen": 0, "last_seen": 0, **extra}


def reading(x, y, sample=None, spread=0.004, **extra):
    out = {"position": [x, y, 0.93], "position_spread_m": spread, **extra}
    if sample:
        out["sample_id"] = sample
    return out


# -- the six rules ---------------------------------------------------------

def test_known_and_near_is_refined():
    labels = [entry("SMP-0006", 1.0, 0.0, spread=0.03)]
    log = bm.observe(labels, [reading(1.01, 0.0, "SMP-0006", spread=0.003)])
    assert [r["rule"] for r in log] == ["refine"]
    x = labels[0]["position"][0]
    # Inverse-variance: the 3 mm look outweighs the 30 mm one a hundred to one,
    # so the blend lands beside the new reading, not halfway between them.
    assert abs(x - 1.01) < 0.0002, x
    assert x < 1.01, x                          # it did move, just barely
    assert labels[0]["position_spread_m"] < 0.003
    assert labels[0]["sightings"] == 2


def test_known_and_far_is_moved():
    labels = [entry("SMP-0006", 1.0, 0.0)]
    log = bm.observe(labels, [reading(1.4, 0.0, "SMP-0006")])
    assert [r["rule"] for r in log] == ["moved"]
    assert labels[0]["position"][0] == 1.4      # replaced, not averaged
    assert labels[0]["moved"] is True
    assert log[0]["moved_m"] == 0.4
    assert len(labels) == 1


def test_unknown_sample_is_inserted():
    labels = [entry("SMP-0006", 1.0, 0.0)]
    log = bm.observe(labels, [reading(2.0, 0.5, "SMP-0044", material="Anethole")])
    assert [r["rule"] for r in log] == ["insert"]
    assert len(labels) == 2
    assert labels[1]["material"] == "Anethole"
    assert labels[1]["sightings"] == 1


def test_unnamed_near_a_known_entry_only_touches_it():
    labels = [entry("SMP-0006", 1.0, 0.0)]
    log = bm.observe(labels, [reading(1.02, 0.0)], cycle=7)
    assert [r["rule"] for r in log] == ["touch"]
    assert labels[0]["position"][0] == 1.0      # not moved by a nameless box
    assert labels[0]["sample_id"] == "SMP-0006"  # not renamed
    assert labels[0]["last_seen"] == 7


def test_unnamed_far_from_everything_becomes_UNK():
    labels = [entry("SMP-0006", 1.0, 0.0)]
    log = bm.observe(labels, [reading(2.0, 0.5)])
    assert [r["rule"] for r in log] == ["unknown"]
    assert labels[1]["sample_id"] is None
    assert labels[1]["unknown_id"] == "UNK-0001"
    assert labels[1]["status"] == "unidentified"


def test_not_seen_goes_missing_and_is_kept():
    labels = [entry("SMP-0006", 1.0, 0.0), entry("SMP-0044", 2.0, 0.0)]
    log = bm.mark_missing(labels, seen={"SMP-0006"},
                          scanned={"SMP-0006", "SMP-0044"}, cycle=9)
    assert [r["rule"] for r in log] == ["missing"]
    assert len(labels) == 2                      # kept, never deleted
    assert labels[1]["status"] == "missing"
    assert labels[1]["position"][0] == 2.0       # and it remembers where


# -- the invariants --------------------------------------------------------

def test_unscanned_entries_are_left_alone():
    """Not looking is not the same as looking and finding nothing."""
    labels = [entry("SMP-0006", 1.0, 0.0), entry("SMP-0044", 2.0, 0.0)]
    log = bm.mark_missing(labels, seen={"SMP-0006"}, scanned={"SMP-0006"})
    assert log == []
    assert labels[1]["status"] == "present"


def test_sample_ids_stay_unique():
    """verify_lookup_table gates on this, and formula_to_actions assumes it."""
    labels = [entry("SMP-0006", 1.0, 0.0)]
    for _ in range(5):
        bm.observe(labels, [reading(1.01, 0.0, "SMP-0006"),
                            reading(1.30, 0.0, "SMP-0006")])
    ids = [e["sample_id"] for e in labels if e["sample_id"]]
    assert len(ids) == len(set(ids)) == 1


def test_identity_is_never_rewritten():
    """A position may be revised; who the bottle is may not."""
    labels = [entry("SMP-0006", 1.0, 0.0, probability=1.0, material="Linalool")]
    bm.observe(labels, [reading(1.01, 0.0, "SMP-0006", probability=0.3,
                                material="Citral")])
    assert labels[0]["material"] == "Linalool"
    assert labels[0]["probability"] == 1.0


def test_repeated_agreeing_looks_tighten_the_spread():
    labels = [entry("SMP-0006", 1.0, 0.0, spread=0.03)]
    spreads = []
    for _ in range(4):
        bm.observe(labels, [reading(1.0, 0.0, "SMP-0006", spread=0.004)])
        spreads.append(labels[0]["position_spread_m"])
    assert all(b < a for a, b in zip(spreads, spreads[1:])), spreads
    assert spreads[-1] < spreads[0] / 1.5, spreads


def test_a_quiet_pass_logs_nothing():
    labels = [entry("SMP-0006", 1.0, 0.0)]
    assert bm.observe(labels, []) == []
    assert bm.mark_missing(labels, seen={"SMP-0006"}, scanned={"SMP-0006"}) == []


def test_missing_then_seen_again_recovers():
    """The point of not deleting: the next pass gets it back."""
    labels = [entry("SMP-0006", 1.0, 0.0)]
    bm.mark_missing(labels, seen=set(), scanned={"SMP-0006"})
    assert labels[0]["status"] == "missing"
    bm.observe(labels, [reading(1.0, 0.0, "SMP-0006")])
    assert labels[0]["status"] == "present"


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = []
    for test in tests:
        try:
            test()
            print(f"PASS  {test.__name__}")
        except AssertionError as exc:
            failed.append(test.__name__)
            print(f"FAIL  {test.__name__}: {exc}")
    print(f"\n{len(tests) - len(failed)}/{len(tests)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
