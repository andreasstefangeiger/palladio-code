# 10. Buch II: Gesamtauswertung der Grundrisse

Stand: 01.10.2026 · Daten: `data/book2/plate_readings.json` (86 Lesungen, 32 Bauten)
· Auswertung: `python -m palladio_code.rooms` → `output/book2/room_analysis.json`

## Datengrundlage

Alle lesbaren Grundrisse eigener Bauten und Entwürfe in Buch II (S. 4–78) wurden am
e-rara-Scan gelesen, nur Hauptwohnräume (ohne Loggien, Höfe, Treppen,
Wirtschaftsflügel). Für die Auswertung zählen Lesungen mit Sicherheit „mittel“
oder „hoch“, symmetrische Wiederholungen einmal: **79 Räume**.
Noch nicht gelesen: Trissino (Meledo), Repeta, Thiene (Quinto), Sarego (Santa
Sofia), die antiken Rekonstruktionen.

Die Tabellen von Howard/Longair (1982) und Mitrović (1990) wurden nicht benutzt.

## Befund 1: Palladios sieben Formen – unabhängig bestätigt

45 von 79 Räumen (57 %) haben exakt ein Verhältnis aus Buch I, Kap. XXI
(1:1 22×, 3:2 9×, 2:1 7×, 5:3 5×, 4:3 2×). Zufällig wären 6–13 % zu erwarten
(Nullmodell, Kap. 7); p ≈ 10⁻²⁰ bis 10⁻³³. Howard/Longair fanden 54 % (82/153).
Unsere eigene Erhebung bestätigt ihren Befund damit unabhängig.

## Befund 2: Gleiche Gewölbehöhen – echt, aber nicht unabhängig von der Raumform

In 17 Paaren liegt ein Langraum neben einem Quadratraum gleicher Breite. In 9
Paaren ergibt eines der drei Mittel des Langraums die Höhe des Quadratraums
(Breite + ⅓) auf 1 % genau: sechsmal das arithmetische, zweimal das harmonische,
einmal das geometrische Mittel.

| Vergleich | Erwartung | p für ≥ 9 von 17 |
|---|---:|---:|
| Raumverhältnis beliebig zwischen 1 und 2 | 18 % | 0,001 |
| Raumverhältnis zufällig aus Palladios bevorzugten Formen | 40 % | 0,20 |

**Lesart:** Gegen beliebige Raumformen ist das Zusammentreffen deutlich. Es folgt
aber fast vollständig aus Palladios Vorliebe für 5:3 und 2:1: Bei 5:3 liefert das
arithmetische, bei 2:1 das harmonische Mittel genau 4/3 der Breite. Das hat
Mitrović (1990) algebraisch gezeigt. Die Daten können nicht trennen, ob Palladio
die Raumform wegen der gleichen Höhe wählte oder umgekehrt; beides ist dieselbe
Ordnung, von zwei Seiten gesehen.

**Korrektur zu Kap. 9:** Die dort genannte gemeinsame Wahrscheinlichkeit
(5 · 10⁻⁶) setzte beliebige Raumlängen voraus. Unter Berücksichtigung der
Formvorliebe ist der Befund nicht mehr auffällig. Kap. 9 bleibt als Einzelfallprüfung
gültig, die Gesamtaussage gilt in der Form dieses Kapitels.

Neu gegenüber Mitrović (der die Regel in vier Bauten sah): Die Gleichheit ist in
acht Bauten erfüllt (Chiericati, Cornaro, Pisani in Montagnana, Badoer, Emo,
Poiana, Sarego in La Miga, Mocenigo an der Brenta), und Palladio sagt sie in fünf
Bauten wörtlich (Kap. 8).

## Befund 3: Die Abweichungen von 5:3 liegen fast alle in einem Band um 5:3

Die nicht-kanonischen Hauptzimmer 26 × 16, 26½ × 16, 27 × 16 und 28 × 16
(Mocenigo, Cornaro, Badoer, Saraceno, Emo, Sarego, Pisani) liegen zwischen 1,63 und
1,75. Mit dem arithmetischen (bzw. bei 28 × 16 dem geometrischen) Mittel ergeben sie
alle Gewölbehöhen innerhalb von 1,6 % der Quadrathöhe 21⅓. Die Breite 16 Fuß und
eine Gewölbehöhe um 21 Fuß scheinen das feste Maß zu sein; die Raumlänge variiert
darum herum. Das ist eine Beobachtung, keine Regel Palladios.

## Hypothese 7:4 (aus Kap. 9) – Stand

Nur ein Raum mit 7:4 hat ein genanntes Verfahren (Pisani, Montagnana: geometrisch,
0,8 % von 4/3). Bei Cornaro nennt der Text 7:4 mit dem arithmetischen Verfahren, die
Tafel zeigt 26½. Die Hypothese bleibt möglich, ist aber mit einem Fall nicht
belegbar. Status unverändert: B-Hypothese, nicht als Regel zu behaupten.

## Grenzen

- Lesungen am Scan mit Unsicherheit; die Zuordnung von Länge und Breite folgt
  teils aus der Plangeometrie.
- Gleiche Höhe wurde nur zwischen Langraum und Quadratraum gleicher Breite geprüft.
- Vier Grundrisse fehlen noch.

## Nächster Schritt

Unabhängige Kontrolle: unsere Lesungen gegen die Tabellen von Howard/Longair
(Anhang A4) und Mitrović (Tab. 1) abgleichen und jede Abweichung am Scan klären.
