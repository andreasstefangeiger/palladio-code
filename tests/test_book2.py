import json
import unittest
from pathlib import Path

from palladio_code.book2 import summarize
from palladio_code.proofs import locate

ROOT = Path(__file__).resolve().parents[1]


class LocateTests(unittest.TestCase):
    LINES = [
        {"text": "prima riga senza", "x": 10, "y": 100, "w": 300, "h": 20},
        {"text": "Le stanze maggiori hanno", "x": 12, "y": 130, "w": 310, "h": 22},
        {"text": "i uolti alti secondo il", "x": 8, "y": 160, "w": 305, "h": 21},
        {"text": "primo modo . Altro", "x": 11, "y": 190, "w": 200, "h": 20},
    ]

    def test_anchor_crossing_lines(self):
        # "hanno i uolti" spans a line break
        x, y, w, h = locate(self.LINES, "hanno i uolti", "primo modo")
        self.assertEqual((x, y), (8, 130))
        self.assertEqual(y + h, 210)
        self.assertEqual(x + w, 322)

    def test_missing_anchor_raises(self):
        with self.assertRaises(ValueError):
            locate(self.LINES, "non presente", "primo")


class Book2SummaryTests(unittest.TestCase):
    def test_fixture_counts(self):
        data = {"statements": [
            {"id": "X-1", "building": "A", "kind": "own_design", "scan_checked": True, "facts": [
                {"room": "maggiori", "floor": 1, "rule": "I23_first"},
                {"room": "mediocri", "floor": 1, "rule": "equal_to:maggiori"},
            ]},
            {"id": "X-2", "building": "B", "kind": "unexecuted_invention", "scan_checked": True, "facts": [
                {"room": "stanze", "floor": 2, "rule": "numeric", "height_ft": 24},
                {"room": "stanze", "floor": 3, "rule": "numeric", "height_ft": 20, "plan_ratio": "3:2"},
            ]},
        ]}
        s = summarize(data)
        self.assertEqual(s["buildings"], 2)
        self.assertEqual(s["vault_methods_named"], {"I23_first": 1})
        self.assertEqual(len(s["equal_height_statements"]), 1)
        self.assertEqual(s["stated_plan_ratios"], {"3:2": 1})
        self.assertAlmostEqual(s["story_reduction_checks"][0]["stated_ratio"], 20 / 24)
        self.assertTrue(s["all_scan_checked"])

    def test_dataset_is_scan_checked_and_well_formed(self):
        data = json.loads((ROOT / "data/book2/text_statements.json").read_text(encoding="utf-8"))
        ids = [st["id"] for st in data["statements"]]
        self.assertEqual(len(ids), len(set(ids)))
        for st in data["statements"]:
            self.assertTrue(st["scan_checked"], st["id"])
            self.assertTrue(st["quote"].strip(), st["id"])
            self.assertEqual(len(st["anchor"]), 2, st["id"])


if __name__ == "__main__":
    unittest.main()
