"""San Giorgio Maggiore against Palladio's own rules, on Bertotti Scamozzi's survey.

Palladio published no plan of San Giorgio. The measured drawings of Ottavio Bertotti Scamozzi
(Le fabbriche e i disegni di Andrea Palladio, IV, plates V–VIII; consulted in the 1846 Genoa
edition) are the oldest published survey with dimensions; they record the built church (C2).
data/san_giorgio/bertotti_scamozzi.json holds the dimensions (labels checked against the scale
bar) and Bertotti's own statements; plate VIII (facade) and plate VI (section) add the orders of
the front and the dome. This module compares them with the scan-checked rules of the Quattro
Libri. data/san_giorgio/criteria.json sets every criterion of the theory (site, form, orders,
material, light ...) against what was built; check_criteria() keeps its references honest.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from .nullmodel import PALLADIO_I21, binomial_upper_tail, continuous_share

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/san_giorgio/bertotti_scamozzi.json"
CRITERIA = ROOT / "data/san_giorgio/criteria.json"
TOL = 0.01


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def feet(data: dict) -> dict[str, float]:
    return {r["id"]: r["feet"] for r in data["plan_readings"]}


def readings(data: dict, key: str) -> dict[str, float]:
    """Bertotti's label where he gives one, otherwise the length scaled from the plate."""
    return {r["id"]: r["feet"] if r.get("feet") is not None else r["scaled_feet"] for r in data[key]}


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


def facade_checks(fr: dict[str, float]) -> list[dict]:
    """Front (plate VIII). Built after Palladio's death on his model (Temanza in Bertotti, p. 23)."""
    h, d, ped, ent = fr["SG-F-COL"], fr["SG-F-D"], fr["SG-F-PED"], fr["SG-F-ENT"]
    side, mid = fr["SG-F-INT-SIDE"], fr["SG-F-INT-MID"]
    body_h = fr["SG-F-BODY-H"]
    return [
        {"rule": "Kompositsäule zehn Moduln", "source": "I.XVIII.1",
         "value": f"{h / d:.1f} Durchmesser (Säule 40:4 Fuß, Durchmesser gemessen {d:.2f} Fuß)",
         "verdict": "erfüllt (Bertotti: 'poco meno di 10')"},
        {"rule": "Postament der Kompositordnung ⅓ der Säule", "source": "I.XVIII.2, I.XIX.3",
         "value": f"{ped / h:.3f} der Säule", "verdict": "erfüllt"},
        {"rule": "Gebälk ⅕ der Säule", "source": "I.XVIII.4", "value": f"{ent / h:.3f} der Säule",
         "verdict": "erfüllt"},
        {"rule": "Gerade Säulenzahl, das Mitteljoch 'alquanto maggiore de gli altri'", "source": "I.XIII.9",
         "value": f"vier Säulen; Mitteljoch {mid / side:.2f}-mal so weit wie die Seitenjoche "
                  f"({side / d:.1f} und {mid / d:.1f} Durchmesser)",
         "verdict": "teilweise: Mitteljoch vorhanden, aber doppelt so weit (Buch IV, Kap. V: 3 zu 2¼)"},
        {"rule": "Säulenabstand bestimmt die Säulenhöhe: 2 D → 9½ D, 1½ D → 10 D", "source": "I.XIII.8",
         "value": f"Seitenjoche {side / d:.1f} D bei Säulen von {h / d:.1f} D",
         "verdict": "zwischen der korinthischen und der kompositen Kopplung"},
        {"rule": "In Tempeln keine Postamente, die Säulen beginnen am Boden", "source": "B4-V-PIEDESTILI",
         "value": "Fassade auf Postamenten von ⅓, Innenraum auf Postamenten von ¼ (SG-T2)",
         "verdict": "nicht erfüllt"},
        {"rule": "Kleine Ordnung: Pilaster 10 Durchmesser, Gebälk ⅕ (Bertotti)", "source": "SG-T6",
         "value": f"{fr['SG-F-MINOR'] / fr['SG-F-MINOR-W']:.1f} Breiten, Gebälk "
                  f"{fr['SG-F-MINOR-ENT'] / fr['SG-F-MINOR']:.3f}",
         "verdict": "bestätigt"},
        {"rule": "Höhe zu Breite des Mittelteils 'una sesta minore' (8:5, Bertotti)", "source": "SG-T6",
         "value": f"{body_h / fr['SG-F-BODY-W-COL']:.2f} über die äußeren Säulen, "
                  f"{body_h / fr['SG-F-BODY-W-PED']:.2f} über das Giebelgesims",
         "verdict": "hängt an der Bezugsbreite; Bertottis Deutung, kein Maß Palladios"},
    ]


def dome_checks(sr: dict[str, float], f: dict[str, float]) -> list[dict]:
    """Crossing dome (plate VI) against the only height rules Palladio gives."""
    w, crown, diameter = f["SG-NAVE-W"], sr["SG-S-DOME-CROWN"], sr["SG-S-DOME-D"]
    return [
        {"rule": "Gewölbte quadratische Räume: Höhe = Breite + ⅓", "source": "I.XXIII.2",
         "value": f"Vierung {w} Fuß → {4 / 3 * w:.1f} Fuß; Kuppelscheitel {crown:.1f} Fuß "
                  f"= {crown / w:.2f} Breiten, schon die Vierungsbögen {sr['SG-S-VAULT']:.1f} Fuß",
         "verdict": "nicht erfüllt (die Regel gilt für Räume, nicht für Vierungskuppeln)"},
        {"rule": "Pantheon: Höhe bis zur Lichtöffnung = Durchmesser", "source": "B4-XX-PANTHEON",
         "value": f"{crown:.1f} : {diameter:.1f} = {crown / diameter:.2f}", "verdict": "nicht erfüllt"},
        {"rule": "Kuppeldurchmesser und Vierung", "source": "SG-S-DOME-D, SG-NAVE-W",
         "value": f"innen {diameter:.1f} Fuß, Vierung {w} Fuß; Schale innen eine Halbkugel",
         "verdict": "Befund ohne Regel"},
    ]


def load_criteria() -> dict:
    return json.loads(CRITERIA.read_text(encoding="utf-8"))


def known_ids(data: dict) -> set[str]:
    """Ids a criterion may cite: rule catalogue, Book III/IV statements, Bertotti readings and text."""
    ids = {r["id"] for path in (ROOT / "data/rules").glob("book*.json")
           for r in json.loads(path.read_text(encoding="utf-8"))["rules"]}
    ids |= {s["id"] for s in json.loads((ROOT / "data/book4/text_statements.json")
                                       .read_text(encoding="utf-8"))["statements"]}
    for key in ("plan_readings", "facade_readings", "section_readings", "text_statements"):
        ids |= {r["id"] for r in data[key]}
    return ids


def check_criteria(criteria: dict, data: dict) -> list[str]:
    problems, known = [], known_ids(data)
    for c in criteria["criteria"]:
        if c["verdict"] not in criteria["verdicts"]:
            problems.append(f"{c['id']}: unknown verdict {c['verdict']}")
        if not c["theory"]["sources"] and c["verdict"] != "keine Regel":
            problems.append(f"{c['id']}: no source for the theory")
        for ref in c["theory"]["sources"] + c["built"]["sources"]:
            if ref not in known:
                problems.append(f"{c['id']}: unknown reference {ref}")
    return problems


def run(out_dir: Path) -> dict:
    data = load()
    f = feet(data)
    rs = rooms(f)
    palladio_rooms = [r for r in rs if r["palladio_time"]]
    hits = sum(r["within_1_percent"] for r in palladio_rooms)
    chance = continuous_share(PALLADIO_I21, TOL * 100)
    criteria = load_criteria()
    problems = check_criteria(criteria, data)
    if problems:
        raise ValueError("; ".join(problems))
    result = {"rooms": rs, "checks": rule_checks(f),
              "facade": facade_checks(readings(data, "facade_readings")),
              "dome": dome_checks(readings(data, "section_readings"), f),
              "criteria_verdicts": dict(Counter(c["verdict"] for c in criteria["criteria"])),
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
    for group in ("checks", "facade", "dome"):
        print(f"[{group}]")
        for c in result[group]:
            print(f"- {c['rule']}: {c['value']} → {c['verdict']}")
    print("criteria:", ", ".join(f"{k} {v}" for k, v in result["criteria_verdicts"].items()))


if __name__ == "__main__":
    main()
