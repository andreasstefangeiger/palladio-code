import unittest

from palladio_code.san_giorgio import feet, load, rooms, rule_checks


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


if __name__ == "__main__":
    unittest.main()
