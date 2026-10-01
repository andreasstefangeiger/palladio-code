# 12. Entwurfsprozess nach Palladio – Entwurfskern

Stand: 01.10.2026 · Code: `src/palladio_code/design.py` · Aufruf: `make design`
oder `python -m palladio_code.design --params meine_parameter.json` → `output/design/`

## Idee

Ein Entwurf entsteht in der Reihenfolge, in der Palladio die Dinge selbst behandelt.
Jede Entscheidung wird mit ihren Regeln und deren Evidenzklasse protokolliert; was
nicht eingehalten wird, erscheint als **Abweichung**, nicht als Fehler. Der Kern
erfindet keine Regeln: Er nutzt die geprüften A-Regeln (Buch I, Kap. XXI, XXIII,
XXV), die gekennzeichneten B-Rekonstruktionen und die am Scan belegte Stelle
Buch II, Kap. II (`B2-CAP2-1`).

## Die Schritte

| Schritt | Entscheidung | Regeln |
|---|---|---|
| 1 Bezugsmaß | Flügelbreite (Standard 16 Fuß), Mauerstärke als **Annahme** | B-SYS-MOD-001 |
| 2 Zentrum | Sala in der Mitte, höchstens zwei Quadrate | A-ORG-CEN-001, A-DIM-HALL-001 |
| 3 Symmetrie | rechter Flügel = linker | A-ORG-SYM-001 |
| 4 Raumfolge | groß – mittel – klein, nebeneinander; Formen aus den sieben | B2-CAP2-1, A-PROP-ROOM-001 |
| 5 Höhen | Flachdecke = Breite; Quadrat Breite + ⅓; Langraum: das Mittel, das die Reihe gleich hoch macht; kleine Räume erhalten Zwischengeschosse | A-HT-ROOM-001, A-HT-VAULT-001…005, B-SYS-VAULT-001 |
| 6 Obergeschoss | ⅙ niedriger (mit Hinweis auf Palladios eigene Abweichungen) | A-HT-STORY-001 |
| 7 Öffnungen | Fenster ⅕–¼ der Raumbreite, Höhe 2⅙ ihrer Breite, oben ⅙ kleiner, Achsen übereinander, Türen 3 × 6½ | A-DIM-WIN-001…003, A-ORG-OPEN-001, A-LOC-WIN-001, A-DIM-DOOR-001 |
| 8 Prüfen | Liste aller Entscheidungen mit Status; ähnlichster Bau Palladios aus `plate_readings.json` | – |

Status je Entscheidung: `follows` (Regel erfüllt), `approx` (innerhalb 1 %, etwa
durch Runden auf halbe Fuß), `deviation` (bewusst abweichend), `assumption`
(keine Regel bei Palladio).

## Ergebnis mit Standardwerten

Flügel 26½ × 16 (5:3, gerundet wie bei Palladio), 16 × 16, 16 × 12 (4:3);
Gewölbe 21¼ und 21⅓ Fuß (Spanne 0,4 %); Kammer 14 Fuß mit Zwischengeschoss;
Sala 57½ × 34½; Obergeschoss 17,8 Fuß; Fenster 3½ × 7,6 Fuß. Ähnlichster Bau:
Villa Mocenigo in Marocco (26 × 16, 16 × 16, 16 × 10).

## Prüfung an Palladio selbst

Der Test `test_chiericati_is_reproduced` erzeugt mit Breite 18 und der Folge
5:3 – 1:1 – 3:2 exakt die Räume des Palazzo Chiericati (30 × 18, 18 × 18, 18 × 12)
und die gleichen Gewölbehöhen von 24 Fuß, die Palladio dort angibt.

## Grenzen

- Nur Villenblock mit einem Hauptgeschoss, Sala als Rechteck; keine Loggien,
  Treppen, Rundsäle.
- Die Lage von Fenstern und Türen ist als Regel protokolliert, aber noch nicht
  gezeichnet.
- Mauerstärke ist eine Annahme.

## Nächster Schritt

Die iPad-Oberfläche: dieselben acht Schritte als Spiel mit Pencil, Klang und
Begründung zu jeder Entscheidung, ausgehend von diesem Kern.
