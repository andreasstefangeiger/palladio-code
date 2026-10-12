import unittest

from palladio_code.san_giorgio import (check_criteria, dome_checks, facade_checks, feet, load, load_criteria,
                                       readings, rooms, rule_checks)


class SanGiorgioTests(unittest.TestCase):
    def setUp(self):
        self.data = load()
        self.f = feet(self.data)

    def test_scaled_values_agree_with_labels(self):
        for r in self.data["plan_readings"]:
            if r.get("label") and r.get("scaled_feet"):
                self.assertLess(abs(r["scaled_feet"] - r["feet"]) / r["feet"], 0.05, r["id"])

    def test_room_forms(self):
        by_space = {r["space"]: r for r in rooms(self.f)}
        self.assertEqual(by_space["Presbyterium"]["nearest"], "4:3")
        self.assertEqual(by_space["Mittelschiff bis zur Vierung"]["nearest"], "2:1")

    def test_aisles_are_not_one_third(self):
        ratio = self.f["SG-AISLE-W"] / self.f["SG-NAVE-W"]
        self.assertGreater(ratio, 0.45)
        verdicts = [c["verdict"] for c in rule_checks(self.f)]
        self.assertTrue(any(v.startswith("nicht erfüllt") for v in verdicts))

    def test_criteria_cite_known_sources(self):
        self.assertEqual(check_criteria(load_criteria(), self.data), [])

    def test_facade_order_follows_book_one(self):
        fr = readings(self.data, "facade_readings")
        h = fr["SG-F-COL"]
        self.assertLess(abs(h / fr["SG-F-D"] - 10) / 10, 0.05)
        self.assertLess(abs(fr["SG-F-PED"] / h - 1 / 3) * 3, 0.03)
        self.assertLess(abs(fr["SG-F-ENT"] / h - 1 / 5) * 5, 0.02)

    def test_facade_middle_bay_is_twice_the_side_bays(self):
        fr = readings(self.data, "facade_readings")
        self.assertAlmostEqual(fr["SG-F-INT-MID"] / fr["SG-F-INT-SIDE"], 2.0, delta=0.1)
        self.assertEqual(len(facade_checks(fr)), 8)

    def test_dome_is_far_above_four_thirds(self):
        sr = readings(self.data, "section_readings")
        self.assertLess(abs(sr["SG-S-DOME-D"] - self.f["SG-NAVE-W"]) / self.f["SG-NAVE-W"], 0.02)
        self.assertGreater(sr["SG-S-DOME-CROWN"] / self.f["SG-NAVE-W"], 2.5)
        self.assertTrue(dome_checks(sr, self.f)[0]["verdict"].startswith("nicht erfüllt"))


if __name__ == "__main__":
    unittest.main()
