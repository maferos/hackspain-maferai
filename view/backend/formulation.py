"""Carry out a formulation with the arm in the live rail scene.

The chat (formula_chat.py) hands over a formula. This plans the pipette's moves
with the rail scene's own IK (simulation/scripts/rail_kinematics.py), plays them
on the viewport's MjData, and moves the liquid with
simulation/scripts/pipetting.py, which refuses a draw unless the tip is down the
bore and under the surface, and a delivery unless it is inside the beaker.

The balance reads the beaker, and each ingredient is dosed against that reading:
full tips while the target is far, then one tip aimed a little short, and a last
small one to close the gap if the check is still outside tolerance. The pipette
delivers with a 1 % scatter, so the loop has something real to correct.

What is simulated and what is not: the arm is posed kinematically, like the
sweep the viewport plays when idle, so it cannot knock the glassware over; the
liquid is a level and a number; and the vessels' identities and poses are read
from the scene model, not from the cameras.

Everything the side panels show comes from here, published as LabState on
:8765 (see dashboard/bridge/README.md).
"""
from __future__ import annotations

import json
import math
import re
import sys
import threading
import time
from dataclasses import dataclass, field
from difflib import get_close_matches
from pathlib import Path

import mujoco
import numpy as np

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "simulation" / "scripts"))
sys.path.insert(0, str(REPO / "dashboard" / "bridge"))
import pipetting as pip  # noqa: E402
import rail_kinematics as rk  # noqa: E402
from labbridge import state as S  # noqa: E402
from labbridge.mujoco_adapter import workcell  # noqa: E402

LOOKUP = REPO / "computer-vision" / "barcodes" / "lookup_table.json"
FORMULAS = REPO / "harness" / "formulas"

DENSITY = pip.DENSITY           # g/ml
TIP_ML = pip.TIP_CAPACITY       # what one draw can hold
TOLERANCE_G = 0.010             # per ingredient, to pass
CLOSE_G = 0.004                 # the loop keeps topping up while further off than this
PIPETTE_CV = 0.01               # relative scatter of each draw
AIM_SHORT = 0.98                # the last big tip aims this far, the top-up closes it
EXACT_BELOW_ML = 0.30           # remainders this small are aimed at exactly
DEAD_COLUMN_M = 0.005           # liquid a flask must keep for the tip to stay under
MAX_BATCH_G = 9.9               # the balance's display reads up to 9.9999 g
MIN_DOSE_G = 0.02

TRANSIT_Z = 1.25                # tip height while the carriage travels
CLEARANCE = 0.06                # tip height over a flask's rim
BEAKER_CLEAR = 0.11             # tip height over the beaker's rim
RAIL_SPEED = 0.6                # m/s
JOINT_SPEED = 1.0               # rad/s, fastest joint
MIN_MOVE_S = 0.4
DISPENSE_S = 1.2
TICK_S = 1 / 30
PUBLISH_S = 0.1
SAMPLE_S = 0.2
TRIP_S = 9.0                    # seconds per draw and delivery, measured, for estimates
INGREDIENT_S = 4.0              # locating and checking each ingredient


def normalise(text: str) -> str:
    """Lower case, Greek letters spelt out, anything else a single space."""
    text = text.lower()
    for greek, word in (("α", "alpha"), ("β", "beta"), ("γ", "gamma")):
        text = text.replace(greek, word)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


# Spanish and short names for the catalogue's liquids, so the chat understands
# them without a language model. Keys are normalised.
ALIASES = {
    "limoneno": "Limonene", "linalol": "Linalool", "citronelol": "Citronellol",
    "anetol": "Anethole", "cinamaldehido": "Cinnamaldehyde", "cinnamic aldehyde": "Cinnamaldehyde",
    "benzaldehido": "Benzaldehyde", "carvona": "Carvone", "alfa pineno": "alpha-Pinene",
    "a pinene": "alpha-Pinene", "alpha pineno": "alpha-Pinene", "beta pineno": "beta-Pinene",
    "b pinene": "beta-Pinene", "alfa terpineol": "alpha-Terpineol", "terpineol": "alpha-Terpineol",
    "acetato de bencilo": "Benzyl acetate", "alcohol feniletilico": "Phenylethyl alcohol",
    "phenethyl alcohol": "Phenylethyl alcohol", "salicilato de metilo": "Methyl salicylate",
    "acetato de linalilo": "Linalyl acetate", "leaf alcohol": "cis-3-Hexen-1-ol",
    "hexenol": "cis-3-Hexen-1-ol", "dihidromircenol": "Dihydromyrcenol",
    "butirato de etilo": "Ethyl butyrate", "acetato de isoamilo": "Isoamyl acetate",
    "benzoato de bencilo": "Benzyl benzoate", "terpinoleno": "Terpinolene",
    "gamma terpineno": "gamma-Terpinene", "mirceno": "Myrcene", "citronelal": "Citronellal",
    "hidroxicitronelal": "Hydroxycitronellal", "acetato de geranilo": "Geranyl acetate",
    "acetato de citronelilo": "Citronellyl acetate", "hexanoato de alilo": "Allyl hexanoate",
    "acetato de isobornilo": "Isobornyl acetate", "beta ionona": "beta-Ionone",
    "ionone": "beta-Ionone", "beta damascona": "beta-Damascone", "damascone": "beta-Damascone",
    "acetoacetato de etilo": "Ethyl acetoacetate", "tetrahidrolinalol": "Tetrahydrolinalool",
    "hedion": "Hedione", "methyl dihydrojasmonate": "Hedione",
}


class Catalogue:
    """The sample catalogue (liquids only) and the five invented formulas."""

    def __init__(self, lookup: Path = LOOKUP, formulas: Path = FORMULAS) -> None:
        table = json.loads(lookup.read_text())
        self.samples: dict[str, dict] = {}
        self.compounds: dict[str, str] = {}     # CAS -> name
        for code, row in table["entries"].items():
            if row.get("phase") != "liquid":
                continue
            self.samples[row["sample_id"]] = {
                "compound": row["material"], "cas": row["cas"], "barcode": code,
                "containerMl": float(row["container_ml"]),
            }
            self.compounds.setdefault(row["cas"], row["material"])
        by_name = {normalise(name): cas for cas, name in self.compounds.items()}
        by_name.update({alias: next(c for c, n in self.compounds.items() if n == name)
                        for alias, name in ALIASES.items()})
        by_name.update({normalise(cas): cas for cas in self.compounds})
        # Longest first, so "alpha terpineol" wins over "terpineol".
        self.names = dict(sorted(by_name.items(), key=lambda kv: -len(kv[0])))
        self.formulas = {}
        for path in sorted(formulas.glob("FRG-*.json")):
            formula = json.loads(path.read_text())
            self.formulas[formula["id"]] = formula

    def find(self, text: str) -> str | None:
        """CAS of the compound a piece of text names, or None."""
        words = f" {normalise(text)} "
        for name, cas in self.names.items():
            if f" {name} " in words:
                return cas
        close = get_close_matches(words.strip(), list(self.names), n=1, cutoff=0.82)
        return self.names[close[0]] if close else None

    def find_all(self, text: str) -> list[tuple[int, str]]:
        """Every compound named in a text, as (position, CAS), in order."""
        words = f" {normalise(text)} "
        found, taken = [], [False] * len(words)
        for name, cas in self.names.items():
            for match in re.finditer(f"(?<= ){re.escape(name)}(?= )", words):
                span = range(match.start(), match.end())
                if any(taken[i] for i in span):
                    continue
                for i in span:
                    taken[i] = True
                found.append((match.start(), cas))
        return sorted(found)


def bench(model: mujoco.MjModel, data: mujoco.MjData, catalogue: Catalogue) -> list[dict]:
    """The open flasks on the bench, what each holds and how much can be drawn.

    Read off the scene: the liquid columns pipetting.py keeps, and the
    catalogue for what each sample id is.
    """
    out = []
    for name, vessel in pip.containers(model, data).items():
        info = catalogue.samples.get(name)
        if info is None:
            continue
        dead_ml = math.pi * vessel.inner_radius**2 * DEAD_COLUMN_M * 1e6
        pos = data.body(vessel.body).xpos
        out.append({
            "sampleId": name, "compound": info["compound"], "cas": info["cas"],
            "volumeMl": round(vessel.volume, 2),
            "usableG": round(max(0.0, vessel.volume - dead_ml) * DENSITY, 3),
            "x": round(float(pos[0]), 3), "y": round(float(pos[1]), 3),
        })
    return sorted(out, key=lambda v: (v["compound"], -v["usableG"]))


def next_draw(remaining_ml: float) -> tuple[str, float]:
    """The dosing loop's rule: what to draw with this much still to go.

    Full tips while the target is far; one aimed a little short once a tip
    would cover it, so the scatter cannot overshoot; then the rest exactly.
    """
    if remaining_ml > TIP_ML + EXACT_BELOW_ML / 2:
        return "FAST", TIP_ML
    if remaining_ml > TIP_ML:
        return "FAST", remaining_ml / 2
    if remaining_ml > EXACT_BELOW_ML:
        return "FINE", remaining_ml * AIM_SHORT
    return "TOP-UP", remaining_ml


def trips_for(grams: float) -> int:
    """How many draws the dosing loop takes for one ingredient, without scatter."""
    ml, n = grams / DENSITY, 0
    while ml * DENSITY > CLOSE_G and n < 50:
        n += 1
        ml -= next_draw(ml)[1]
    return n


def resolve(lines: list[dict], shelf: list[dict], catalogue: Catalogue,
            formula_id: str = "CHAT", name: str = "Chat formula") -> dict:
    """Match a requested formula to the flasks on this bench.

    Args:
        lines: ``[{"compound": name or CAS, "grams": float}]``.
        shelf: From :func:`bench`.
        catalogue: The sample catalogue.

    Returns:
        The formula as the chat shows it and the run takes it: every line with
        the flask it would be drawn from, or the reason it cannot be.
    """
    merged: dict[str, float] = {}
    unknown = []
    for line in lines:
        cas = catalogue.find(str(line.get("compound", "")))
        grams = float(line.get("grams") or 0)
        if cas is None:
            unknown.append(str(line.get("compound")))
            continue
        merged[cas] = merged.get(cas, 0.0) + grams
    ingredients = []
    for cas, grams in merged.items():
        compound = catalogue.compounds[cas]
        flasks = [v for v in shelf if v["cas"] == cas]
        best = max(flasks, key=lambda v: v["usableG"], default=None)
        problem = None
        if grams < MIN_DOSE_G:
            problem = f"below the {MIN_DOSE_G:g} g the pipette can dose"
        elif best is None:
            problem = "not on this bench"
        elif best["usableG"] < grams:
            problem = f"only {best['usableG']:.2f} g can be drawn from {best['sampleId']}"
        ingredients.append({
            "id": f"ing-{normalise(compound).replace(' ', '-')}", "compound": compound, "cas": cas,
            "grams": round(grams, 3), "sampleId": best["sampleId"] if best else None,
            "barcode": catalogue.samples[best["sampleId"]]["barcode"] if best else None,
            "problem": problem,
        })
    runnable = [i for i in ingredients if not i["problem"]]
    total = sum(i["grams"] for i in runnable)
    if total > MAX_BATCH_G:
        for ing in runnable:
            ing["problem"] = f"batch over {MAX_BATCH_G:g} g"
        runnable = []
    trips = sum(trips_for(i["grams"]) for i in runnable)
    return {
        "id": formula_id, "name": name, "ingredients": ingredients, "unknown": unknown,
        "targetMass": round(total, 3), "runnable": bool(runnable),
        "estimate": {"trips": trips, "seconds": round(trips * TRIP_S + INGREDIENT_S * len(runnable) + 8)},
    }


class Aborted(Exception):
    """The operator stopped the run."""


@dataclass
class Pose:
    """Carriage X and the six arm joints."""

    x: float
    q: np.ndarray

    def toward(self, other: "Pose") -> "Pose":
        """``other`` with each free joint unwrapped to the nearest turn of this one."""
        delta = (other.q - self.q + np.pi) % (2 * np.pi) - np.pi
        return Pose(other.x, self.q + delta)


@dataclass
class Dose:
    """One ingredient as the run doses it."""

    id: str
    compound: str
    cas: str
    target: float
    sample: str
    barcode: str
    container_ml: float
    status: str = "queued"
    dispensed: float | None = None
    trips: int = 0
    passed: bool | None = None


@dataclass
class Step:
    id: str
    label: str
    ingredient: str | None = None
    status: str = "queued"
    started: float | None = None
    completed: float | None = None
    detail: list = field(default_factory=list)

    def as_dict(self) -> dict:
        return S.step(self.id, self.label, self.ingredient, self.status, 1,
                      self.started, self.completed, self.detail)


class FormulationRun:
    """One formulation, executed in its own thread on the viewport's scene.

    Args:
        scene: The viewer's SceneRenderer: its model, data and ``_data_lock``,
            and ``resume_pose()`` for where to leave the arm.
        formula: From :func:`resolve`.
        server: The LabState publisher.
        catalogue: The sample catalogue.
        run_id: Shown in the task panel.
        speed: Time scale, for rehearsals and tests; 1 is real time.
        seed: For the pipette's scatter.
    """

    def __init__(self, scene, formula: dict, server, catalogue: Catalogue, run_id: str,
                 speed: float = 1.0, seed: int | None = None) -> None:
        self.scene = scene
        self.model, self.data, self.lock = scene.model, scene.data, scene._data_lock
        self.server = server
        self.catalogue = catalogue
        self.run_id = run_id
        self.speed = speed
        self.rng = np.random.default_rng(seed)
        self.formula = formula
        self.doses = [
            Dose(i["id"], i["compound"], i["cas"], i["grams"], i["sampleId"], i["barcode"],
                 catalogue.samples[i["sampleId"]]["containerMl"])
            for i in formula["ingredients"] if not i.get("problem")
        ]
        if not self.doses:
            raise ValueError("nothing in this formula can be dosed on this bench")
        self.target = sum(d.target for d in self.doses)
        self.balance_id = (pip.display_prefix(self.model) or "balance_2_").rstrip("_")
        self._stop = threading.Event()
        self.thread: threading.Thread | None = None
        self.status = "running"
        self.fsm = "PLAN"
        self.action = "Planning the pipette's moves"
        self.camera = "overview"
        self.current: Dose | None = None
        self.mode = "stopped"
        self.flow = 0.0
        self.stable = True
        self.net0 = 0.0
        self.moving = False
        self.recoveries = 0
        self.sampling = False
        self.parking = False
        self.summary = None
        self.located: tuple[float, float] | None = None
        self.steps = self._plan_steps()
        self.pipeline_hint = "planner"
        self._t0 = time.monotonic()
        self._next_publish = 0.0
        self._next_sample = 0.0
        known = {mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_SITE, i)
                 for i in range(self.model.nsite)}
        if "arm_pip_tip" not in known:
            raise ValueError("this scene has no pipette on the arm")
        rk.TCP_SITE = "arm_pip_tip"
        with self.lock:
            self.vessels = pip.containers(self.model, self.data)
            self.pose = Pose(float(self.data.body("rail_carriage").xpos[0]),
                             self.data.qpos[rk.arm_qpos(self.model)].copy())
            self.tip = self.data.site(rk.TCP_SITE).xpos.copy()
        self.beaker = self.vessels["beaker"]
        self.pipette = pip.Pipette()
        # IK runs on a copy, so solving never moves the arm on camera.
        self.plan = mujoco.MjData(self.model)

    # --- control ----------------------------------------------------------

    def start(self) -> None:
        self.thread = threading.Thread(target=self._run, name=f"formulation:{self.run_id}", daemon=True)
        self.thread.start()

    def stop(self) -> None:
        self._stop.set()

    @property
    def elapsed(self) -> float:
        return (time.monotonic() - self._t0) * self.speed

    # --- the run ----------------------------------------------------------

    def _run(self) -> None:
        try:
            self._begin()
            for dose in self.doses:
                self._dose(dose)
            self._finish()
        except Aborted:
            self.status = "aborted"
            self._event("run stopped by the operator", "warn")
        except Exception as exc:  # noqa: BLE001 -- the viewer keeps running
            self.status = "failed"
            self._event(f"run failed: {exc}", "error")
        finally:
            self.sampling = False
            if self.status != "completed":
                # What was under way when it stopped did not finish.
                for step in self.steps:
                    if step.status == "active":
                        step.status, step.completed = "failed", self.elapsed
                for dose in self.doses:
                    if dose.status == "active":
                        dose.status = "failed"
                self.current, self.mode, self.flow, self.stable = None, "stopped", 0.0, True
            try:
                self._park()
            except Exception as exc:  # noqa: BLE001
                self._event(f"could not park the arm: {exc}", "error")
            self._publish(force=True)
            self.scene.formulation_finished(self)

    def _begin(self) -> None:
        # The sweep may have moved the arm since the run was made.
        with self.lock:
            self.pose = Pose(float(self.data.body("rail_carriage").xpos[0]),
                             self.data.qpos[rk.arm_qpos(self.model)].copy())
            self.tip = self.data.site(rk.TCP_SITE).xpos.copy()
        snapshot = S.empty_state(self.run_id, workcell(self.model, self.data, self.balance_id, self._rail()))
        snapshot["run"].update(status="running", simulated=True, scripted=False, phase="plan")
        snapshot["robot"] = self._robot()
        self.server.snapshot(snapshot)
        self._event(f"formula {self.formula['id']} accepted: {len(self.doses)} ingredients, "
                    f"{self.target:.3f} g into the beaker on {self.balance_id}", "info")
        skipped = [i for i in self.formula["ingredients"] if i.get("problem")]
        for ing in skipped:
            self._event(f"{ing['compound']} skipped: {ing['problem']}", "warn")
        self._set_step("tare", "active")
        self.fsm, self.action = "TARE", f"Fresh beaker on {self.balance_id}, taring"
        with self.lock:
            self.beaker.volume = 0.0
            self.pipette.volume = 0.0
            pip.sync(self.model, {"beaker": self.beaker}, self.pipette)
            pip.show_mass(self.model, 0.0)
        self._wait(0.8)
        self._set_step("tare", "completed")
        self._event(f"{self.balance_id} tared at 0.000 g", "ok")
        self.beaker_path = self._plan_beaker()

    def _dose(self, dose: Dose) -> None:
        self.current = dose
        dose.status = "active"
        vessel = self.vessels.get(dose.sample)
        self._set_step(f"loc-{dose.id}", "active")
        self.fsm, self.camera = "LOCATE", "overview"
        self.action = f"Locating {dose.sample} · {dose.compound}"
        self.pipeline_hint = "localization"
        path = self._plan_vessel(vessel) if vessel else None
        if path is not None:
            self.located = (float(path["axis"][0]), float(path["axis"][1]))
        self._wait(1.0)
        if path is None:
            dose.status = "failed"
            self._set_step(f"loc-{dose.id}", "failed")
            self._event(f"{dose.sample} is out of the arm's reach; {dose.compound} skipped", "error")
            return
        self.pipeline_hint = "barcode"
        self._wait(0.6)
        self._event(f"{dose.sample} identified: {dose.compound} ({dose.barcode})", "ok")
        self._set_step(f"loc-{dose.id}", "completed")

        self.pipeline_hint = None
        self._set_step(f"dose-{dose.id}", "active")
        self.net0 = self.beaker.mass
        dose.dispensed = 0.0
        self.sampling = True
        while True:
            remaining = dose.target - self._net()
            if remaining <= CLOSE_G:
                break
            if dose.trips >= trips_for(dose.target) + 3:
                self._event(f"{dose.compound}: giving up after {dose.trips} draws", "error")
                break
            self.mode, ask = next_draw(remaining / DENSITY)
            dose.trips += 1
            self._trip(dose, vessel, path, ask)
        self.mode = "stopped"

        self._set_step(f"dose-{dose.id}", "completed")
        self._set_step(f"ver-{dose.id}", "active")
        self.fsm, self.action = "VERIFY", f"Checking {dose.compound} on {self.balance_id}"
        self.pipeline_hint = "verification"
        self._wait(0.8)
        self.sampling = False
        dose.dispensed = self._net()
        error = dose.dispensed - dose.target
        dose.passed = abs(error) <= TOLERANCE_G
        dose.status = "completed" if dose.passed else "failed"
        self._set_step(f"ver-{dose.id}", "completed" if dose.passed else "failed")
        self._event(f"{dose.compound}: {dose.dispensed:.3f} g of {dose.target:.3f} g "
                    f"({error:+.3f}) in {dose.trips} draws", "ok" if dose.passed else "warn")

    def _trip(self, dose: Dose, vessel: pip.Container, path: dict, ask_ml: float) -> None:
        """Draw once from the flask and deliver it into the beaker."""
        n = dose.trips
        detail = [("draw", str(n)), ("mode", self.mode), ("tip", f"{ask_ml:.2f} ml")]
        self._detail(f"dose-{dose.id}", detail)
        self.fsm, self.camera = "TRAVERSE", "overview"
        self.action = f"To {dose.sample} for draw {n} ({ask_ml:.2f} ml)"
        self.pipeline_hint = None
        self._move(self._lift_here())
        self._move(path["transit"])
        self._move(path["over"])

        self.fsm, self.camera, self.pipeline_hint = "ASPIRATE", "robot", None
        self.action = f"Drawing {ask_ml:.2f} ml of {dose.compound} from {dose.sample}"
        drawn = False
        for attempt in range(2):
            down = self._plan_down(vessel, path["over"], deeper=attempt > 0)
            if down is None:
                break
            self._move(down, min_s=0.6)
            self._wait(0.3)
            asked = max(0.0, ask_ml * (1 + self.rng.normal(0, PIPETTE_CV)))
            with self.lock:
                drawn = pip.aspirate(self.model, self.data, vessel, self.pipette, asked)
            if drawn:
                break
            self.recoveries += 1
            self._event(f"draw refused: {self.pipette.events[-1]}; going deeper", "warn")
        self._wait(0.5)
        self._move(path["over"], min_s=0.6)
        if not drawn:
            raise RuntimeError(f"could not draw from {dose.sample}")
        self._event(f"{dose.sample}: drew {self.pipette.volume:.3f} ml", "info")

        self.fsm, self.camera, self.pipeline_hint = "TRANSFER", "overview", None
        self.action = f"Carrying {self.pipette.volume:.2f} ml to the beaker"
        self._move(path["transit"])
        self._move(self.beaker_path["transit"])
        self._move(self.beaker_path["clear"])
        self._move(self.beaker_path["into"], min_s=0.6)

        self.fsm, self.camera, self.pipeline_hint = "DISPENSE", "robot", None
        self.action = f"Delivering {dose.compound} into the beaker"
        held = self.pipette.volume
        self.stable = False
        self.flow = held * DENSITY / DISPENSE_S
        start = self.elapsed
        while self.pipette.volume > 1e-9:
            frac = min(1.0, (self.elapsed - start) / DISPENSE_S)
            give = self.pipette.volume - held * (1 - frac)
            if frac >= 1.0 or give > 0:
                with self.lock:
                    ok = pip.dispense(self.model, self.data, self.beaker, self.pipette,
                                      None if frac >= 1.0 else give)
                    pip.show_mass(self.model, max(0.0, self._net()))
                if not ok:
                    raise RuntimeError(f"delivery refused: {self.pipette.events[-1]}")
            self._tick()
        self.flow = 0.0
        self._wait(0.3)
        self.stable = True
        dose.dispensed = self._net()
        self._move(self.beaker_path["clear"], min_s=0.6)

    def _finish(self) -> None:
        self.current = None
        self._set_step("check", "active")
        self.fsm, self.action = "VERIFY", "Final check of the batch"
        self.pipeline_hint = "verification"
        with self.lock:
            pip.show_mass(self.model, self.beaker.mass)
        self._wait(1.0)
        self.net0 = 0.0
        dosed = [d for d in self.doses if d.dispensed is not None]
        passed = bool(dosed) and all(d.passed for d in self.doses)
        self._set_step("check", "completed" if passed else "failed")
        self.status = "completed"
        total = self.beaker.mass
        self._event(f"batch {total:.3f} g of {self.target:.3f} g · "
                    f"{'PASS' if passed else 'out of tolerance'}", "ok" if passed else "warn")
        self.summary = {
            "targetMass": self.target, "finalMass": total,
            "absoluteError": abs(total - self.target),
            "ingredientsDone": sum(bool(d.passed) for d in self.doses),
            "ingredientsTotal": len(self.doses), "recoveries": self.recoveries,
            "executionSeconds": self.elapsed, "passed": passed,
        }

    def _park(self) -> None:
        self._set_step("park", "active")
        self.fsm, self.action, self.camera = "PARK", "Parking the arm", "overview"
        self.pipeline_hint = None
        self.sampling = False
        if self.pipette.volume > 0:
            self.pipette.volume = 0.0
            with self.lock:
                pip.sync(self.model, {}, self.pipette)
        # A second stop must not strand the arm on the way home.
        self.parking = True
        self._move(self._lift_here())
        resume = self.scene.resume_pose()
        if resume is not None:
            resume = Pose(float(resume[0]), np.asarray(resume[1], dtype=float))
            tip = self._tip_at(resume)
            lifted = self._solve(np.array([tip[0], tip[1], TRANSIT_Z]), station=resume.x, seed=self.pose)
            if lifted is not None:
                self._move(lifted)
            self._move(resume)
        self._set_step("park", "completed")
        self.fsm, self.action, self.moving = "IDLE", "Idle", False
        self.pipeline_hint = None

    # --- planning ---------------------------------------------------------

    def _plan_steps(self) -> list[Step]:
        steps = [Step("tare", f"Tare {self.balance_id} with an empty beaker")]
        for d in self.doses:
            steps += [
                Step(f"loc-{d.id}", f"Locate {d.sample} · {d.compound}", d.id),
                Step(f"dose-{d.id}", f"Pipette {d.target:.3f} g of {d.compound}", d.id),
                Step(f"ver-{d.id}", f"Verify on {self.balance_id}", d.id),
            ]
        steps += [Step("check", f"Final check · {self.target:.3f} g"), Step("park", "Park the arm")]
        return steps

    def _solve(self, target: np.ndarray, station: float | None = None,
               seed: Pose | None = None) -> Pose | None:
        """IK on the private copy: a pose reaching ``target``, or None."""
        seed = seed or self.pose
        self.plan.qpos[:] = self.data.qpos
        self.plan.qpos[rk.arm_qpos(self.model)] = seed.q
        rk.set_rail(self.model, self.plan, seed.x)
        if station is None:
            x = rk.reach(self.model, self.plan, target)
            if x is None:
                return None
        else:
            x = rk.set_rail(self.model, self.plan, station)
            if not rk.solve_any(self.model, self.plan, target):
                return None
        return seed.toward(Pose(float(x), self.plan.qpos[rk.arm_qpos(self.model)].copy()))

    def _plan_vessel(self, vessel: pip.Container) -> dict | None:
        axis = self.data.body(vessel.body).xpos.copy()
        rim = float(self.data.site(vessel.mouth).xpos[2])
        over = self._solve(np.array([axis[0], axis[1], rim + CLEARANCE]))
        if over is None:
            return None
        transit = self._solve(np.array([axis[0], axis[1], TRANSIT_Z]), station=over.x, seed=over)
        return {"over": over, "transit": transit or over, "axis": axis}

    def _plan_down(self, vessel: pip.Container, over: Pose, deeper: bool) -> Pose | None:
        """Into the bore: a quarter of the way down the column, or near the floor."""
        axis = self.data.body(vessel.body).xpos
        column = vessel.height()
        below = max(min(column * 0.25, column - 0.003), 0.003) if not deeper else max(column - 0.0015, 0.0015)
        z = float(axis[2]) + vessel.floor + column - below
        return self._solve(np.array([axis[0], axis[1], z]), station=over.x, seed=over)

    def _plan_beaker(self) -> dict:
        mouth = self.data.site(self.beaker.mouth).xpos.copy()
        into = np.array([mouth[0], mouth[1], mouth[2] - 0.01])
        clear = self._solve(into + [0, 0, BEAKER_CLEAR])
        if clear is None:
            raise RuntimeError("the beaker is out of the arm's reach")
        down = self._solve(into, station=clear.x, seed=clear)
        transit = self._solve(np.array([mouth[0], mouth[1], TRANSIT_Z]), station=clear.x, seed=clear)
        if down is None:
            raise RuntimeError("the tip cannot get into the beaker")
        return {"clear": clear, "into": down, "transit": transit or clear}

    def _lift_here(self) -> Pose:
        up = self._solve(np.array([self.tip[0], self.tip[1], max(TRANSIT_Z, self.tip[2])]),
                         station=self.pose.x)
        return up or self.pose

    def _tip_at(self, pose: Pose) -> np.ndarray:
        rk.set_rail(self.model, self.plan, pose.x)
        self.plan.qpos[rk.arm_qpos(self.model)] = pose.q
        mujoco.mj_kinematics(self.model, self.plan)
        return self.plan.site(rk.TCP_SITE).xpos.copy()

    # --- motion and time ----------------------------------------------------

    def _move(self, goal: Pose | None, min_s: float = MIN_MOVE_S) -> None:
        if goal is None:
            return
        start = self.pose
        goal = start.toward(goal)
        seconds = max(abs(goal.x - start.x) / RAIL_SPEED,
                      float(np.max(np.abs(goal.q - start.q))) / JOINT_SPEED, min_s)
        t0 = self.elapsed
        self.moving = True
        while True:
            u = min(1.0, (self.elapsed - t0) / seconds)
            s = u * u * (3 - 2 * u)
            self._apply(Pose(start.x + (goal.x - start.x) * s, start.q + (goal.q - start.q) * s))
            if u >= 1.0:
                break
            self._tick()
        self.moving = False

    def _apply(self, pose: Pose) -> None:
        with self.lock:
            rk.set_rail(self.model, self.data, pose.x)
            self.data.qpos[rk.arm_qpos(self.model)] = pose.q
            mujoco.mj_forward(self.model, self.data)
            self.tip = self.data.site(rk.TCP_SITE).xpos.copy()
        self.pose = pose

    def _wait(self, seconds: float) -> None:
        t0 = self.elapsed
        while self.elapsed - t0 < seconds:
            self._tick()

    def _tick(self) -> None:
        if self._stop.is_set() and not self.parking:
            raise Aborted
        now = self.elapsed
        if self.sampling and now >= self._next_sample:
            self.server.mass_sample(now, self._net())
            self._next_sample = now + SAMPLE_S * self.speed
        self._publish()
        time.sleep(TICK_S)

    def _net(self) -> float:
        return self.beaker.mass - self.net0

    # --- LabState -----------------------------------------------------------

    def _event(self, message: str, level: str = "info") -> None:
        self.server.event(self.elapsed, message, level)

    def _set_step(self, step_id: str, status: str) -> None:
        for step in self.steps:
            if step.id == step_id:
                step.status = status
                if status == "active":
                    step.started = self.elapsed
                elif status in ("completed", "failed"):
                    step.completed = self.elapsed
        self._publish(force=True)

    def _detail(self, step_id: str, detail: list) -> None:
        for step in self.steps:
            if step.id == step_id:
                step.detail = [list(kv) for kv in detail]

    def _rail(self) -> dict:
        joint = self.model.joint(rk.RAIL_JOINT)
        home = self.model.body("rail_carriage").pos
        return {"x0": float(home[0] + joint.range[0]), "x1": float(home[0] + joint.range[1]), "y": float(home[1])}

    def _robot(self) -> dict:
        dose = self.current
        robot = S.robot_state(
            self.fsm, S.vec3(self.pose.x, *self.model.body("rail_carriage").pos[1:]), S.vec3(*self.tip),
            arm="UR10e", end_effector="PIPETTE",
            target_object=dose.sample if dose else None, compound=dose.compound if dose else None,
            gripper="open", current_action=self.action, recoveries=self.recoveries)
        robot["tipVolumeMl"] = self.pipette.volume
        return robot

    def _publish(self, force: bool = False) -> None:
        now = time.monotonic()
        if not force and now < self._next_publish:
            return
        self._next_publish = now + PUBLISH_S
        self.server.patch(self._patch(), timestamp=time.time())

    def _patch(self) -> dict:
        dose = self.current
        done = sum(d.status in ("completed", "failed") for d in self.doses)
        dispensed = sum(d.dispensed or 0.0 for d in self.doses)
        passed = sum(bool(d.passed) for d in self.doses)
        hint = self.pipeline_hint if self.status == "running" else None

        def node(node_id, model, lines, active=False, trouble=False):
            status = "active" if active or hint == node_id else "warn" if trouble else "ok"
            return S.pipeline_node(node_id, model, lines, status)

        info = self.catalogue.samples.get(dose.sample) if dose else None
        patch = {
            "run": {"id": self.run_id, "status": self.status, "elapsedSeconds": self.elapsed,
                    "progress": min(1.0, dispensed / self.target) if self.target else 0.0,
                    "phase": self.fsm.lower(), "simulated": True, "scripted": False},
            "recipe": {
                "id": self.formula["id"], "name": self.formula["name"], "targetMass": self.target,
                "ingredients": [S.ingredient(d.id, d.compound, d.target, "liquid", d.cas, d.dispensed,
                                             d.sample if d.status != "queued" else None, d.container_ml,
                                             d.status) for d in self.doses],
            },
            "execution": {"currentStepId": next((s.id for s in self.steps if s.status == "active"), None),
                          "steps": [s.as_dict() for s in self.steps]},
            "balance": {
                "id": self.balance_id, "netMass": self._net() if dose else self.beaker.mass,
                "totalMass": self.beaker.mass, "targetMass": dose.target if dose else self.target,
                "batchTargetMass": self.target, "flowRate": self.flow, "mode": self.mode,
                "stable": self.stable, "ingredientId": dose.id if dose else None,
            },
            "robot": self._robot(),
            "perception": S.perception_state(
                self.camera, target=dose.sample if dose else None,
                target_class="amber flask" if dose else None,
                barcode=dose.barcode if dose and dose.status != "queued" else None,
                barcode_status="catalogue" if dose else "idle",
                identity=dose.compound if dose else None,
                container_ml=info["containerMl"] if info else None),
            "pipeline": [
                node("camera", "Scene cameras", ["general · live", f"view {self.camera}"]),
                node("detection", "YOLO", ["—", "—"]),
                node("localization", "Scene poses",
                     [f"x {self.located[0]:+.2f} · y {self.located[1]:+.2f} m" if dose and self.located else "—",
                      "from the sim model, not the cameras"]),
                node("barcode", "Catalogue", [dose.barcode if dose else "—", dose.compound if dose else "—"]),
                node("planner", "Rail IK",
                     [f"{done}/{len(self.doses)} ingredients", f"{sum(d.trips for d in self.doses)} draws"]),
                node("motion", "Kinematic", ["MOVING" if self.moving else "HOLD", f"rail {self.pose.x:+.2f} m"],
                     active=self.moving and self.status == "running"),
                node("dosing", "Pipette loop",
                     [f"{self.mode} · {self.pipette.volume:.2f} ml", f"{self.flow:.3f} g/s"],
                     active=self.sampling and self.status == "running"),
                node("verification", "Balance check",
                     [f"{passed}/{len(self.doses)} PASS", f"tol ±{TOLERANCE_G:.3f} g"],
                     trouble=any(d.passed is False for d in self.doses)),
            ],
            "summary": self.summary,
        }
        return patch


def idle_state(model: mujoco.MjModel, data: mujoco.MjData) -> dict:
    """The LabState before any formula has run: the workcell, nothing else."""
    joint = model.joint(rk.RAIL_JOINT)
    home = model.body("rail_carriage").pos
    rail = {"x0": float(home[0] + joint.range[0]), "x1": float(home[0] + joint.range[1]), "y": float(home[1])}
    balance = (pip.display_prefix(model) or "balance_2_").rstrip("_")
    state = S.empty_state("—", workcell(model, data, balance, rail))
    state["robot"]["arm"] = "UR10e"
    state["robot"]["endEffector"] = "PIPETTE"
    state["balance"]["id"] = balance
    return state
