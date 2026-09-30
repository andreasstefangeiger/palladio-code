"""Test Palladio's Book II height statements against the woodcut dimensions.

Two questions, each with its own chance baseline:

1. Stated heights in feet: which of the Book I, ch. XXIII rules produces the
   stated height from the printed room dimensions, and how often would an
   arbitrary height on a half-foot grid between width and length come that close?
2. Equal vault heights (Book I, ch. XXIII: "piu stanze di diverse grandezze
   habbiano i uolti egualmente alti"): where Palladio names the method for an
   oblong room next to a square room, how close is the resulting height to the
   square room's height (width + 1/3), and how often would an arbitrary length on a
   half-foot grid come that close?
"""
from __future__ import annotations

import argparse
import json
from math import sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STEP = 0.5  # half-foot grid, as in the null model


def arithmetic(length: float, width: float) -> float:
    return (length + width) / 2


def geometric(length: float, width: float) -> float:
    return sqrt(length * width)


def harmonic(length: float, width: float) -> float:
    return 2 * length * width / (length + width)


def square_rule(width: float) -> float:
    return width * 4 / 3


METHODS = {"I23_first": arithmetic, "I23_second": geometric, "I23_third": harmonic}


def candidates(length: float, width: float) -> dict[str, float]:
    result = {
        "flat_h_eq_w": width,
        "I23_first": arithmetic(length, width),
        "I23_second": geometric(length, width),
        "I23_third": harmonic(length, width),
    }
    if length == width:
        result["I23_square_4_3"] = square_rule(width)
    return result


def rel_dev(value: float, target: float) -> float:
    return abs(value - target) / target


def grid(lo: float, hi: float, step: float = STEP):
    n = 0
    while lo + n * step <= hi + 1e-9:
        yield lo + n * step
        n += 1


def stated_height_test(height: float, length: float, width: float) -> dict:
    options = candidates(length, width)
    best_rule, best_value = min(options.items(), key=lambda kv: rel_dev(height, kv[1]))
    best = rel_dev(height, best_value)
    # chance: arbitrary heights between width and max(length, 4/3 width)
    hi = max(length, square_rule(width))
    pool = list(grid(width, hi))
    close = sum(1 for h in pool if min(rel_dev(h, v) for v in options.values()) <= best + 1e-12)
    return {
        "candidates": {k: round(v, 3) for k, v in options.items()},
        "best_rule": best_rule,
        "best_value": round(best_value, 3),
        "deviation_percent": round(best * 100, 2),
        "chance_share": round(close / len(pool), 3),
        "chance_pool": f"heights {width}-{hi} ft in {STEP} ft steps ({len(pool)} values)",
    }


def square_partner_test(method: str, length: float, width: float) -> dict:
    value = METHODS[method](length, width)
    target = square_rule(width)
    dev = rel_dev(value, target)
    pool = list(grid(width + STEP, 2 * width))
    close = sum(1 for other in pool if rel_dev(METHODS[method](other, width), target) <= dev + 1e-12)
    return {
        "method_height": round(value, 3),
        "square_room_height": round(target, 3),
        "deviation_percent": round(dev * 100, 2),
        "chance_share": round(close / len(pool), 3),
        "chance_pool": f"lengths {width + STEP}-{2 * width} ft in {STEP} ft steps ({len(pool)} values)",
    }


# Each case links a scan-checked statement (data/book2/text_statements.json)
# to room dimensions read from the woodcut (data/book2/plate_readings.json).
STATED_HEIGHTS = [
    {"id": "B2-MMA-1", "building": "Villa Mocenigo", "room": "stanze maggiori", "height": 21, "length": 26, "width": 16},
    {"id": "B2-MMA-1", "building": "Villa Mocenigo", "room": "camerini", "height": 17, "length": 16, "width": 10},
    {"id": "B2-BAR-1", "building": "Palazzo Barbarano", "room": "stanze 1 1/2 quadro (24 x 16)", "height": 21.5, "length": 24, "width": 16},
    {"id": "B2-BAR-1", "building": "Palazzo Barbarano", "room": "stanze quadre", "height": 21.5, "length": 16, "width": 16},
    {"id": "B2-BAR-1", "building": "Palazzo Barbarano", "room": "left room (24 x 19?, low confidence)", "height": 21.5, "length": 24, "width": 19},
    {"id": "B2-TRV-1", "building": "Palazzo Trissino (inventione)", "room": "stanze maggiori, flat ceiling", "height": 27, "length": 40, "width": 20},
    {"id": "B2-TRV-1", "building": "Palazzo Trissino (inventione)", "room": "stanza mediocre, vaulted", "height": 18, "length": 20, "width": 18},
    {"id": "B2-GAR-1", "building": "Palazzo Garzadore (inventione)", "room": "camerini", "height": 16, "length": 16, "width": 8},
]

SQUARE_PARTNERS = [
    {"id": "B2-CHI-1", "building": "Palazzo Chiericati", "method": "I23_first", "length": 30, "width": 18,
     "text": "mediocri (square 18) as high as the maggiori"},
    {"id": "B2-COR-1", "building": "Villa Cornaro", "method": "I23_first", "length": 26.5, "width": 16,
     "text": "mediocri square, one third higher than wide"},
    {"id": "B2-COR-1", "building": "Villa Cornaro (text ratio 7:4)", "method": "I23_first", "length": 28, "width": 16,
     "text": "as stated in the text instead of the woodcut"},
    {"id": "B2-PMO-1", "building": "Villa Pisani, Montagnana", "method": "I23_second", "length": 28, "width": 16,
     "text": "mediocri square (height not stated)"},
    {"id": "B2-MMA-1", "building": "Villa Mocenigo", "method": "I23_first", "length": 26, "width": 16,
     "text": "mediocri as high as the maggiori"},
    {"id": "B2-INV1-1", "building": "Inventione p. 71", "method": "I23_first", "length": 30, "width": 18,
     "text": "no square room of width 18 named; implied first-floor height"},
]


def run(output: Path) -> dict:
    stated = [{**case, **stated_height_test(case["height"], case["length"], case["width"])} for case in STATED_HEIGHTS]
    partners = [{**case, **square_partner_test(case["method"], case["length"], case["width"])} for case in SQUARE_PARTNERS]
    independent = [p for p in partners if p["building"] in {
        "Palazzo Chiericati", "Villa Cornaro", "Villa Pisani, Montagnana", "Villa Mocenigo"}]
    joint = 1.0
    for p in independent:
        joint *= p["chance_share"]
    result = {
        "stated_heights": stated,
        "square_partners": partners,
        "square_partner_joint_chance": {
            "buildings": [p["building"] for p in independent],
            "product_of_chance_shares": joint,
            "note": "Assumes independent choices of length; a heuristic bound, not a formal test.",
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Test Book II heights against woodcut dimensions")
    parser.add_argument("--output", type=Path, default=ROOT / "output/book2/height_tests.json")
    args = parser.parse_args()
    result = run(args.output)
    for row in result["stated_heights"]:
        print(f"{row['building'][:28]:28s} {row['room'][:34]:34s} h={row['height']:5} best={row['best_rule']:15s}"
              f" {row['best_value']:7} dev={row['deviation_percent']:5}% chance={row['chance_share']}")
    print()
    for row in result["square_partners"]:
        print(f"{row['building'][:30]:30s} {row['method']:10s} {row['length']}x{row['width']}: {row['method_height']}"
              f" vs {row['square_room_height']} dev={row['deviation_percent']}% chance={row['chance_share']}")
    print("joint:", result["square_partner_joint_chance"]["product_of_chance_shares"])


if __name__ == "__main__":
    main()
