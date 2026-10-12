"""Rule catalogue of the whole Quattro Libri.

data/rules/register.json lists every chapter of the four books with its position in the
ALTO OCR; data/rules/book<N>.json holds the rules read from those chapters. The OCR only
locates text: every quotation is read again from the scan crop before it counts (A).

    python -m palladio_code.catalogue status
    python -m palladio_code.catalogue dump 1 XIIII        # chapter text with page/line numbers
    python -m palladio_code.catalogue check               # consistency of register and rule files
"""
from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "data/rules"
ALTO = ROOT / "data/source/erara_ocr_alto.xml"
NS = {"a": "http://www.loc.gov/standards/alto/ns-v3#"}

KINDS = {
    "prescription": "Gebot (si deue, si farà …)",
    "prohibition": "Verbot (non si deue, non si farà …)",
    "range": "Spielraum mit Grenzen (non meno … nè più …)",
    "preference": "Vorzug oder Urteil (meglio, più lodeuole, mi piace …)",
    "procedure": "Konstruktions- oder Arbeitsverfahren",
    "proportion": "Maß- oder Proportionsangabe als Norm",
    "principle": "allgemeiner Grundsatz",
}
ATTRIBUTION = {
    "palladio": "Palladio als eigene Regel",
    "vitruvius": "Palladio gibt Vitruv wieder (genannt)",
    "antichi": "Palladio berichtet die Praxis der Antiken als Vorbild",
    "alberti": "Palladio gibt Alberti wieder (genannt)",
    "custom": "Palladio beschreibt den Brauch seiner Zeit als Regel",
}


def load(name: str) -> dict:
    return json.loads((RULES / name).read_text(encoding="utf-8"))


def rule_files() -> list[Path]:
    return sorted(RULES.glob("book*.json"))


@lru_cache(maxsize=1)
def _pages() -> dict[int, list[str]]:
    root = ET.parse(ALTO).getroot()
    pages = {}
    for page in root.findall(".//a:Page", NS):
        lines = [" ".join(s.attrib.get("CONTENT", "") for s in line.findall("a:String", NS))
                 for line in page.findall(".//a:TextLine", NS)]
        pages[int(page.attrib["PHYSICAL_IMG_NR"])] = lines
    return pages


def chapter(book: int, ch: str) -> dict:
    for c in load("register.json")["chapters"]:
        if c["book"] == book and c["chapter"] == ch:
            return c
    raise KeyError(f"no chapter {ch} in book {book}")


def chapter_lines(book: int, ch: str) -> list[tuple[int, int, str]]:
    """(phys, line, text) from the chapter heading to the next heading."""
    c, pages = chapter(book, ch), _pages()
    start, end = c["start"], c["end"]
    out = []
    for phys in range(start["phys"], end["phys"] + 1):
        lines = pages.get(phys, [])
        lo = start["line"] if phys == start["phys"] else 0
        hi = end["line"] if (phys == end["phys"] and end["line"] is not None) else len(lines)
        out += [(phys, i, lines[i]) for i in range(lo, min(hi, len(lines)))]
    return out


def check() -> list[str]:
    problems = []
    register = load("register.json")
    known = {(c["book"], c["chapter"]) for c in register["chapters"]}
    ids = []
    for path in rule_files():
        data = json.loads(path.read_text(encoding="utf-8"))
        for r in data["rules"]:
            ids.append(r["id"])
            if (r["book"], r["chapter"]) not in known:
                problems.append(f"{r['id']}: chapter {r['chapter']} not in register")
            if r["kind"] not in KINDS:
                problems.append(f"{r['id']}: unknown kind {r['kind']}")
            if r["attribution"] not in ATTRIBUTION:
                problems.append(f"{r['id']}: unknown attribution {r['attribution']}")
            if r.get("evidence_class") == "A" and not r.get("scan_checked"):
                problems.append(f"{r['id']}: class A without scan check")
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    if dupes:
        problems.append(f"duplicate ids: {dupes}")
    return problems


def status() -> dict:
    register = load("register.json")
    counts = Counter()
    for path in rule_files():
        for r in json.loads(path.read_text(encoding="utf-8"))["rules"]:
            counts[(r["book"], r["chapter"])] += 1
    by_book = {}
    for c in register["chapters"]:
        b = by_book.setdefault(c["book"], Counter())
        b[c["status"]] += 1
        b["rules"] += counts[(c["book"], c["chapter"])]
    return {str(k): dict(v) for k, v in by_book.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Rule catalogue of the Quattro Libri")
    sub = parser.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dump")
    d.add_argument("book", type=int)
    d.add_argument("chapter")
    sub.add_parser("status")
    sub.add_parser("check")
    args = parser.parse_args()
    if args.cmd == "dump":
        for phys, i, text in chapter_lines(args.book, args.chapter):
            print(f"{phys}:{i:02d} {text}")
    elif args.cmd == "status":
        print(json.dumps(status(), indent=1))
    else:
        problems = check()
        print("\n".join(problems) if problems else "ok")


if __name__ == "__main__":
    main()
