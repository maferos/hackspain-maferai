"""Record one pass of the scripted run for the robot viewer to play on its own.

Steps :class:`ScriptedRun` through the whole run at the publisher's rate,
without waiting, and writes ``view/frontend/public/scripted-run.json``: the
snapshot, then every message in run time. A ``state_update`` keeps only the
top-level keys that changed since the previous one, and in lists of records
(plan steps, pipeline modules, ingredients) only the records that changed;
replayed in order it gives the same state as the live feed. The evaluator's
ground truth is left out (the viewer does not use it).

Run from ``dashboard/bridge`` with the repo's virtual environment, after
changing the scripted run::

    python -m labbridge.record_run
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import mujoco

from labbridge.mock_run import ACTIVE_BALANCE, RAIL, SCENE, ScriptedRun
from labbridge.mujoco_adapter import vessels, workcell

OUT = Path(__file__).resolve().parents[3] / "view" / "frontend" / "public" / "scripted-run.json"
# The run keeps publishing this long after its last step, as the live loop does.
TAIL_S = 5.0

logger = logging.getLogger("labbridge.record_run")


def compact(new, old):
    """``new`` with every list of ``{id}`` records that kept its ids reduced to
    ``{"$changed": {index: record}}``; the viewer rebuilds it from the list it
    already has. Most ticks change one step of forty, not the plan."""
    if isinstance(new, dict) and isinstance(old, dict):
        return {k: compact(v, old.get(k)) for k, v in new.items()}
    if (
        isinstance(new, list)
        and isinstance(old, list)
        and len(new) == len(old)
        and new
        and all(isinstance(a, dict) and isinstance(b, dict) and "id" in a and a.get("id") == b.get("id") for a, b in zip(new, old))
    ):
        return {"$changed": {str(i): a for i, (a, b) in enumerate(zip(new, old)) if a != b}}
    return new


def rounded(x, digits: int = 4):
    """Round every float so float noise does not count as a change."""
    if isinstance(x, float):
        return round(x, digits)
    if isinstance(x, dict):
        return {k: rounded(v, digits) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [rounded(v, digits) for v in x]
    return x


class Recorder:
    """Stands in for :class:`StateServer` and keeps what the run publishes."""

    def __init__(self) -> None:
        self.messages: list[dict] = []
        self.time = 0.0
        self.keep_state = True
        self.previous: dict = {}

    def patch(self, patch: dict, timestamp: float | None = None) -> None:
        if not self.keep_state:
            return
        patch = rounded({k: v for k, v in patch.items() if k != "evaluator"})
        changed = {k: compact(v, self.previous.get(k)) for k, v in patch.items() if self.previous.get(k) != v}
        self.previous.update(patch)
        if changed:
            self.messages.append({"type": "state_update", "time": round(self.time, 2), "patch": changed})

    def event(self, time: float, message: str, level: str = "info") -> None:
        self.messages.append({"type": "event", "time": round(time, 2), "message": message, "level": level})

    def mass_sample(self, time: float, mass: float) -> None:
        self.messages.append({"type": "mass_sample", "time": round(time, 2), "mass": round(mass, 4)})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scene", type=Path, default=SCENE)
    parser.add_argument("--rate", type=float, default=10.0, help="run steps per second (every mass sample is kept)")
    parser.add_argument("--state-rate", type=float, default=5.0, help="state updates kept per second")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")

    model = mujoco.MjModel.from_xml_path(str(args.scene))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    run = ScriptedRun(model, data, vessels(model))
    snapshot = run.initial_state(workcell(model, data, ACTIVE_BALANCE, RAIL))
    snapshot.pop("evaluator", None)

    recorder = Recorder()
    every = max(1, round(args.rate / args.state_rate))
    steps = round((run.duration + TAIL_S) * args.rate)
    last: dict = {}
    for i in range(steps + 1):
        recorder.time = i / args.rate
        recorder.keep_state = i % every == 0 or i == steps
        last = run.apply(recorder.time, recorder, last)

    doc = {"duration": round(run.duration + TAIL_S, 2), "snapshot": rounded(snapshot), "messages": recorder.messages}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    logger.info("%s: %.0f s, %d messages, %.0f kB", args.out, doc["duration"], len(doc["messages"]), args.out.stat().st_size / 1024)


if __name__ == "__main__":
    main()
