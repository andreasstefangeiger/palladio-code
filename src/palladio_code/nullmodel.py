"""Chance baselines for proportion claims ("Nullmodell").

How often would a room "match" a target ratio if its dimensions had been chosen
without any proportional intention? The answer depends on the tolerance, on the
number of admissible targets and on the grid of plausible dimensions. This module
enumerates such grids exhaustively (no random numbers), so every figure is exactly
reproducible.

Nothing here is evidence about Palladio. It only states what a claimed match is
worth: a match rate that the null already reaches carries no information.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from math import comb, sqrt
from pathlib import Path

from .ratios import DEFAULT_TARGETS, RatioTarget

ROOT = Path(__file__).resolve().parents[2]

PHI = (1 + sqrt(5)) / 2

PALLADIO_I21 = tuple(t for t in DEFAULT_TARGETS if t.origin == "Palladio I.21")

# Just-intonation intervals within one octave, as listed by Howard/Longair 1982
# (their scales 1 and 2) plus minor third and minor sixth used by Mitrovic 1990.
JUST_OCTAVE = tuple(
    RatioTarget(label, float(Fraction(label.replace(":", "/"))), "just intonation")
    for label in (
        "1:1", "16:15", "10:9", "9:8", "6:5", "5:4", "4:3",
        "3:2", "8:5", "5:3", "15:8", "2:1",
    )
)

# Ratios proposed in the literature beyond Book I, ch. XXI.
LITERATURE_EXTRA = (
    RatioTarget("sqrt(3):1", sqrt(3), "Mitrovic 1990 (triangulature)"),
    RatioTarget("phi:1", PHI, "golden section debate (March/Fletcher 2001)"),
    RatioTarget("7:4", 7 / 4, "Palladio II text (Pisani Montagnana, Cornaro)"),
    RatioTarget("13:8", 13 / 8, "Palladio II text (Saraceno)"),
)


def _merge(*groups: tuple[RatioTarget, ...]) -> tuple[RatioTarget, ...]:
    seen: dict[str, RatioTarget] = {}
    for group in groups:
        for target in group:
            seen.setdefault(target.label, target)
    return tuple(sorted(seen.values(), key=lambda t: t.value))


TARGET_SETS = {
    "palladio_I21": PALLADIO_I21,
    "just_octave": JUST_OCTAVE,
    "I21_plus_just": _merge(PALLADIO_I21, JUST_OCTAVE),
    "everything_proposed": _merge(PALLADIO_I21, JUST_OCTAVE, LITERATURE_EXTRA),
}


@dataclass(frozen=True)
class Grid:
    """Plausible room dimensions in (Vicentine) feet, width <= length."""

    name: str
    min_width: Fraction
    max_width: Fraction
    step: Fraction
    max_ratio: Fraction

    def rooms(self):
        w = self.min_width
        while w <= self.max_width:
            length = w
            while length <= w * self.max_ratio:
                yield w, length
                length += self.step
            w += self.step


GRIDS = {
    "half_feet_8_40_r2": Grid("half_feet_8_40_r2", Fraction(8), Fraction(40), Fraction(1, 2), Fraction(2)),
    "whole_feet_8_40_r2": Grid("whole_feet_8_40_r2", Fraction(8), Fraction(40), Fraction(1), Fraction(2)),
    "half_feet_10_30_r2": Grid("half_feet_10_30_r2", Fraction(10), Fraction(30), Fraction(1, 2), Fraction(2)),
    "half_feet_8_40_r2.5": Grid("half_feet_8_40_r2.5", Fraction(8), Fraction(40), Fraction(1, 2), Fraction(5, 2)),
}

TOLERANCES_PERCENT = (0.0, 0.25, 0.5, 1.0, 2.0, 3.0)

# Floating-point slack for "exact" matches of rational targets on a rational grid.
_EXACT = 1e-9


def relative_deviation(ratio: float, target: float) -> float:
    return abs(ratio - target) / target


def matches(ratio: float, targets, tolerance_percent: float) -> bool:
    limit = max(tolerance_percent / 100.0, _EXACT)
    return any(relative_deviation(ratio, t.value) <= limit for t in targets)


def match_share(grid: Grid, targets, tolerance_percent: float) -> float:
    """Share of all grid rooms whose length/width ratio matches any target."""
    total = hits = 0
    for w, length in grid.rooms():
        total += 1
        hits += matches(float(length / w), targets, tolerance_percent)
    return hits / total


def continuous_share(targets, tolerance_percent: float, max_ratio: float = 2.0) -> float:
    """Analytic share if the ratio were uniform on [1, max_ratio] (overlaps merged)."""
    tol = tolerance_percent / 100.0
    intervals = sorted(
        (max(1.0, t.value * (1 - tol)), min(max_ratio, t.value * (1 + tol)))
        for t in targets
        if t.value <= max_ratio
    )
    covered, current_end = 0.0, 1.0
    for start, end in intervals:
        start = max(start, current_end)
        if end > start:
            covered += end - start
            current_end = end
    return covered / (max_ratio - 1.0)


def near_target_share(grid: Grid, target: float, band_percent: float, within_percent: float) -> dict:
    """Among grid rooms whose ratio lies within +-band of target, the share lying within +-within.

    This is the look-elsewhere question behind claims such as "26:15 is within 0.07%
    of sqrt(3)": given that a room falls near the target at all, how close is close
    by chance?
    """
    in_band = close = 0
    for w, length in grid.rooms():
        dev = relative_deviation(float(length / w), target) * 100
        if dev <= band_percent:
            in_band += 1
            close += dev <= within_percent
    share = close / in_band if in_band else 0.0
    return {"rooms_in_band": in_band, "rooms_close": close, "share_close_given_band": share}


def chance_best_of(n: int, p: float) -> float:
    """Probability that at least one of n independent rooms achieves a p-event."""
    return 1 - (1 - p) ** n


def binomial_upper_tail(k: int, n: int, p: float) -> float:
    """P(X >= k) for X ~ Binomial(n, p), computed exactly."""
    return sum(comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k, n + 1))


def published_claim_checks(grid: Grid) -> list[dict]:
    """Chance baselines for specific published claims (claims quoted, not re-measured)."""
    checks = []

    sqrt3 = near_target_share(grid, sqrt(3), band_percent=2.0, within_percent=0.07)
    checks.append({
        "claim": "Villa Rotonda 26:15 within 0.07% of sqrt(3); six rooms near sqrt(3) in Book II",
        "source": "Mitrovic 1990, JSAH 49, 285-286",
        "question": "Six rooms lie within about 2% of sqrt(3). How likely is it that the best of them is within 0.07%?",
        "share_close_given_band": sqrt3["share_close_given_band"],
        "probability_best_of_6": chance_best_of(6, sqrt3["share_close_given_band"]),
    })

    sqrt2 = near_target_share(grid, sqrt(2), band_percent=2.0, within_percent=0.17)
    checks.append({
        "claim": "Villa Ragona 21 1/4 : 15 within 0.17% of sqrt(2)",
        "source": "Howard/Longair 1982, 135; Mitrovic 1990, 285",
        "question": "For one room near sqrt(2), how likely is a deviation of at most 0.17% on this grid?",
        "share_close_given_band": sqrt2["share_close_given_band"],
        "note": "Palladio's use of a quarter foot here is not captured by a half-foot grid; see quarter-foot run.",
    })

    exact_null = match_share(grid, PALLADIO_I21, 0.0)
    checks.append({
        "claim": "82 of 153 main-room ratios in Book II plans are exactly one of Palladio's I.21 ratios",
        "source": "Howard/Longair 1982, JSAH 41, 135 (their count, not re-measured here)",
        "question": "How likely are 82 or more exact matches among 153 rooms without proportional intention?",
        "null_share_exact": exact_null,
        "expected_by_chance": 153 * exact_null,
        "p_value_at_least_82": binomial_upper_tail(82, 153, exact_null),
        "note": "Treats rooms as independent; symmetric duplicates were already removed by Howard/Longair.",
    })

    for tol in (2.0,):
        checks.append({
            "claim": "93% of 183 Book II room ratios within 2% of the proposed ratios",
            "source": "Tikhonova 2019, Nexus Network Journal 21 (as summarised; full text not read)",
            "question": "Which share would rooms without proportional intention reach at 2% tolerance?",
            "null_share_palladio_I21": match_share(grid, PALLADIO_I21, tol),
            "null_share_I21_plus_just": match_share(grid, TARGET_SETS["I21_plus_just"], tol),
            "null_share_everything_proposed": match_share(grid, TARGET_SETS["everything_proposed"], tol),
            "note": "Tikhonova's own target set (squares and their parts) is larger than I.21; its exact size must be read from the full text.",
        })
    return checks


def run(output_dir: Path) -> dict:
    results = {
        "method": (
            "Exhaustive enumeration of room grids; share of rooms whose length/width ratio "
            "lies within a relative tolerance of any target. No random sampling."
        ),
        "grids": {name: {
            "min_width": float(g.min_width), "max_width": float(g.max_width),
            "step": float(g.step), "max_ratio": float(g.max_ratio),
            "rooms": sum(1 for _ in g.rooms()),
        } for name, g in GRIDS.items()},
        "target_sets": {name: [t.label for t in ts] for name, ts in TARGET_SETS.items()},
        "match_shares": {},
        "continuous_uniform_shares": {},
    }
    for grid_name, grid in GRIDS.items():
        results["match_shares"][grid_name] = {
            set_name: {str(tol): match_share(grid, targets, tol) for tol in TOLERANCES_PERCENT}
            for set_name, targets in TARGET_SETS.items()
        }
    for set_name, targets in TARGET_SETS.items():
        results["continuous_uniform_shares"][set_name] = {
            str(tol): continuous_share(targets, tol) for tol in TOLERANCES_PERCENT if tol > 0
        }
    results["published_claim_checks"] = published_claim_checks(GRIDS["half_feet_8_40_r2"])
    quarter = Grid("quarter_feet_8_40_r2", Fraction(8), Fraction(40), Fraction(1, 4), Fraction(2))
    results["published_claim_checks_quarter_feet"] = published_claim_checks(quarter)[:2]

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "nullmodel_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Chance baselines for proportion claims")
    parser.add_argument("--output", type=Path, default=ROOT / "output" / "nullmodel")
    args = parser.parse_args()
    results = run(args.output)
    grid = "half_feet_8_40_r2"
    print(f"Grid {grid}: {results['grids'][grid]['rooms']} rooms")
    for set_name, row in results["match_shares"][grid].items():
        print(f"  {set_name:22s} " + "  ".join(f"{tol}%: {share:6.1%}" for tol, share in row.items()))


if __name__ == "__main__":
    main()
