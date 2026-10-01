"""Whole-book analysis of the room dimensions read from the Book II woodcuts.

1. How many rooms have exactly one of the Book I, ch. XXI ratios, compared with
   the null model (docs/07)?
2. Equal vault heights: in every building with a square room of width w and an
   oblong room of the same width, does one of the three means of the oblong room
   give (nearly) the square room's height 4/3 w? Which mean, and for which ratio?
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

from .heights import METHODS, rel_dev, square_rule
from .nullmodel import GRIDS, PALLADIO_I21, match_share
from .nullmodel import binomial_upper_tail

ROOT = Path(__file__).resolve().parents[2]
TOLERANCE = 0.01  # 1 % for "nearly equal" heights


def load_rooms(path: Path, min_confidence: str = "medium") -> list[dict]:
    order = {"low": 0, "medium": 1, "high": 2}
    data = json.loads(path.read_text(encoding="utf-8"))
    seen, rooms = set(), []
    for room in data["rooms"]:
        if room["length"] is None or order[room["confidence"]] < order[min_confidence]:
            continue
        key = (room["building"], room["length"], room["width"])
        if key in seen:  # symmetric duplicates and repeated readings count once
            continue
        seen.add(key)
        rooms.append(room)
    return rooms


def exact_label(length: float, width: float) -> str | None:
    ratio = Fraction(length).limit_denominator(8) / Fraction(width).limit_denominator(8)
    for target in PALLADIO_I21:
        if abs(float(ratio) - target.value) < 1e-9:
            return target.label
    return None


def ratio_census(rooms: list[dict]) -> dict:
    labels = Counter()
    exact = 0
    for room in rooms:
        label = exact_label(room["length"], room["width"])
        labels[label or "other"] += 1
        exact += label is not None
    n = len(rooms)
    null_half = match_share(GRIDS["half_feet_8_40_r2"], PALLADIO_I21, 0.0)
    null_whole = match_share(GRIDS["whole_feet_8_40_r2"], PALLADIO_I21, 0.0)
    return {
        "rooms": n,
        "exact_I21": exact,
        "share": exact / n,
        "by_ratio": dict(labels),
        "null_share_half_feet": null_half,
        "null_share_whole_feet": null_whole,
        "p_value_half_feet": binomial_upper_tail(exact, n, null_half),
        "p_value_whole_feet": binomial_upper_tail(exact, n, null_whole),
    }


def square_partners(rooms: list[dict]) -> list[dict]:
    by_building: dict[str, list[dict]] = {}
    for room in rooms:
        by_building.setdefault(room["building"], []).append(room)
    rows = []
    for building, items in by_building.items():
        squares = {r["width"] for r in items if r["length"] == r["width"]}
        for room in items:
            if room["length"] == room["width"] or room["width"] not in squares:
                continue
            target = square_rule(room["width"])
            devs = {m: rel_dev(f(room["length"], room["width"]), target) for m, f in METHODS.items()}
            best = min(devs, key=devs.get)
            rows.append({
                "building": building,
                "room": f"{room['length']} x {room['width']}",
                "ratio": round(room["length"] / room["width"], 4),
                "square_height": round(target, 3),
                "deviation_percent": {m: round(v * 100, 2) for m, v in devs.items()},
                "best_mean": best,
                "matches_within_1_percent": devs[best] <= TOLERANCE,
            })
    return rows


def run(readings: Path, output: Path) -> dict:
    rooms = load_rooms(readings)
    partners = square_partners(rooms)
    result = {
        "ratio_census": ratio_census(rooms),
        "square_partner_pairs": partners,
        "square_partner_summary": {
            "pairs": len(partners),
            "within_1_percent": sum(p["matches_within_1_percent"] for p in partners),
            "best_mean_counts": dict(Counter(p["best_mean"] for p in partners if p["matches_within_1_percent"])),
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Whole-book room analysis for Book II")
    parser.add_argument("--readings", type=Path, default=ROOT / "data/book2/plate_readings.json")
    parser.add_argument("--output", type=Path, default=ROOT / "output/book2/room_analysis.json")
    args = parser.parse_args()
    result = run(args.readings, args.output)
    print(json.dumps(result["ratio_census"], indent=2))
    for row in result["square_partner_pairs"]:
        print(f"{row['building'][:34]:34s} {row['room']:12s} r={row['ratio']:<6} best={row['best_mean']:10s}"
              f" dev={row['deviation_percent'][row['best_mean']]:5}%  {'MATCH' if row['matches_within_1_percent'] else ''}")
    print(result["square_partner_summary"])


if __name__ == "__main__":
    main()
