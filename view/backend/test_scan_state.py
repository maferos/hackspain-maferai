"""The panels' LabState from the live scan, and the chat's formula against it."""
import threading
import time
import unittest
from types import SimpleNamespace

import numpy as np

from catalogue import Catalogue, shelf_from_tracks
from formula_chat import FormulaChat
from scan_state import Fetch, ScanState, fsm_of


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
        self.state = ScanState(SimpleNamespace(pattern={"pattern": "p06"}), None, self.catalogue)

    def patch(self, caption, scan=None, error=None):
        w = world(self.tracks, caption, scan)
        return self.state._patch(SimpleNamespace(error=error), w, w.snapshot(), 12.5,
                                 np.array([-1.5, 0.14, 1.45]), np.array([-1.2, -0.3, 1.1]), False)

    def test_the_tally_counts_what_the_rings_said(self):
        p = self.patch("initial scan 2/3: looking at track 3 at (-0.50, -0.40)")
        self.assertEqual({k: p["scan"][k] for k in ("named", "tracked", "waiting", "empty", "unreachable")},
                         {"named": 1, "tracked": 4, "waiting": 1, "empty": 1, "unreachable": 1})
        self.assertEqual(p["run"]["id"], "SCAN-P06")
        self.assertEqual(p["run"]["status"], "running")
        self.assertEqual(p["recipe"]["ingredients"], [])

    def test_the_robot_and_plan_follow_the_caption(self):
        p = self.patch("initial scan 2/3: reading the ring at track 3 at (-0.50, -0.40)")
        self.assertEqual(p["robot"]["fsmState"], "READ_RING")
        self.assertEqual(p["robot"]["targetObject"], "track 3")
        self.assertEqual(p["perception"]["activeCamera"], "wrist")
        steps = {s["id"]: s for s in p["execution"]["steps"]}
        self.assertEqual(steps["track-3"]["status"], "active")
        self.assertEqual(steps["track-1"]["label"], "SMP-0014 · Geraniol")
        self.assertEqual(steps["track-1"]["status"], "completed")
        self.assertEqual(steps["track-4"]["status"], "failed")
        self.assertNotIn("track-5", steps)
        self.assertEqual(p["execution"]["currentStepId"], "track-3")
        self.assertEqual(steps["map"]["status"], "queued")

    def test_a_mapped_bench_completes_the_run(self):
        p = self.patch("idle: watching the bench", scan={"scans": [{}]})
        self.assertEqual(p["run"]["status"], "completed")
        self.assertEqual({s["id"]: s["status"] for s in p["execution"]["steps"]}["map"], "completed")
        self.assertEqual(p["robot"]["fsmState"], "IDLE")

    def test_an_error_fails_the_run(self):
        self.assertEqual(self.patch("starting", error="Cannot start scan: no weights")["run"]["status"], "failed")

    def test_captions(self):
        self.assertEqual(fsm_of("travelling to SMP-0014"), "TRAVERSE")
        self.assertEqual(fsm_of("closing on SMP-0014"), "GRASP")
        self.assertEqual(fsm_of("initial scan: the fixed camera surveys the bench"), "SURVEY")


class ChatAgainstScanTest(unittest.TestCase):
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
        self.assertEqual(f["estimate"]["picks"], 2)

    def test_forms(self):
        f = self.chat.reply("50% geraniol 50% nerol 2 g total")["formula"]
        self.assertEqual({k: v[0] for k, v in self.lines(f).items()}, {"Geraniol": 1.0, "Nerol": 1.0})
        self.assertIn("Geraniol", self.chat.reply("what's on the bench?")["reply"])
        self.assertEqual(self.chat.reply("pick")["action"], "start")
        self.assertEqual(self.chat.reply("para")["action"], "stop")
        self.assertEqual(self.chat.reply("1 g unobtainium, 0.5 g nerol")["formula"]["unknown"], ["unobtainium"])

    def test_claude_proposals_are_checked_too(self):
        blocks = [SimpleNamespace(type="tool_use", name="propose_formula",
                                  input={"name": "Rose", "ingredients": [{"compound": "Geraniol", "grams": 1.0},
                                                                          {"compound": "Linalool", "grams": 1.0}]})]
        chat = FormulaChat(self.catalogue, lambda: self.shelf)
        chat._client = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: SimpleNamespace(content=blocks)))
        answer = chat.reply("something rosy")
        self.assertEqual(self.lines(answer["formula"])["Linalool"][2], "not identified on the bench")
        self.assertIn("1 of 2", answer["reply"])


class FetchTest(unittest.TestCase):
    def test_each_flask_is_picked_through_the_controller(self):
        tracks = [track(1, "named", "SMP-0014"), track(2, "named", "SMP-0039")]
        w = world(tracks, scan={"scans": [{}]})
        formula = {"ingredients": [
            {"id": "a", "compound": "Geraniol", "cas": "106-24-1", "grams": 1.0, "sampleId": "SMP-0014", "problem": None},
            {"id": "b", "compound": "Hedione", "cas": "24851-98-7", "grams": 0.3, "sampleId": None,
             "problem": "not identified on the bench"},
            {"id": "c", "compound": "Nerol", "cas": "106-25-2", "grams": 0.5, "sampleId": "SMP-0039", "problem": None},
        ]}
        fetch = Fetch(formula, w)

        def controller():
            # Takes each pick command as the real controller does and picks.
            while fetch.status == "running":
                with w.lock:
                    asked = [c for c in w.commands if c["cmd"] == "pick"]
                    w.commands.clear()
                for command in asked:
                    t = next(t for t in tracks if t.id == command["track"])
                    t.state, t.picks = "picked", t.picks + 1
                time.sleep(0.05)

        threading.Thread(target=controller, daemon=True).start()
        fetch.start()
        fetch.thread.join(10)
        self.assertEqual(fetch.status, "completed")
        self.assertEqual([i["status"] for i in fetch.items], ["completed", "skipped", "completed"])

    def test_stop_clears_the_queue(self):
        w = world([track(1, "named", "SMP-0014")], scan={"scans": [{}]})
        fetch = Fetch({"ingredients": [{"id": "a", "compound": "Geraniol", "cas": "106-24-1", "grams": 1.0,
                                        "sampleId": "SMP-0014", "problem": None}]}, w)
        fetch.start()
        time.sleep(0.3)
        fetch.stop()
        fetch.thread.join(5)
        self.assertEqual(fetch.status, "aborted")
        self.assertEqual(w.commands, [])
        self.assertEqual(fetch.items[0]["status"], "failed")


if __name__ == "__main__":
    unittest.main()
