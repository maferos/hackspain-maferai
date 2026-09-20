"""The formula order and its workflow, from the chat to the balance.

A formula arrives from the chat or as JSON and becomes one order: the formula
as JSON (the harness/formulas format, plus the flask the scan found for each
line), written to simulation/out/formula_order.json and served at
GET /api/formula for the robot's executor, and a workflow the panels show and
cross off as it goes.

    order:        scan → formula → check → dose → QC → done
    ingredient:   locate → pick → carry → dose → verify → return

Who crosses a step off:

* The executor, for any step, in process through :meth:`Workflow.report` or
  over HTTP with POST /api/workflow/report::

      {"ingredient": "SMP-0014", "step": "dose", "status": "active", "mass": 0.84}

  ``ingredient`` is the sample id, the compound or the ingredient id; ``status``
  is active, completed, failed or skipped; ``mass`` is the balance's net
  reading for that ingredient, in grams. A report of "order" / "qc" closes the
  order.
* The backend, for what it can see without being told: the scan naming the
  flask's ring (locate), the controller's caption and the gripper (pick,
  return), and the reported mass against the target (verify).

A step never goes backwards, and reports and observations agree on that.

Until the executor exists, VIEW_FORMULA_EXECUTOR=fetch (the default) has the
arm fetch each flask through the scan controller's own pick: it locates, picks
and returns, and the order says it was fetched, not dosed. Set it to
``external`` to leave the arm to an executor that reports.
"""
from __future__ import annotations

import json
import os
import re
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from catalogue import MAX_BATCH_G, MIN_DOSE_G, REPO, Catalogue, resolve as cat_resolve

ORDER_FILE = REPO / "simulation" / "out" / "formula_order.json"
EXECUTOR = os.environ.get("VIEW_FORMULA_EXECUTOR", "fetch")
TOLERANCE_G = 0.010
BALANCE = "balance_2"
LOG_KEEP = 40

STEPS = {
    "fetch": ("locate", "pick", "return"),
    "external": ("locate", "pick", "carry", "dose", "verify", "return"),
}
STEP_LABELS = {
    "locate": "Locate {sample} by its ring",
    "pick": "Pick {sample}",
    "carry": "Carry it to " + BALANCE,
    "dose": "Dose {grams:.3f} g of {compound}",
    "verify": "Verify on " + BALANCE,
    "return": "Return {sample} to the bench",
}
# A formula's stages. The bench scan is not among them: the scan is the lab's
# own task, done once, and a formula that ran after it does not carry a copy.
STAGES = {
    "fetch": (("formula", "Formula"), ("check", "Check"), ("fetch", "Fetch"), ("done", "Done")),
    "external": (("formula", "Formula"), ("check", "Check"), ("dose", "Dose"),
                 ("qc", "QC"), ("done", "Done")),
}
# The scan task's, which is the one step it is.
SCAN_STAGES = (("scan", "Scan"),)
DONE = ("completed", "failed", "skipped")
# The controller's captions that name a sample, and the step each one is.
CAPTION_STEPS = (
    (re.compile(r"^(travelling to|moving over|reaching down for|closing on) (SMP-\d{4})"), "pick", "active"),
    (re.compile(r"^(lifting|holding) (SMP-\d{4})"), "pick", "completed"),
    (re.compile(r"^(putting) (SMP-\d{4}) back"), "return", "active"),
    (re.compile(r"^(releasing) (SMP-\d{4})"), "return", "active"),
    (re.compile(r"^(clear of) (SMP-\d{4})"), "return", "completed"),
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def lines_from_json(doc) -> tuple[list[dict], dict]:
    """The lines of a formula given as JSON, in any of the forms it comes in.

    Accepts the harness/formulas files (``material``, ``batch_g``), this
    module's own order JSON, simple lines (``compound``/``name``, ``grams``/
    ``g``), a bare list of them, or ``{"id": "FRG-101", "batch_g": 3}`` for a
    catalogue formula.

    Returns:
        The lines as ``[{"compound", "grams"}]`` and the formula's header
        (``id``, ``name``, ``batch_g`` when given).

    Raises:
        ValueError: When there is nothing that reads as a formula.
    """
    if isinstance(doc, list):
        doc = {"ingredients": doc}
    if not isinstance(doc, dict):
        raise ValueError("a formula is a JSON object or a list of ingredients")
    head = {k: doc[k] for k in ("id", "name") if isinstance(doc.get(k), str)}
    batch = doc.get("batch_g") or (doc.get("batch") or {}).get("concentrate_g")
    if batch is not None:
        head["batch_g"] = float(batch)
    lines = []
    for item in doc.get("ingredients") or []:
        if not isinstance(item, dict):
            raise ValueError("each ingredient is an object")
        name = item.get("cas") or item.get("compound") or item.get("material") or item.get("name")
        grams = item.get("grams", item.get("batch_g", item.get("g")))
        if grams is None and item.get("concentrate_pct") is not None and batch:
            grams = float(item["concentrate_pct"]) / 100 * float(batch)
        if name is None or grams is None:
            raise ValueError(f"ingredient {item} needs a compound and grams")
        lines.append({"compound": str(name), "grams": float(grams)})
    if not lines and "id" not in head:
        raise ValueError("no ingredients in this JSON")
    return lines, head


class Order:
    """One formula on its way through the lab."""

    def __init__(self, order_id: str, formula: dict, source: str, executor: str) -> None:
        self.id, self.formula, self.source, self.executor = order_id, formula, source, executor
        self.created = time.time()
        self.started: float | None = None
        self.finished: float | None = None
        self.status = "queued"
        self.check: dict | None = None
        self.heap: dict | None = None       # the harness's plan, see actions.py
        self.qc: dict | None = None
        self.doc: dict = {}
        self.log: list[dict] = []
        self.items = []
        for ing in formula["ingredients"]:
            steps = {s: {"status": "skipped" if ing["problem"] else "queued", "started": None,
                         "completed": None, "note": ""} for s in STEPS[executor]}
            self.items.append({**ing, "mass": None, "steps": steps})

    def elapsed(self) -> float:
        if self.started is None:
            return 0.0
        return (self.finished or time.time()) - self.started

    def active_items(self) -> list[dict]:
        return [i for i in self.items if not i["problem"]]


class Workflow:
    """The current order: its JSON, its steps, and who has crossed what off.

    Args:
        catalogue: The sample catalogue.
        shelf: Returns the flasks the scan has named (catalogue.shelf_from_tracks).
        on_mass: Called with (grams) for every mass the executor reports, for
            the balance chart.
        executor: ``fetch`` or ``external``, see the module docstring.
        scene_model: Returns ``(model, data)`` of the compiled scene, for the
            action plan: it is the only thing that knows which bottles have a
            free joint. Without it the plan still builds, calling none of them
            liftable.
        scene_name: Named in the reason an ingredient could not be placed.
        scan_done: Whether the bench scan has finished. The scan is the lab's
            first task and no formula is checked or started before it is done:
            a flask the arm has not looked at yet is not a flask the bench
            lacks, and checking against half a bench rejects orders it should
            have run.
    """

    def __init__(self, catalogue: Catalogue, shelf, on_mass=None, executor: str = EXECUTOR,
                 order_file: Path | None = ORDER_FILE, scene_model=None,
                 scene_name: str = "the bench", scan_done=None) -> None:
        self.catalogue, self.shelf, self.on_mass = catalogue, shelf, on_mass
        self.executor = executor if executor in STEPS else "fetch"
        self.order_file = order_file
        self.scene_model = scene_model or (lambda: (None, None))
        self.scene_name = scene_name
        self.scan_done = scan_done or (lambda: True)
        self.orders: list[Order] = []
        self.lock = threading.RLock()
        self._numbers = iter(range(1, 10_000))

    # --- the queue ----------------------------------------------------------

    @property
    def order(self) -> Order | None:
        """The order everything else means: the live one, else the last made.

        Most of this module was written when there was only ever one. It reads
        the same now — the front of the queue — and falls back to the last
        finished order so the panel keeps showing a result instead of emptying.
        """
        live = [o for o in self.orders if o.status in ("queued", "running")]
        return live[0] if live else (self.orders[-1] if self.orders else None)

    def waiting(self) -> list[Order]:
        """The orders behind the front of the queue, in the order they arrived."""
        live = [o for o in self.orders if o.status in ("queued", "running")]
        return live[1:]

    def pump(self) -> Order | None:
        """Admit the front of the queue once the scan is done. Returns it.

        The scan is the lab's first task; only when it is finished does a
        formula get checked, planned and handed over. Rejected orders fall out
        here, one per call, so the queue keeps moving without a loop that could
        admit a whole queue in one tick.
        """
        with self.lock:
            if not self.scan_done():
                return None
            for order in self.orders:
                if order.status in ("queued", "running"):
                    return self._admit(order) if order.check is None else order
            return None

    # --- the formula as JSON ------------------------------------------------

    def formula_json(self, resolved: dict, source: str) -> dict:
        """A resolved formula (catalogue.resolve) in the harness/formulas format.

        Each line keeps the harness keys (``material``, ``cas``, ``batch_g``,
        ``concentrate_pct``, ``samples``) and adds the flask the scan found
        (``sample_id``, ``located``), or why there is none (``problem``).
        """
        total = sum(i["grams"] for i in resolved["ingredients"]) or 1.0
        shelf = {v["sampleId"]: v for v in self.shelf()}
        ingredients = []
        for ing in resolved["ingredients"]:
            flask = shelf.get(ing["sampleId"])
            ingredients.append({
                "id": ing["id"], "material": ing["compound"], "cas": ing["cas"],
                "batch_g": ing["grams"], "concentrate_pct": round(100 * ing["grams"] / total, 2),
                "samples": sorted(s for s, v in self.catalogue.samples.items() if v["cas"] == ing["cas"]),
                "sample_id": ing["sampleId"],
                "located": {"x": flask["x"], "y": flask["y"], "track": flask["track"]} if flask else None,
                "problem": ing["problem"],
            })
        return {
            "id": resolved["id"], "name": resolved["name"], "source": source,
            "catalogue": "computer-vision/barcodes/lookup_table.json",
            "batch": {"concentrate_g": resolved["targetMass"],
                      "make_g": round(sum(i["grams"] for i in resolved["ingredients"] if not i["problem"]), 3)},
            "tolerance_g": TOLERANCE_G, "balance": BALANCE,
            "ingredients": ingredients, "unknown": resolved.get("unknown", []),
        }

    # --- orders ---------------------------------------------------------------

    def submit(self, formula: dict, source: str) -> Order:
        """Put a formula on the queue, and check it if its turn has come.

        The queue is the lab's task list after the scan. A formula sent while
        the bench is still being read waits, unchecked: which flasks are on the
        bench is not known yet, and an order rejected for a flask nobody has
        looked at is a wrong answer given early.
        """
        with self.lock:
            doc = self.formula_json(formula, source)
            order = Order(f"ORD-{next(self._numbers):03d}", formula, source, self.executor)
            doc["order"] = {"id": order.id, "created": _now(), "executor": self.executor}
            order.doc = doc
            self.orders.append(order)
            # Before the scan, nothing has been matched to a flask yet, so the
            # weight worth reporting is what was asked for, not what the empty
            # bench could supply.
            asked = sum(i["batch_g"] for i in doc["ingredients"])
            ahead = [o for o in self.orders[:-1] if o.status in ("queued", "running")]
            self._log(f"{order.id} received from the {source}: {formula['name']}, "
                      f"{len(order.items)} ingredients, {asked:.3f} g"
                      + (f", {len(ahead)} ahead of it" if ahead else ""), "info")
            if not self.scan_done():
                self._log(f"{order.id} waits for the bench scan", "info")
                self._write()
                return order
            if ahead:
                self._write()
                return order
            return self._admit(order)

    def _admit(self, order: Order) -> Order:
        """Check a queued formula against the finished bench, and plan it.

        Called when the order reaches the front of the queue, not when it is
        sent, so the bench it is judged against is the whole bench.
        """
        with self.lock:
            if order.check is not None:
                return order
            self._reresolve(order)
            doc = order.doc
            total = sum(i["batch_g"] for i in doc["ingredients"] if not i["problem"])
            # A formula the bench cannot make is rejected whole, not run with
            # the lines it happens to have: half a fragrance is not a fragrance.
            # Whatever fails, fails here, so the panel's Check stage carries the
            # reason instead of it surfacing at the end as QC.
            problems = [{"compound": i["compound"], "reason": i["problem"]}
                        for i in order.items if i["problem"]]
            if not order.items:
                problems = [{"compound": "—", "reason": "no ingredients in this formula"}]
            elif total > MAX_BATCH_G:
                problems.append({"compound": "—", "reason":
                                 f"the batch is {total:.2f} g; the balance takes {MAX_BATCH_G:g} g at most"})
            if problems:
                order.check = {"passed": False, "problems": problems, "seconds": 0.0}
                order.status = "rejected"
                order.finished = order.created
                for item in order.items:
                    for step in item["steps"].values():
                        step["status"] = "skipped"
                for problem in problems:
                    self._log(f"{order.id} cannot run: {problem['compound']} — {problem['reason']}", "warn")
                self._log(f"{order.id} rejected at the check", "warn")
                self._write()
                return order
            order.check = {"passed": True, "problems": [], "seconds": 0.0}
            order.heap = self._plan(order)
            self._log(f"{order.id} passed the check: {len(order.active_items())} ingredients on the bench",
                      "info")
            if order.heap:
                got = order.heap["summary"]
                self._log(f"{order.id} planned: {got['actions']} actions over {got['ingredients']} "
                          f"ingredients, {got['executable']} of them a skill that exists", "info")
            self._write()
            return order

    def _reresolve(self, order: Order) -> None:
        """Match the formula to the bench again, now that the bench is whole.

        An order queued during the scan was resolved against whatever had been
        named at the time — on an empty bench, every line reads "not identified"
        and the check would refuse a formula it could perfectly well make.
        Deferring the verdict is not enough; the question has to be asked again.
        """
        lines = [{"compound": i["cas"] or i["compound"], "grams": i["grams"]}
                 for i in order.formula["ingredients"]]
        if not lines:
            return
        resolved = cat_resolve(lines, self.shelf(), self.catalogue,
                               order.formula.get("id", "CHAT"), order.formula.get("name", ""))
        order.formula = resolved
        doc = self.formula_json(resolved, order.source)
        doc["order"] = order.doc.get("order", {})
        order.doc = doc
        order.items = []
        for ing in resolved["ingredients"]:
            steps = {s: {"status": "skipped" if ing["problem"] else "queued", "started": None,
                         "completed": None, "note": ""} for s in STEPS[order.executor]}
            order.items.append({**ing, "mass": None, "steps": steps})

    def _plan(self, order: Order) -> dict | None:
        """Every primitive this order implies, against the bench as it is now.

        The six steps run the order; this is the same order spelled out the way
        a VLA is told, and it is only ever read. A planner that cannot run
        leaves the order without one rather than stopping it.
        """
        try:
            import actions as act
            return act.heap(order.doc, self.shelf(), *self.scene_model(),
                            scene=self.scene_name, balance=int(BALANCE.rsplit("_", 1)[-1]))
        except Exception as exc:                        # never fail an order over the plan
            self._log(f"{order.id}: no action plan ({exc})", "warn")
            return None

    def start(self) -> None:
        """The executor has taken the order."""
        with self.lock:
            order = self.order
            if order is not None and order.started is None:
                order.started, order.status = time.time(), "running"
                self._log(f"{order.id} started by the {order.executor} executor", "ok")

    def abort(self, why: str = "stopped by the operator") -> None:
        with self.lock:
            order = self.order
            if order is None or order.status not in ("queued", "running"):
                return
            order.status, order.finished = "aborted", time.time()
            for item in order.items:
                for step in item["steps"].values():
                    if step["status"] == "active":
                        step.update(status="failed", completed=order.elapsed(), note=why)
            self._log(f"{order.id} {why}", "warn")
            self._write()

    def report(self, ingredient: str | None, step: str, status: str, mass: float | None = None,
               note: str | None = None, source: str = "executor") -> None:
        """Cross a step off, or mark it under way.

        Args:
            ingredient: Sample id, compound or ingredient id; None or "order"
                for the order itself (``qc``, ``done``).
            step: One of the ingredient steps, or ``qc``/``done`` for the order.
            status: active, completed, failed or skipped.
            mass: Net grams on the balance for this ingredient, if known.
            note: A few words for the task panel.

        Raises:
            KeyError: For an unknown ingredient or step.
        """
        with self.lock:
            order = self.order
            if order is None or order.status not in ("queued", "running"):
                raise KeyError("there is no order running")
            if status not in ("active", "completed", "failed", "skipped"):
                raise KeyError(f"unknown status {status!r}")
            if order.started is None:
                self.start()
            if ingredient in (None, "", "order"):
                if step not in ("qc", "done"):
                    raise KeyError(f"unknown order step {step!r}")
                if status in DONE:
                    self._close(passed=status == "completed", note=note)
                return
            item = self._item(ingredient)
            if step not in item["steps"]:
                raise KeyError(f"unknown step {step!r}; this order has {', '.join(item['steps'])}")
            if mass is not None:
                item["mass"] = float(mass)
                if self.on_mass:
                    self.on_mass(float(mass))
            self._advance(item, step, status, note, source)
            if step == "dose" and status == "completed":
                # What came out of the flask is gone from it: the next formula's
                # check sees the lower level.
                if item["sampleId"]:
                    left = self.catalogue.levels.take(item["sampleId"], item["mass"] or item["grams"])
                    self._log(f"{item['sampleId']} has {left:.3g} ml left", "info")
                if "verify" in item["steps"]:
                    self._verify(item)
            self._maybe_close()
            self._write()

    # --- what the backend sees for itself ---------------------------------

    def observe(self, tracks, caption: str, holding: bool) -> None:
        """Cross off what the scan and the arm show, a few times a second."""
        with self.lock:
            order = self.order
            if order is None or order.status not in ("queued", "running"):
                return
            named = {t.sample: t for t in tracks if t.sample and t.state != "lost"}
            for item in order.items:
                if item["problem"] == "not identified on the bench":
                    # The scan may name it after the order came in.
                    flask = next((f for f in self.shelf() if f["cas"] == item["cas"]), None)
                    if flask is not None:
                        item["problem"], item["sampleId"] = None, flask["sampleId"]
                        for step in item["steps"].values():
                            step["status"] = "queued"
                        self._log(f"{item['compound']}: the scan found {flask['sampleId']}", "ok")
                if item["problem"]:
                    continue
                track = named.get(item["sampleId"])
                if track is not None and item["steps"]["locate"]["status"] not in DONE:
                    ring = track.confirmation.marker_id if track.confirmation else None
                    self._advance(item, "locate", "completed",
                                  f"ring {ring} at ({track.xy[0]:+.2f}, {track.xy[1]:+.2f})"
                                  if ring is not None else "named by its ring", "scan")
            caption = (caption or "").strip()
            for pattern, step, status in CAPTION_STEPS:
                match = pattern.match(caption)
                if not match:
                    continue
                item = next((i for i in order.active_items() if i["sampleId"] == match.group(2)), None)
                if item is None or step not in item["steps"]:
                    break
                if step == "pick" and status == "completed" and not holding:
                    status = "active"
                if order.started is None:
                    self.start()
                self._advance(item, step, status, None, "arm")
                break
            self._maybe_close()

    # --- internals ----------------------------------------------------------

    def _item(self, key: str) -> dict:
        key = str(key)
        for item in self.order.items:
            if key in (item["id"], item["sampleId"], item["cas"]) or key.lower() == item["compound"].lower():
                return item
        raise KeyError(f"no ingredient {key!r} in {self.order.id}")

    def _advance(self, item: dict, step: str, status: str, note, source: str) -> None:
        steps = item["steps"]
        names = list(steps)
        record = steps[step]
        if record["status"] in DONE or (record["status"] == "active" and status == "active"):
            if note:
                record["note"] = note
            return
        clock = self.order.elapsed()
        if status == "active":
            record.update(status="active", started=clock)
        else:
            record.update(status=status, completed=clock)
            if record["started"] is None:
                record["started"] = clock
        if note:
            record["note"] = note
        # An executor starting or finishing a step says the ones before it are
        # over. What the arm is seen doing only speaks for that step: a grasp
        # that closed on nothing still goes on to put the hand back.
        for earlier in (names[:names.index(step)] if source == "executor" else ()):
            if steps[earlier]["status"] not in DONE:
                steps[earlier].update(status="completed", completed=clock)
                if steps[earlier]["started"] is None:
                    steps[earlier]["started"] = clock
        if status != "active":
            label = STEP_LABELS[step].format(sample=item["sampleId"], compound=item["compound"],
                                             grams=item["grams"])
            level = {"completed": "ok", "failed": "warn", "skipped": "info"}[status]
            mark = "✓" if status == "completed" else "✗" if status == "failed" else "–"
            self._log(f"{mark} {item['compound']}: {label[0].lower()}{label[1:]}"
                      + (f" · {note}" if note else ""), level)

    def _verify(self, item: dict) -> None:
        mass = item["mass"]
        if mass is None:
            return
        error = mass - item["grams"]
        ok = abs(error) <= TOLERANCE_G
        self._advance(item, "verify", "completed" if ok else "failed",
                      f"{mass:.3f} g ({error:+.3f})", "balance")

    def _maybe_close(self) -> None:
        order = self.order
        items = order.active_items()
        if order.status != "running" or not items:
            return
        if all(all(s["status"] in DONE for s in i["steps"].values()) for i in items):
            if order.executor == "fetch":
                self._close(passed=all(i["steps"]["pick"]["status"] == "completed" for i in items),
                            note="fetched, not dosed: the arm has the gripper")
            else:
                masses = [i["mass"] for i in items if i["mass"] is not None]
                self._close(passed=all(i["steps"].get("verify", {}).get("status") == "completed"
                                       for i in items), note=f"{sum(masses):.3f} g in the beaker"
                            if masses else None)

    def _close(self, passed: bool, note: str | None) -> None:
        order = self.order
        order.status, order.finished = "completed", time.time()
        masses = [i["mass"] for i in order.active_items() if i["mass"] is not None]
        target = sum(i["grams"] for i in order.active_items())
        order.qc = {"passed": passed, "note": note, "finalMass": sum(masses) if masses else None,
                    "targetMass": target, "seconds": order.elapsed()}
        self._log(f"{order.id} {'complete' if passed else 'finished with problems'}"
                  + (f" · {note}" if note else ""), "ok" if passed else "warn")
        self._write()

    def _log(self, message: str, level: str) -> None:
        order = self.order
        if order is None:
            return
        order.log.append({"time": round(order.elapsed(), 1), "message": message, "level": level})
        del order.log[:-LOG_KEEP]

    def _write(self) -> None:
        order = self.order
        if order is None or self.order_file is None:
            return
        doc = dict(order.doc)
        doc["order"] = {**doc["order"], "status": order.status, "qc": order.qc,
                        "progress": {i["sampleId"] or i["compound"]: {k: v["status"] for k, v in i["steps"].items()}
                                     for i in order.items}}
        try:
            self.order_file.parent.mkdir(parents=True, exist_ok=True)
            self.order_file.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
        except OSError:
            pass

    # --- LabState -----------------------------------------------------------

    def state(self, scan_done: bool) -> dict | None:
        """The ``order`` block of LabState, or None before the first order."""
        with self.lock:
            order = self.order
            if order is None:
                return None
            items = order.active_items()
            done = sum(all(s["status"] in DONE for s in i["steps"].values()) for i in items)
            return {
                "id": order.id, "status": order.status, "executor": order.executor,
                "source": order.source, "formula": order.doc,
                "elapsedSeconds": order.elapsed(), "estimateSeconds": order.formula["estimate"]["seconds"],
                "stages": self._stages(order, scan_done), "qc": order.qc, "check": order.check,
                "heap": order.heap,
                "done": done, "total": len(items),
                "queue": [{"id": o.id, "name": o.formula["name"], "status": o.status,
                           "ingredients": len(o.items)} for o in self.waiting()],
                "ingredients": [{
                    "id": i["id"], "compound": i["compound"], "cas": i["cas"], "grams": i["grams"],
                    "sampleId": i["sampleId"], "problem": i["problem"], "mass": i["mass"],
                    "steps": [{"id": k, **v} for k, v in i["steps"].items()],
                } for i in order.items],
                "log": list(order.log),
            }

    def _stages(self, order: Order, scan_done: bool) -> list[dict]:
        """The stage bar, with every failure shown on the stage that failed.

        A rejected formula stops at Check and the rest is skipped; a dose that
        failed marks the fetching stage, not Done. Done only ever fails on its
        own account, which it cannot, so it is completed or waiting.
        """
        items = order.active_items()
        worked = order.started is not None
        all_done = order.status == "completed"
        checked = order.check is not None
        if not checked:
            # Still on the queue. Nothing about this formula has happened yet,
            # so the bar says so rather than ticking Formula and lighting a
            # Check that is not running.
            return [{"id": sid, "label": label, "status": "queued"}
                    for sid, label in STAGES[order.executor]]
        status = {
            "formula": "completed",
            "check": "completed" if checked else "active",
            "fetch": "completed" if all_done else "active" if worked else "queued",
            "dose": "completed" if all(all(s["status"] in DONE for s in i["steps"].values()) for i in items)
            else "active" if worked else "queued",
            "qc": "completed" if all_done else "queued",
            "done": "completed" if all_done else "queued",
        }
        if order.status == "rejected":
            # Nothing was attempted: the check is the failure and the rest of
            # the bar never happened.
            return [{"id": sid, "label": label,
                     "status": "failed" if sid == "check" else status[sid] if sid == "formula"
                     else "skipped"} for sid, label in STAGES[order.executor]]
        if order.status == "aborted":
            status = {k: ("failed" if v == "active" else v) for k, v in status.items()}
        # A step that failed belongs to the stage that runs it.
        if any(s["status"] == "failed" for i in items for s in i["steps"].values()):
            for sid in ("fetch", "dose"):
                if status[sid] in ("completed", "active"):
                    status[sid] = "failed"
        if order.qc and not order.qc["passed"]:
            status["qc"] = "failed"
        return [{"id": sid, "label": label, "status": status[sid]} for sid, label in STAGES[order.executor]]

    def plan_steps(self) -> list[dict]:
        """The order's steps for the task panel's plan, grouped by ingredient."""
        with self.lock:
            order = self.order
            if order is None:
                return []
            out = []
            for item in order.active_items():
                for sid, step in item["steps"].items():
                    detail = [("", step["note"])] if step["note"] else []
                    out.append({
                        "id": f"{order.id}-{item['id']}-{sid}",
                        "label": STEP_LABELS[sid].format(sample=item["sampleId"], compound=item["compound"],
                                                         grams=item["grams"]),
                        "ingredientId": item["id"], "status": step["status"], "attempt": 1,
                        "startedAt": step["started"], "completedAt": step["completed"],
                        "detail": [list(kv) for kv in detail],
                        "group": f"{item['compound']} · {item['sampleId']}",
                    })
            return out
