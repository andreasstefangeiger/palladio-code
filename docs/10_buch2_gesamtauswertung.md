# 10. Buch II: Gesamtauswertung der Grundrisse

Stand: 17.11.2026 · Daten: `data/book2/plate_readings.json` (86 Lesungen, 32 Bauten),
`data/book2/completion.json`
· Auswertung: `python -m palladio_code.rooms` → `output/book2/room_analysis.json`

## Datengrundlage

Alle lesbaren Grundrisse eigener Bauten und Entwürfe in Buch II (S. 4–78) wurden am
e-rara-Scan gelesen, nur Hauptwohnräume (ohne Loggien, Höfe, Treppen,
Wirtschaftsflügel). Für die Auswertung zählen Lesungen mit Sicherheit „mittel“
oder „hoch“, symmetrische Wiederholungen einmal: **79 Räume**.
Noch nicht gelesen: Trissino (Meledo), Repeta, Thiene (Quinto), Sarego (Santa
Sofia), die antiken Rekonstruktionen.

Die Tabellen von Howard/Longair (1982) und Mitrović/Djordjević (1990) wurden nicht benutzt.

## Befund 1: Palladios sieben Formen – unabhängig bestätigt

43 von 79 Räumen (54 %) haben exakt ein Verhältnis aus Buch I, Kap. XXI
(1:1 21×, 3:2 9×, 2:1 6×, 5:3 5×, 4:3 2×). Zufällig wären 6–13 % zu erwarten
(Nullmodell, Kap. 7); p ≈ 10⁻²⁰ bis 10⁻³³. Howard/Longair fanden ebenfalls 54 % (82/153).
Unsere eigene Erhebung bestätigt ihren Befund damit unabhängig.

## Befund 2: Gleiche Gewölbehöhen – echt, aber nicht unabhängig von der Raumform

In 16 Paaren liegt ein Langraum neben einem Quadratraum gleicher Breite. In 8
Paaren ergibt eines der drei Mittel des Langraums die Höhe des Quadratraums
(Breite + ⅓) auf 1 % genau: sechsmal das arithmetische, je einmal das harmonische
und das geometrische Mittel.

| Vergleich | Erwartung | p für ≥ 8 von 16 |
|---|---:|---:|
| Raumverhältnis beliebig zwischen 1 und 2 | 18 % | 0,004 |
| Raumverhältnis zufällig aus Palladios bevorzugten Formen | 40 % | 0,28 |

**Lesart:** Gegen beliebige Raumformen ist das Zusammentreffen deutlich. Es folgt
aber fast vollständig aus Palladios Vorliebe für 5:3 und 2:1: Bei 5:3 liefert das
arithmetische, bei 2:1 das harmonische Mittel genau 4/3 der Breite. Das hat
Mitrović/Djordjević (1990) algebraisch gezeigt. Die Daten können nicht trennen, ob Palladio
die Raumform wegen der gleichen Höhe wählte oder umgekehrt; beides ist dieselbe
Ordnung, von zwei Seiten gesehen.

**Korrektur zu Kap. 9:** Die dort genannte gemeinsame Wahrscheinlichkeit
(5 · 10⁻⁶) setzte beliebige Raumlängen voraus. Unter Berücksichtigung der
Formvorliebe ist der Befund nicht mehr auffällig. Kap. 9 bleibt als Einzelfallprüfung
gültig, die Gesamtaussage gilt in der Form dieses Kapitels.

Neu gegenüber Mitrović (der die Regel in vier Bauten sah): Die Gleichheit ist in
sieben Bauten erfüllt (Chiericati, Cornaro, Pisani in Montagnana, Badoer, Emo,
Poiana, Sarego in La Miga), und Palladio sagt sie in fünf
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

## Nachtrag vom 17.11.2026: unvollendete Bauten und Entwürfe

Palladio sagt in der Vorrede zu Buch II, einige gezeichnete Bauten seien nicht
fertig. Aus dem Gebauten lasse sich aber erkennen, wie das fertige Werk sein solle
(II.III.7). Deshalb wurde für jeden gemessenen Bau geprüft, was der Text über
seinen Stand sagt (`data/book2/completion.json`, elf Stellen, am Scan gelesen).

- **Unvollendet oder begonnen, nach Palladio:**
  - Palazzo Porto: nur „quella parte di fabrica, ch'è stata fatta“; der Hof steht
    im Futur („hauerà le colonne“).
  - Palazzo della Torre (Verona): Der Bauherr starb, der Bau ist zu „vna buona
    parte“ fertig.
  - Palazzo Thiene: Der Vater gab ihm „principio“; der Hauptsaal steht im Futur
    („ui sarà la Sala maggiore“); nur einige Räume sind „hora … finite“.
  - Palazzo Capra: begonnen, alles Übrige im Futur.
  - Palazzo Barbarano: begonnen. Palladio sagt außerdem, dass der gedruckte
    Grundriss **nicht** der zuletzt beschlossene ist. Den neuen habe er nicht
    rechtzeitig schneiden lassen können: „Non ho posto ancho il disegno della
    pianta, secondo che è stato ultimamente concluso, e secondo che sono hormai
    state gettate le fondamenta“ (S. 22).
  - Villa Thiene in Cigogna: vom Vater „principiata“; zum Stand sagt Palladio nichts.
- **Entwürfe:** Die „inuentioni“ von Kap. XVII sind nach II.XVII.1 nicht ausgeführt.
- **Keine Angabe:** Alle übrigen 18 Bauten. Das beweist nicht, dass sie 1570 fertig
  waren.

| Gruppe | Räume | genau eine der sieben Formen |
|---|---:|---:|
| unvollendet oder begonnen (6 Bauten) | 18 | 9 (50 %) |
| keine Angabe (18 Bauten) | 49 | 27 (55 %) |
| Entwürfe aus Kap. XVII (7) | 12 | 7 (58 %) |

- **Befund.** Die Vorliebe für die sieben Formen hängt nicht davon ab, ob ein Bau
  stand, begonnen oder nur entworfen war. Das passt zu dem, was die Tafeln sind:
  Palladios Entwürfe, nicht Bauaufnahmen. Befund 1 gilt deshalb für seine
  Entwurfspraxis, wie schon oben formuliert.
- **Palazzo Barbarano:** Seine drei Räume beschreiben einen überholten Entwurf.
  Weil sie wie die übrigen Entwürfe zählen, ändert das den Befund nicht. Für einen
  Vergleich mit dem gebauten Palast taugen sie nicht.

## Grenzen

- Lesungen am Scan mit Unsicherheit; die Zuordnung von Länge und Breite folgt
  teils aus der Plangeometrie.
- Gleiche Höhe wurde nur zwischen Langraum und Quadratraum gleicher Breite geprüft.
- Vier Grundrisse fehlen noch.

## Nächster Schritt

Unabhängige Kontrolle: unsere Lesungen gegen die Tabellen von Howard/Longair
(Anhang A4) und Mitrović (Tab. 1) abgleichen und jede Abweichung am Scan klären.


*Stand nach Abgleich mit Mitrović (Kap. 11): Garzadore und Mocenigo an der Brenta korrigiert; Zahlen oben aktualisiert.*
