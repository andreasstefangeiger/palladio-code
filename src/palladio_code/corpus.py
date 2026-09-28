from __future__ import annotations

import json
import csv
import re
import sqlite3
import unicodedata
from collections import Counter
from pathlib import Path

from .alto import iter_pages

SOURCE_WORK = "I quattro libri dell'architettura (Venetia 1570)"

BOOK_RANGES = {
    1: range(9, 73),
    2: range(73, 153),
    3: range(153, 201),
    4: range(201, 338),
}

MARKERS = {
    "obligation": [
        r"\bsi de(?:ve|ue)\b", r"\bdeono\b", r"\bdebbono\b", r"\bdouera\b",
        r"\bbisogna\b", r"\bsi richiede\b", r"\be necessario\b",
        r"\bsi fara\b", r"\bsi faranno\b", r"\bsi fanno\b",
    ],
    "prohibition": [
        r"\bnon si (?:deve|deue|fara|faranno)\b", r"\bnon deono\b",
        r"\bsi deve schifare\b", r"\bsi deue schifare\b",
    ],
    "recommendation": [
        r"\ba me pare\b", r"\bmi piace\b", r"\bmi piacera\b",
        r"\bsaranno lodeuoli\b", r"\be meglio\b", r"\bsi sogliono\b",
        r"\bio sono solito\b", r"\btorna bene\b",
    ],
    "condition": [r"\bse si\b", r"\bquando\b", r"\bouero\b", r"\bnel caso\b"],
    "purpose": [r"\baccioche\b", r"\bperche\b", r"\baffine che\b"],
}

QUANTITY_RE = re.compile(
    r"\b(?:\d+|vna?|due|tre|quattro|cinque|sei|sette|otto|noue|dieci|meta|mez[oa]|"
    r"terza|quarta|quinta|sesta|settima|ottaua|diametr[oi]|modul[oi]|pied[ei]|onci[ae]|"
    r"quadro|quadri|proportion[ei]|larghezza|lunghezza|altezza)\b"
)

CATEGORY_KEYWORDS = {
    "site_orientation": ("sito", "aria", "vento", "leuante", "ponente", "mezo giorno"),
    "room_proportion": ("stanza", "stanze", "sala", "sale", "larghezza", "lunghezza"),
    "vertical_dimension": ("altezza", "alto", "volto", "uolto", "solaro"),
    "opening": ("finestra", "finestre", "porta", "porte", "luce"),
    "column_order": ("colonna", "colonne", "capitello", "architraue", "fregio", "cornice"),
    "construction": ("muro", "muri", "fondament", "traue", "arco", "volta", "uolta"),
    "material": ("pietra", "legname", "calce", "arena", "metallo", "marmo"),
    "circulation": ("scala", "scale", "grado", "gradi", "entrata"),
    "roof": ("tetto", "coperto", "piogg", "tegole"),
    "temple": ("tempio", "tempij", "cella", "portico"),
    "urban_public": ("strada", "strade", "piazza", "ponte", "basilica"),
}

PHASE_BY_CATEGORY = {
    "site_orientation": "site_and_orientation",
    "room_proportion": "space_organization_and_proportion",
    "vertical_dimension": "vertical_dimensioning",
    "opening": "openings_and_light",
    "column_order": "orders_and_detail",
    "construction": "construction",
    "material": "materials",
    "circulation": "circulation",
    "roof": "roof",
    "temple": "building_type_and_composition",
    "urban_public": "urban_and_public_architecture",
    "other": "unclassified",
}


def book_for_physical(number: int) -> int | None:
    for book, numbers in BOOK_RANGES.items():
        if number in numbers:
            return book
    return None


def normalize_search(text: str) -> str:
    value = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("ſ", "s")
    value = re.sub(r"\s+", " ", value)
    # The institutional OCR regularly reads the long-s form of standalone
    # Italian "si" and "se" as "fi" and "fe". Restricting this correction to
    # whole tokens avoids altering ordinary words beginning with f.
    value = re.sub(r"\bfi\b", "si", value)
    value = re.sub(r"\bfe\b", "se", value)
    return value.strip()


def _printed_page_candidate(lines: list[str]) -> str | None:
    head = " ".join(lines[:8])
    values = re.findall(r"(?<!\d)\d{1,3}(?!\d)", head)
    return values[-1] if values else None


def _chapter_candidate(lines: list[str]) -> str | None:
    text = " ".join(lines)
    match = re.search(r"\bCap(?:itolo)?\s*\.?\s*([IVXLCDM]+)\b", text, re.I)
    return match.group(1).upper() if match else None


def _passages(lines: list[str]) -> list[str]:
    text = re.sub(r"\s+", " ", " ".join(lines)).strip()
    pieces = re.split(r"(?<=[.;:!?])\s+(?=[A-ZÀÈÉÌÒÙ])", text)
    result: list[str] = []
    buffer = ""
    for piece in pieces:
        if len(piece) < 55:
            buffer = f"{buffer} {piece}".strip()
            continue
        if buffer:
            piece = f"{buffer} {piece}"
            buffer = ""
        if len(piece) > 1200:
            result.extend(piece[i : i + 900] for i in range(0, len(piece), 900))
        else:
            result.append(piece)
    if buffer:
        result.append(buffer)
    return result


def _marker_types(normalized: str) -> list[str]:
    found = []
    for marker_type, patterns in MARKERS.items():
        if any(re.search(pattern, normalized) for pattern in patterns):
            found.append(marker_type)
    return found


def _category(normalized: str) -> str:
    scores = {
        category: sum(normalized.count(word) for word in words)
        for category, words in CATEGORY_KEYWORDS.items()
    }
    best, score = max(scores.items(), key=lambda item: item[1])
    return best if score else "other"


def extract_rule_candidates(page: dict) -> list[dict]:
    book = book_for_physical(page["physical_image_number"])
    if book is None:
        return []
    printed = _printed_page_candidate(page["lines"])
    chapter = _chapter_candidate(page["lines"])
    candidates = []
    for passage in _passages(page["lines"]):
        normalized = normalize_search(passage)
        markers = _marker_types(normalized)
        quantity_count = len(QUANTITY_RE.findall(normalized))
        quantity = quantity_count > 0
        category = _category(normalized)
        if not markers and quantity_count >= 2 and category != "other":
            markers.append("measurement_statement")
        if not markers and not (quantity and "proportion" in normalized):
            continue
        score = min(1.0, 0.18 + 0.17 * len(markers) + (0.22 if quantity else 0.0)
                    + (0.12 if "obligation" in markers or "prohibition" in markers else 0.0))
        candidates.append({
            "source_work": SOURCE_WORK,
            "book": book,
            "chapter_candidate": chapter,
            "printed_page_candidate": printed,
            "pdf_page": page["physical_image_number"] + 1,
            "passage_ocr": passage,
            "normalized_passage": normalized,
            "marker_types": markers,
            "category_candidate": category,
            "design_phase_candidate": PHASE_BY_CATEGORY[category],
            "extraction_score": score,
            "contains_quantity": quantity,
            "status": "automatic_unverified_candidate",
            "notes": "OCR passage; verify against scan before A classification.",
        })
    return candidates


def _image_metrics(data: bytes) -> dict:
    import cv2
    import numpy as np

    array = np.frombuffer(data, dtype=np.uint8)
    gray = cv2.imdecode(array, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        return {"ink_coverage": None, "edge_density": None,
                "long_horizontal_lines": 0, "long_vertical_lines": 0}
    scale = min(1.0, 620 / max(gray.shape))
    small = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    normalized = cv2.divide(
        small,
        cv2.morphologyEx(small, cv2.MORPH_CLOSE,
                         cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))),
        scale=255,
    )
    _, binary = cv2.threshold(normalized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ink_coverage = float(np.mean(binary < 128))
    edges = cv2.Canny(binary, 50, 150)
    edge_density = float(np.mean(edges > 0))
    min_length = max(45, min(small.shape) // 6)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 360, threshold=35,
                            minLineLength=min_length, maxLineGap=8)
    horizontal = vertical = 0
    if lines is not None:
        for x1, y1, x2, y2 in np.asarray(lines).reshape(-1, 4):
            angle = abs(float(np.degrees(np.arctan2(y2 - y1, x2 - x1))))
            if min(angle, abs(180 - angle)) <= 3:
                horizontal += 1
            elif abs(90 - angle) <= 3:
                vertical += 1
    return {
        "ink_coverage": ink_coverage,
        "edge_density": edge_density,
        "long_horizontal_lines": horizontal,
        "long_vertical_lines": vertical,
    }


def _page_class(words: int, metrics: dict) -> tuple[str, float, list[str]]:
    h = metrics["long_horizontal_lines"]
    v = metrics["long_vertical_lines"]
    ink = metrics["ink_coverage"] or 0.0
    edges = metrics["edge_density"] or 0.0
    line_score = min(1.0, (h + v) / 38)
    low_text = max(0.0, min(1.0, (190 - words) / 170))
    density_score = min(1.0, edges / 0.11)
    score = 0.48 * line_score + 0.34 * low_text + 0.18 * density_score
    reasons = [f"words={words}", f"orthogonal_lines={h+v}", f"ink={ink:.4f}", f"edges={edges:.4f}"]
    if words < 55 and h + v >= 14:
        return "drawing_dominant", score, reasons
    if words < 180 and h + v >= 10:
        return "mixed_text_drawing", score, reasons
    if words >= 180:
        return "text_dominant", score, reasons
    return "uncertain", score, reasons


def process_full_corpus(conn: sqlite3.Connection, alto_path: str | Path,
                        pdf_path: str | Path, output_dir: str | Path) -> dict:
    from pypdf import PdfReader

    pages = list(iter_pages(alto_path))
    reader = PdfReader(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    all_candidates = []
    drawing_rows = []

    for page in pages:
        physical = page["physical_image_number"]
        pdf_page = physical + 1
        words = sum(len(line.split()) for line in page["lines"])
        chars = sum(len(line) for line in page["lines"])
        metrics = {"ink_coverage": None, "edge_density": None,
                   "long_horizontal_lines": 0, "long_vertical_lines": 0}
        if 1 <= pdf_page <= len(reader.pages):
            images = list(reader.pages[pdf_page - 1].images)
            if images:
                metrics = _image_metrics(images[0].data)
        page_class, illustration_score, reasons = _page_class(words, metrics)
        page_id = f"ERARA-PHYS-{physical:03d}"
        book = book_for_physical(physical)
        printed = _printed_page_candidate(page["lines"])
        conn.execute(
            """INSERT INTO corpus_pages VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (page_id, physical, pdf_page, book, printed, page["alto_page_id"],
             words, chars, metrics["ink_coverage"], metrics["edge_density"],
             metrics["long_horizontal_lines"], metrics["long_vertical_lines"],
             illustration_score, page_class, "automatic_unverified",),
        )
        page_candidates = extract_rule_candidates(page)
        for sequence, item in enumerate(page_candidates, start=1):
            item["candidate_id"] = f"AC-B{book}-P{physical:03d}-{sequence:02d}"
            item["page_id"] = page_id
            all_candidates.append(item)
            conn.execute(
                """
                INSERT INTO automatic_rule_candidates VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (item["candidate_id"], page_id, item["source_work"], item["book"],
                 item["chapter_candidate"], item["printed_page_candidate"], item["pdf_page"],
                 item["passage_ocr"], item["normalized_passage"],
                 json.dumps(item["marker_types"], ensure_ascii=False),
                 item["category_candidate"], item["design_phase_candidate"],
                 item["extraction_score"], int(item["contains_quantity"]),
                 item["status"], item["notes"]),
            )
        if book and page_class in {"drawing_dominant", "mixed_text_drawing"}:
            drawing_rows.append({"page_id": page_id, "book": book, "score": illustration_score,
                                 "page_class": page_class, "reasons": reasons})

    for book in range(1, 5):
        ranked = sorted((row for row in drawing_rows if row["book"] == book),
                        key=lambda row: row["score"], reverse=True)
        for rank, row in enumerate(ranked, start=1):
            conn.execute(
                "INSERT INTO automatic_drawing_candidates VALUES (?,?,?,?,?)",
                (row["page_id"], row["page_class"],
                 json.dumps(row["reasons"], ensure_ascii=False), rank,
                 "automatic_unverified_candidate"),
            )
    conn.commit()

    (output_dir / "automatic_rule_candidates.json").write_text(
        json.dumps(all_candidates, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    review_queue = sorted(
        all_candidates,
        key=lambda item: (-item["extraction_score"], item["book"], item["pdf_page"],
                          item["candidate_id"]),
    )
    with (output_dir / "automatic_review_queue.csv").open("w", encoding="utf-8", newline="") as handle:
        fields = [
            "candidate_id", "book", "chapter_candidate", "printed_page_candidate",
            "pdf_page", "marker_types", "category_candidate", "design_phase_candidate",
            "extraction_score", "contains_quantity", "status", "passage_ocr",
        ]
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for item in review_queue:
            row = dict(item)
            row["marker_types"] = "|".join(item["marker_types"])
            writer.writerow(row)

    topic_index = {}
    for category in sorted({item["category_candidate"] for item in all_candidates}):
        matches = [item for item in review_queue if item["category_candidate"] == category]
        topic_index[category] = {
            "count": len(matches),
            "by_book": {str(book): sum(item["book"] == book for item in matches)
                        for book in range(1, 5)},
            "top_candidate_ids": [item["candidate_id"] for item in matches[:12]],
        }
    (output_dir / "topic_index.json").write_text(
        json.dumps(topic_index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    phase_index = {}
    for phase in sorted({item["design_phase_candidate"] for item in all_candidates}):
        matches = [item for item in review_queue if item["design_phase_candidate"] == phase]
        phase_index[phase] = {
            "count": len(matches),
            "top_candidate_ids": [item["candidate_id"] for item in matches[:12]],
        }
    (output_dir / "design_phase_index.json").write_text(
        json.dumps(phase_index, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    ratio_terms = re.compile(r"\b(?:proportion|diametr|modul|larghezza|lunghezza|altezza)")
    ratio_candidates = [
        item for item in review_queue
        if item["contains_quantity"] and ratio_terms.search(item["normalized_passage"])
    ]
    (output_dir / "automatic_ratio_candidates.json").write_text(
        json.dumps(ratio_candidates, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    category_counts = Counter(item["category_candidate"] for item in all_candidates)
    marker_counts = Counter(marker for item in all_candidates for marker in item["marker_types"])
    result = {
        "pages_processed": len(pages),
        "pages_by_book": {str(book): sum(book_for_physical(p["physical_image_number"]) == book for p in pages)
                          for book in range(1, 5)},
        "paratext_pages_unassigned_to_book": sum(
            book_for_physical(page["physical_image_number"]) is None for page in pages
        ),
        "automatic_rule_candidates": len(all_candidates),
        "rule_candidates_by_book": {str(book): sum(item["book"] == book for item in all_candidates)
                                    for book in range(1, 5)},
        "rule_candidates_by_category": dict(category_counts.most_common()),
        "marker_counts": dict(marker_counts.most_common()),
        "drawing_candidate_pages": len(drawing_rows),
        "drawing_candidates_by_book": {str(book): sum(row["book"] == book for row in drawing_rows)
                                       for book in range(1, 5)},
        "ratio_candidates": len(ratio_candidates),
        "derived_indices": [
            "automatic_review_queue.csv", "topic_index.json",
            "design_phase_index.json", "automatic_ratio_candidates.json",
        ],
        "status": "automatic_full_corpus_pass_complete_editorial_review_pending",
    }
    (output_dir / "full_corpus_summary.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return result
