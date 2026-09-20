"""Briefs: the palette a model is given, and what it is allowed to write.

The model is stubbed. What is under test is everything around it — that the
palette is the bench and not the catalogue, that a formula the builder would
refuse never reaches the queue, and that a brief is composed when its turn
comes rather than when it is sent.
"""
import json
import unittest

import brief
from catalogue import Catalogue, shelf_from_tracks
from test_scan_state import track
from workflow import Workflow


class FakeBlock:
    def __init__(self, text):
        self.type, self.text = "text", text


class FakeAnswer:
    def __init__(self, text):
        self.content = [FakeBlock(text)]


class FakeClient:
    """Answers with each canned reply in turn, and remembers the prompts."""

    def __init__(self, *replies):
        self.replies, self.prompts = list(replies), []
        self.messages = self

    def create(self, *, model, max_tokens, messages):
        self.prompts.append(messages[-1]["content"])
        return FakeAnswer(self.replies.pop(0) if self.replies else "{}")


def spec(*pairs, name="Test Accord", product="Eau de Cologne"):
    return json.dumps({"name": name, "family": "test", "product": product,
                       "description": "d", "ingredients": [list(p) for p in pairs]})


class PaletteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = Catalogue()

    def shelf(self, *samples):
        tracks = [track(i + 1, "named", s, (-1.0 - i * 0.2, -0.3), ring=i)
                  for i, s in enumerate(samples)]
        return shelf_from_tracks(tracks, self.catalogue)

    def test_the_palette_is_the_bench_not_the_catalogue(self):
        import build_formulas as bf
        entries = brief.palette(self.shelf("SMP-0001", "SMP-0006"), bf.load_catalogue())
        self.assertEqual([e["compound"] for e in entries], ["Limonene", "Linalool"])
        # Each carries what a perfumer would need, and what is left to pour.
        self.assertEqual(set(entries[0]), {"compound", "note", "family", "odour",
                                           "grams_left", "ifra_max_pct"})

    def test_the_fullest_flask_speaks_for_a_compound(self):
        import build_formulas as bf
        # Two flasks of Limonene: the palette reports the one with the most in it.
        self.catalogue.levels.set_ml("SMP-0001", 3.0)
        self.catalogue.levels.set_ml("SMP-0005", 44.0)
        entries = brief.palette(self.shelf("SMP-0001", "SMP-0005"), bf.load_catalogue())
        self.assertEqual([e["compound"] for e in entries], ["Limonene"])
        self.assertAlmostEqual(entries[0]["grams_left"], 44.0, places=2)

    def test_a_bare_bench_is_not_composed_on(self):
        with self.assertRaises(ValueError) as caught:
            brief.compose("anything", self.shelf("SMP-0001"), FakeClient())
        self.assertIn("too few", str(caught.exception))


class ComposeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = Catalogue()

    def setUp(self):
        # A bench with tops, a heart and a base, all full.
        self.samples = ["SMP-0001", "SMP-0006", "SMP-0016", "SMP-0106", "SMP-0066", "SMP-0021"]
        for s in self.samples:
            self.catalogue.levels.set_ml(s, self.catalogue.samples[s]["containerMl"])
        tracks = [track(i + 1, "named", s, (-1.0 - i * 0.2, -0.3), ring=i)
                  for i, s in enumerate(self.samples)]
        self.shelf = shelf_from_tracks(tracks, self.catalogue)

    def test_a_good_spec_becomes_a_harness_formula(self):
        client = FakeClient(spec(("Limonene", 60.0), ("Linalool", 40.0)))
        out = brief.compose("fresh", self.shelf, client, formula_id="ORD-009")
        self.assertEqual(out["id"], "ORD-009")
        self.assertEqual([i["material"] for i in out["ingredients"]], ["Limonene", "Linalool"])
        # The builder's fields, which the model was never asked for.
        self.assertEqual(out["ingredients"][0]["note"], "top")
        self.assertEqual(out["ingredients"][0]["batch_g"], 6.0)
        self.assertIn("samples", out["ingredients"][0])

    def test_the_palette_reaches_the_model(self):
        client = FakeClient(spec(("Limonene", 100.0)))
        brief.compose("fresh", self.shelf, client)
        prompt = client.prompts[0]
        self.assertIn("Limonene", prompt)
        self.assertIn("fresh", prompt)
        # A compound that is not on this bench is not offered.
        self.assertNotIn("Nerolidol", prompt)

    def test_percentages_that_miss_100_are_sent_back(self):
        client = FakeClient(spec(("Limonene", 50.0)),                    # sums to 50
                            spec(("Limonene", 60.0), ("Linalool", 40.0)))
        out = brief.compose("fresh", self.shelf, client)
        self.assertEqual(len(client.prompts), 2)
        self.assertIn("100", client.prompts[1])
        self.assertEqual(round(sum(i["concentrate_pct"] for i in out["ingredients"])), 100)

    def test_a_compound_off_the_bench_is_sent_back(self):
        client = FakeClient(spec(("Nerolidol", 100.0)),
                            spec(("Limonene", 100.0)))
        brief.compose("fresh", self.shelf, client)
        self.assertIn("Nerolidol", client.prompts[1])

    def test_more_than_the_flask_holds_is_sent_back(self):
        self.catalogue.levels.set_ml("SMP-0001", 0.5)       # 0.5 g of Limonene left
        shelf = shelf_from_tracks(
            [track(i + 1, "named", s, (-1.0 - i * 0.2, -0.3), ring=i)
             for i, s in enumerate(self.samples)], self.catalogue)
        client = FakeClient(spec(("Limonene", 100.0)),      # 10 g, and 0.5 g is there
                            spec(("Linalool", 100.0)))
        out = brief.compose("fresh", shelf, client)
        self.assertIn("only 0.500 g is left", client.prompts[1])
        self.assertEqual(out["ingredients"][0]["material"], "Linalool")

    def test_a_model_that_never_gets_it_right_fails_loudly(self):
        client = FakeClient(*[spec(("Limonene", 50.0))] * brief.ATTEMPTS)
        with self.assertRaises(ValueError):
            brief.compose("fresh", self.shelf, client)


class QueueTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalogue = Catalogue()

    def setUp(self):
        self.samples = ["SMP-0001", "SMP-0006", "SMP-0016", "SMP-0106", "SMP-0066", "SMP-0021"]
        for s in self.samples:
            self.catalogue.levels.set_ml(s, self.catalogue.samples[s]["containerMl"])
        self.tracks = []
        self.shelf = lambda: shelf_from_tracks(self.tracks, self.catalogue)

    def fill(self):
        self.tracks = [track(i + 1, "named", s, (-1.0 - i * 0.2, -0.3), ring=i)
                       for i, s in enumerate(self.samples)]

    def test_a_brief_waits_for_the_scan_and_is_composed_on_the_whole_bench(self):
        client = FakeClient(spec(("Limonene", 60.0), ("Linalool", 40.0), name="Summer Rind"))
        wf = Workflow(self.catalogue, self.shelf, executor="external", order_file=None,
                      scan_done=lambda: False, client=client)
        order = wf.submit_brief("something fresh and citrusy", "chat")
        # The bench is still being read, so nothing was asked of the model.
        self.assertEqual(order.status, "queued")
        self.assertIsNone(order.composed)
        self.assertEqual(client.prompts, [])

        self.fill()                                     # the scan finishes
        wf.scan_done = lambda: True
        wf.pump()
        self.assertEqual(order.composed["name"], "Summer Rind")
        self.assertTrue(order.check["passed"])
        self.assertEqual([i["compound"] for i in order.items], ["Limonene", "Linalool"])
        # And the palette it was composed on was the finished bench.
        self.assertIn("Linalool", client.prompts[0])

    def test_a_brief_the_model_cannot_write_is_rejected_not_lost(self):
        wf = Workflow(self.catalogue, self.shelf, executor="external", order_file=None,
                      client=FakeClient(*["nonsense"] * brief.ATTEMPTS))
        self.fill()
        order = wf.submit_brief("something impossible", "chat")
        self.assertEqual(order.status, "rejected")
        self.assertFalse(order.check["passed"])

    def test_without_a_key_a_brief_says_so(self):
        wf = Workflow(self.catalogue, self.shelf, executor="external", order_file=None, client=None)
        self.fill()
        order = wf.submit_brief("something fresh", "chat")
        self.assertEqual(order.status, "rejected")
        self.assertIn("ANTHROPIC_API_KEY", order.check["problems"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
