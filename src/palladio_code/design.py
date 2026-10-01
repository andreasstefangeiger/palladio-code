"""Step-by-step design process after Palladio (villa block, one main floor).

The process follows the order in which Palladio treats the matter in Book I
(ch. XXI rooms, XXIII heights, XXV openings) and Book II (ch. II sequence of rooms).
Every decision is recorded with the rules it rests on and their evidence class;
nothing is decided silently. Rules the design does not meet are reported as
deliberate deviations, never hidden.

Units: Vicentine feet. Walls are an explicit assumption (Palladio's woodcuts give
clear room dimensions; wall thicknesses vary, see docs/10).
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path

from .heights import METHODS, rel_dev, square_rule

ROOT = Path(__file__).resolve().parents[2]

# Book I, ch. XXI: the seven forms (round excluded for this rectangular planner)
SEVEN_FORMS = {"1:1": 1.0, "4:3": 4 / 3, "sqrt2:1": 2 ** 0.5, "3:2": 1.5, "5:3": 5 / 3, "2:1": 2.0}
TOLERANCE = 0.01

# Book II, ch. II (B2-CAP2-1, scan-checked): stanze grandi, mediocri, e picciole,
# l'una a canto l'altra. Default wing: large oblong, square, small room. The wing
# width (module) is shared; a large room extends it, a small room shortens it.
DEFAULT_WING = [{"form": "5:3", "size": "grande"},
                {"form": "1:1", "size": "mediocre"},
                {"form": "4:3", "size": "picciola"}]  # 16 x 12: Foscari, Saraceno, Sarego


@dataclass
class Decision:
    step: int
    topic: str
    decision: str
    rules: list[str]
    status: str = "follows"  # follows | approx | deviation | assumption
    note: str = ""


@dataclass
class Room:
    name: str
    form: str
    width: float  # dimension shared by the wing (along the facade)
    depth: float
    ceiling: str = "vault"
    height: float | None = None
    height_rule: str | None = None
    x: float = 0.0
    y: float = 0.0

    @property
    def length(self) -> float:
        return max(self.width, self.depth)

    @property
    def breadth(self) -> float:
        return min(self.width, self.depth)

    @property
    def ratio(self) -> float:
        return self.length / self.breadth


@dataclass
class Design:
    params: dict
    rooms: list[Room] = field(default_factory=list)
    sala: Room | None = None
    decisions: list[Decision] = field(default_factory=list)
    windows: dict = field(default_factory=dict)
    upper_floor: dict = field(default_factory=dict)

    def log(self, *args, **kwargs) -> None:
        self.decisions.append(Decision(*args, **kwargs))


def snap(value: float, step: float = 0.5) -> float:
    return round(value / step) * step


def form_ratio(form: str) -> float:
    if form not in SEVEN_FORMS:
        raise ValueError(f"unknown form {form!r}; choose one of {sorted(SEVEN_FORMS)}")
    return SEVEN_FORMS[form]


def choose_vault_height(length: float, breadth: float, target: float | None) -> tuple[float, str]:
    """Square: width + 1/3. Oblong: the mean closest to the row target (or the first mean)."""
    if length == breadth:
        return square_rule(breadth), "I23_square_4_3"
    options = {m: f(length, breadth) for m, f in METHODS.items()}
    if target is None:
        return options["I23_first"], "I23_first"
    method = min(options, key=lambda m: rel_dev(options[m], target))
    return options[method], method


def run_design(params: dict) -> Design:
    d = Design(params=params)
    w = float(params.get("module", 16))
    wing = params.get("wing", DEFAULT_WING)
    wall = float(params.get("wall", 1.5))
    ceiling = params.get("ceiling", "vault")

    # Step 1: module
    d.log(1, "Bezugsmass", f"Raumbreite der Fluegel {w:g} Fuss",
          ["B-SYS-MOD-001"], "follows",
          "Palladios Hauptzimmer in Buch II sind meist 16-18 Fuss breit (docs/10).")
    d.log(1, "Mauerstaerke", f"{wall:g} Fuss", [], "assumption",
          "Palladio gibt in Buch II keine Regel; Holzschnitte zeigen etwa 1-2 1/2 Fuss.")

    # Step 4 (before 2/3, because the wing defines the depth): rooms of one wing
    y = wall
    for entry in wing:
        form, size = entry["form"], entry["size"]
        r = form_ratio(form)
        depth = w if r == 1 else snap(w * r if size == "grande" else w / r)
        room = Room(name=size, form=form, width=w, depth=depth, ceiling=ceiling, y=y)
        d.rooms.append(room)
        y += depth + wall
        dev = rel_dev(room.ratio, r)
        status = "follows" if dev < 1e-9 else ("approx" if dev <= TOLERANCE else "deviation")
        note = "" if status == "follows" else (
            f"auf halbe Fuss gerundet: {room.ratio:.4f} statt {r:.4f} "
            "(Palladio rundet ebenso, z. B. 26 1/2 x 16 bei Cornaro, Badoer, Saraceno)")
        d.log(4, "Raumform", f"{room.name}: {room.length:g} x {room.breadth:g} ({form})",
              ["A-PROP-ROOM-001", "B2-CAP2-1"], status, note)
    wing_depth = y
    sizes = [rm.width * rm.depth for rm in d.rooms]  # grande >= mediocre >= picciola
    descending = all(a >= b for a, b in zip(sizes, sizes[1:]))
    d.log(4, "Raumfolge", "gross - mittel - klein, nebeneinander" if descending else "Folge nicht absteigend",
          ["B2-CAP2-1"], "follows" if descending else "deviation")

    # Step 2: centre
    sala_d = wing_depth - 2 * wall
    sala_form = params.get("sala_form", "5:3")
    sala_w = float(params["sala_width"]) if params.get("sala_width") else snap(sala_d / form_ratio(sala_form))
    d.sala = Room("sala", sala_form, sala_w, sala_d, ceiling=params.get("sala_ceiling", "vault"),
                  x=wall + w + wall, y=wall)
    two_squares = d.sala.ratio <= 2 + 1e-9
    d.log(2, "Zentrum", f"Sala in der Mitte, {d.sala.length:g} x {d.sala.breadth:g}",
          ["A-ORG-CEN-001", "A-DIM-HALL-001"], "follows" if two_squares else "deviation",
          f"Laenge/Breite {d.sala.ratio:.2f}" + ("" if two_squares else " - mehr als zwei Quadrate"))

    # Step 3: symmetry (by construction)
    for room in d.rooms:
        room.x = wall
    d.log(3, "Symmetrie", "rechter Fluegel spiegelt den linken", ["A-ORG-SYM-001"], "follows")

    # Step 5: heights
    squares = [rm for rm in d.rooms if rm.length == rm.breadth]
    target = square_rule(squares[0].breadth) if (squares and ceiling == "vault") else None
    for room in d.rooms:
        if room.ceiling == "flat":
            room.height, room.height_rule = room.breadth, "flat_h_eq_w"
            rules = ["A-HT-ROOM-001"]
        else:
            room.height, room.height_rule = choose_vault_height(room.length, room.breadth, target)
            rules = ["A-HT-VAULT-001"] if room.height_rule == "I23_square_4_3" else \
                {"I23_first": ["A-HT-VAULT-002"], "I23_second": ["A-HT-VAULT-003"],
                 "I23_third": ["A-HT-VAULT-004"]}[room.height_rule]
        d.log(5, "Hoehe", f"{room.name}: {room.height:.2f} Fuss ({room.height_rule})", rules)
    # small rooms receive mezzanines (B2-CAP2-1) and are not held to the common height
    heights = [rm.height for rm in d.rooms if rm.ceiling == "vault" and rm.name != "picciola"]
    if len(heights) > 1:
        spread = (max(heights) - min(heights)) / max(heights)
        d.log(5, "Gleiche Gewoelbehoehe", f"Spanne {spread * 100:.1f} %",
              ["A-HT-VAULT-005", "B-SYS-VAULT-001"], "follows" if spread <= TOLERANCE else "deviation",
              "Kleine Raeume ausgenommen: sie erhalten Zwischengeschosse "
              "(B2-CAP2-1: le picciole si amezeranno).")

    # Step 6: upper floor
    main_h = max(heights) if heights else w
    upper = main_h * 5 / 6
    d.upper_floor = {"height": round(upper, 2), "ceiling": "flat"}
    d.log(6, "Obergeschoss", f"{upper:.2f} Fuss, Flachdecke", ["A-HT-STORY-001"], "follows",
          "Palladio selbst weicht in den Zahlenbeispielen von Buch II davon ab (docs/08).")

    # Step 7: openings
    win_w = snap(w / 4.5, 0.25)
    win_h = win_w * 13 / 6
    ok_w = w / 5 - 1e-9 <= win_w <= w / 4 + 1e-9
    d.windows = {"width": win_w, "height": round(win_h, 2), "upper_height": round(win_h * 5 / 6, 2),
                 "door": {"width": 3, "height": 6.5}}
    d.log(7, "Fenster", f"{win_w:g} x {win_h:.2f} Fuss", ["A-DIM-WIN-001", "A-DIM-WIN-002"],
          "follows" if ok_w else "deviation")
    d.log(7, "Fenster oben", f"lichte Hoehe {win_h * 5 / 6:.2f} Fuss", ["A-DIM-WIN-003"])
    d.log(7, "Achsen", "Fenster mittig im Raum, oben ueber unten, rechts wie links",
          ["A-ORG-OPEN-001", "A-LOC-WIN-001"])
    d.log(7, "Tueren", "3 x 6 1/2 Fuss", ["A-DIM-DOOR-001"])
    return d


def nearest_palladio(design: Design, readings: Path) -> dict:
    """Palladio's own building in Book II whose main rooms resemble the design most."""
    data = json.loads(readings.read_text(encoding="utf-8"))
    ours = sorted((rm.length, rm.breadth) for rm in design.rooms)
    best = None
    by_building: dict[str, list] = {}
    for r in data["rooms"]:
        if r["length"] and r["confidence"] != "low":
            by_building.setdefault(r["building"], []).append((r["length"], r["width"]))
    for building, rooms in by_building.items():
        cost = 0.0
        for length, breadth in ours:
            cost += min(abs(length - l2) + abs(breadth - b2) for l2, b2 in rooms)
        if best is None or cost < best[1]:
            best = (building, cost, sorted(set(rooms)))
    return {"building": best[0], "distance_ft": best[1], "rooms": best[2]}


def to_svg(design: Design, scale: float = 8.0) -> str:
    wall = float(design.params.get("wall", 1.5))
    w = design.rooms[0].width
    total_w = wall + w + wall + design.sala.width + wall + w + wall
    total_d = max(rm.y + rm.depth for rm in design.rooms) + wall
    W, H = total_w * scale, total_d * scale
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -20 {W + 40:.0f} {H + 60:.0f}" '
           f'font-family="Georgia, serif" font-size="11">',
           f'<rect x="0" y="0" width="{W:.1f}" height="{H:.1f}" fill="#2b2b2b"/>']

    def rect(x, y, rw, rd, label):
        out.append(f'<rect x="{x * scale:.1f}" y="{y * scale:.1f}" width="{rw * scale:.1f}" '
                   f'height="{rd * scale:.1f}" fill="#faf8f3"/>')
        cx, cy = (x + rw / 2) * scale, (y + rd / 2) * scale
        for k, line in enumerate(label.split("\n")):
            out.append(f'<text x="{cx:.1f}" y="{cy + 13 * k:.1f}" text-anchor="middle" fill="#222">{line}</text>')

    right_x = wall + w + wall + design.sala.width + wall
    for rm in design.rooms:
        label = f"{rm.length:g} x {rm.breadth:g}\n{rm.form}\nh {rm.height:.1f}"
        rect(wall, rm.y, rm.width, rm.depth, label)
        rect(right_x, rm.y, rm.width, rm.depth, label)
    s = design.sala
    rect(s.x, s.y, s.width, s.depth, f"Sala\n{s.length:g} x {s.breadth:g}")
    out.append(f'<text x="0" y="{H + 30:.1f}" fill="#555">Piedi vicentini - Palladio-Code, Entwurfsprozess</text>')
    out.append("</svg>")
    return "\n".join(out)


def report(design: Design, readings: Path) -> dict:
    return {
        "params": design.params,
        "rooms": [{"name": r.name, "form": r.form, "length": r.length, "breadth": r.breadth,
                   "ceiling": r.ceiling, "height": round(r.height, 3), "height_rule": r.height_rule}
                  for r in design.rooms],
        "sala": {"length": design.sala.length, "breadth": design.sala.breadth},
        "upper_floor": design.upper_floor,
        "windows": design.windows,
        "decisions": [d.__dict__ for d in design.decisions],
        "deviations": [d.__dict__ for d in design.decisions if d.status == "deviation"],
        "nearest_palladio_building": nearest_palladio(design, readings),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Palladian step-by-step design process")
    parser.add_argument("--params", type=Path, help="JSON file with module, wing, ceiling, wall, sala_width")
    parser.add_argument("--out", type=Path, default=ROOT / "output/design")
    args = parser.parse_args()
    params = json.loads(args.params.read_text(encoding="utf-8")) if args.params else {}
    design = run_design(params)
    args.out.mkdir(parents=True, exist_ok=True)
    result = report(design, ROOT / "data/book2/plate_readings.json")
    (args.out / "design.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.out / "design.svg").write_text(to_svg(design), encoding="utf-8")
    for dec in design.decisions:
        print(f"[{dec.step}] {dec.topic:22s} {dec.decision:48s} {dec.status:10s} {','.join(dec.rules)}")
    print("aehnlichster Bau Palladios:", result["nearest_palladio_building"]["building"])


if __name__ == "__main__":
    main()
