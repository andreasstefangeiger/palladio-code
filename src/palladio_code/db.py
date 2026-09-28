from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize(db_path: str | Path, schema_path: str | Path) -> sqlite3.Connection:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        db_path.unlink()
    conn = connect(db_path)
    conn.executescript(Path(schema_path).read_text(encoding="utf-8"))
    return conn


def ingest_rules(conn: sqlite3.Connection, rules_path: str | Path) -> None:
    rows = json.loads(Path(rules_path).read_text(encoding="utf-8"))
    for row in rows:
        conn.execute(
            """
            INSERT INTO rules (
                rule_id, evidence_class, status, building_type, design_phase,
                category, subcategory, rule_text_de, condition_text_de,
                exception_text_de, purpose_text_de, reasoning_de, confidence,
                ratio_json, dimension_json, unit, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["rule_id"], row["evidence_class"], row.get("status", "pilot"),
                row.get("building_type"), row["design_phase"], row["category"],
                row.get("subcategory"), row["rule_text_de"], row.get("condition"),
                row.get("exception"), row.get("purpose"), row.get("reasoning"),
                row.get("confidence"), json.dumps(row.get("ratio"), ensure_ascii=False),
                json.dumps(row.get("dimension"), ensure_ascii=False), row.get("unit"),
                row.get("notes"),
            ),
        )
        for source in row.get("sources", []):
            conn.execute(
                """
                INSERT INTO rule_sources (
                    rule_id, source_work, book, chapter, printed_page,
                    pdf_page, quotation_original, translation_de, transcription_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["rule_id"], source["source_work"], source["book"],
                    source["chapter"], source.get("printed_page"), source.get("pdf_page"),
                    source["quotation_original"], source.get("translation_de"),
                    source.get("transcription_status", "checked_against_scan"),
                ),
            )
        for parent in row.get("derived_from", []):
            conn.execute(
                "INSERT INTO rule_derivations (rule_id, source_rule_id) VALUES (?, ?)",
                (row["rule_id"], parent),
            )
    conn.commit()


def ingest_drawings(conn: sqlite3.Connection, drawings_path: str | Path) -> None:
    rows = json.loads(Path(drawings_path).read_text(encoding="utf-8"))
    for row in rows:
        conn.execute(
            """
            INSERT INTO drawings (
                drawing_id, source_work, book, chapter, printed_page, pdf_page,
                drawing_type, building_name, image_path, roi_json, selection_reason,
                attribution_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["drawing_id"], row["source_work"], row["book"], row.get("chapter"),
                row.get("printed_page"), row["pdf_page"], row["drawing_type"],
                row.get("building_name"), row["image_path"],
                json.dumps(row.get("roi"), ensure_ascii=False), row["selection_reason"],
                row.get("attribution_status", "published_by_palladio_1570"),
            ),
        )
    conn.commit()


def ingest_measurements(conn: sqlite3.Connection, analysis_json: str | Path) -> None:
    data = json.loads(Path(analysis_json).read_text(encoding="utf-8"))
    for item in data["measurements"]:
        cursor = conn.execute(
            """
            INSERT INTO measurements (
                drawing_id, region_id, measurement_method, reference_line,
                quantity, raw_value, unit, endpoint_json, algorithm, algorithm_version,
                confidence, human_review_required, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["drawing_id"], item.get("region_id"), item["measurement_method"],
                item.get("reference_line"), item["quantity"], item["raw_value"],
                item.get("unit", "pixel"), json.dumps(item.get("endpoints")),
                data["algorithm"], data["algorithm_version"], item.get("confidence"),
                int(item.get("human_review_required", True)), item.get("notes"),
            ),
        )
        measurement_id = cursor.lastrowid
        for rank, hypothesis in enumerate(item.get("ratio_hypotheses", []), start=1):
            conn.execute(
                """
                INSERT INTO ratio_hypotheses (
                    measurement_id, rank, measured_ratio, target_label,
                    target_value, deviation_percent, target_origin, within_pilot_tolerance
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    measurement_id, rank, item.get("measured_ratio"),
                    hypothesis["label"], hypothesis["target"],
                    hypothesis["deviation_percent"], hypothesis["origin"],
                    int(hypothesis["deviation_percent"] <= data["tolerance_percent"]),
                ),
            )
    conn.commit()


def export_tables(conn: sqlite3.Connection, output_dir: str | Path) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    tables = [
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    ]
    for table in tables:
        rows = conn.execute(f"SELECT * FROM {table}").fetchall()
        with (output / f"{table}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            if rows:
                writer.writerow(rows[0].keys())
                writer.writerows([tuple(row) for row in rows])
            else:
                columns = [row[1] for row in conn.execute(f"PRAGMA table_info({table})")]
                writer.writerow(columns)

