"""The panels' LabState from the live scan, the formula chat, and the order workflow."""
import json
import threading
import time
import unittest
from types import SimpleNamespace

import numpy as np

from catalogue import Catalogue, shelf_from_tracks
from formula_chat import FormulaChat
from scan_state import FetchExecutor, ScanState, fsm_of
from workflow import Workflow, lines_from_json


def track(id, state, sample=None, xy=(0.0, 0.0), note="", ring=None):
    confirmation = SimpleNamespace(sample_id=sample, marker_id=ring, refined_xy=xy) if sample else None
    return SimpleNamespace(id=id, state=state, sample=sample, xy=xy, note=note, picks=0,
                           confirmation=confirmation, wrist_only=False)


def world(tracks, caption="", scan=None):
    return SimpleNamespace(lock=threading.Lock(), commands=[], scan=scan, caption=caption,
                           cycle_seconds=1.5, events=[], snapshot=lambda: list(tracks))


class ScanStateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = Catalogue()

    def setUp(self):
        self.tracks = [
            track(1, "named", "SMP-0014", (-1.2, -0.3), "ring read, 4 markers", ring=13),
            track(2, "empty", note="no ring from 2 views: not a sample"),
            track(3, "proposed", xy=(-0.5, -0.4)),
            track(4, "unreachable", xy=(0.9, 0.5), note="the wrist camera cannot get there"),
            track(5, "lost"),
        ]
        self.world = world(self.tracks)
        scene = SimpleNamespace(pattern={"pattern": "p06"}, scan=SimpleNamespace(world=self.world, error=None))
        self.server = SimpleNamespace(mass_sample=lambda time, mass: None)
        self.state = ScanState(scene, self.server, self.catalogue, executor="external")
        self.state.workflow.order_file = None

    def patch(self, caption, scan=None, error=None):
        self.world.caption, self.world.scan = caption, scan
        return self.state._patch(SimpleNamespace(error=error), self.world, self.world.snapshot(), 12.5,
                                 np.array([-1.5, 0.14, 1.45]), np.array([-1.2, -0.3, 1.1]), False)

    def test_the_tally_counts_what_the_rings_said(self):
        p = self.patch("initial scan 2/3: looking at track 3 at (-0.50, -0.40)")
        self.assertEqual({k: p["scan"][k] for k in ("named", "tracked", "waiting", "empty", "unreachable")},
                         {"named": 1, "tracked": 4, "waiting": 1, "empty": 1, "unreachable": 1})
        self.assertEqual(p["run"]["id"], "SCAN-P06")
        self.assertEqual(p["run"]["status"], "running")
        self.assertIsNone(p["order"])
        self.assertEqual([s["status"] for s in p["workflow"]["stages"]][:2], ["active", "queued"])

    def test_the_robot_and_plan_follow_the_caption(self):
        p = self.patch("initial scan 2/3: reading the ring at track 3 at (-0.50, -0.40)")
        self.assertEqual(p["robot"]["fsmState"], "READ_RING")
        self.assertEqual(p["robot"]["targetObject"], "track 3")
        self.assertEqual(p["perception"]["activeCamera"], "wrist")
        steps = {s["id"]: s for s in p["execution"]["steps"]}
        self.assertEqual(steps["track-3"]["status"], "active")
        self.assertEqual(steps["track-1"]["label"], "SMP-0014 · Geraniol")
        self.assertEqual(steps["track-4"]["status"], "failed")
        self.assertNotIn("track-5", steps)
        self.assertEqual(p["execution"]["currentStepId"], "track-3")

    def test_a_mapped_bench_completes_the_scan(self):
        p = self.patch("idle: watching the bench", scan={"scans": [{}]})
        self.assertEqual(p["run"]["status"], "completed")
        self.assertEqual(p["workflow"]["stages"][0]["status"], "completed")
        self.assertEqual(p["robot"]["fsmState"], "IDLE")

    def test_an_order_takes_over_the_plan_and_the_balance(self):
        self.patch("idle: watching the bench", scan={"scans": [{}]})
        chat = FormulaChat(self.catalogue, self.state.shelf)
        self.state.dispatch(chat.reply("1.2 g geraniol")["formula"], "chat")
        self.state.workflow.observe(self.tracks, "", False)
        self.state.workflow.report("SMP-0014", "dose", "active", mass=0.7)
        p = self.patch("holding SMP-0014", scan={"scans": [{}]})
        self.assertEqual(p["order"]["id"], "ORD-001")
        self.assertEqual(p["run"]["id"], "ORD-001")
        self.assertEqual(p["balance"]["netMass"], 0.7)
        self.assertEqual(p["balance"]["targetMass"], 1.2)
        self.assertEqual(p["balance"]["mode"], "dosing")
        steps = [s for s in p["execution"]["steps"] if s["id"] != "scan"]
        self.assertEqual([s["status"] for s in steps],
                         ["completed", "completed", "completed", "active", "queued", "queued"])
        self.assertEqual(p["pipeline"][6]["status"], "active")

    def test_captions(self):
        self.assertEqual(fsm_of("travelling to SMP-0014"), "TRAVERSE")
        self.assertEqual(fsm_of("closing on SMP-0014"), "GRASP")
        self.assertEqual(fsm_of("initial scan: the fixed camera surveys the bench"), "SURVEY")
        self.assertEqual(fsm_of("over the flasks to track 3"), "TRAVERSE")


class ChatTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = Catalogue()
        tracks = [track(1, "named", "SMP-0014"), track(2, "named", "SMP-0039"), track(3, "proposed")]
        cls.shelf = shelf_from_tracks(tracks, cls.catalogue)
        cls.chat = FormulaChat(cls.catalogue, lambda: cls.shelf)

    def lines(self, formula):
        return {i["compound"]: (i["grams"], i["sampleId"], i["problem"]) for i in formula["ingredients"]}

    def test_only_named_flasks_are_offered(self):
        self.assertEqual([f["sampleId"] for f in self.shelf], ["SMP-0014", "SMP-0039"])
        f = self.chat.reply("1,2 g geraniol, 0.5 g nerol y 300 mg hedione")["formula"]
        lines = self.lines(f)
        self.assertEqual(lines["Geraniol"], (1.2, "SMP-0014", None))
        self.assertEqual(lines["Hedione"][2], "not identified on the bench")
        self.assertEqual(f["source"], "chat")

    def test_forms(self):
        f = self.chat.reply("50% geraniol 50% nerol 2 g total")["formula"]
        self.assertEqual({k: v[0] for k, v in self.lines(f).items()}, {"Geraniol": 1.0, "Nerol": 1.0})
        self.assertIn("Geraniol", self.chat.reply("what's on the bench?")["reply"])
        self.assertEqual(self.chat.reply("send")["action"], "start")
        self.assertEqual(self.chat.reply("para")["action"], "stop")
        self.assertEqual(self.chat.reply("1 g unobtainium, 0.5 g nerol")["formula"]["unknown"], ["unobtainium"])
        self.assertEqual(self.chat.reply("2 g of FRG-101")["formula"]["source"], "catalogue")

    def test_json_in_every_form(self):
        harness = json.loads((Catalogue().formulas["FRG-101"] and json.dumps(Catalogue().formulas["FRG-101"])))
        for doc in (
            {"ingredients": [{"material": "Geraniol", "batch_g": 1.2}, {"compound": "nerol", "grams": 0.5}]},
            [{"name": "Geraniol", "g": 1.2}, {"cas": "106-25-2", "grams": 0.5}],
        ):
            answer = self.chat.reply(json.dumps(doc))
            self.assertEqual(answer["formula"]["source"], "json")
            self.assertEqual({k: v[0] for k, v in self.lines(answer["formula"]).items()},
                             {"Geraniol": 1.2, "Nerol": 0.5})
        lines, head = lines_from_json(harness)
        self.assertEqual(head["id"], "FRG-101")
        self.assertAlmostEqual(sum(line["grams"] for line in lines), 10.0, places=1)
        self.assertEqual(self.chat.reply('{"id": "FRG-103", "batch_g": 2}')["formula"]["id"], "FRG-103")
        self.assertIn("not a formula", self.chat.reply("{not json")["reply"])

    def test_claude_proposals_are_checked_too(self):
        blocks = [SimpleNamespace(type="tool_use", name="propose_formula",
                                  input={"name": "Rose", "ingredients": [{"compound": "Geraniol", "grams": 1.0},
                                                                          {"compound": "Linalool", "grams": 1.0}]})]
        chat = FormulaChat(self.catalogue, lambda: self.shelf)
        chat._client = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: SimpleNamespace(content=blocks)))
        answer = chat.reply("something rosy")
        self.assertEqual(self.lines(answer["formula"])["Linalool"][2], "not identified on the bench")
        self.assertIn("1 of 2", answer["reply"])


class WorkflowTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = Catalogue()

    def setUp(self):
        self.tracks = [track(1, "named", "SMP-0014", (-1.2, -0.3), ring=13),
                       track(2, "named", "SMP-0039", (-0.8, -0.4), ring=38)]
        self.shelf = lambda: shelf_from_tracks(self.tracks, self.catalogue)
        self.chat = FormulaChat(self.catalogue, self.shelf)

    def order(self, executor, text="1.2 g geraniol, 0.5 g nerol, 0.3 g hedione"):
        masses = []
        wf = Workflow(self.catalogue, self.shelf, on_mass=masses.append, executor=executor, order_file=None)
        wf.submit(self.chat.reply(text)["formula"], "chat")
        return wf, masses

    def test_the_json_is_the_harness_format_plus_the_flask(self):
        wf, _ = self.order("external")
        doc = wf.order.doc
        self.assertEqual(doc["batch"], {"concentrate_g": 2.0, "make_g": 1.7})
        line = doc["ingredients"][0]
        self.assertEqual((line["material"], line["batch_g"], line["sample_id"]), ("Geraniol", 1.2, "SMP-0014"))
        self.assertEqual(line["located"]["track"], 1)
        self.assertIn("SMP-0011", line["samples"])
        self.assertEqual(doc["ingredients"][2]["problem"], "not identified on the bench")

    def test_executor_reports_cross_off_and_verify(self):
        wf, masses = self.order("external")
        wf.observe(self.tracks, "", False)
        wf.report("SMP-0014", "dose", "completed", mass=1.204)
        wf.report("Geraniol", "return", "completed")
        wf.report("ing-nerol", "dose", "completed", mass=0.53)
        wf.report("SMP-0039", "return", "completed")
        state = wf.state(True)
        steps = {i["compound"]: {s["id"]: s["status"] for s in i["steps"]} for i in state["ingredients"]}
        self.assertEqual(steps["Geraniol"]["verify"], "completed")
        self.assertEqual(steps["Nerol"]["verify"], "failed")
        self.assertEqual(steps["Hedione"]["dose"], "skipped")
        self.assertEqual(state["status"], "completed")
        self.assertFalse(state["qc"]["passed"])
        self.assertEqual(masses, [1.204, 0.53])
        self.assertEqual(state["stages"][-1]["status"], "failed")
        with self.assertRaises(KeyError):
            wf.report("SMP-0014", "dose", "active")

    def test_steps_never_go_backwards_and_the_arm_only_speaks_for_its_step(self):
        wf, _ = self.order("external")
        wf.observe(self.tracks, "putting SMP-0014 back", False)
        steps = {s: v["status"] for s, v in wf.order.items[0]["steps"].items()}
        self.assertEqual(steps["return"], "active")
        self.assertEqual(steps["pick"], "queued")
        wf.observe(self.tracks, "holding SMP-0014", True)
        self.assertEqual(wf.order.items[0]["steps"]["pick"]["status"], "completed")
        wf.report("SMP-0014", "pick", "active")
        self.assertEqual(wf.order.items[0]["steps"]["pick"]["status"], "completed")

    def test_a_flask_named_after_the_order_joins_it(self):
        wf, _ = self.order("external")
        self.assertEqual(wf.order.items[2]["problem"], "not identified on the bench")
        self.tracks.append(track(3, "named", "SMP-0108", ring=107))
        wf.observe(self.tracks, "", False)
        self.assertIsNone(wf.order.items[2]["problem"])
        self.assertEqual(wf.order.items[2]["steps"]["locate"]["status"], "completed")

    def test_one_order_at_a_time_and_stop(self):
        wf, _ = self.order("external")
        with self.assertRaises(RuntimeError):
            wf.submit(self.chat.reply("1 g geraniol")["formula"], "chat")
        wf.abort()
        self.assertEqual(wf.state(True)["status"], "aborted")
        wf.submit(self.chat.reply("1 g geraniol")["formula"], "chat")
        self.assertEqual(wf.order.id, "ORD-002")


class FetchExecutorTest(unittest.TestCase):
    def test_each_flask_is_picked_through_the_controller(self):
        catalogue = Catalogue()
        tracks = [track(1, "named", "SMP-0014"), track(2, "named", "SMP-0039")]
        w = world(tracks, scan={"scans": [{}]})
        shelf = lambda: shelf_from_tracks(tracks, catalogue)
        wf = Workflow(catalogue, shelf, executor="fetch", order_file=None)
        wf.submit(FormulaChat(catalogue, shelf).reply("1 g geraniol, 0.5 g nerol, 0.2 g hedione")["formula"], "chat")
        executor = FetchExecutor(wf, w)

        def controller():
            # Takes each pick command as the real controller does, with its captions.
            while executor.thread.is_alive():
                with w.lock:
                    asked = [c for c in w.commands if c["cmd"] == "pick"]
                    w.commands.clear()
                for command in asked:
                    t = next(t for t in tracks if t.id == command["track"])
                    for caption, holding in ((f"closing on {t.sample}", False), (f"holding {t.sample}", True),
                                             (f"putting {t.sample} back", False), (f"clear of {t.sample}", False)):
                        wf.observe(tracks, caption, holding)
                    t.state, t.picks = "picked", t.picks + 1
                time.sleep(0.05)

        executor.start()
        threading.Thread(target=controller, daemon=True).start()
        executor.thread.join(10)
        wf.observe(tracks, "idle: watching the bench", False)
        state = wf.state(True)
        self.assertEqual(state["status"], "completed")
        self.assertTrue(state["qc"]["passed"])
        self.assertEqual([[s["status"] for s in i["steps"]] for i in state["ingredients"]],
                         [["completed"] * 3, ["completed"] * 3, ["skipped"] * 3])


if __name__ == "__main__":
    unittest.main()
