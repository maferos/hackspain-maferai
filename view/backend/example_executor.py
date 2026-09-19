"""An example formula executor: how the real one talks to the viewer.

It does not move the arm. It waits for an order (GET /api/formula), and for
each ingredient reports its steps as a real executor would, with the balance
reading climbing to the target while it "doses" (POST /api/workflow/report).
The panels then cross the steps off exactly as they will for the real one.

    python view/backend/example_executor.py                  # against :8000
    python view/backend/example_executor.py --backend http://localhost:8010 --speed 2

Run the backend with VIEW_FORMULA_EXECUTOR=external so the built-in fetch does
not take the order first. The real executor reads the same JSON (also written
to simulation/out/formula_order.json) and reports the same way, over HTTP or in
process with ``scene.lab.workflow.report(...)``.
"""
from __future__ import annotations

import argparse
import json
import random
import time
import urllib.error
import urllib.request


def call(backend: str, path: str, body: dict | None = None) -> dict | None:
    request = urllib.request.Request(
        backend + path, data=None if body is None else json.dumps(body).encode(),
        headers={"Content-Type": "application/json"}, method="GET" if body is None else "POST")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 409):
            return None
        raise
    except (urllib.error.URLError, ConnectionError, TimeoutError):
        return None  # the backend is restarting; try again next time round


def run_order(backend: str, order: dict, speed: float) -> None:
    def report(sample, step, status, **extra):
        call(backend, "/api/workflow/report", {"ingredient": sample, "step": step, "status": status, **extra})

    def wait(seconds):
        time.sleep(seconds / speed)

    for line in order["ingredients"]:
        sample = line["sample_id"]
        if line.get("problem") or not sample:
            continue
        target = float(line["batch_g"])
        report(sample, "pick", "active", note="closing on the flask")
        wait(3)
        report(sample, "pick", "completed", note="held on force feedback")
        report(sample, "carry", "active")
        wait(3)
        report(sample, "carry", "completed")
        # Pour fast, then slow near the target, as a dosing controller would.
        mass, final = 0.0, target + random.uniform(-0.006, 0.006)
        report(sample, "dose", "active", mass=mass, note="fast pour")
        while mass < final:
            step = 0.12 if final - mass > 0.25 else 0.02
            mass = min(final, mass + step)
            report(sample, "dose", "active", mass=round(mass, 4),
                   note="fast pour" if final - mass > 0.25 else "slow pour")
            wait(0.3)
        report(sample, "dose", "completed", mass=round(mass, 4))
        wait(1)
        report(sample, "return", "active")
        wait(3)
        report(sample, "return", "completed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", default="http://localhost:8000")
    parser.add_argument("--speed", type=float, default=1.0, help="time scale; 2 runs twice as fast")
    args = parser.parse_args()
    done = set()
    print(f"waiting for orders on {args.backend}")
    while True:
        order = call(args.backend, "/api/formula")
        # An order is its id and when it was made: ids start again with the backend.
        key = (order["order"]["id"], order["order"]["created"]) if order else None
        if order and order["order"]["status"] in ("queued", "running") and key not in done:
            print(f"running {key[0]}: {order['name']}", flush=True)
            run_order(args.backend, order, args.speed)
            done.add(key)
        time.sleep(1)


if __name__ == "__main__":
    main()
