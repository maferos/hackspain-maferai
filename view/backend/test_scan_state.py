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
        # While the bench is being read the bar is the scan task's one step, not
        # a formula's: the scan is a task, never a stage of somebody's formula.
        self.assertEqual([(s["id"], s["status"]) for s in p["workflow"]["stages"]], [("scan", "active")])

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
        # The scan task is done, so the bar moves on to what a formula would do.
        self.assertEqual([s["id"] for s in p["workflow"]["stages"]][0], "formula")
        self.assertEqual(p["robot"]["fsmState"], "IDLE")

    def test_a_formula_never_carries_a_scan_stage(self):
        self.patch("idle: watching the bench", scan={"scans": [{}]})
        chat = FormulaChat(self.catalogue, self.state.shelf)
        self.state.dispatch(chat.reply("1.2 g geraniol")["formula"], "chat")
        p = self.patch("idle: watching the bench", scan={"scans": [{}]})
        ids = [s["id"] for s in p["workflow"]["stages"]]
        self.assertNotIn("scan", ids)
        self.assertEqual(ids[:2], ["formula", "check"])

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
        # The invented levels are not this suite's subject: fill the bench so a
        # test that fails, fails about what it is testing.
        for sample in ("SMP-0014", "SMP-0039"):
            self.catalogue.levels.set_ml(sample, self.catalogue.samples[sample]["containerMl"])

    # The default formula is one the bench can make; the check rejects anything
    # else outright, which the rejection tests below are about.
    def order(self, executor, text="1.2 g geraniol, 0.5 g nerol"):
        masses = []
        wf = Workflow(self.catalogue, self.shelf, on_mass=masses.append, executor=executor, order_file=None)
        wf.submit(self.chat.reply(text)["formula"], "chat")
        return wf, masses

    def test_the_json_is_the_harness_format_plus_the_flask(self):
        wf, _ = self.order("external", "1.2 g geraniol, 0.5 g nerol, 0.3 g hedione")
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
        self.assertEqual(state["status"], "completed")
        self.assertFalse(state["qc"]["passed"])
        self.assertEqual(masses, [1.204, 0.53])
        stages = {s["id"]: s["status"] for s in state["stages"]}
        self.assertEqual(stages["qc"], "failed")
        self.assertEqual(stages["dose"], "failed")
        self.assertNotEqual(stages["done"], "failed")
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

    def test_a_compound_off_the_bench_is_rejected_at_the_check(self):
        wf, _ = self.order("external", "1.2 g geraniol, 0.3 g hedione")
        state = wf.state(True)
        self.assertEqual(state["status"], "rejected")
        self.assertFalse(state["check"]["passed"])
        self.assertEqual([p["compound"] for p in state["check"]["problems"]], ["Hedione"])
        self.assertEqual(state["check"]["problems"][0]["reason"], "not identified on the bench")
        stages = {s["id"]: s["status"] for s in state["stages"]}
        self.assertEqual(stages["check"], "failed")
        # Nothing after the check was attempted, and Done did not fail: the
        # failure belongs to the stage that found it.
        self.assertEqual(stages["dose"], "skipped")
        self.assertEqual(stages["done"], "skipped")
        # Not a step of it was run, including the lines that were on the bench.
        self.assertTrue(all(s["status"] == "skipped"
                            for i in wf.order.items for s in i["steps"].values()))

    def test_a_flask_without_enough_left_is_rejected_at_the_check(self):
        self.catalogue.levels.set_ml("SMP-0039", 0.4)       # 0.4 g of nerol left
        wf, _ = self.order("external", "1.2 g geraniol, 0.5 g nerol")
        state = wf.state(True)
        self.assertEqual(state["status"], "rejected")
        self.assertEqual([p["compound"] for p in state["check"]["problems"]], ["Nerol"])
        self.assertIn("only 0.4 g left in SMP-0039", state["check"]["problems"][0]["reason"])

    def test_dosing_draws_the_flask_down(self):
        wf, _ = self.order("external")
        before = self.catalogue.levels.left_ml("SMP-0014")
        wf.report("SMP-0014", "dose", "completed", mass=1.204)
        self.assertAlmostEqual(self.catalogue.levels.left_ml("SMP-0014"), before - 1.204, places=3)

    def test_a_second_formula_queues_behind_the_first(self):
        wf, _ = self.order("external")
        second = wf.submit(self.chat.reply("1 g geraniol")["formula"], "chat")
        # It is accepted, not refused, and it is not what the panel is about.
        self.assertEqual(wf.order.id, "ORD-001")
        self.assertEqual([o.id for o in wf.waiting()], ["ORD-002"])
        # Behind the front, it is not checked: the bench it will be judged
        # against is the one standing when its turn comes.
        self.assertIsNone(second.check)
        wf.abort()
        self.assertEqual(wf.state(True)["id"], "ORD-002")
        wf.pump()
        self.assertIsNotNone(wf.order.check)

    def test_a_formula_queued_on_an_empty_bench_is_matched_again_later(self):
        # The trap: an order queued mid-scan was resolved against whatever had
        # been named at the time. Deferring the verdict is not enough — on an
        # empty bench every line reads "not identified", and the check would
        # refuse a formula the finished bench can make.
        empty = []
        shelf = lambda: shelf_from_tracks(empty, self.catalogue)
        wf = Workflow(self.catalogue, shelf, executor="external", order_file=None,
                      scan_done=lambda: False)
        order = wf.submit(FormulaChat(self.catalogue, self.shelf)
                          .reply("1.2 g geraniol, 0.5 g nerol")["formula"], "chat")
        wf.shelf = self.shelf                   # the scan finishes; the bench fills
        wf.scan_done = lambda: True
        wf.pump()
        self.assertTrue(order.check["passed"], order.check)
        self.assertEqual([i["sampleId"] for i in order.items], ["SMP-0014", "SMP-0039"])

    def test_a_formula_sent_before_the_scan_waits_unchecked(self):
        wf = Workflow(self.catalogue, self.shelf, executor="external", order_file=None,
                      scan_done=lambda: False)
        order = wf.submit(self.chat.reply("1.2 g geraniol, 0.5 g nerol")["formula"], "chat")
        self.assertEqual(order.status, "queued")
        self.assertIsNone(order.check)
        self.assertIsNone(wf.pump())        # still scanning: nothing is admitted
        wf.scan_done = lambda: True
        self.assertIs(wf.pump(), order)
        self.assertTrue(order.check["passed"])


class FetchExecutorTest(unittest.TestCase):
    def setUp(self):
        self.catalogue = Catalogue()
        self.tracks = [track(1, "named", "SMP-0014"), track(2, "named", "SMP-0039")]
        self.world = world(self.tracks, scan={"scans": [{}]})
        shelf = lambda: shelf_from_tracks(self.tracks, self.catalogue)
        self.wf = Workflow(self.catalogue, shelf, executor="fetch", order_file=None)
        for sample in ("SMP-0014", "SMP-0039"):
            self.catalogue.levels.set_ml(sample, self.catalogue.samples[sample]["containerMl"])
        self.wf.submit(FormulaChat(self.catalogue, shelf)
                       .reply("1 g geraniol, 0.5 g nerol")["formula"], "chat")

    def run_arm(self, executor):
        """Take each pick command as the real controller does, with its captions."""
        self.asked = []
        def controller():
            while executor.thread.is_alive():
                with self.world.lock:
                    asked = [c for c in self.world.commands if c["cmd"] == "pick"]
                    self.world.commands.clear()
                self.asked += asked
                for command in asked:
                    t = next(t for t in self.tracks if t.id == command["track"])
                    for caption in (f"travelling to {t.sample}",
                                    f"lowering the hand over {t.sample}",
                                    f"lifting the hand off {t.sample}",
                                    f"carrying {t.sample} to the balance",
                                    f"over the beaker with {t.sample}"):
                        self.wf.observe(self.tracks, caption, False)
                    t.picks += 1
                time.sleep(0.05)
        executor.start()
        threading.Thread(target=controller, daemon=True).start()
        executor.thread.join(10)
        self.wf.observe(self.tracks, "idle: watching the bench", False)

    def test_every_flask_is_visited_and_dosed_through_the_controller(self):
        self.run_arm(FetchExecutor(self.wf, self.world))
        state = self.wf.state(True)
        self.assertEqual(state["status"], "completed")
        self.assertTrue(state["qc"]["passed"])
        self.assertEqual([[s["status"] for s in i["steps"]] for i in state["ingredients"]],
                         [["completed"] * 3, ["completed"] * 3])

    def test_the_arm_is_told_the_dose_and_the_balance_is_told_it_landed(self):
        self.run_arm(FetchExecutor(self.wf, self.world))
        # Nothing is weighed: the pipetting is mimed, so what the formula asked
        # for is what the arm is sent for and what the balance reports.
        wanted = [i["grams"] for i in self.wf.state(True)["ingredients"]]
        self.assertEqual([c["ml"] for c in self.asked], wanted)
        self.assertEqual([i["mass"] for i in self.wf.state(True)["ingredients"]], wanted)

    def test_a_flask_the_scan_lost_is_neither_visited_nor_dosed(self):
        self.tracks[0].state = "lost"
        self.run_arm(FetchExecutor(self.wf, self.world))
        steps = [[s["status"] for s in i["steps"]]
                 for i in self.wf.state(True)["ingredients"]]
        self.assertEqual(steps[0], ["failed", "skipped", "skipped"])
        self.assertEqual(steps[1], ["completed"] * 3)


if __name__ == "__main__":
    unittest.main()
