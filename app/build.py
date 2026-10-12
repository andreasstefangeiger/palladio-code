"""Build the single-file app: template + engine + data bundle -> app/dist/palladio-labor.html.

The data bundle is generated from the repository's evidence files, so the app never
carries its own copy of a rule: pilot_rules.json (A/B rules with quotations),
data/book2/text_statements.json (scan-checked Book II statements) and
data/book2/plate_readings.json (woodcut room dimensions).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"


def rules_bundle() -> dict:
    out = {}
    for rule in json.loads((ROOT / "data/pilot_rules.json").read_text(encoding="utf-8")):
        src = rule["sources"][0]
        out[rule["rule_id"]] = {
            "cls": rule["evidence_class"],
            "text": rule["rule_text_de"],
            "it": src.get("quotation_original", ""),
            "de": src.get("translation_de", ""),
            "where": f"Buch {src.get('book')}, Kap. {src.get('chapter')}, S. {src.get('printed_page')}",
            "confidence": rule.get("confidence"),
        }
    statements = json.loads((ROOT / "data/book2/text_statements.json").read_text(encoding="utf-8"))
    for st in statements["statements"]:
        if st["id"] == "B2-CAP2-1":
            out[st["id"]] = {
                "cls": "A",
                "text": "Im Haus soll es große, mittlere und kleine Räume geben, alle nebeneinander, "
                        "damit sie einander dienen; die kleinen erhalten Zwischengeschosse.",
                "it": st["quote"],
                "de": "",
                "where": "Buch II, Kap. II, S. 4",
            }
    return out


def readings_bundle() -> list:
    data = json.loads((ROOT / "data/book2/plate_readings.json").read_text(encoding="utf-8"))
    return [{k: r[k] for k in ("building", "printed_page", "room", "length", "width", "confidence")}
            for r in data["rooms"]]


def build() -> Path:
    template = (APP / "index.template.html").read_text(encoding="utf-8")
    engine = (APP / "engine.js").read_text(encoding="utf-8")
    engine = re.sub(r"^export ", "", engine, flags=re.M)
    data = {"rules": rules_bundle(), "readings": readings_bundle()}
    html = template.replace("/*__ENGINE__*/", engine).replace(
        "/*__DATA__*/", "const DATA = " + json.dumps(data, ensure_ascii=False) + ";")
    out = APP / "dist" / "palladio-labor.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


if __name__ == "__main__":
    print(build())
