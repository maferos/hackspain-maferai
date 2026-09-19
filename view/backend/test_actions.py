"""The bridge from the live bench to harness/formula_to_actions."""
import unittest

import actions as act
from catalogue import Catalogue, shelf_from_tracks
from formula_chat import FormulaChat
from test_scan_state import track
from workflow import Workflow


class LabelsTest(unittest.TestCase):
    def test_a_shelf_becomes_the_entries_resolve_reads(self):
        shelf = [{"sampleId": "SMP-0014", "x": -1.2, "y": -0.3, "containerMl": 50.0}]
        entry = act.labels(shelf)[0]
        self.assertEqual(entry["sample_id"], "SMP-0014")
        self.assertEqual(entry["position"], [-1.2, -0.3, act.LABEL_Z])
        self.assertEqual(entry["container_ml"], 50.0)

    def test_every_verb_is_owned_by_a_step_the_executor_reports(self):
        # A verb with no step would never be crossed off, and the panel would
        # show it queued for the whole run.
        from workflow import STEPS
        self.assertEqual(set(act.STEP_OF), set(act.f2a.ORDER))
        self.assertTrue(set(act.STEP_OF.values()) <= set(STEPS["external"]))


class HeapTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = Catalogue()

    def setUp(self):
        self.tracks = [track(1, "named", "SMP-0014", (-1.2, -0.3), ring=13),
                       track(2, "named", "SMP-0039", (-0.8, -0.4), ring=38)]
        self.shelf = lambda: shelf_from_tracks(self.tracks, self.catalogue)
        for sample in ("SMP-0014", "SMP-0039"):
            self.catalogue.levels.set_ml(sample, self.catalogue.samples[sample]["containerMl"])
        self.chat = FormulaChat(self.catalogue, self.shelf)

    def order(self, text="1.2 g geraniol, 0.5 g nerol"):
        wf = Workflow(self.catalogue, self.shelf, executor="external", order_file=None,
                      scene_name="the test bench")
        return wf.submit(self.chat.reply(text)["formula"], "chat")

    def test_a_chat_formula_plans_against_the_scanned_bench(self):
        heap = self.order().heap
        self.assertIsNotNone(heap)
        self.assertEqual(heap["summary"]["ingredients"], 2)
        self.assertEqual(heap["summary"]["resolved"], 2)
        self.assertEqual(heap["summary"]["missing"], 0)
        # Ten primitives an ingredient, each carrying the step that crosses it off.
        self.assertEqual(len(heap["actions"]), 20)
        self.assertTrue(all(a["step"] for a in heap["actions"]))
        self.assertEqual([a["verb"] for a in heap["actions"][:10]], list(act.f2a.ORDER))

    def test_the_bottles_are_the_ones_the_scan_named(self):
        legs = {l["compound"]: l["sample"] for l in self.order().heap["legs"]}
        self.assertEqual(legs, {"Geraniol": "SMP-0014", "Nerol": "SMP-0039"})

    def test_without_a_scene_nothing_is_called_welded(self):
        # The free joints are a fact about the scene. Not having one is not
        # evidence that every flask is scenery, which would read as a bench the
        # arm cannot touch.
        heap = self.order().heap
        self.assertEqual(heap["summary"]["unliftable"], 0)

    def test_only_the_verbs_with_a_skill_are_executable(self):
        by_verb = {}
        for a in self.order().heap["actions"]:
            by_verb.setdefault(a["verb"], set()).add(a["executable"])
        self.assertEqual(by_verb["pick"], {True})
        self.assertEqual(by_verb["move_to_balance"], {True})
        # Dosing and weighing are shown but not invented: no skill does them.
        self.assertEqual(by_verb["dose"], {False})
        self.assertEqual(by_verb["verify_mass"], {False})

    def test_a_rejected_order_is_never_planned(self):
        order = self.order("1.2 g geraniol, 0.3 g hedione")
        self.assertEqual(order.status, "rejected")
        self.assertIsNone(order.heap)


if __name__ == "__main__":
    unittest.main()
