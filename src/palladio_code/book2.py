"""Summaries of Palladio's own statements on room heights in Book II.

Input is the scan-checked statement file data/book2/text_statements.json. The
summary only counts what Palladio says; checks against plan dimensions follow in
a separate step once the woodcut figures have been read from the scan.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

STORY_REDUCTION = 5 / 6  # Book I ch. XXIII: upper rooms one sixth lower (A-HT-STORY-001)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def facts(data: dict):
    for st in data["statements"]:
        for fact in st["facts"]:
            yield st, fact


def summarize(data: dict) -> dict:
    rule_by_kind: dict[str, Counter] = {}
    for st, fact in facts(data):
        rule = fact.get("rule") or "unspecified"
        if rule.startswith("equal_to:") or rule.startswith("higher_than:"):
            rule = rule.split(":")[0]
        rule_by_kind.setdefault(st["kind"], Counter())[rule] += 1

    buildings = {st["building"] for st in data["statements"]}
    vault_methods = Counter()
    for st, fact in facts(data):
        if fact.get("rule") in {"I23_first", "I23_second", "I23_third", "I23_square_4_3"}:
            vault_methods[fact["rule"]] += 1

    equal_height = [
        {"id": st["id"], "building": st["building"], "room": fact["room"], "rule": fact["rule"]}
        for st, fact in facts(data)
        if (fact.get("rule") or "").startswith("equal_to:")
    ]
    numeric = [
        {"id": st["id"], "building": st["building"], "room": fact["room"],
         "floor": fact.get("floor"), "ceiling": fact.get("ceiling"), "height_ft": fact.get("height_ft")}
        for st, fact in facts(data)
        if fact.get("rule") == "numeric"
    ]
    beyond_book_one = [
        {"id": st["id"], "building": st["building"], "room": fact["room"],
         "height_factor": fact.get("height_factor"), "note": fact.get("note")}
        for st, fact in facts(data)
        if fact.get("rule") == "other"
    ]
    plan_ratios = Counter(fact["plan_ratio"] for _, fact in facts(data) if fact.get("plan_ratio"))

    story_checks = []
    for st in data["statements"]:
        by_floor = {f.get("floor"): f.get("height_ft") for f in st["facts"] if f.get("height_ft")}
        for lower, upper in ((1, 2), (2, 3)):
            if by_floor.get(lower) and by_floor.get(upper):
                story_checks.append({
                    "id": st["id"], "floors": [lower, upper],
                    "heights_ft": [by_floor[lower], by_floor[upper]],
                    "stated_ratio": by_floor[upper] / by_floor[lower],
                    "book_one_rule": STORY_REDUCTION,
                })

    return {
        "statements": len(data["statements"]),
        "facts": sum(1 for _ in facts(data)),
        "buildings": len(buildings),
        "all_scan_checked": all(st.get("scan_checked") for st in data["statements"]),
        "rules_by_kind": {k: dict(v) for k, v in rule_by_kind.items()},
        "vault_methods_named": dict(vault_methods),
        "equal_height_statements": equal_height,
        "numeric_heights": numeric,
        "height_rules_beyond_book_one": beyond_book_one,
        "stated_plan_ratios": dict(plan_ratios),
        "story_reduction_checks": story_checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise Book II height statements")
    parser.add_argument("--statements", type=Path, default=ROOT / "data/book2/text_statements.json")
    parser.add_argument("--output", type=Path, default=ROOT / "output/book2/text_summary.json")
    args = parser.parse_args()
    summary = summarize(load(args.statements))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("statements", "facts", "buildings", "vault_methods_named",
                                              "stated_plan_ratios")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
