from __future__ import annotations

import argparse
import json
from pathlib import Path

from .alto import extract_chapter_candidates
from .analyzer import analyze_drawing
from .db import export_tables, ingest_drawings, ingest_measurements, ingest_rules, initialize
from .corpus import process_full_corpus

ROOT = Path(__file__).resolve().parents[2]


def run_all() -> None:
    config = json.loads((ROOT / "config/pilot.json").read_text(encoding="utf-8"))
    output = ROOT / "output"
    analysis_dir = output / "analysis"
    conn = initialize(output / "palladio_code.sqlite", ROOT / "schema.sql")
    ingest_rules(conn, ROOT / "data/pilot_rules.json")
    ingest_drawings(conn, ROOT / "data/pilot_drawings.json")
    for drawing in config["drawings"]:
        result = analyze_drawing(
            drawing, ROOT, analysis_dir,
            tolerance_percent=config["tolerance_percent"],
        )
        ingest_measurements(conn, result)
    full_corpus = process_full_corpus(
        conn,
        ROOT / config["alto_path"],
        ROOT / config["pdf_path"],
        output,
    )
    candidates = extract_chapter_candidates(ROOT / config["alto_path"])
    (output / "chapter_candidates.json").write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    export_tables(conn, output / "csv")
    counts = {
        "rules": conn.execute("SELECT count(*) FROM rules").fetchone()[0],
        "a_rules": conn.execute("SELECT count(*) FROM rules WHERE evidence_class='A'").fetchone()[0],
        "b_rules": conn.execute("SELECT count(*) FROM rules WHERE evidence_class='B'").fetchone()[0],
        "drawings": conn.execute("SELECT count(*) FROM drawings").fetchone()[0],
        "measurements": conn.execute("SELECT count(*) FROM measurements").fetchone()[0],
        "ratio_hypotheses": conn.execute("SELECT count(*) FROM ratio_hypotheses").fetchone()[0],
        "chapter_candidates": len(candidates),
        "full_corpus": full_corpus,
    }
    (output / "pilot_summary.json").write_text(
        json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    conn.close()
    print(json.dumps(counts, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Palladio-Code pilot pipeline")
    parser.add_argument("command", choices=["all"], nargs="?", default="all")
    args = parser.parse_args()
    if args.command == "all":
        run_all()


if __name__ == "__main__":
    main()
