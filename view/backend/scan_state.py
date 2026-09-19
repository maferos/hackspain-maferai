"""The side panels' LabState, read off the live scan (live_scan.py).

The scan owns the arm and the cameras; this only watches it. A few times a
second it turns vision_pick's world model (the tracks and what their rings
said), the arm's joints and gripper, and the controller's caption into the
LabState the panels read on :8765 (see dashboard/bridge/README.md), and forwards
the scan's log lines as events. Nothing is scripted: a panel shows what the
scan is doing, or says it is waiting.

It also runs the chat's "pick" requests (``Fetch``): each flask of a formula,
in turn, through the controller's own pick command, so the arm finds it by its
ring, lifts it on the gripper's force feedback and puts it back.
"""
from __future__ import annotations

import re
import sys
import threading
import time

from catalogue import REPO, Catalogue
from live_scan import vp

sys.path.insert(0, str(REPO / "dashboard" / "bridge"))
from labbridge import state as S  # noqa: E402
from labbridge.mujoco_adapter import workcell  # noqa: E402

rk = vp.rk
PUBLISH_S = 0.25
BALANCE = "balance_2"
PICK_TIMEOUT_S = 240.0

# The controller's captions, as states for the Robot panel: the first match wins.
CAPTIONS = (
    ("idle", "IDLE"), ("settling", "INIT"), ("raising the hand", "INIT"),
    ("parking", "PARK"), ("survey", "SURVEY"), ("travelling", "TRAVERSE"),
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


class Fetch:
    """The chat's formula, fetched flask by flask through the controller.

    Args:
        formula: From catalogue.resolve.
        world: The scan's world model, whose ``commands`` the controller reads.
    """

    def __init__(self, formula: dict, world) -> None:
        self.formula, self.world = formula, world
        self.items = [dict(i, status="queued" if not i["problem"] else "skipped", note=i["problem"] or "")
                      for i in formula["ingredients"]]
        self.status = "running"
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._run, name="formula-fetch", daemon=True)

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _run(self) -> None:
        for item in self.items:
            if item["status"] != "queued":
                continue
            if self._stop.is_set():
                break
            item["status"] = "active"
            item["note"] = "waiting for the scan to finish"
            while self.world.scan is None and not self._stop.wait(0.5):
                pass
            track = next((t for t in self.world.snapshot()
                          if t.sample == item["sampleId"] and t.state != "lost"), None)
            if track is None:
                item["status"], item["note"] = "failed", "the scan no longer sees it"
                continue
            picks = track.picks
            item["note"] = f"track {track.id}: asking the arm to pick it"
            with self.world.lock:
                self.world.commands.append({"cmd": "pick", "track": track.id})
            began = time.monotonic()
            while not self._stop.wait(0.5):
                if track.picks > picks:
                    item["status"] = "completed"
                    item["note"] = "picked and put back" if track.state == "picked" else track.note
                    if track.state == "missed":
                        item["status"] = "failed"
                    break
                if track.state in ("unreachable", "lost", "missed"):
                    item["status"], item["note"] = "failed", track.note
                    break
                if time.monotonic() - began > PICK_TIMEOUT_S:
                    item["status"], item["note"] = "failed", "the arm did not get to it"
                    break
        if self._stop.is_set():
            self.status = "aborted"
            with self.world.lock:
                self.world.commands[:] = [c for c in self.world.commands if c.get("cmd") != "pick"]
            for item in self.items:
                if item["status"] in ("queued", "active"):
                    item["status"], item["note"] = "failed", "stopped"
        else:
            self.status = "completed"


class ScanState:
    """Publishes the live scan as LabState, from its own thread.

    Args:
        scene: The viewer's SceneRenderer (``scan``, ``model``, ``data``,
            ``_data_lock``, ``pattern``).
        server: The LabState publisher.
        catalogue: For the compound behind each sample id.
    """

    def __init__(self, scene, server, catalogue: Catalogue) -> None:
        self.scene, self.server, self.catalogue = scene, server, catalogue
        self.fetch: Fetch | None = None
        self._scan = None
        self._sent: list[str] = []
        self._done: dict[int, float] = {}
        self._started: dict[int, float] = {}
        self._phase = "init"
        self._mapped_at: float | None = None

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
            self._scan, self._sent, self._done, self._started, self._phase = scan, [], {}, {}, "init"
            self._mapped_at = None
            if self.fetch:
                self.fetch.stop()
                self.fetch = None
            with self.scene._data_lock:
                doc = workcell(self.scene.model, self.scene.data, BALANCE, self._rail())
            self.server.snapshot(S.empty_state(self._run_id(), doc))
        world = scan.world
        tracks = world.snapshot()
        with self.scene._data_lock:
            clock = float(self.scene.data.time)
            carriage = self.scene.data.body("rail_carriage").xpos.copy()
            tip = self.scene.data.site(rk.TCP_SITE).xpos.copy()
            holding = rk.read_grip(self.scene.model, self.scene.data).holding
        self._forward_events(world)
        self.server.patch(self._patch(scan, world, tracks, clock, carriage, tip, holding),
                          timestamp=time.time())

    def _run_id(self) -> str:
        pattern = self.scene.pattern or {}
        return f"SCAN-{pattern['pattern'].upper()}" if pattern.get("pattern") else "SCAN"

    def _rail(self) -> dict:
        model = self.scene.model
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
        status = "failed" if scan.error else "running"
        if done and not (self.fetch and self.fetch.status == "running"):
            status = "completed"
        info = self.catalogue.samples.get(focus.sample) if focus is not None and focus.sample else None
        target = (focus.sample or f"track {focus.id}") if focus is not None else None
        reading = fsm in ("LOOK", "READ_RING")
        ring = (focus.confirmation.marker_id if focus is not None and focus.confirmation else None)
        steps = self._steps(tracks, focus, fsm, clock, done)
        fetch = self.fetch

        patch = {
            "run": {"id": self._run_id(), "status": status, "elapsedSeconds": clock,
                    "progress": len(named) / max(len(named) + len(waiting), 1),
                    "phase": fsm.lower(), "simulated": True, "scripted": False},
            "scan": {"named": len(named), "tracked": len(live), "waiting": len(waiting),
                     "empty": len(empty), "unreachable": len(unreachable),
                     "wristOnly": sum(bool(t.wrist_only) for t in named), "done": done,
                     "cycleSeconds": round(world.cycle_seconds, 2), "error": scan.error,
                     "caption": caption},
            "recipe": self._recipe(),
            "execution": {"currentStepId": next((s["id"] for s in steps if s["status"] == "active"), None),
                          "steps": steps},
            "balance": {"id": BALANCE, "netMass": 0.0, "totalMass": 0.0, "targetMass": 0.0,
                        "batchTargetMass": 0.0, "flowRate": 0.0, "mode": "stopped", "stable": True,
                        "ingredientId": None},
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
                S.pipeline_node("planner", "Scan controller",
                                ["BENCH MAPPED" if done else f"{len(waiting)} to look at", fsm],
                                "ok" if done else "active" if fsm in ("SURVEY", "PARK") else "ok"),
                S.pipeline_node("motion", "Rail + UR10e",
                                ["MOVING" if fsm in MOVING else "HOLD", f"rail {carriage[0]:+.2f} m"],
                                "active" if fsm in MOVING else "ok"),
                S.pipeline_node("dosing", "—", ["no dosing tool", "gripper on the arm"], "idle"),
                S.pipeline_node("verification", "Bench map",
                                [f"{len(named)}/{len(live)} identified",
                                 "written" if done else "after the scan"],
                                "ok" if done else "idle"),
            ],
            "summary": None,
        }
        return patch

    def _recipe(self) -> dict:
        fetch = self.fetch
        if fetch is None:
            return {"id": "BENCH", "name": "Bench scan", "targetMass": 0.0, "ingredients": []}
        formula = fetch.formula
        return {
            "id": formula["id"], "name": formula["name"], "targetMass": formula["targetMass"],
            "mode": "fetch",
            "ingredients": [
                dict(S.ingredient(i["id"], i["compound"], i["grams"], "liquid", i["cas"], None,
                                  i["sampleId"], None,
                                  i["status"] if i["status"] != "skipped" else "failed"),
                     note=i["note"])
                for i in fetch.items],
        }

    def _steps(self, tracks, focus, fsm, clock, done) -> list[dict]:
        steps = [
            S.step("park", "Park at the end of the rail", status=(
                "active" if self._phase == "init" else "completed")),
            S.step("survey", "Survey the bench with the fixed camera", status=(
                "queued" if self._phase == "init" else "active" if self._phase == "survey" else "completed")),
        ]
        for step in steps:
            step["group"] = "Initial scan"
        rows = []
        for t in tracks:
            if t.state in ("lost", "tentative"):
                continue
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
        if self.fetch is not None:
            for item in self.fetch.items:
                status = {"skipped": "failed"}.get(item["status"], item["status"])
                step = S.step(f"fetch-{item['id']}", f"Pick {item['sampleId'] or '—'} · {item['compound']}",
                              item["id"], status, detail=[("", item["note"])] if item["note"] else ())
                steps.append(step)
        return steps
