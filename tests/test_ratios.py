import unittest
from math import sqrt

from palladio_code.ratios import deviation_percent, normalized_ratio, rank_targets


class RatioTests(unittest.TestCase):
    def test_orientation_is_not_privileged(self):
        self.assertEqual(normalized_ratio(3, 4), normalized_ratio(4, 3))
        self.assertAlmostEqual(normalized_ratio(3, 4), 4 / 3)

    def test_deviation(self):
        self.assertAlmostEqual(deviation_percent(1.347, 4 / 3), 1.025, places=3)

    def test_sqrt2_is_available(self):
        ranked = rank_targets(sqrt(2))
        self.assertEqual(ranked[0]["label"], "sqrt(2):1")
        self.assertAlmostEqual(ranked[0]["deviation_percent"], 0.0)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            normalized_ratio(0, 1)


if __name__ == "__main__":
    unittest.main()

