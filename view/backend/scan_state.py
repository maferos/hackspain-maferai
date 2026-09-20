"""The side panels' LabState, read off the live scan (live_scan.py) and the order.

The scan owns the arm and the cameras; this only watches it. A few times a
second it turns vision_pick's world model (the tracks and what their rings
said), the arm's joints and gripper, the controller's caption and the current
formula order (workflow.py) into the LabState the panels read on :8765 (see
dashboard/bridge/README.md), and forwards the scan's log lines as events.
Nothing is scripted: a panel shows what is going on, or says it is waiting.

``FetchExecutor`` stands in for the formula executor until there is one: it
has the arm fetch each flask of the order through the scan controller's own
pick command, one after the other.
"""
from __future__ import annotations

import os
import re
import sys
import threading
import time

from catalogue import REPO, Catalogue, shelf_from_tracks
from live_scan import vp
from gantry_motion import is_gantry
from workflow import DONE, SCAN_STAGES, Workflow

sys.path.insert(0, str(REPO / "dashboard" / "bridge"))
from labbridge import state as S  # noqa: E402
from labbridge.mujoco_adapter import workcell  # noqa: E402

rk = vp.rk
PUBLISH_S = 0.25
BALANCE = "balance_2"
PICK_TIMEOUT_S = 600.0

# The controller's captions, as states for the Robot panel: the first match wins.
CAPTIONS = (
    ("idle", "IDLE"), ("settling", "INIT"), ("raising the hand", "INIT"), ("back to carry", "RETREAT"),
    ("parking", "PARK"), ("survey", "SURVEY"), ("travelling", "TRAVERSE"), ("over the flasks", "TRAVERSE"),
    ("turning the camera", "APPROACH"), ("looking at", "LOOK"), ("reading the ring", "READ_RING"),
    ("backing off", "RETREAT"), ("is gone", "RETARGET"), ("moving over", "APPROACH"),
    ("reaching down", "REACH"), ("closing on", "GRASP"), ("lifting", "LIFT"),
    ("holding", "HOLD"), ("putting", "PLACE"), ("releasing", "RELEASE"), ("clear of", "RETREAT"),
)
MOVING = {"INIT", "PARK", "TRAVERSE", "APPROACH", "LOOK", "RETREAT", "RETARGET", "REACH",
          "LIFT", "PLACE"}
TRACK = re.compile(r"track (\d+)")
SAMPLE = re.compile(r"\b(SMP-\d{4})\b")
EVENT = re.compile(r"^\[\s*([\d.]+) s\] (.*)$")


def fsm_of(caption: str) -> str:
    text = caption.lower()
    return next((state for key, state in CAPTIONS if key in text), "WORKING")


def level_of(message: str) -> str:
    text = message.lower()
    if any(k in text for k in ("lost", "gone", "moved", "missed", "nothing", "unreachable",
                               "cannot", "not a sample")):
        return "warn"
    if any(k in text for k in ("ring reads", "lifted it", "scan done", "named")):
        return "ok"
    return "info"


def _anthropic():
    """The client briefs are composed with, or None without a key.

    The key is read from the environment, which ``server.py`` loads from the
    gitignored ``view/backend/.env``.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic
        return anthropic.Anthropic()
    except Exception:                                   # package missing or key refused
        return None


class FetchExecutor:
    """Fetches each flask of the current order through the scan controller.

    The arm carries the gripper, so this locates, picks and returns; it never
    doses. The workflow crosses the steps off from what the arm is seen doing;
    this reports what only it knows: a flask gone, a miss, a timeout.
    """

    def __init__(self, workflow: Workflow, world) -> None:
        self.workflow, self.world = workflow, world
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._run, name="formula-fetch", daemon=True)

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _run(self) -> None:
        order = self.workflow.order
        while self.world.scan is None and not self._stop.wait(0.5):
            pass
        self.workflow.start()
        for item in order.active_items():
            if self._stop.is_set() or order.status != "running":
                break
            self._fetch(item)
        if self._stop.is_set():
            with self.world.lock:
                self.world.commands[:] = [c for c in self.world.commands if c.get("cmd") != "pick"]

    def _fetch(self, item: dict) -> None:
        report = self.workflow.report
        sample = item["sampleId"]
        track = next((t for t in self.world.snapshot() if t.sample == sample and t.state != "lost"), None)
        if track is None:
            report(sample, "locate", "failed", note="the scan no longer sees it")
            report(sample, "pick", "skipped")
            report(sample, "return", "skipped")
            return
        picks = track.picks
        with self.world.lock:
            self.world.commands.append({"cmd": "pick", "track": track.id})
        began = time.monotonic()
        while not self._stop.wait(0.3):
            if track.picks > picks:
                break
            if track.state in ("unreachable", "lost"):
                report(sample, "pick", "failed", note=track.note)
                report(sample, "return", "skipped")
                return
            if time.monotonic() - began > PICK_TIMEOUT_S:
                with self.world.lock:
                    self.world.commands[:] = [c for c in self.world.commands if c.get("track") != track.id]
                report(sample, "pick", "failed", note="the arm did not get to it")
                report(sample, "return", "skipped")
                return
        if self._stop.is_set():
            return
        steps = item["steps"]
        if track.state == "missed" and steps["pick"]["status"] not in DONE:
            report(sample, "pick", "failed", note="the gripper closed on nothing")
        elif steps["pick"]["status"] not in DONE:
            report(sample, "pick", "completed", note="lifted on the gripper's force feedback")
        if steps["return"]["status"] not in DONE:
            report(sample, "return", "completed", note="put back where it stood")


class ScanState:
    """Publishes the live scan and the order as LabState, from its own thread.

    Args:
        scene: The viewer's SceneRenderer (``scan``, ``model``, ``data``,
            ``_data_lock``, ``pattern``, ``stop``).
        server: The LabState publisher.
        catalogue: For the compound behind each sample id.
    """

    def __init__(self, scene, server, catalogue: Catalogue, executor: str | None = None) -> None:
        self.scene, self.server, self.catalogue = scene, server, catalogue
        kwargs = {"executor": executor} if executor else {}
        # The action plan needs the compiled scene to tell a bottle the gripper
        # can lift from the welded stock that looks just like it.
        self.workflow = Workflow(catalogue, self.shelf, on_mass=self._mass,
                                 scene_model=lambda: (self.scene.model, self.scene.data),
                                 scene_name=self._scene_name(),
                                 scan_done=self._scan_done, client=_anthropic(), **kwargs)
        self.executor: FetchExecutor | None = None
        self._scan = None
        self._sent: list[str] = []
        self._done: dict[int, float] = {}
        self._started: dict[int, float] = {}
        self._phase = "init"
        self._mapped_at: float | None = None

    def _scan_done(self) -> bool:
        """Whether the bench has been read right through at least once."""
        scan = self.scene.scan
        return bool(scan and scan.world and scan.world.scan is not None)

    def _scene_name(self) -> str:
        """The bench a plan could not place an ingredient on, by its seed."""
        pattern = getattr(self.scene, "pattern", None)
        name = pattern.get("pattern") if isinstance(pattern, dict) else pattern
        return f"the {name} bench" if name else "this bench"

    def shelf(self) -> list[dict]:
        """The flasks the current scan has named."""
        scan = self.scene.scan
        return shelf_from_tracks(scan.world.snapshot(), self.catalogue) if scan and scan.world else []

    def dispatch(self, formula: dict, source: str):
        """Make a resolved formula the current order and set the arm on it.

        An order the check rejected is returned as it is: it stays on the panel
        with its failed Check, and the arm is never told about it.
        """
        order = self.workflow.submit(formula, source)
        self._pump()
        return order

    def _pump(self) -> None:
        """Start the front of the queue, once the scan has finished with the bench.

        The scan is the lab's first task and nothing runs beside it. After that
        one formula runs at a time: the executor is made for the order at the
        front, and the next one waits until that one is off the queue.
        """
        if self.scene.scan is None:
            return
        if self.executor is not None and self.executor.thread.is_alive():
            return
        order = self.workflow.pump()
        if order is None or order.status == "rejected":
            return
        if self.workflow.executor == "fetch":
            self.executor = FetchExecutor(self.workflow, self.scene.scan.world)
            self.executor.start()

    def stop_order(self) -> None:
        if self.executor is not None:
            self.executor.stop()
        self.workflow.abort()

    def _mass(self, grams: float) -> None:
        order = self.workflow.order
        self.server.mass_sample(order.elapsed() if order else 0.0, grams)

    def run_forever(self) -> None:
        self.server.start()
        while not self.scene.stop.is_set():
            try:
                self.publish()
            except Exception as exc:  # noqa: BLE001 -- the panels must not take the viewer down
                print(f"[view] lab state: {exc!r}")
            time.sleep(PUBLISH_S)

    # --- one tick ---------------------------------------------------------

    def publish(self) -> None:
        scan = self.scene.scan
        if scan is None or scan.world is None:
            return
        if scan is not self._scan:
            # A new layout: a new scan, from the start.
            if self._scan is not None:
                self.stop_order()
            self._scan, self._sent, self._done, self._started, self._phase = scan, [], {}, {}, "init"
            self._mapped_at = None
            with self.scene._data_lock:
                doc = workcell(self.scene.model, self.scene.data, BALANCE, self._rail())
            self.server.snapshot(S.empty_state(self._run_id(), doc))
        world = scan.world
        tracks = world.snapshot()
        with self.scene._data_lock:
            clock = float(self.scene.data.time)
            body = "gantry_bridge" if is_gantry(self.scene.model) else "rail_carriage"
            carriage = self.scene.data.body(body).xpos.copy()
            tip = self.scene.data.site(rk.TCP_SITE).xpos.copy()
            holding = rk.read_grip(self.scene.model, self.scene.data).holding
        self.workflow.observe(tracks, world.caption or "", holding)
        self._pump()
        self._forward_events(world)
        self.server.patch(self._patch(scan, world, tracks, clock, carriage, tip, holding),
                          timestamp=time.time())

    def _run_id(self) -> str:
        pattern = self.scene.pattern or {}
        return f"SCAN-{pattern['pattern'].upper()}" if pattern.get("pattern") else "SCAN"

    def _rail(self) -> dict:
        model = self.scene.model
        if is_gantry(model):
            joint, home = model.joint("gantry_x"), model.body("gantry_bridge").pos
        else:
            joint, home = model.joint(rk.RAIL_JOINT), model.body("rail_carriage").pos
        return {"x0": float(home[0] + joint.range[0]), "x1": float(home[0] + joint.range[1]),
                "y": float(home[1])}

    def _forward_events(self, world) -> None:
        for line in list(world.events):
            if line in self._sent:
                continue
            self._sent.append(line)
            match = EVENT.match(line)
            clock, message = (float(match.group(1)), match.group(2)) if match else (0.0, line)
            self.server.event(clock, message, level_of(message))
        del self._sent[:-120]

    # --- the document -------------------------------------------------------

    def _focus(self, caption: str, tracks) -> "vp.Track | None":
        by_id = {t.id: t for t in tracks}
        if (m := TRACK.search(caption)) and int(m.group(1)) in by_id:
            return by_id[int(m.group(1))]
        if m := SAMPLE.search(caption):
            return next((t for t in tracks if t.sample == m.group(1)), None)
        return None

    def _patch(self, scan, world, tracks, clock, carriage, tip, holding) -> dict:
        caption = world.caption or ""
        fsm = fsm_of(caption)
        focus = self._focus(caption, tracks)
        live = [t for t in tracks if t.state not in ("lost", "tentative")]
        named = [t for t in live if t.sample]
        empty = [t for t in live if t.state == "empty"]
        unreachable = [t for t in live if t.state == "unreachable"]
        refined = [t for t in named if t.confirmation and t.confirmation.refined_xy]
        waiting = [t for t in live if t.state == "proposed"]
        done = world.scan is not None
        if done and self._mapped_at is None:
            self._mapped_at = clock
        if fsm in ("SURVEY", "LOOK", "READ_RING", "TRAVERSE") and self._phase == "init":
            self._phase = "survey"
        if fsm in ("LOOK", "READ_RING"):
            self._phase = "look"
        order = self.workflow.state(done)
        # A formula only takes over once the scan has finished with the bench.
        # Until then the run, the plan and the bar all belong to the scan, and
        # a queued order speaks for none of them.
        busy = done and order is not None and order["status"] in ("queued", "running")
        status = "failed" if scan.error else "completed" if done and not busy else "running"
        info = self.catalogue.samples.get(focus.sample) if focus is not None and focus.sample else None
        target = (focus.sample or f"track {focus.id}") if focus is not None else None
        reading = fsm in ("LOOK", "READ_RING")
        ring = (focus.confirmation.marker_id if focus is not None and focus.confirmation else None)
        steps = self._steps(tracks, focus, clock, done, order if busy else None)
        dosing = self._dosing(order)
        external = self.workflow.executor == "external"

        return {
            # With an order, the run is the order, from queued to its end.
            # While the bench is being read the run is the scan, whatever sits
            # on the queue: the header should name the task, not the next job.
            "run": {"id": order["id"] if busy else self._run_id(),
                    "status": status if not done or not order or scan.error else
                    "running" if busy else order["status"],
                    "elapsedSeconds": order["elapsedSeconds"] if order else clock,
                    "progress": (order["done"] / max(order["total"], 1)) if order
                    else len(named) / max(len(named) + len(waiting), 1),
                    "phase": fsm.lower(), "simulated": True, "scripted": False},
            "scan": {"named": len(named), "tracked": len(live), "waiting": len(waiting),
                     "empty": len(empty), "unreachable": len(unreachable),
                     "wristOnly": sum(bool(t.wrist_only) for t in named), "done": done,
                     "cycleSeconds": round(world.cycle_seconds, 2), "error": scan.error,
                     "caption": caption},
            "order": order,
            # The lab's current task. The bench scan is the first one and
            # nothing else starts until it is done; after that the task is
            # whichever formula is at the front of the queue.
            "task": {
                "type": "scan" if not done else ("formula" if busy else "idle"),
                "id": order["id"] if (done and busy and order) else self._run_id(),
                "title": ("Bench scan" if not done else
                          order["formula"]["name"] if (busy and order) else "Waiting for a formula"),
                "status": "failed" if scan.error else "running" if (not done or busy) else "completed",
                "queued": len(order["queue"]) if order else 0,
            },
            # The scan is a task of its own: while it runs the bar is its single
            # step, not a formula's. A formula's bar appears when one starts.
            "workflow": {"stages": self._scan_stages(done, bool(scan.error)) if not done
                         else order["stages"] if busy or order else self._idle_stages(done),
                         "executor": self.workflow.executor},
            "recipe": self._recipe(order),
            "execution": {"currentStepId": next((s["id"] for s in steps if s["status"] == "active"), None),
                          "steps": steps},
            "balance": {"id": BALANCE, "netMass": dosing["mass"] if dosing else 0.0,
                        "totalMass": sum(i["mass"] or 0.0 for i in order["ingredients"]) if order else 0.0,
                        "targetMass": dosing["grams"] if dosing else 0.0,
                        "batchTargetMass": order["formula"]["batch"]["make_g"] if order else 0.0,
                        "flowRate": 0.0, "mode": "dosing" if dosing and dosing["active"] else "stopped",
                        "stable": not (dosing and dosing["active"]),
                        "ingredientId": dosing["id"] if dosing else None},
            "robot": S.robot_state(
                fsm, S.vec3(*carriage), S.vec3(*tip), arm="UR10e", end_effector="GRIPPER",
                target_object=target, compound=info["compound"] if info else None,
                gripper="holding" if holding else "open", current_action=caption),
            "perception": S.perception_state(
                "wrist" if reading else "overview", target=target,
                target_class="amber flask" if focus is not None else None,
                barcode=f"ArUco {ring}" if ring is not None else None,
                barcode_status="ring" if ring is not None else ("reading" if reading else "idle"),
                identity=focus.sample if focus is not None else None,
                container_ml=info["containerMl"] if info else None),
            "pipeline": [
                S.pipeline_node("camera", "General + wrist", [f"cycle {world.cycle_seconds:.1f} s",
                                "wrist camera on the arm"], "active" if reading else "ok"),
                S.pipeline_node("detection", "YOLO", ["—", "—"], "ok"),
                S.pipeline_node("localization", "Bench-plane ray",
                                [f"{len(live)} on the bench", f"{len(refined)} placed by ring"],
                                "active" if fsm == "SURVEY" else "ok"),
                S.pipeline_node("barcode", "ArUco ring", [f"{len(named)} named", f"{len(empty)} not samples"],
                                "active" if reading else "ok" if named else "idle"),
                S.pipeline_node("planner", "Order" if busy else "Scan controller",
                                [f"{order['id']} · {order['done']}/{order['total']}" if busy
                                 else "BENCH MAPPED" if done else f"{len(waiting)} to look at", fsm],
                                "active" if busy or (not done and fsm in ("SURVEY", "PARK")) else "ok"),
                S.pipeline_node("motion", "Rail + UR10e",
                                ["MOVING" if fsm in MOVING else "HOLD", f"rail {carriage[0]:+.2f} m"],
                                "active" if fsm in MOVING else "ok"),
                S.pipeline_node("dosing", "Executor" if external else "—",
                                [f"{dosing['compound']} {dosing['mass'] or 0:.3f} g" if dosing
                                 else "waiting" if external else "no dosing tool",
                                 f"target {dosing['grams']:.3f} g" if dosing else
                                 "reports mass" if external else "gripper on the arm"],
                                "active" if dosing and dosing["active"] else "ok" if external else "idle"),
                S.pipeline_node("verification", "QC" if order else "Bench map",
                                self._qc_lines(order, named, live, done),
                                "warn" if order and order["qc"] and not order["qc"]["passed"]
                                else "ok" if (order and order["qc"]) or (not order and done) else "idle"),
            ],
            "summary": None,
        }

    def _dosing(self, order: dict | None) -> dict | None:
        """The ingredient on the balance: dosing now, or the last one reported."""
        if not order:
            return None
        for item in order["ingredients"]:
            steps = {s["id"]: s["status"] for s in item["steps"]}
            if steps.get("dose") == "active":
                return {**item, "active": True}
        weighed = [i for i in order["ingredients"] if i["mass"] is not None]
        return {**weighed[-1], "active": False} if weighed else None

    def _qc_lines(self, order, named, live, done) -> list[str]:
        if order:
            qc = order["qc"]
            if qc:
                mass = f"{qc['finalMass']:.3f} g" if qc["finalMass"] is not None else "not weighed"
                return ["PASS" if qc["passed"] else "CHECK", mass]
            return [f"{order['done']}/{order['total']} ingredients", "after the last one"]
        return [f"{len(named)}/{len(live)} identified", "written" if done else "after the scan"]

    def _scan_stages(self, done: bool, failed: bool) -> list[dict]:
        """The scan task's bar, which is the one step it is."""
        status = "failed" if failed else "completed" if done else "active"
        return [{"id": sid, "label": label, "status": status} for sid, label in SCAN_STAGES]

    def _idle_stages(self, done: bool) -> list[dict]:
        work = "Fetch" if self.workflow.executor == "fetch" else "Dose"
        stages = [("formula", "Formula", "queued"),
                  ("check", "Check", "queued"), (work.lower(), work, "queued")]
        if work == "Dose":
            stages.append(("qc", "QC", "queued"))
        stages.append(("done", "Done", "queued"))
        return [{"id": i, "label": label, "status": st} for i, label, st in stages]

    def _recipe(self, order: dict | None) -> dict:
        if order is None:
            return {"id": "BENCH", "name": "Bench scan", "targetMass": 0.0, "ingredients": []}
        formula = order["formula"]
        return {
            "id": formula["id"], "name": formula["name"], "targetMass": formula["batch"]["concentrate_g"],
            "ingredients": [S.ingredient(i["id"], i["compound"], i["grams"], "liquid", i["cas"], i["mass"],
                                         i["sampleId"], None,
                                         "failed" if i["problem"] else
                                         "completed" if all(s["status"] in DONE for s in i["steps"]) else
                                         "active" if any(s["status"] != "queued" for s in i["steps"]) else "queued")
                            for i in order["ingredients"]],
        }

    def _steps(self, tracks, focus, clock, done, order) -> list[dict]:
        live = [t for t in tracks if t.state not in ("lost", "tentative")]
        busy = order is not None
        if busy:
            # With an order on, the scan is one line and the order is the plan.
            named = sum(bool(t.sample) for t in live)
            scan = S.step("scan", f"Bench scan · {named}/{len(live)} named",
                          status="completed" if done else "active", completed_at=self._mapped_at)
            scan["group"] = "Bench"
            return [scan] + self.workflow.plan_steps()
        steps = [
            S.step("park", "Stretch the arm out along the rail", status=(
                "active" if self._phase == "init" else "completed")),
            S.step("survey", "Survey the bench with the fixed camera", status=(
                "queued" if self._phase == "init" else "active" if self._phase == "survey" else "completed")),
        ]
        for step in steps:
            step["group"] = "Initial scan"
        rows = []
        for t in live:
            active = focus is not None and t.id == focus.id and not done
            if active:
                self._started.setdefault(t.id, clock)
            if t.state != "proposed" and t.id not in self._done:
                self._done[t.id] = clock
            if t.sample:
                info = self.catalogue.samples.get(t.sample)
                label = f"{t.sample} · {info['compound']}" if info else t.sample
                status = "failed" if t.state in ("unreachable", "missed") else "completed"
            elif t.state == "empty":
                label, status = f"Track {t.id} · not a sample", "completed"
            elif t.state == "unreachable":
                label, status = f"Track {t.id} · out of reach", "failed"
            else:
                label, status = f"Read the ring of track {t.id}", "queued"
            if active:
                status = "active"
            x, y = t.xy
            step = S.step(f"track-{t.id}", label, status=status,
                          started_at=self._started.get(t.id),
                          completed_at=self._done.get(t.id) if status in ("completed", "failed") else None,
                          detail=[("at", f"{x:+.3f}, {y:+.3f} m"), ("", t.note)])
            after = self._mapped_at is not None and self._done.get(t.id, 0.0) > self._mapped_at
            step["group"] = "Watching the bench" if after else "Initial scan"
            rows.append((0 if status in ("completed", "failed") else 1 if status == "active" else 2,
                         self._done.get(t.id, float("inf")), x, step))
        steps += [step for *_, step in sorted(rows, key=lambda r: r[:3])]
        mapped = S.step("map", "Write the bench map", status="completed" if done else "queued",
                        completed_at=self._mapped_at)
        mapped["group"] = "Initial scan"
        steps.append(mapped)
        return steps
