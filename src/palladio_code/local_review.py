from __future__ import annotations

import argparse
import json
import time
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_LABELS = {"probable_rule", "measurement_statement", "descriptive", "ocr_noise"}


def _load_existing(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            result[item["candidate_id"]] = item
    return result


def _request(model: str, batch: list[dict], second_pass: bool = False,
             base_url: str = "http://127.0.0.1:11434") -> list[dict]:
    candidates = [
        {
            "candidate_id": item["candidate_id"],
            "book": item["book"],
            "marker_types": item["marker_types"],
            "passage_ocr": item["passage_ocr"],
        }
        for item in batch
    ]
    control_note = (
        "Zweiter unabhängiger Kontrolllauf: Prüfe besonders streng, ob eine Aussage "
        "wirklich generalisierbar normativ ist; im Zweifel descriptive oder measurement_statement."
        if second_pass else ""
    )
    prompt = f"""Du sichtest OCR aus Palladios Quattro libri (1570). Ordne jede Fundstelle nur vorläufig ein.

{control_note}

Kategorien:
- probable_rule: normative, konditionale oder empfehlende architektonische Handlungsregel
- measurement_statement: konkrete Maß- oder Proportionsaussage, aber nicht eindeutig normativ
- descriptive: historische, typologische oder objektspezifische Beschreibung
- ocr_noise: Text zu beschädigt oder Fundmarker offensichtlich durch OCR-Fehler entstanden

Wichtig: Dies ist keine Einstufung als wissenschaftlich bestätigte A- oder B-Regel. Behalte jede candidate_id exakt bei. Gib für jeden Eingang genau ein Ergebnis zurück. Die knappe Begründung auf Deutsch, höchstens 18 Wörter.

Eingang:
{json.dumps(candidates, ensure_ascii=False)}
"""
    schema = {
        "type": "object",
        "properties": {
            "reviews": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "candidate_id": {"type": "string"},
                        "label": {"type": "string", "enum": sorted(ALLOWED_LABELS)},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                        "reason": {"type": "string"},
                    },
                    "required": ["candidate_id", "label", "confidence", "reason"],
                },
            }
        },
        "required": ["reviews"],
    }
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "think": False,
        "format": schema,
        "options": {"temperature": 0.1 if second_pass else 0, "num_ctx": 8192,
                    "num_predict": 1200},
        "keep_alive": "30m",
    }).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/chat", data=body,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(request, timeout=900) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return json.loads(payload["message"]["content"])["reviews"]


def run(model: str, batch_size: int, limit: int | None = None,
        output_stem: str = "local_llm_review", second_pass: bool = False,
        base_url: str = "http://127.0.0.1:11434") -> None:
    source = ROOT / "output/automatic_rule_candidates.json"
    output = ROOT / "output" / f"{output_stem}.jsonl"
    summary_path = ROOT / "output" / f"{output_stem}_summary.json"
    candidates = json.loads(source.read_text(encoding="utf-8"))
    existing = _load_existing(output)
    pending = [item for item in candidates if item["candidate_id"] not in existing]
    if limit is not None:
        pending = pending[:limit]
    total_target = len(existing) + len(pending)
    print(f"Lokal zu prüfen: {len(pending)}; bereits vorhanden: {len(existing)}", flush=True)

    with output.open("a", encoding="utf-8") as handle:
        for start in range(0, len(pending), batch_size):
            batch = pending[start:start + batch_size]
            expected = {item["candidate_id"] for item in batch}
            last_error = None
            for attempt in range(1, 4):
                try:
                    reviews = _request(model, batch, second_pass=second_pass,
                                       base_url=base_url)
                    by_id = {item["candidate_id"]: item for item in reviews}
                    if set(by_id) != expected:
                        raise ValueError("Lokales Modell lieferte nicht genau die angeforderten IDs")
                    if any(item["label"] not in ALLOWED_LABELS for item in reviews):
                        raise ValueError("Lokales Modell lieferte eine unbekannte Kategorie")
                    for candidate in batch:
                        review = by_id[candidate["candidate_id"]]
                        record = {
                            "candidate_id": candidate["candidate_id"],
                            "model": model,
                            "label": review["label"],
                            "confidence": round(float(review["confidence"]), 3),
                            "reason": review["reason"].strip(),
                            "status": "local_model_triage_unverified",
                        }
                        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
                        existing[record["candidate_id"]] = record
                    handle.flush()
                    break
                except Exception as exc:  # retry local service/model formatting failures
                    last_error = exc
                    print(f"Versuch {attempt}/3 fehlgeschlagen: {exc}", flush=True)
                    time.sleep(attempt * 2)
            else:
                # Keep the long local run alive. Unwritten candidates remain
                # pending and are retried automatically on the next invocation,
                # preferably one by one.
                print(
                    f"Paket übersprungen; wird später erneut versucht: {last_error}",
                    flush=True,
                )
                continue
            done = len(existing)
            print(f"Fortschritt: {done}/{total_target}", flush=True)

    counts = Counter(item["label"] for item in existing.values())
    confidences = [float(item["confidence"]) for item in existing.values()]
    summary = {
        "model": model,
        "reviewed": len(existing),
        "source_candidates": len(candidates),
        "complete": len(existing) == len(candidates),
        "remaining": len(candidates) - len(existing),
        "labels": dict(counts.most_common()),
        "mean_confidence": round(sum(confidences) / len(confidences), 3) if confidences else None,
        "status": "local_model_triage_unverified",
        "credits_used": 0,
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lokale, fortsetzbare LLM-Vorsortierung")
    parser.add_argument("--model", default="gemma4:12b")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--output-stem", default="local_llm_review")
    parser.add_argument("--second-pass", action="store_true")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    args = parser.parse_args()
    run(args.model, args.batch_size, args.limit, args.output_stem,
        args.second_pass, args.base_url)


if __name__ == "__main__":
    main()
