import unittest
from fractions import Fraction
from math import sqrt

from palladio_code.nullmodel import (
    GRIDS,
    PALLADIO_I21,
    TARGET_SETS,
    Grid,
    binomial_upper_tail,
    chance_best_of,
    continuous_share,
    match_share,
    near_target_share,
)
from palladio_code.ratios import RatioTarget


class NullModelTests(unittest.TestCase):
    def test_tiny_grid_by_hand(self):
        # Rooms (ratio <= 2): 2x2, 2x3, 2x4, 3x3, 3x4, 3x5, 3x6
        # ratios 1, 3/2, 2, 1, 4/3, 5/3, 2 -- all of them Palladio I.21 ratios
        grid = Grid("tiny", Fraction(2), Fraction(3), Fraction(1), Fraction(2))
        self.assertEqual(len(list(grid.rooms())), 7)
        only_square = (RatioTarget("1:1", 1.0, "test"),)
        self.assertAlmostEqual(match_share(grid, only_square, 0.0), 2 / 7)
        self.assertAlmostEqual(match_share(grid, PALLADIO_I21, 0.0), 1.0)

    def test_irrational_targets_never_match_exactly(self):
        grid = GRIDS["half_feet_8_40_r2"]
        sqrt2 = (RatioTarget("sqrt(2):1", sqrt(2), "test"),)
        self.assertEqual(match_share(grid, sqrt2, 0.0), 0.0)

    def test_share_grows_with_tolerance_and_target_count(self):
        grid = GRIDS["half_feet_10_30_r2"]
        small = match_share(grid, PALLADIO_I21, 1.0)
        self.assertLess(match_share(grid, PALLADIO_I21, 0.5), small)
        self.assertLess(small, match_share(grid, TARGET_SETS["everything_proposed"], 1.0))

    def test_continuous_share_single_target(self):
        target = (RatioTarget("3:2", 1.5, "test"),)
        # window 1.5 * [0.98, 1.02] has width 0.06 on an interval of length 1
        self.assertAlmostEqual(continuous_share(target, 2.0), 0.06)

    def test_continuous_share_merges_overlaps(self):
        targets = (RatioTarget("a", 1.5, "t"), RatioTarget("b", 1.5, "t"))
        self.assertAlmostEqual(continuous_share(targets, 2.0), 0.06)

    def test_near_target_counts_are_consistent(self):
        result = near_target_share(GRIDS["half_feet_8_40_r2"], sqrt(3), 2.0, 0.07)
        self.assertGreater(result["rooms_in_band"], 0)
        self.assertLessEqual(result["rooms_close"], result["rooms_in_band"])

    def test_probability_helpers(self):
        self.assertAlmostEqual(chance_best_of(1, 0.3), 0.3)
        self.assertAlmostEqual(chance_best_of(2, 0.5), 0.75)
        self.assertAlmostEqual(binomial_upper_tail(0, 10, 0.2), 1.0)
        self.assertAlmostEqual(binomial_upper_tail(2, 2, 0.5), 0.25)


if __name__ == "__main__":
    unittest.main()
