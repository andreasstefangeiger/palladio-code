"""Book IV (temples and churches) against the proportion theory of Book I.

Question: does Palladio give sacred buildings a proportion theory of their own, or does the
theory of Book I hold for them as well? Three scan-checked inputs answer it:

- data/book4/text_statements.json: every statement on proportion in Book IV (Proemio,
  chapters I–V and the temple chapters), plus the Book I and III passages they relate to;
- data/book4/matrix.json: each topic of Book I set against what Book IV says about it;
- data/book4/plate_readings.json: cella dimensions read from the temple plans.

The plate test asks whether the ancient temples, as Palladio drew and measured them, follow
the seven room forms of Book I ch. XXI, against the same null model as Book II.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from .nullmodel import PALLADIO_I21, binomial_upper_tail, continuous_share

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/book4"
VITRUVIAN_CELLA = 5 / 4  # Book IV ch. V: cella 5 of 8 parts of a temple twice as long as wide


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def rule_ids() -> set[str]:
    return {r["rule_id"] for r in json.loads((ROOT / "data/pilot_rules.json").read_text(encoding="utf-8"))}


def validate(statements: dict, matrix: dict) -> list[str]:
    """Problems that would make the comparison untrustworthy; empty when all is well."""
    problems = []
    ids = [st["id"] for st in statements["statements"]]
    if len(ids) != len(set(ids)):
        problems.append("duplicate statement ids")
    for st in statements["statements"]:
        if not st.get("scan_checked"):
            problems.append(f"{st['id']}: not scan-checked")
        if st["kind"] not in statements["kind_vocabulary"]:
            problems.append(f"{st['id']}: unknown kind {st['kind']}")
        if st["relation_book1"] not in statements["relation_vocabulary"]:
            problems.append(f"{st['id']}: unknown relation {st['relation_book1']}")
    known = set(ids) | rule_ids()
    for row in matrix["rows"]:
        for ref in row["book1"] + row["book3"] + row["book4"]:
            if ref not in known:
                problems.append(f"matrix '{row['topic']}': unknown reference {ref}")
    return problems


def nearest_form(ratio: float) -> tuple[str, float]:
    target = min(PALLADIO_I21, key=lambda t: abs(ratio - t.value) / t.value)
    return target.label, (ratio - target.value) / target.value


def summarize_text(statements: dict) -> dict:
    sts = statements["statements"]
    back = [st for st in sts if st["kind"] == "back_reference"]
    return {
        "statements": len(sts),
        "by_kind": dict(Counter(st["kind"] for st in sts)),
        "by_relation": dict(Counter(st["relation_book1"] for st in sts)),
        "back_references": [{"id": st["id"], "to": st["relation_book1"], "topic": st["topic"]} for st in back],
        "back_reference_topics": sorted({st["topic"] for st in back}),
        "refers_to_room_forms_or_heights": any(st["topic"] in {"temple_plan", "heights"} for st in back),
        "outside_seven_forms": [st["id"] for st in sts if st["relation_book1"] == "outside_seven_forms"],
        "vitruvius_named": [st["id"] for st in sts if st["relation_book1"] == "vitruvius"],
    }


def analyze_plates(plates: dict) -> dict:
    rows = []
    for r in plates["readings"]:
        ratio = max(r["width_ft"], r["length_ft"]) / min(r["width_ft"], r["length_ft"])
        label, dev = nearest_form(ratio)
        rows.append({"id": r["id"], "building": r["building"], "printed_page": r["printed_page"],
                     "width_ft": round(r["width_ft"], 3), "length_ft": round(r["length_ft"], 3),
                     "ratio": round(ratio, 4), "nearest": label, "deviation": round(dev, 4),
                     "deviation_from_5_4": round((ratio - VITRUVIAN_CELLA) / VITRUVIAN_CELLA, 4),
                     "confidence": r["confidence"]})
    n = len(rows)
    tests = {}
    for tol in (1, 2):
        hits = sum(1 for row in rows if abs(row["deviation"]) <= tol / 100)
        chance = continuous_share(PALLADIO_I21, tol)
        tests[f"{tol}%"] = {"hits": hits, "n": n, "chance": round(chance, 4),
                            "p_at_least": round(binomial_upper_tail(hits, n, chance), 4)}
    return {
        "readings": rows,
        "seven_forms": tests,
        "within_2_percent_of_5_4": [row["id"] for row in rows if abs(row["deviation_from_5_4"]) <= 0.02],
        "excluded": len(plates["excluded"]),
    }


def matrix_markdown(matrix: dict) -> str:
    lines = ["| Thema | Buch I | Buch III/IV | Befund | Klasse |", "|---|---|---|---|---|"]
    for row in matrix["rows"]:
        b1 = ", ".join(row["book1"]) or "–"
        b34 = ", ".join(row["book3"] + row["book4"]) or "–"
        lines.append(f"| {row['topic']} | {b1} | {b34} | {row['relation']} | {row['evidence']} |")
    return "\n".join(lines)


def run(out_dir: Path) -> dict:
    statements, matrix, plates = load("text_statements.json"), load("matrix.json"), load("plate_readings.json")
    problems = validate(statements, matrix)
    if problems:
        raise ValueError("; ".join(problems))
    result = {"text": summarize_text(statements), "plates": analyze_plates(plates)}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "matrix.md").write_text(matrix_markdown(matrix) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Book IV against the proportion theory of Book I")
    parser.add_argument("--out", type=Path, default=ROOT / "output/book4")
    args = parser.parse_args()
    result = run(args.out)
    text, plates = result["text"], result["plates"]
    print(f"{text['statements']} statements; back references to: {', '.join(text['back_reference_topics'])}; "
          f"room forms or heights referenced: {text['refers_to_room_forms_or_heights']}")
    for tol, t in plates["seven_forms"].items():
        print(f"temple cellas within {tol} of a Book I form: {t['hits']}/{t['n']} "
              f"(chance {t['chance']:.0%}, p = {t['p_at_least']:.3f})")
    print(f"cellas within 2% of Vitruvius' 5:4: {len(plates['within_2_percent_of_5_4'])}")


if __name__ == "__main__":
    main()
