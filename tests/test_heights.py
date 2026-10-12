import json
import unittest
from pathlib import Path

from palladio_code.heights import (
    arithmetic, candidates, geometric, harmonic, square_partner_test, stated_height_test,
)

ROOT = Path(__file__).resolve().parents[1]


class MeansTests(unittest.TestCase):
    def test_palladio_book_one_examples(self):
        # Book I, ch. XXIII: 12 x 6 -> 9 (first), 9 x 4 -> 6 (second), 12 x 6 -> 8 (third)
        self.assertEqual(arithmetic(12, 6), 9)
        self.assertEqual(geometric(9, 4), 6)
        self.assertEqual(harmonic(12, 6), 8)

    def test_square_rule_only_for_squares(self):
        self.assertIn("I23_square_4_3", candidates(18, 18))
        self.assertNotIn("I23_square_4_3", candidates(30, 18))

    def test_chiericati_equal_heights(self):
        result = square_partner_test("I23_first", 30, 18)
        self.assertEqual(result["method_height"], 24)
        self.assertEqual(result["deviation_percent"], 0)

    def test_exact_stated_height(self):
        result = stated_height_test(21, 26, 16)
        self.assertEqual(result["best_rule"], "I23_first")
        self.assertEqual(result["deviation_percent"], 0)
        self.assertLess(result["chance_share"], 0.2)

    def test_plate_readings_file(self):
        data = json.loads((ROOT / "data/book2/plate_readings.json").read_text(encoding="utf-8"))
        for room in data["rooms"]:
            self.assertIn(room["confidence"], {"high", "medium", "low"})
            if room["length"] is not None:
                self.assertGreaterEqual(room["length"], room["width"])


if __name__ == "__main__":
    unittest.main()
