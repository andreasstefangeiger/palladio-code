"""San Giorgio Maggiore against Palladio's own rules, on Bertotti Scamozzi's survey.

Palladio published no plan of San Giorgio. The measured drawings of Ottavio Bertotti Scamozzi
(Le fabbriche e i disegni di Andrea Palladio, IV, plates V–VIII; consulted in the 1846 Genoa
edition) are the oldest published survey with dimensions; they record the built church (C2).
data/san_giorgio/bertotti_scamozzi.json holds the dimensions (labels checked against the scale
bar) and Bertotti's own statements. This module compares them with the scan-checked rules of
the Quattro Libri.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .nullmodel import PALLADIO_I21, binomial_upper_tail, continuous_share

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/san_giorgio/bertotti_scamozzi.json"
TOL = 0.01


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def feet(data: dict) -> dict[str, float]:
    return {r["id"]: r["feet"] for r in data["plan_readings"]}


def nearest_form(ratio: float) -> tuple[str, float]:
    t = min(PALLADIO_I21, key=lambda t: abs(ratio - t.value) / t.value)
    return t.label, (ratio - t.value) / t.value


def rooms(f: dict[str, float]) -> list[dict]:
    """Main spaces of Palladio's time (the choir was built after his death, Bertotti p. 21 n. b)."""
    spaces = [
        ("Mittelschiff bis zur Vierung", f["SG-NAVE-L"], f["SG-NAVE-W"], True),
        ("Vierung", f["SG-NAVE-W"], f["SG-CROSSING"], True),
        ("Querhausarm (ohne Apsis)", f["SG-NAVE-W"], f["SG-ARM"], True),
        ("Presbyterium", f["SG-PRES-W"], f["SG-PRES-L"], True),
        ("Mönchschor mit Apsis (nach Palladio)", f["SG-CHOIR-L"], f["SG-CHOIR-W"], False),
    ]
    out = []
    for name, a, b, palladio in spaces:
        ratio = max(a, b) / min(a, b)
        label, dev = nearest_form(ratio)
        out.append({"space": name, "a": a, "b": b, "ratio": round(ratio, 4), "nearest": label,
                    "deviation": round(dev, 4), "within_1_percent": abs(dev) <= TOL, "palladio_time": palladio})
    return out


def rule_checks(f: dict[str, float]) -> list[dict]:
    """Each check names the rule (catalogue id) and the measured or stated value (Bertotti)."""
    width, length = f["SG-NAVE-W"], f["SG-NAVE-L"]
    am = (length + width) / 2
    gm = (length * width) ** 0.5
    hm = 2 * length * width / (length + width)
    checks = [
        {"rule": "Saal höchstens zwei Quadrate; Basilika: Mittelraum zwei Quadrate",
         "source": "I.XXI.3 (A-DIM-HALL-001); B3-XIX-BASILICA", "value": f"Mittelschiff {length/width:.2f} Breiten",
         "verdict": "erfüllt (2:1)"},
        {"rule": "Seitenschiffe der Kirche wie bei der Basilika: ⅓ des Mittelraums",
         "source": "B4-V-CHIESE → B3-XIX-BASILICA", "value": f"{f['SG-AISLE-W']/width:.2f} der Mittelschiffbreite",
         "verdict": "nicht erfüllt (etwa ½; Bertotti: 'la metà')"},
        {"rule": "Kreis und Quadrat als vollkommenste Formen; Kreuzform",
         "source": "B4-II-FORME, B4-II-RITONDA, B4-II-CROCE", "value": "Vierung quadratisch mit Kuppelkreis, Querhausarme quadratisch mit Halbkreisapsiden",
         "verdict": "erfüllt (qualitativ)"},
        {"rule": "Kompositsäule 10 Moduln, Gebälk ⅕",
         "source": "I.XVIII.1, I.XVIII.4", "value": "innen 10¼ Durchmesser, Gebälk ⅕; Fassade knapp 10, Gebälk ⅕ (Bertotti)",
         "verdict": "erfüllt (innen +2,5 %)"},
        {"rule": "Postament der Kompositordnung ⅓ der Säule (korinthisch ¼)",
         "source": "I.XVIII.2, I.XIX.3", "value": "innen ¼, Fassade knapp ⅓ (Bertotti)",
         "verdict": "Fassade erfüllt; innen das Maß der korinthischen Ordnung"},
        {"rule": "Bogenöffnung der Kompositordnung zwei Quadrate und ein halbes hoch",
         "source": "I.XVIII.1", "value": "Arkaden der Seitenschiffe 2½ Breiten (Bertotti)", "verdict": "erfüllt"},
        {"rule": "Gewölbehöhe nach einem der drei Mittel; sonst Urteil des Architekten",
         "source": "I.XXIII.3–6 (A-HT-VAULT-002…005, B1-XXIII-GIUDICIO)",
         "value": f"ausgeführt ≈ 61–62 Fuß; arithmetisch {am:.1f}, geometrisch {gm:.1f}, harmonisch {hm:.1f}",
         "verdict": "keines der drei Mittel; 'altre altezze … secondo il suo giudicio'"},
    ]
    return checks


def run(out_dir: Path) -> dict:
    data = load()
    f = feet(data)
    rs = rooms(f)
    palladio_rooms = [r for r in rs if r["palladio_time"]]
    hits = sum(r["within_1_percent"] for r in palladio_rooms)
    chance = continuous_share(PALLADIO_I21, TOL * 100)
    result = {"rooms": rs, "checks": rule_checks(f),
              "seven_forms": {"hits": hits, "n": len(palladio_rooms), "chance": round(chance, 4),
                              "p_at_least": round(binomial_upper_tail(hits, len(palladio_rooms), chance), 5)}}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "analysis.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="San Giorgio Maggiore against Palladio's rules")
    parser.add_argument("--out", type=Path, default=ROOT / "output/san_giorgio")
    result = run(parser.parse_args().out)
    for r in result["rooms"]:
        print(f"{r['space']:40s} {r['a']:7.2f} × {r['b']:6.2f}  {r['ratio']:.3f}  ~{r['nearest']} {100*r['deviation']:+.1f} %")
    s = result["seven_forms"]
    print(f"seven forms within 1 %: {s['hits']}/{s['n']} (chance {s['chance']:.0%}, p = {s['p_at_least']})")
    for c in result["checks"]:
        print(f"- {c['rule']}: {c['value']} → {c['verdict']}")


if __name__ == "__main__":
    main()
