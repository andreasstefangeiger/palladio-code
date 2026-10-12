import json
import tempfile
import unittest
from pathlib import Path

from palladio_code.rooms import exact_label, load_rooms, square_partners


class RoomsTests(unittest.TestCase):
    def test_exact_labels(self):
        self.assertEqual(exact_label(30, 18), "5:3")
        self.assertEqual(exact_label(16, 16), "1:1")
        self.assertIsNone(exact_label(26.5, 16))

    def test_square_partner_detection(self):
        rooms = [
            {"building": "X", "length": 30, "width": 18},
            {"building": "X", "length": 18, "width": 18},
            {"building": "Y", "length": 24, "width": 16},  # no square of width 16 in Y
        ]
        rows = square_partners(rooms)
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["matches_within_1_percent"])
        self.assertEqual(rows[0]["best_mean"], "I23_first")

    def test_load_rooms_filters_and_deduplicates(self):
        data = {"rooms": [
            {"building": "A", "length": 20, "width": 10, "confidence": "high"},
            {"building": "A", "length": 20, "width": 10, "confidence": "medium"},
            {"building": "A", "length": 19, "width": 10, "confidence": "low"},
            {"building": "A", "length": None, "width": 8, "confidence": "high"},
        ]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "r.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(len(load_rooms(path)), 1)


if __name__ == "__main__":
    unittest.main()
