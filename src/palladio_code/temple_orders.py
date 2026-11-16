"""The orders of the temples in Book IV against the measures of Book I.

Input is data/book4/orders.json: what Palladio himself writes about each temple (order, aspect,
column spacing, column length, entablature, base, pedestal), read from the scan of 1570. The
numbers on the plates are not used. The norms are rules of the catalogue (Book I, ch. XIII–XVIII).

Raw statement, norm and reading stay apart: the module reports the stated value, the norm of
the named order and the difference. It does not decide whether a difference was intended.

    python -m palladio_code.temple_orders
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/book4/orders.json"


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def catalogue_ids() -> set[str]:
    return {r["id"] for path in (ROOT / "data/rules").glob("book*.json")
            for r in json.loads(path.read_text(encoding="utf-8"))["rules"]}


def validate(data: dict) -> list[str]:
    problems, known = [], catalogue_ids()
    ids = [s["id"] for s in data["statements"]]
    if len(ids) != len(set(ids)):
        problems.append("duplicate statement ids")
    for s in data["statements"]:
        if not s.get("scan_checked"):
            problems.append(f"{s['id']}: not scan-checked")
        if s["chapter"] not in data["buildings"]:
            problems.append(f"{s['id']}: chapter {s['chapter']} has no building name")
        order = s["features"].get("order")
        if order and order not in data["norms"]:
            problems.append(f"{s['id']}: unknown order {order}")
        maniera = s["features"].get("maniera")
        if maniera and maniera not in data["maniere"]:
            problems.append(f"{s['id']}: unknown maniera {maniera}")
    refs = [r for norm in data["norms"].values() for r in norm["rules"]]
    refs += data["maniere"]["rules"] + [data["column_height_by_spacing"]["rule"]]
    problems += [f"norm cites unknown rule {r}" for r in refs if r not in known]
    return problems


def profiles(data: dict) -> list[dict]:
    """One row per temple: the features of all its statements, each with the statement that carries it."""
    rows = {}
    for s in data["statements"]:
        row = rows.setdefault(s["chapter"], {"chapter": s["chapter"], "building": data["buildings"][s["chapter"]],
                                             "features": {}, "sources": {}})
        for key, value in s["features"].items():
            row["features"].setdefault(key, value)
            row["sources"].setdefault(key, s["id"])
    for row in rows.values():
        f = row["features"]
        if "column_length_ft" in f:  # Tempio della Pace: Palladio gives feet, not diameters
            f["column_D"] = round(f["column_length_ft"] / f["column_diameter_ft"], 2)
            f["entablature"] = round(f["entablature_ft"] / f["column_length_ft"], 4)
            row["sources"]["column_D"] = row["sources"]["entablature"] = row["sources"]["column_length_ft"]
    return list(rows.values())


def spacing(features: dict, maniere: dict) -> tuple[float | None, str]:
    """Column spacing in diameters: the stated number, else the number of the named manner."""
    if "intercol_D" in features:
        return features["intercol_D"], "stated"
    if "intercol_D_range" in features:
        lo, hi = features["intercol_D_range"]
        return (hi, "below") if lo is None else ((lo + hi) / 2, "range")
    if "maniera" in features:
        return maniere[features["maniera"]], "maniera"
    return None, ""


def spacing_label(s: dict) -> str:
    if s["how"] == "below":
        return f"< {s['range'][1]:g}"
    if s["how"] == "range":
        return f"{s['range'][0]:g}–{s['range'][1]:g}"
    return f"{s['stated']:g}"


def compare(data: dict) -> dict:
    norms, maniere = data["norms"], data["maniere"]
    rows = profiles(data)
    entablature, spacings, columns, bases = [], [], [], []
    for row in rows:
        f, order = row["features"], row["features"].get("order")
        norm = norms.get(order, {})
        if "entablature" in f:
            target = norm.get("entablature")
            entablature.append({"chapter": row["chapter"], "building": row["building"], "order": order,
                                "stated": f["entablature"], "note": f.get("entablature_note", ""),
                                "norm": target,
                                "deviation": round(f["entablature"] / target - 1, 3) if target else None,
                                "source": row["sources"]["entablature"]})
        value, how = spacing(f, maniere)
        if value is not None:
            target = norm.get("intercol_D")
            spacings.append({"chapter": row["chapter"], "building": row["building"], "order": order,
                             "stated": value, "how": how, "range": f.get("intercol_D_range"),
                             "maniera": f.get("maniera"), "norm": target,
                             "relation": None if target is None else
                             ("enger" if how == "below" or value < target - 1e-9 else
                              "gleich" if abs(value - target) < 1e-9 else "weiter")})
        if "column_D" in f:
            target = norm.get("column_D")
            by_spacing = data["column_height_by_spacing"].get(str(value).rstrip("0").rstrip(".")) if value else None
            columns.append({"chapter": row["chapter"], "building": row["building"], "order": order,
                            "stated": f["column_D"], "norm": target,
                            "deviation": round(f["column_D"] / target - 1, 3) if isinstance(target, (int, float)) else None,
                            "norm_by_spacing": by_spacing, "source": row["sources"]["column_D"]})
        if "base" in f:
            bases.append({"chapter": row["chapter"], "building": row["building"], "order": order,
                          "base": f["base"], "note": f.get("base_note", ""), "norm": norm.get("base")})
    corinthian_ent = [e for e in entablature if e["order"] == "Corinthio"]
    corinthian_sp = [s for s in spacings if s["order"] == "Corinthio"]
    return {
        "temples": rows,
        "entablature": entablature,
        "spacing": spacings,
        "columns": columns,
        "bases": bases,
        "summary": {
            "temples": len(rows),
            "orders": dict(Counter(r["features"].get("order", "nicht genannt") for r in rows)),
            "corinthian_entablature": dict(Counter(str(e["stated"]) for e in corinthian_ent)),
            "corinthian_entablature_at_norm": sum(1 for e in corinthian_ent if abs(e["deviation"]) <= 0.05),
            "corinthian_entablature_n": len(corinthian_ent),
            "corinthian_spacing": dict(Counter(s["relation"] for s in corinthian_sp)),
            "corinthian_spacing_n": len(corinthian_sp),
            "all_spacing_values": dict(Counter(spacing_label(s) for s in spacings)),
            "spacing_n": len(spacings),
            "bases": dict(Counter(b["base"] for b in bases)),
        },
    }


def markdown(result: dict) -> str:
    def cell(v):
        return "–" if v in (None, "") else str(v)
    lines = ["| Kap. | Tempel | Ordnung | Säulenabstand (D) | Säule (D) | Gebälk | Basis |",
             "|---|---|---|---|---|---|---|"]
    sp = {s["chapter"]: s for s in result["spacing"]}
    for row in result["temples"]:
        f = row["features"]
        s = sp.get(row["chapter"])
        gap = "–" if not s else (f"{s['stated']:g} ({s['maniera']})" if s["how"] == "maniera" else spacing_label(s))
        lines.append(f"| {row['chapter']} | {row['building']} | {cell(f.get('order'))} | {gap} | "
                     f"{cell(f.get('column_D'))} | {cell(f.get('entablature'))} | {cell(f.get('base'))} |")
    return "\n".join(lines)


def run(out_dir: Path) -> dict:
    data = load()
    problems = validate(data)
    if problems:
        raise ValueError("; ".join(problems))
    result = compare(data)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "orders.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "orders.md").write_text(markdown(result) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Orders of the temples in Book IV against Book I")
    parser.add_argument("--out", type=Path, default=ROOT / "output/book4")
    result = run(parser.parse_args().out)
    print(markdown(result))
    s = result["summary"]
    print(f"\n{s['temples']} temples; orders: {s['orders']}")
    print(f"Corinthian entablature: {s['corinthian_entablature']} "
          f"({s['corinthian_entablature_at_norm']}/{s['corinthian_entablature_n']} within 5 % of 1/5)")
    print(f"Corinthian spacing against 2 D: {s['corinthian_spacing']} (n = {s['corinthian_spacing_n']})")
    for c in result["columns"]:
        print(f"column {c['building']}: {c['stated']} D, norm {c['norm']} D, by spacing {c['norm_by_spacing']} D")
    print(f"bases: {s['bases']}")


if __name__ == "__main__":
    main()
