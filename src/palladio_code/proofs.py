"""Scan proofs for transcribed statements.

For every statement in a statements file the ALTO word coordinates locate the
quoted lines on the page; the matching region is fetched from the e-rara IIIF
image service and stitched into proof sheets. A human (or model) reads the crop
and confirms or corrects the transcription. The OCR is only used to find the
place on the page, never as the quotation itself.
"""
from __future__ import annotations

import argparse
import io
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NS = {"a": "http://www.loc.gov/standards/alto/ns-v3#"}
MANIFEST = "https://www.e-rara.ch/i3f/v20/103248/manifest"


def page_lines(alto_path: Path, phys: int) -> list[dict]:
    root = ET.parse(alto_path).getroot()
    for page in root.findall(".//a:Page", NS):
        if int(page.attrib["PHYSICAL_IMG_NR"]) != phys:
            continue
        lines = []
        for line in page.findall(".//a:TextLine", NS):
            text = " ".join(s.attrib.get("CONTENT", "") for s in line.findall("a:String", NS))
            a = line.attrib
            lines.append({"text": text, "x": int(a["HPOS"]), "y": int(a["VPOS"]),
                          "w": int(a["WIDTH"]), "h": int(a["HEIGHT"])})
        return lines
    raise KeyError(f"page {phys} not in ALTO")


def locate(lines: list[dict], start: str, end: str) -> tuple[int, int, int, int]:
    """Bounding box (x, y, w, h) of the lines spanned by the first start anchor and the next end anchor.

    Anchors are matched on the page text joined across line breaks, so they may cross lines.
    """
    joined, offsets = "", []
    for line in lines:
        offsets.append(len(joined))
        joined += line["text"] + " "
    begin = joined.index(start)
    finish = joined.index(end, begin) + len(end)
    chosen = [line for line, off in zip(lines, offsets) if off < finish and off + len(line["text"]) >= begin]
    x0 = min(line["x"] for line in chosen)
    y0 = min(line["y"] for line in chosen)
    x1 = max(line["x"] + line["w"] for line in chosen)
    y1 = max(line["y"] + line["h"] for line in chosen)
    return x0, y0, x1 - x0, y1 - y0


def canvas_services() -> dict[int, str]:
    with urllib.request.urlopen(MANIFEST, timeout=60) as response:
        manifest = json.load(response)
    canvases = manifest["sequences"][0]["canvases"]
    return {i + 1: c["images"][0]["resource"]["service"]["@id"] for i, c in enumerate(canvases)}


def fetch_region(service: str, box: tuple[int, int, int, int], margin: int = 12, width: int = 1100):
    from PIL import Image

    x, y, w, h = box
    region = f"{max(0, x - margin)},{max(0, y - margin)},{w + 2 * margin},{h + 2 * margin}"
    url = f"{service}/{region}/{min(width, w + 2 * margin)},/0/default.jpg"
    with urllib.request.urlopen(url, timeout=90) as response:
        return Image.open(io.BytesIO(response.read())).convert("RGB"), url


def build_sheets(statements_path: Path, alto_path: Path, out_dir: Path, per_sheet: int = 5) -> list[dict]:
    from PIL import Image, ImageDraw

    data = json.loads(statements_path.read_text(encoding="utf-8"))
    services = canvas_services()
    out_dir.mkdir(parents=True, exist_ok=True)
    records, crops = [], []
    for st in data["statements"]:
        box = locate(page_lines(alto_path, st["phys"]), *st["anchor"])
        image, url = fetch_region(services[st["phys"]], box)
        crops.append((st["id"], image))
        records.append({"id": st["id"], "phys": st["phys"], "box": box, "iiif": url})
    for n in range(0, len(crops), per_sheet):
        group = crops[n : n + per_sheet]
        width = max(img.width for _, img in group)
        height = sum(img.height + 40 for _, img in group)
        sheet = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(sheet)
        y = 0
        for sid, img in group:
            draw.text((6, y + 10), sid, fill="red")
            sheet.paste(img, (0, y + 36))
            y += img.height + 40
        sheet.save(out_dir / f"proof_sheet_{n // per_sheet + 1:02d}.jpg", quality=85)
    (out_dir / "proof_regions.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Build scan proof sheets for statements")
    parser.add_argument("statements", type=Path)
    parser.add_argument("--alto", type=Path, default=ROOT / "data/source/erara_ocr_alto.xml")
    parser.add_argument("--out", type=Path, default=ROOT / "output/book2/proofs")
    args = parser.parse_args()
    records = build_sheets(args.statements, args.alto, args.out)
    print(f"{len(records)} regions -> {args.out}")


if __name__ == "__main__":
    main()
