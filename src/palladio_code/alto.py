from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"a": "http://www.loc.gov/standards/alto/ns-v3#"}
CAP_RE = re.compile(r"\bCAP(?:ITOLO)?\s*\.?\s*([IVXLCDM]+)\b", re.I)


def _line_text(line: ET.Element) -> str:
    return " ".join(
        token.attrib.get("CONTENT", "") for token in line.findall("a:String", NS)
    ).strip()


def iter_pages(path: str | Path):
    root = ET.parse(path).getroot()
    for page in root.findall(".//a:Page", NS):
        lines = [_line_text(line) for line in page.findall(".//a:TextLine", NS)]
        yield {
            "physical_image_number": int(page.attrib["PHYSICAL_IMG_NR"]),
            "alto_page_id": page.attrib["ID"],
            "width": int(page.attrib["WIDTH"]),
            "height": int(page.attrib["HEIGHT"]),
            "lines": [line for line in lines if line],
        }


def extract_chapter_candidates(path: str | Path) -> list[dict]:
    """Extract heading candidates; this deliberately does not claim editorial certainty."""
    result: list[dict] = []
    for page in iter_pages(path):
        lines = page["lines"]
        for index, line in enumerate(lines):
            match = CAP_RE.search(line)
            if not match:
                continue
            context = " ".join(lines[max(0, index - 2) : index + 2])
            upper_letters = sum(ch.isupper() for ch in context)
            lower_letters = sum(ch.islower() for ch in context)
            # Headings in this edition are predominantly uppercase. Body references
            # such as "al cap. vi" are rejected by this simple, auditable heuristic.
            if upper_letters < 12 or upper_letters < lower_letters * 0.35:
                continue
            result.append(
                {
                    "physical_image_number": page["physical_image_number"],
                    "pdf_page": page["physical_image_number"] + 1,
                    "alto_page_id": page["alto_page_id"],
                    "roman_candidate": match.group(1).upper(),
                    "heading_context_ocr": context,
                    "status": "machine_candidate_needs_editorial_review",
                }
            )
    return result

