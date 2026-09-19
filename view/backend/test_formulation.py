"""The formula chat and the formulation run, against a real seeded bench."""
import threading
import unittest
from types import SimpleNamespace

import mujoco

import formulation as F
from formula_chat import FormulaChat
from scene_patterns import SIM, build_pattern


class FakeServer:
    def __init__(self):
        self.patches, self.events, self.samples = [], [], []

    def snapshot(self, state):
        self.snapshot_state = state

    def patch(self, patch, timestamp=None):
        self.patches.append(patch)

    def event(self, time, message, level="info"):
        self.events.append((level, message))

    def mass_sample(self, time, mass):
        self.samples.append(mass)


class FakeScene:
    def __init__(self, model, data):
        self.model, self.data, self._data_lock = model, data, threading.Lock()
        self.finished = threading.Event()

    def resume_pose(self):
        return None

    def formulation_finished(self, run):
        self.finished.set()


class FormulationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model, _ = build_pattern(SIM / "models/minihannover_rail_scene.xml", "p01")
        cls.data = mujoco.MjData(cls.model)
        mujoco.mj_forward(cls.model, cls.data)
        cls.catalogue = F.Catalogue()
        cls.shelf = F.bench(cls.model, cls.data, cls.catalogue)
        cls.chat = FormulaChat(cls.catalogue, lambda: cls.shelf)

    def lines(self, formula):
        return {i["compound"]: (i["grams"], i["sampleId"], i["problem"]) for i in formula["ingredients"]}

    def test_the_bench_is_the_open_flasks_of_the_pattern(self):
        self.assertEqual(len(self.shelf), 16)
        self.assertTrue(all(f["usableG"] > 0 for f in self.shelf))

    def test_lines_in_either_order_and_spanish(self):
        a = self.chat.reply("1,2 g geraniol, 0.5 g nerol y 300 mg hedione")["formula"]
        b = self.chat.reply("Geraniol: 1.2 g\nnerol 0.5g\nhedion 0.3 g")["formula"]
        self.assertEqual(self.lines(a), self.lines(b))
        self.assertEqual(self.lines(a)["Geraniol"][0], 1.2)
        self.assertEqual(a["targetMass"], 2.0)
        self.assertTrue(a["runnable"])

    def test_percentages_take_the_total(self):
        f = self.chat.reply("50% geraniol 30% nerol 20% hedione 4 g total")["formula"]
        self.assertEqual({k: v[0] for k, v in self.lines(f).items()}, {"Geraniol": 2.0, "Nerol": 1.2, "Hedione": 0.8})

    def test_catalogue_formula_marks_what_is_missing(self):
        f = self.chat.reply("2 g of FRG-101")["formula"]
        lines = self.lines(f)
        self.assertEqual(lines["Limonene"][2], "not on this bench")
        self.assertIsNone(lines["Hedione"][2])
        self.assertAlmostEqual(sum(v[0] for v in lines.values()), 2.0, places=2)

    def test_unknown_compounds_are_named_not_guessed(self):
        f = self.chat.reply("1 g unobtainium, 0.5 g carvone")["formula"]
        self.assertEqual(list(self.lines(f)), ["Carvone"])
        self.assertEqual(f["unknown"], ["unobtainium"])

    def test_commands(self):
        self.assertEqual(self.chat.reply("run")["action"], "start")
        self.assertEqual(self.chat.reply("para")["action"], "stop")
        self.assertIsNone(self.chat.reply("3 g para geraniol")["action"])
        self.assertIn("compounds", self.chat.reply("what's on the bench?")["reply"])

    def test_claude_proposals_go_through_the_bench(self):
        blocks = [
            SimpleNamespace(type="text", text="A rosy accord."),
            SimpleNamespace(type="tool_use", name="propose_formula",
                            input={"name": "Rose", "ingredients": [{"compound": "Geraniol", "grams": 1.0},
                                                                    {"compound": "Linalool", "grams": 1.0}]}),
        ]
        calls = []
        client = SimpleNamespace(messages=SimpleNamespace(
            create=lambda **kw: calls.append(kw) or SimpleNamespace(content=blocks)))
        chat = FormulaChat(self.catalogue, lambda: self.shelf)
        chat._client = client
        answer = chat.reply("something rosy", [{"role": "assistant", "text": "hi"}, {"role": "user", "text": "hello"}])
        self.assertEqual(answer["reply"], "A rosy accord.")
        self.assertEqual(self.lines(answer["formula"])["Linalool"][2], "not on this bench")
        self.assertEqual(calls[0]["messages"][0]["role"], "user")
        blocks[:] = [SimpleNamespace(type="tool_use", name="start_run", input={})]
        answer = chat.reply("go ahead")
        self.assertEqual(answer["action"], "start")
        self.assertEqual(answer["formula"]["name"], "Rose")

    def test_a_run_doses_every_ingredient_within_tolerance(self):
        model, _ = build_pattern(SIM / "models/minihannover_rail_scene.xml", "p01")
        data = mujoco.MjData(model)
        mujoco.mj_forward(model, data)
        formula = F.resolve([{"compound": "Geraniol", "grams": 1.5}, {"compound": "Nerol", "grams": 0.4}],
                            F.bench(model, data, self.catalogue), self.catalogue)
        scene, server = FakeScene(model, data), FakeServer()
        before = {v["sampleId"]: v["volumeMl"] for v in F.bench(model, data, self.catalogue)}
        run = F.FormulationRun(scene, formula, server, self.catalogue, "RUN-T", speed=60, seed=3)
        run.start()
        self.assertTrue(scene.finished.wait(120))
        self.assertEqual(run.status, "completed", server.events)
        self.assertTrue(run.summary["passed"])
        for dose in run.doses:
            self.assertLessEqual(abs(dose.dispensed - dose.target), F.TOLERANCE_G)
        self.assertAlmostEqual(run.beaker.mass, sum(d.dispensed for d in run.doses), places=6)
        # The liquid came out of the flasks the formula named.
        after = {v["sampleId"]: v["volumeMl"] for v in F.bench(model, data, self.catalogue)}
        drawn = sum(before[s] - after[s] for s in before)
        self.assertAlmostEqual(drawn * F.DENSITY, run.beaker.mass, delta=0.02)
        self.assertTrue(server.samples)
        self.assertEqual(server.patches[-1]["run"]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
