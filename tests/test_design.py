import json
import unittest
from pathlib import Path

from palladio_code.design import nearest_palladio, run_design, to_svg

ROOT = Path(__file__).resolve().parents[1]


def statuses(design, topic):
    return [d.status for d in design.decisions if d.topic == topic]


class DesignTests(unittest.TestCase):
    def test_default_villa_follows_palladio(self):
        d = run_design({})
        dims = [(r.length, r.breadth) for r in d.rooms]
        self.assertEqual(dims, [(26.5, 16), (16, 16), (16, 12)])
        self.assertEqual(statuses(d, "Gleiche Gewoelbehoehe"), ["follows"])
        self.assertEqual(statuses(d, "Raumfolge"), ["follows"])
        self.assertNotIn("deviation", [x.status for x in d.decisions])

    def test_chiericati_is_reproduced(self):
        # Palazzo Chiericati (Book II p. 6): 30 x 18, 18 x 18, 18 x 12; vaults 24 = 24
        d = run_design({"module": 18, "wing": [
            {"form": "5:3", "size": "grande"}, {"form": "1:1", "size": "mediocre"},
            {"form": "3:2", "size": "picciola"}]})
        self.assertEqual([(r.length, r.breadth) for r in d.rooms], [(30, 18), (18, 18), (18, 12)])
        self.assertAlmostEqual(d.rooms[0].height, 24)
        self.assertAlmostEqual(d.rooms[1].height, 24)

    def test_flat_ceiling_height_equals_width(self):
        d = run_design({"ceiling": "flat"})
        self.assertTrue(all(r.height == r.breadth for r in d.rooms))

    def test_unequal_heights_are_reported(self):
        d = run_design({"wing": [{"form": "2:1", "size": "grande"}, {"form": "1:1", "size": "mediocre"}],
                        "module": 16})
        # 2:1 with the harmonic mean also gives 4/3 w: the planner must pick it
        self.assertEqual(d.rooms[0].height_rule, "I23_third")
        self.assertEqual(statuses(d, "Gleiche Gewoelbehoehe"), ["follows"])

    def test_sala_over_two_squares_is_a_deviation(self):
        d = run_design({"sala_width": 20})
        self.assertEqual(statuses(d, "Zentrum"), ["deviation"])

    def test_every_rule_id_exists(self):
        known = {r["rule_id"] for r in json.loads((ROOT / "data/pilot_rules.json").read_text(encoding="utf-8"))}
        known |= {"B2-CAP2-1"}
        d = run_design({})
        for dec in d.decisions:
            for rule in dec.rules:
                self.assertIn(rule, known, rule)

    def test_svg_and_nearest(self):
        d = run_design({})
        self.assertIn("<svg", to_svg(d))
        self.assertTrue(nearest_palladio(d, ROOT / "data/book2/plate_readings.json")["building"])


if __name__ == "__main__":
    unittest.main()
