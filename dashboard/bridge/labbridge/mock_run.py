"""Drive the console from the real MuJoCo scene without a robot or planner.

Loads ``minihannover_scene.xml``, publishes the workcell and the seven free
containers as the simulation would, streams the ``general`` and ``wrist``
cameras, and replays a scripted formulation: the containers are moved
kinematically to the formulation balance, tilted while a mass ramp is
published, and put back. The console should show real renders in the
viewport and every panel moving in step.

Run from ``dashboard/bridge`` with the repo's virtual environment::

    python -m labbridge.mock_run --fps 1

Then open the robot viewer (``view/frontend``, ``npm run dev``) at
http://localhost:5173; its panels read the state on :8765.

This file is also the reference for the real integration: the simulation
loop replaces ``ScriptedRun`` with its planner and keeps everything else.
"""

from __future__ import annotations

import argparse
import logging
import math
import threading
import time
from pathlib import Path

import mujoco
import numpy as np

from labbridge import state as S
from labbridge.mujoco_adapter import CameraStreamer, Vessel, ground_truth, quat_tilt_x, set_free_body_pose, vessels, workcell
from labbridge.server import FrameServer, StateServer

logger = logging.getLogger("labbridge.mock_run")

REPO = Path(__file__).resolve().parents[3]
SCENE = REPO / "simulation" / "models" / "minihannover_scene.xml"

BASE_Y, BASE_Z = -1.05, 0.90
RAIL = {"x0": -2.8, "x1": 2.8, "y": BASE_Y}
RAIL_SPEED = 0.6
CARRY = (0.35, 0.32)
POUR_Z = 1.15
ACTIVE_BALANCE = "balance_2"

# The scripted perturbation: while the arm approaches the Eugenol flask, the
# flask is moved (as a judge would with the mouse). The approach is cancelled,
# the pose invalidated, the target re-detected and the approach retried.
DISPLACED_SAMPLE = "SMP-0021"
DISPLACED_TO = (0.58, -0.55)
REACQUIRE_AFTER_S = 2.1

# Recipe FRG-031: four liquids of the scene's catalogue (registry v6, liquids
# only), all on the aisle side.
RECIPE = {
    "id": "FRG-031",
    "name": "Floral Accord 01",
    "targetMass": 10.0,
    "ingredients": [
        # id, compound, cas, phase, target, sample id, barcode, ml, dose error
        ("ing-linalool", "Linalool", "78-70-6", "liquid", 4.2, "SMP-0009", "2007063201700", 50, 0.004),
        ("ing-isoamyl-acetate", "Isoamyl acetate", "123-92-2", "liquid", 3.0, "SMP-0120", "2005058322201", 100, -0.003),
        ("ing-eugenol", "Eugenol", "97-53-0", "liquid", 1.0, "SMP-0021", "2001316174674", 10, 0.006),
        ("ing-benzyl-benzoate", "Benzyl benzoate", "120-51-4", "liquid", 1.8, "SMP-0125", "2008263636767", 100, -0.001),
    ],
}

PHASES = (
    # fsm state, camera, seconds (None = computed), macro phase
    ("LOCATE", "overview", 1.6, "perceive"),
    ("TRAVERSE", "robot", None, "move"),
    ("APPROACH", "wrist", 3.2, "move"),
    ("READ_BARCODE", "wrist", 1.8, "identify"),
    ("VERIFY_ID", "wrist", 0.7, "identify"),
    ("PICK", "wrist", 2.4, "move"),
    ("MOVE_TO_POUR", "robot", None, "move"),
    ("DOSING", "robot", None, "dose"),
    ("VERIFY_MASS", "robot", 1.6, "verify"),
    ("RETURN_BOTTLE", "wrist", None, "move"),
)

STEP_LABELS = {
    "LOCATE": "Locate candidate · {compound}",
    "TRAVERSE": "Traverse rail → x {x:.2f} m",
    "APPROACH": "Approach vessel #{index}",
    "READ_BARCODE": "Read barcode · wrist camera",
    "VERIFY_ID": "Verify identity · {compound}",
    "PICK": "Pick {sample}",
    "MOVE_TO_POUR": "Move to " + ACTIVE_BALANCE + " · tare",
    "DOSING": "Dose {compound}",
    "VERIFY_MASS": "Verify mass",
    "RETURN_BOTTLE": "Return {sample}",
}


def smoothstep(u: float) -> float:
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


class ScriptedRun:
    """A fixed sequence of phases with the container animated in the scene.

    Everything the console needs is derived from ``time``, so the run can be
    replayed. The real system replaces this class: its planner decides the
    phases, its controller moves the arm and the physics moves the containers.
    """

    def __init__(self, model: mujoco.MjModel, data: mujoco.MjData, vessel_list: list[Vessel]) -> None:
        self.model = model
        self.data = data
        self.by_id = {v.sample_id: v for v in vessel_list}
        self.vessel_list = vessel_list
        self.balance = next(b for b in workcell(model, data, ACTIVE_BALANCE)["balances"] if b["active"])
        self.pour = np.array([self.balance["position"]["x"], self.balance["position"]["y"], POUR_Z])
        self.home = {v.index: v.position(data).copy() for v in vessel_list}
        displaced = self.by_id[DISPLACED_SAMPLE]
        self.displaced_index = displaced.index
        self.displaced_to = np.array([DISPLACED_TO[0], DISPLACED_TO[1], self.home[displaced.index][2]])
        self.segments = self._compile()
        self.duration = self.segments[-1]["end"]
        self.steps = self._steps()
        recover = next(s for s in self.segments if s["kind"] == "RECOVER")
        self.displace_t = recover["start"]
        self.reacquire_t = recover["start"] + REACQUIRE_AFTER_S

    def rest_position(self, index: int, t: float) -> np.ndarray:
        """Where a container stands on the bench at time ``t`` (the truth)."""
        if index == self.displaced_index and t >= self.displace_t:
            return self.displaced_to
        return self.home[index]

    def reset_scene(self) -> None:
        """Put every container back where the scene file has it."""
        for v in self.vessel_list:
            set_free_body_pose(self.model, self.data, v, self.home[v.index], np.array([1.0, 0, 0, 0]))

    # -- compile --------------------------------------------------------------

    def _compile(self) -> list[dict]:
        segs: list[dict] = []
        t = 0.0
        base = self.pour[0]
        target_pos = None

        def add(kind, dur, **kw):
            nonlocal t
            kw.setdefault("target", target_pos)
            kw.setdefault("attempt", 1)
            # Every segment knows where the rail carriage is, so the run can start anywhere.
            kw.setdefault("base_from", base)
            kw.setdefault("base_to", base)
            seg = {"kind": kind, "start": t, "end": t + dur, **kw}
            segs.append(seg)
            t += dur
            return seg

        add("LOAD_RECIPE", 1.2, camera="overview", macro="plan", ingredient=None, step="parse")
        add("SCAN_SCENE", 2.6, camera="overview", macro="perceive", ingredient=None, step="detect")
        for i, row in enumerate(RECIPE["ingredients"]):
            ing_id, compound, cas, phase, target, sample, barcode, ml, err = row
            v = self.by_id[sample]
            home = self.home[v.index]
            target_pos = home
            for fsm, camera, dur, macro in PHASES:
                if fsm == "APPROACH" and sample == DISPLACED_SAMPLE:
                    # Half an approach, the flask is moved, recover, approach again.
                    step = f"{fsm}-{ing_id}"
                    add(fsm, 1.4, camera=camera, macro=macro, ingredient=i, step=step)
                    home = target_pos = self.displaced_to
                    add("RECOVER", 2.6, camera=camera, macro="plan", ingredient=i, step=step)
                    add(fsm, 3.0, camera=camera, macro=macro, ingredient=i, step=step, attempt=2)
                    continue
                if fsm == "TRAVERSE":
                    dist = abs(home[0] - base)
                    if dist < 0.05:
                        continue
                    dur = dist / RAIL_SPEED + 0.8
                    seg = add(fsm, dur, camera=camera, macro=macro, ingredient=i, step=f"{fsm}-{ing_id}", base_from=base, base_to=home[0])
                    base = home[0]
                    continue
                if fsm == "MOVE_TO_POUR":
                    dur = 2.4 + abs(self.pour[0] - base) / RAIL_SPEED
                    add(fsm, dur, camera=camera, macro=macro, ingredient=i, step=f"{fsm}-{ing_id}", base_from=base, base_to=self.pour[0])
                    base = self.pour[0]
                    continue
                if fsm == "DOSING":
                    fast, slow = (0.42, 0.084) if phase == "liquid" else (0.34, 0.07)
                    m_fast = max(target * 0.5, target - 0.55)
                    m_slow = target - 0.06
                    t_fast, t_slow = m_fast / fast, (m_slow - m_fast) / slow
                    dur = t_fast + t_slow + 3.3
                    add(fsm, dur, camera=camera, macro=macro, ingredient=i, step=f"{fsm}-{ing_id}", dose=dict(target=target, final=target + err, t_fast=t_fast, t_slow=t_slow, m_fast=m_fast, m_slow=m_slow, fast=fast, slow=slow))
                    continue
                if fsm == "RETURN_BOTTLE":
                    dur = 3.4 + abs(home[0] - base) / RAIL_SPEED
                    add(fsm, dur, camera=camera, macro=macro, ingredient=i, step=f"{fsm}-{ing_id}", base_from=base, base_to=home[0])
                    base = home[0]
                    continue
                add(fsm, dur, camera=camera, macro=macro, ingredient=i, step=f"{fsm}-{ing_id}")
        target_pos = None
        add("VALIDATE", 2.2 + abs(self.pour[0] - base) / RAIL_SPEED, camera="overview", macro="verify", ingredient=None, step="validate", base_from=base, base_to=self.pour[0])
        base = self.pour[0]
        add("COMPLETE", 0.8, camera="overview", macro="verify", ingredient=None, step="complete")
        return segs

    def _steps(self) -> list[dict]:
        steps = [S.step("parse", "Parse formulation"), S.step("detect", "Detect candidate containers")]
        seen = set()
        for seg in self.segments:
            if seg["ingredient"] is None or seg["step"] in seen:
                continue
            seen.add(seg["step"])
            row = RECIPE["ingredients"][seg["ingredient"]]
            v = self.by_id[row[5]]
            label = STEP_LABELS[seg["kind"]].format(compound=row[1], index=v.index, sample=row[5], x=self.home[v.index][0])
            steps.append(S.step(seg["step"], label, row[0]))
        steps += [S.step("validate", "Validate final mass"), S.step("complete", "Complete formulation")]
        return steps

    # -- state at time t -------------------------------------------------------

    def segment_at(self, t: float) -> dict:
        for seg in self.segments:
            if t < seg["end"]:
                return seg
        return self.segments[-1]

    def mass_at(self, seg: dict, local: float) -> tuple[float, str, float]:
        d = seg["dose"]
        if local < d["t_fast"]:
            return d["fast"] * local, "fast", d["fast"]
        if local < d["t_fast"] + d["t_slow"]:
            return d["m_fast"] + d["slow"] * (local - d["t_fast"]), "slow", d["slow"]
        p = local - d["t_fast"] - d["t_slow"]
        pulses = min(4, int(p / 0.7) + 1)
        return min(d["final"], d["m_slow"] + (d["final"] - d["m_slow"]) * pulses / 4), ("pulse" if p < 2.8 else "stopped"), 0.02

    def apply(self, t: float, server: StateServer, last: dict) -> dict:
        """Move the scene to time ``t`` and publish the corresponding patch."""
        seg = self.segment_at(t)
        u = (t - seg["start"]) / max(1e-6, seg["end"] - seg["start"])
        local = t - seg["start"]
        kind = seg["kind"]
        i = seg["ingredient"]
        row = RECIPE["ingredients"][i] if i is not None else None
        v = self.by_id[row[5]] if row else None
        home = seg["target"] if v is not None else None
        base_x = lerp(seg["base_from"], seg["base_to"], smoothstep(u)) if "base_from" in seg else last.get("base_x", self.pour[0])
        completed = t >= self.duration
        recovering = kind == "RECOVER"
        pose_invalid = recovering and local < REACQUIRE_AFTER_S
        recoveries = sum(1 for s in self.segments if s["kind"] == "RECOVER" and s["start"] <= t)

        # --- container animation (kinematic; physics would do this for real)
        tilt = 0.0
        ee = np.array([base_x, BASE_Y + CARRY[0], BASE_Z + CARRY[1]])
        gripper = "open"
        if v is not None:
            if kind == "APPROACH" and seg["attempt"] == 1 and v.index == self.displaced_index:
                # The approach that gets interrupted: half way down, towards the old pose.
                orig = self.home[v.index]
                ee = np.array([orig[0], orig[1], lerp(1.22, 1.16, smoothstep(u))])
            elif kind == "APPROACH":
                ee = np.array([home[0], home[1], lerp(1.22, 1.10, smoothstep(u))])
            elif recovering:
                orig = self.home[v.index]
                f = smoothstep((local - REACQUIRE_AFTER_S) / 0.5)
                ee = np.array([lerp(orig[0], home[0], f), lerp(orig[1], home[1], f), 1.16])
            elif kind in ("READ_BARCODE", "VERIFY_ID"):
                ee = np.array([home[0], home[1], 1.06])
            elif kind == "PICK":
                ee = np.array([home[0], home[1], 0.965 if u < 0.6 else lerp(0.965, 1.12, smoothstep((u - 0.6) / 0.4))])
                gripper = "open" if u < 0.35 else "closing" if u < 0.6 else "attached"
            elif kind == "MOVE_TO_POUR":
                gripper = "attached"
                if u < 0.15:
                    ee = np.array([home[0], lerp(home[1], BASE_Y + CARRY[0], smoothstep(u / 0.15)), lerp(1.12, BASE_Z + CARRY[1], smoothstep(u / 0.15))])
                elif u < 0.85:
                    ee = np.array([base_x, BASE_Y + CARRY[0], BASE_Z + CARRY[1]])
                else:
                    f = smoothstep((u - 0.85) / 0.15)
                    ee = np.array([lerp(base_x, self.pour[0], f), lerp(BASE_Y + CARRY[0], self.pour[1], f), lerp(BASE_Z + CARRY[1], self.pour[2], f)])
            elif kind in ("DOSING", "VERIFY_MASS"):
                gripper = "attached"
                ee = self.pour.copy()
                if kind == "DOSING":
                    _, mode, _ = self.mass_at(seg, local)
                    tilt = {"fast": 52.0, "slow": 37.2, "pulse": 30.0, "stopped": 0.0}[mode]
                else:
                    tilt = lerp(30.0, 0.0, smoothstep(local / 0.5))
            elif kind == "RETURN_BOTTLE":
                gripper = "attached" if u < 0.82 else "releasing" if u < 0.9 else "open"
                if u < 0.12:
                    f = smoothstep(u / 0.12)
                    ee = np.array([self.pour[0], lerp(self.pour[1], BASE_Y + CARRY[0], f), lerp(self.pour[2], BASE_Z + CARRY[1], f)])
                elif u < 0.6:
                    ee = np.array([base_x, BASE_Y + CARRY[0], BASE_Z + CARRY[1]])
                elif u < 0.72:
                    f = smoothstep((u - 0.6) / 0.12)
                    ee = np.array([home[0], lerp(BASE_Y + CARRY[0], home[1], f), lerp(BASE_Z + CARRY[1], 1.12, f)])
                elif u < 0.82:
                    ee = np.array([home[0], home[1], lerp(1.12, 0.965, smoothstep((u - 0.72) / 0.1))])
                elif u < 0.9:
                    ee = np.array([home[0], home[1], 0.965])
                else:
                    ee = np.array([home[0], home[1], lerp(0.965, 1.12, smoothstep((u - 0.9) / 0.1))])
            if gripper in ("attached", "releasing"):
                set_free_body_pose(self.model, self.data, v, ee - np.array([0, 0, 0.07]), quat_tilt_x(tilt))
            elif kind == "RETURN_BOTTLE" and u >= 0.9 or kind not in ("PICK", "MOVE_TO_POUR", "DOSING", "VERIFY_MASS", "RETURN_BOTTLE"):
                set_free_body_pose(self.model, self.data, v, home, np.array([1.0, 0, 0, 0]))

        # --- balance
        net, mode, flow = last.get("net", 0.0), "stopped", 0.0
        stable = True
        if kind == "DOSING":
            net, mode, flow = self.mass_at(seg, local)
            stable = mode in ("stopped",)
            net += 0.002 * math.sin(t * 9.1) if mode != "stopped" else 0.0
        elif kind == "MOVE_TO_POUR" and u > 0.98:
            net = 0.0
        total = sum(r[4] + r[8] for k, r in enumerate(RECIPE["ingredients"]) if any(s["kind"] == "DOSING" and s["ingredient"] == k and s["end"] <= t for s in self.segments))
        if kind == "DOSING":
            total += net

        # --- knowledge
        verified = {s["ingredient"] for s in self.segments if s["kind"] == "VERIFY_ID" and s["end"] <= t}
        handling = row is not None
        is_verified = i in verified
        target_name = (row[5] if is_verified else f"vessel #{v.index}") if handling else None
        barcode_known = handling and (kind not in ("LOCATE", "TRAVERSE", "APPROACH", "RECOVER") and not (kind == "READ_BARCODE" and local < 1.1))
        barcode_status = "idle" if not handling else "reading" if kind == "READ_BARCODE" or (kind == "VERIFY_ID" and local < 0.4) else ("verified" if is_verified or kind == "VERIFY_ID" else "idle")
        detections = self.vessel_list if t > 3.0 else self.vessel_list[: int(len(self.vessel_list) * max(0.0, (t - 1.2)) / 1.8)]
        offset = np.array([0.006, -0.004, 0])

        def estimate(index: int) -> tuple[np.ndarray, bool]:
            """Perceived position of a container and whether it is out of date."""
            if index == self.displaced_index and self.displace_t <= t < self.reacquire_t:
                return self.home[index] + offset, True
            return self.rest_position(index, t) + offset, False

        perceived = []
        for pv in detections:
            pos, stale = estimate(pv.index)
            perceived.append(
                {
                    "index": pv.index,
                    "id": next((r[5] for k, r in enumerate(RECIPE["ingredients"]) if r[5] == pv.sample_id and k in verified), None),
                    "cls": pv.cls,
                    "confidence": 0.86 + 0.01 * pv.index,
                    "position": S.vec3(*pos),
                    "stale": stale,
                }
            )

        # --- steps and ingredients
        steps = []
        for st in self.steps:
            own = [s for s in self.segments if s["step"] == st["id"]]
            done = completed or (own and own[-1]["end"] <= t)
            containing = next((s for s in own if s["start"] <= t < s["end"]), None)
            status = "completed" if done else ("retrying" if containing["kind"] == "RECOVER" else "active") if containing else "queued"
            attempt = containing["attempt"] if containing else (own[-1]["attempt"] if own else 1)
            detail = []
            if status == "retrying":
                detail = [("recovery", "target displaced → replanning" if pose_invalid else "target reacquired"), ("attempt", "2 of 3")]
            elif status == "active" and kind == "DOSING":
                detail = [("target", f"{row[4]:.3f} g"), ("current", f"{net:.3f} g"), ("mode", mode.upper())]
            elif status == "active" and kind in ("TRAVERSE", "MOVE_TO_POUR"):
                detail = [("rail x", f"{base_x:.2f} m")]
            elif status == "active" and attempt > 1:
                detail = [("attempt", f"{attempt} of 3")]
            steps.append(S.step(st["id"], st["label"], st["ingredientId"], status, attempt=attempt, started_at=own[0]["start"] if own and own[0]["start"] <= t else None, completed_at=own[-1]["end"] if done and own else None, detail=detail))
        ingredients = []
        for k, r in enumerate(RECIPE["ingredients"]):
            own = [s for s in self.segments if s["ingredient"] == k]
            done = completed or own[-1]["end"] <= t
            active = not done and any(s["start"] <= t < s["end"] for s in own)
            dose = next(s for s in own if s["kind"] == "DOSING")
            dispensed = dose["dose"]["final"] if dose["end"] <= t else (net if dose["start"] <= t else None)
            ingredients.append(S.ingredient(r[0], r[1], r[4], r[3], r[2], dispensed, r[5] if k in verified else None, r[7] if k in verified else None, "completed" if done else "active" if active else "queued"))

        passed = sum(1 for x in ingredients if x["status"] == "completed")
        # The chart history grows through mass_sample messages; a patch must not
        # carry a history array or it would replace the samples on the console.
        balance = S.balance_state(ACTIVE_BALANCE, net, total, row[4] if row else 0.0, RECIPE["targetMass"], flow, mode, stable, row[0] if row else None)
        del balance["history"], balance["historyWindow"]
        patch = {
            "run": {"status": "completed" if completed else "running", "elapsedSeconds": min(t, self.duration), "progress": min(1.0, t / self.duration), "phase": seg["macro"]},
            "recipe": {"ingredients": ingredients},
            "execution": {"currentStepId": seg["step"], "steps": steps},
            "balance": balance,
            "robot": S.robot_state(
                kind,
                S.vec3(base_x, BASE_Y, BASE_Z),
                S.vec3(*ee),
                end_effector="POUR" if kind in ("DOSING", "VERIFY_MASS") else "GRIPPER",
                target_object=target_name,
                compound=row[1] if row else None,
                gripper=gripper,
                current_action=("Target displaced · pose invalidated, replanning" if pose_invalid else "Target reacquired · retry approach")
                if recovering
                else f"{kind.replace('_', ' ').title()}" + (f" · tilt {tilt:.1f}°" if tilt else ""),
                tilt_deg=tilt,
                ik_error_mm=0.3,
                distance_to_target=float(np.linalg.norm(ee - home)) if v is not None and kind in ("APPROACH", "READ_BARCODE", "VERIFY_ID", "PICK") else None,
                recoveries=recoveries,
                replans=recoveries,
            ),
            "perception": S.perception_state(
                seg["camera"],
                perceived,
                v.index if handling else None,
                target_name,
                v.cls if handling else None,
                (0.86 + 0.01 * v.index) if handling else None,
                row[6] if barcode_known else None,
                barcode_status,
                row[1] if handling and is_verified else None,
                row[7] if handling and is_verified else None,
                None if not handling or pose_invalid else S.vec3(*estimate(v.index)[0]),
                None if not handling or pose_invalid else 11,
                None,
                {
                    "detector": "active" if kind in ("SCAN_SCENE", "LOCATE") or (recovering and not pose_invalid) else "ok",
                    "localizer": "warn" if pose_invalid else "active" if kind == "LOCATE" else "ok",
                    "barcode": "active" if kind == "READ_BARCODE" else ("ok" if barcode_status == "verified" else "idle"),
                    "wristCam": "active" if seg["camera"] == "wrist" else "idle",
                },
            ),
            "pipeline": [
                S.pipeline_node("camera", "GoPro RGB" if seg["camera"] != "wrist" else "Wrist RGB", ["1920×1080 · 30 fps", f"scene cam {seg['camera']}"], "active" if kind in ("SCAN_SCENE", "APPROACH", "READ_BARCODE", "RECOVER") else "ok"),
                S.pipeline_node("detection", "YOLO11s", ["14 ms · 640 px", f"{len(perceived)} detections"], "active" if kind in ("SCAN_SCENE", "LOCATE") or (recovering and not pose_invalid) else "ok"),
                S.pipeline_node("localization", "Bench-plane ray", ["pose invalidated" if pose_invalid else "±11 mm", f"{len(perceived)} candidates"], "warn" if pose_invalid else "active" if kind == "LOCATE" else "ok"),
                S.pipeline_node("barcode", "EAN-13", [row[6] if barcode_known else "—", barcode_status.upper()], "active" if kind == "READ_BARCODE" else ("ok" if barcode_status == "verified" else "idle")),
                S.pipeline_node("planner", "FSM", [f"STATE {kind}", f"replans {recoveries}"], "active" if kind in ("LOAD_RECIPE", "LOCATE", "RECOVER") else "ok"),
                S.pipeline_node("motion", "IK · mink", ["TRACKING" if kind in ("TRAVERSE", "APPROACH", "PICK", "MOVE_TO_POUR", "RETURN_BOTTLE") else "HOLD", f"rail {base_x:.2f}"], "active" if kind in ("TRAVERSE", "APPROACH", "PICK", "MOVE_TO_POUR", "RETURN_BOTTLE") else "ok"),
                S.pipeline_node("dosing", "Closed loop", [mode.upper(), f"{flow:.3f} g/s"], "active" if kind == "DOSING" else "ok"),
                S.pipeline_node("verification", "Mass check", [f"{passed}/{len(ingredients)} PASS", "tol ±0.010 g"], "active" if kind in ("VERIFY_MASS", "VALIDATE", "COMPLETE") else "ok"),
            ],
            "evaluator": {"groundTruth": ground_truth(self.data, self.vessel_list)},
            "summary": {
                "targetMass": RECIPE["targetMass"],
                "finalMass": total,
                "absoluteError": abs(total - RECIPE["targetMass"]),
                "ingredientsDone": passed,
                "ingredientsTotal": len(ingredients),
                "recoveries": recoveries,
                "executionSeconds": self.duration,
                "passed": abs(total - RECIPE["targetMass"]) <= 0.05,
            }
            if completed
            else None,
        }
        server.patch(patch, timestamp=time.time())
        if kind == "DOSING" or last.get("kind") == "DOSING":
            server.mass_sample(t, net)
        if recovering and last.get("kind") != "RECOVER":
            moved = float(np.linalg.norm(self.displaced_to[:2] - self.home[v.index][:2])) * 100
            server.event(t, f"target displaced: {row[5]} moved {moved:.1f} cm, pose invalidated", "warn")
            server.event(t, "planner: APPROACH cancelled → RECOVER, re-detect from wrist camera", "warn")
        elif recovering and not pose_invalid and last.get("pose_invalid"):
            server.event(t, f"target reacquired at ({self.displaced_to[0]:.2f}, {self.displaced_to[1]:.2f}) ±12 mm", "ok")
        elif kind != last.get("kind"):
            server.event(t, f"planner: {last.get('kind', 'START')} → {kind}" + (f" ({row[1]})" if row else ""), "ok" if kind in ("VERIFY_ID", "VERIFY_MASS", "COMPLETE") else "info")
        return {"kind": kind, "net": net, "base_x": base_x, "pose_invalid": pose_invalid}

    def initial_state(self, workcell_doc: dict) -> dict:
        self.reset_scene()
        state = S.empty_state("RUN-042", workcell_doc)
        state["run"]["status"] = "running"
        state["run"]["scripted"] = True
        state["recipe"] = {"id": RECIPE["id"], "name": RECIPE["name"], "targetMass": RECIPE["targetMass"], "ingredients": [S.ingredient(r[0], r[1], r[4], r[3], r[2]) for r in RECIPE["ingredients"]]}
        state["execution"] = {"currentStepId": "parse", "steps": self.steps}
        state["balance"]["id"] = ACTIVE_BALANCE
        state["balance"]["batchTargetMass"] = RECIPE["targetMass"]
        state["evaluator"] = {"groundTruth": ground_truth(self.data, self.vessel_list)}
        return state


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--scene", type=Path, default=SCENE)
    parser.add_argument("--state-port", type=int, default=8765)
    parser.add_argument("--frame-port", type=int, default=8766)
    parser.add_argument("--fps", type=float, default=1.0, help="camera frames per second (0 disables rendering)")
    parser.add_argument("--cameras", default="general,wrist", help="scene cameras to stream, comma separated (add room_aisle for the robot slot)")
    parser.add_argument("--rate", type=float, default=10.0, help="state updates per second")
    parser.add_argument("--speed", type=float, default=1.0, help="playback speed of the scripted run")
    parser.add_argument("--start", type=float, default=0.0, help="seconds into the run to start at")
    parser.add_argument("--loop", action="store_true", help="restart the run when it completes")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")

    model = mujoco.MjModel.from_xml_path(str(args.scene))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    vessel_list = vessels(model)
    logger.info("scene %s: %d free containers: %s", args.scene.name, len(vessel_list), ", ".join(f"{v.body}={v.sample_id}" for v in vessel_list))

    state_server = StateServer(port=args.state_port)
    frame_server = FrameServer(port=args.frame_port)
    state_server.start()
    frame_server.start()

    run = ScriptedRun(model, data, vessel_list)
    state_server.snapshot(run.initial_state(workcell(model, data, ACTIVE_BALANCE, RAIL)))
    logger.info("scripted run: %.0f s, %d steps", run.duration, len(run.steps))

    lock = threading.Lock()
    stop = threading.Event()

    cameras = [c.strip() for c in args.cameras.split(",") if c.strip()]

    def render_loop() -> None:
        streamer = CameraStreamer(model)
        try:
            while not stop.is_set():
                t0 = time.time()
                for cam in cameras:
                    frame_server.push(cam, streamer.jpeg(data, cam, lock))
                time.sleep(max(0.0, 1.0 / args.fps - (time.time() - t0)))
        finally:
            streamer.close()

    if args.fps > 0:
        threading.Thread(target=render_loop, name="render", daemon=True).start()

    t = args.start
    last: dict = {}
    period = 1.0 / args.rate
    try:
        while True:
            tick = time.time()
            with lock:
                last = run.apply(t, state_server, last)
            if t >= run.duration + 5 and args.loop:
                t, last = 0.0, {}
                state_server.snapshot(run.initial_state(workcell(model, data, ACTIVE_BALANCE, RAIL)))
            elif t < run.duration + 5:
                t += period * args.speed
            time.sleep(max(0.0, period - (time.time() - tick)))
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        state_server.stop()
        frame_server.stop()


if __name__ == "__main__":
    main()
