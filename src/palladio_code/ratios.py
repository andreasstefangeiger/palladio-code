from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class RatioTarget:
    label: str
    value: float
    origin: str


DEFAULT_TARGETS = (
    RatioTarget("1:1", 1.0, "Palladio I.21"),
    RatioTarget("sqrt(2):1", sqrt(2), "Palladio I.21"),
    RatioTarget("4:3", 4 / 3, "Palladio I.21"),
    RatioTarget("3:2", 3 / 2, "Palladio I.21"),
    RatioTarget("5:3", 5 / 3, "Palladio I.21"),
    RatioTarget("2:1", 2.0, "Palladio I.21"),
    RatioTarget("5:4", 5 / 4, "exploratory"),
    RatioTarget("6:5", 6 / 5, "exploratory"),
)


def normalized_ratio(a: float, b: float) -> float:
    """Return the larger-to-smaller ratio without silently choosing an axis."""
    if a <= 0 or b <= 0:
        raise ValueError("ratio inputs must be positive")
    return max(a, b) / min(a, b)


def deviation_percent(measured: float, target: float) -> float:
    if measured <= 0 or target <= 0:
        raise ValueError("ratios must be positive")
    return abs(measured - target) / target * 100.0


def rank_targets(measured: float, targets=DEFAULT_TARGETS) -> list[dict]:
    ranked = [
        {
            "label": item.label,
            "target": item.value,
            "origin": item.origin,
            "deviation_percent": deviation_percent(measured, item.value),
        }
        for item in targets
    ]
    return sorted(ranked, key=lambda item: item["deviation_percent"])

