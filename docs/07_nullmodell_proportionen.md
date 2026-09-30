# 7. Nullmodell: Was ist ein Proportionstreffer wert?

Stand: 30.09.2026 · Code: `src/palladio_code/nullmodel.py` · Ergebnis:
`output/nullmodel/nullmodel_results.json` · Aufruf: `make nullmodel`

## Forschungslücke

Seit Wittkower (1949) wird geprüft, ob Palladios Grundrisse in Buch II seinen
Raumverhältnissen aus Buch I, Kap. XXI, oder musikalischen Intervallen folgen
(Howard/Longair 1982; Mitrović 1990, 2001, 2004; March 1998, 2015; Tikhonova 2019;
Hales 2022). In der eingesehenen Literatur fehlt durchgehend eine Angabe, wie viele
Treffer **ohne jede Proportionsabsicht** zu erwarten wären. Howard/Longair bestimmen
eine Zufallsrate nur für einzelne „harmonische Zahlen“, nicht für Verhältnisse.

Einschränkung: Die Nexus-Artikel (Tikhonova, Wassell, March 2015, Hales) und die
Monographien (Mitrović 2004, March 1998, Bürklin/Ebert 2024) sind noch nicht im
Volltext gelesen. Die Lücke ist gut begründet, aber nicht abschließend gesichert.

## Methode

Räume werden als Rechtecke mit Breite ≤ Länge auf einem Raster bauüblicher Maße
vollständig aufgezählt (keine Zufallsstichprobe, daher exakt reproduzierbar):

| Raster | Breite | Schritt | Länge/Breite | Räume |
|---|---|---|---|---:|
| `half_feet_8_40_r2` (Standard) | 8–40 Fuß | ½ Fuß | ≤ 2 | 3185 |
| `whole_feet_8_40_r2` | 8–40 Fuß | 1 Fuß | ≤ 2 | 825 |
| `half_feet_10_30_r2` | 10–30 Fuß | ½ Fuß | ≤ 2 | 1681 |
| `half_feet_8_40_r2.5` | 8–40 Fuß | ½ Fuß | ≤ 2,5 | 4729 |

Gezählt wird der Anteil der Räume, deren Verhältnis innerhalb einer relativen
Toleranz an **irgendeinem** Zielverhältnis liegt. Zielmengen:

- `palladio_I21`: 1:1, √2:1, 4:3, 3:2, 5:3, 2:1 (Buch I, Kap. XXI; A-PROP-ROOM-001)
- `just_octave`: reine Intervalle einer Oktave (12 Werte)
- `I21_plus_just`: Vereinigung beider
- `everything_proposed`: zusätzlich √3, Goldener Schnitt, 7:4, 13:8

Das Raster ist eine Annahme, keine Quelle. Deshalb werden vier Raster und eine
analytische Gleichverteilung verglichen; die Befunde sind über alle stabil.

## Ergebnisse (Standardraster)

Anteil zufällig gewählter Räume, die „passen“:

| Zielmenge | exakt | 0,5 % | 1 % | 2 % | 3 % |
|---|---:|---:|---:|---:|---:|
| Palladio I.21 (6 Verhältnisse) | 6,4 % | 9,9 % | 16,2 % | 31,1 % | 45,2 % |
| reine Intervalle (12) | 8,7 % | 17,4 % | 31,1 % | 58,7 % | 78,7 % |
| I.21 + Intervalle | 8,7 % | 18,9 % | 33,5 % | 64,3 % | 86,8 % |
| alles Vorgeschlagene | 9,5 % | 24,6 % | 41,1 % | 72,7 % | 95,1 % |

**Lesart:** Wer bei 2 % Toleranz alle in der Literatur vorgeschlagenen Verhältnisse
zulässt, findet bei fast drei Vierteln beliebiger Räume einen „Treffer“, bei 3 %
Toleranz bei 95 %.

## Prüfung publizierter Behauptungen

Die Zahlen der Autoren werden zitiert, nicht neu gemessen.

1. **Palladios eigene Formen sind echt bevorzugt.** Howard/Longair zählen 82 von
   153 Hauptzimmern mit *exakt* einem I.21-Verhältnis. Zufällig zu erwarten wären
   etwa 10 (6,4 %); die Wahrscheinlichkeit für ≥ 82 liegt bei etwa 10⁻⁵⁵. Auch mit
   dem ungünstigsten Raster (ganze Fuß, 12,7 % Zufallsrate) liegt die Wahrscheinlichkeit bei etwa 10⁻³³. Palladios
   Vorliebe für seine sieben Formen ist damit statistisch gesichert.
2. **Toleranzbasierte Trefferquoten sagen wenig.** Tikhonova (2019) berichtet
   93 % innerhalb von 2 % Toleranz. Das Nullmodell erreicht bei 2 % bereits 31 %
   (nur I.21) bis 73 % (alle Vorschläge). Ihre eigene Zielmenge („Quadrate und
   ihre Teile“) muss im Volltext geprüft werden; je größer sie ist, desto näher
   rückt die Zufallsrate an 93 %.
3. **√3 an der Rotonda ist kein starker Beleg.** Mitrović (1990) nennt 26:15 „nur
   0,07 %“ von √3 entfernt und sechs Räume nahe √3. Unter Räumen, die ohnehin
   innerhalb von 2 % um √3 liegen, erreichen 1,8 % (½-Fuß-Raster) bzw. 2,9 %
   (¼-Fuß-Raster) diese Nähe. Dass der beste von sechs Räumen sie erreicht, ist mit
   11–16 % Wahrscheinlichkeit schon zufällig zu erwarten.
4. **√2 an der Villa Ragona bleibt offen.** 21¼ : 15 liegt 0,17 % von √2 entfernt;
   zufällig erreichen das 6–7 % der Räume nahe √2. Bemerkenswert ist eher der
   seltene Viertelfuß, den Palladio hier setzt; das ist ein Indiz, kein Beweis.

## Grenzen

- Das Nullmodell behandelt Räume als unabhängig. In Palladios Grundrissen hängen
  Räume über gemeinsame Wände und Symmetrie zusammen.
- Die Gleichverteilung auf dem Raster ist eine Idealisierung. Bauliche Zwänge
  (Balkenlängen, Mauerstärken, Grundstück) können bestimmte Maße bevorzugen.
- Die Befunde 1–4 prüfen Zahlen aus der Literatur. Sie ersetzen nicht die eigene
  Erhebung aus dem Druck von 1570.

## Nächster Schritt

Eigene Datengrundlage aus dem Scan (e-rara, DOI 10.3931/e-rara-363), unabhängig von
den Tabellen von 1982 und 1990:

1. alle Raum- und Höhenangaben im **Text** von Buch II mit Zitat und Fundstelle;
2. die **Maßzahlen auf den Holzschnitten**, am Scan gelesen;
3. Test der Höhenregeln aus Buch I, Kap. XXIII (flach h = b; gewölbt 4/3 bzw. drei
   Mittel; gleiche Höhe benachbarter Räume) gegen das Nullmodell.
