"""Palladio's milieu: which ideas about the world the sources around him state, and which of them recur in Palladio.

data/umfeld/sources.json lists four freely digitised works of the milieu (Trissino, Barbaro's Vitruvius,
Giorgi, Pacioli). data/umfeld/passages.json holds passages read on the page images (wording: class A) and
tags them with motifs (interpretation: class D). Each motif names the catalogue rules in which Palladio
states the same idea, or none.

The module checks the data and writes a motif-by-source matrix:

    python -m palladio_code.umfeld

Output: output/umfeld/matrix.json and output/umfeld/matrix.md.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/umfeld"
OUT = ROOT / "output/umfeld"
REQUIRED = ("id", "source", "locator", "leaf", "quote", "de", "motifs", "scan_checked")


def load() -> tuple[dict, dict]:
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    passages = json.loads((DATA / "passages.json").read_text(encoding="utf-8"))
    return sources, passages


def catalogue_ids() -> set[str]:
    return {r["id"] for path in (ROOT / "data/rules").glob("book*.json")
            for r in json.loads(path.read_text(encoding="utf-8"))["rules"]}


def validate(sources: dict, passages: dict) -> list[str]:
    """Known sources and motifs, existing catalogue rules, unique ids, every quote read on the scan."""
    problems = []
    source_ids = {s["id"] for s in sources["sources"]}
    motifs = passages["motifs"]
    rules = catalogue_ids()
    for key, motif in motifs.items():
        for rule in motif["palladio"]:
            if rule not in rules:
                problems.append(f"motif {key}: unknown rule {rule}")
    seen = set()
    for p in passages["passages"]:
        missing = [f for f in REQUIRED if f not in p]
        if missing:
            problems.append(f"{p.get('id')}: missing {missing}")
            continue
        if p["id"] in seen:
            problems.append(f"{p['id']}: duplicate id")
        seen.add(p["id"])
        if p["source"] not in source_ids:
            problems.append(f"{p['id']}: unknown source {p['source']}")
        if not p["scan_checked"]:
            problems.append(f"{p['id']}: quote not checked on the scan")
        for m in p["motifs"]:
            if m not in motifs:
                problems.append(f"{p['id']}: unknown motif {m}")
    return problems


def matrix(sources: dict, passages: dict) -> dict:
    """For each motif: passages per source, and whether Palladio states it (catalogue rules)."""
    order = [s["id"] for s in sources["sources"]]
    rows = []
    for key, motif in passages["motifs"].items():
        hits = {sid: [p["id"] for p in passages["passages"] if p["source"] == sid and key in p["motifs"]]
                for sid in order}
        rows.append({"motif": key, "label": motif["label"], "sources": hits,
                     "in_milieu": sum(1 for v in hits.values() if v),
                     "palladio": motif["palladio"], "in_palladio": bool(motif["palladio"])})
    return {"sources": order, "rows": rows,
            "shared": [r["motif"] for r in rows if r["in_milieu"] and r["in_palladio"]],
            "milieu_only": [r["motif"] for r in rows if r["in_milieu"] and not r["in_palladio"]]}


def markdown(m: dict) -> str:
    head = "| Motiv | " + " | ".join(m["sources"]) + " | Palladio |"
    lines = [head, "|" + "---|" * (len(m["sources"]) + 2)]
    for r in m["rows"]:
        cells = [", ".join(r["sources"][s]) or "–" for s in m["sources"]]
        lines.append(f"| {r['label']} | " + " | ".join(cells) + f" | {', '.join(r['palladio']) or '–'} |")
    return "\n".join(lines) + "\n"


def run() -> dict:
    sources, passages = load()
    problems = validate(sources, passages)
    if problems:
        raise SystemExit("\n".join(problems))
    m = matrix(sources, passages)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "matrix.json").write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (OUT / "matrix.md").write_text(markdown(m), encoding="utf-8")
    return m


def main() -> None:
    m = run()
    print("shared with Palladio:", ", ".join(m["shared"]))
    print("milieu only:", ", ".join(m["milieu_only"]))


if __name__ == "__main__":
    main()
