# 8. Buch II: Was Palladio selbst über Raumhöhen sagt

Stand: 30.09.2026 · Daten: `data/book2/text_statements.json` · Auswertung:
`output/book2/text_summary.json` (`python -m palladio_code.book2`) · Scanbelege:
`output/book2/proof_regions.json` (`python -m palladio_code.proofs data/book2/text_statements.json`)

## Vorgehen

1. Der vollständige Text von Buch II (Druck 1570, e-rara) wurde gelesen.
2. Jede Aussage zu Raumverhältnis, Deckenart und Raumhöhe wurde als Zitat mit
   Bauwerk, Druckseite und Bildnummer erfasst: **31 Stellen, 65 Einzelangaben,
   27 Bauten** (eigene Bauten, nicht ausgeführte Entwürfe, antike Rekonstruktionen).
3. Jede Stelle wurde über die ALTO-Wortkoordinaten auf dem Scan lokalisiert, als
   Bildausschnitt aus dem IIIF-Dienst geladen und gegen die Transkription gelesen.
   Die Texterkennung dient nur zum Auffinden, nie als Zitat.
4. Korrekturen am Scan: u. a. Palladios Entwurf für Venedig (S. 72) nennt
   „uentitre piedi“ (23 Fuß); die Texterkennung hatte daraus „uentiti c“ gemacht.

Die Tabellen von Howard/Longair (1982) und Mitrović (1990) wurden nicht verwendet.

## Befunde (nur Palladios eigene Worte)

**1. Wenn Palladio ein Höhenverfahren nennt, ist es meist das erste.**
Von elf ausdrücklich benannten Gewölbeverfahren sind sieben das erste
(arithmetisches Mittel), je zwei das zweite (geometrisch) und das dritte bzw.
„letzte“ (harmonisch). Dazu kommt zweimal die Regel für quadratische Räume
(Breite plus ein Drittel). Die Namen „arithmetisch“ usw. verwendet Palladio
nicht; er verweist auf die „modi“ aus Buch I, Kap. XXIII.

**2. Flachdecken: Höhe gleich Breite, ohne Ausnahme im Text.**
Siebenmal steht „alte quanto larghe“ (Antonini, Valmarana, Pisani Bagnolo,
Saraceno, Angarano, Mocenigo an der Brenta u. a.). Keine Textstelle widerspricht.

**3. Gleiche Gewölbehöhen benachbarter Räume sagt Palladio ausdrücklich.**
Chiericati (die mittleren Räume „so hoch wie die großen“), Mocenigo in Marocco
(21 Fuß für große und mittlere Räume), Saraceno (Saal und Kammern gleich hoch wie
die Hauptzimmer), Barbarano („di tutti questi luoghi“ 21½ Fuß). Die Regel aus
Buch I, Kap. XXIII (gleiche Gewölbe über verschieden großen Räumen) ist in Buch II
also nicht nur erschließbar, sondern an fünf Bauten wörtlich belegt.

**4. Buch II kennt Höhenregeln, die in Buch I fehlen.**
- Saal gewölbt, Höhe = 1½ Breite (Pisani in Bagnolo, Poiana);
- Kämpfer in Höhe der Breite, Stich ⅓ der Breite (Mocenigo an der Brenta; antike
  Rekonstruktionen), rechnerisch wieder 4/3;
- Kammern und Gang „zwei Quadrate“ hoch (Pisani in Montagnana);
- oberer Saal = Breite plus Gesimsstärke (Garzadore).
Diese Angaben sind Kandidaten für neue A-Regeln (ausdrücklich, belegt), aber
jeweils an einen Bau gebunden; ihre Verallgemeinerung wäre B.

**5. Die Geschossregel aus Buch I wird in den Zahlenbeispielen nicht eingehalten.**
Buch I verlangt, dass obere Räume um ein Sechstel niedriger sind (Faktor 5/6 ≈ 0,83).
Die beiden einzigen Zahlenangaben aufeinanderfolgender Geschosse in Buch II:
20 → 18 Fuß (0,90) und 23 → 18 Fuß (0,78). Beide weichen ab. Zwei Fälle genügen
nicht für eine Regel, zeigen aber, dass Palladio die Sechstelregel nicht mechanisch
anwendet.

**6. Nicht-musikalische Raumverhältnisse stehen im Text selbst.**
Genannt werden 5:3 (6×), 1:1 (5×), 3:2 (4×), 7:4 (2×), 13:8, 2:1, 5:2 (je 1×).
7:4, 13:8 und 5:2 gehören nicht zu den sieben Formen aus Buch I, Kap. XXI.

## Grenzen

- Der Text nennt Höhen nur für einen Teil der Räume; die übrigen Bauten sagen
  nur „in uolto“ oder „in solaro“.
- Ob die genannten Verfahren zu den Maßen der Holzschnitte passen, ist damit noch
  nicht geprüft. Das ist der nächste Schritt.

## Nächster Schritt

Maßzahlen der Grundrisse am Scan lesen, zunächst für die Bauten mit Höhenangabe
(Barbarano, Mocenigo Marocco, Chiericati, Cornaro, Pisani Montagnana, Saraceno,
Trissino, Garzadore, die Entwürfe S. 71–72), und dann für jede Angabe prüfen,
welches Mittel die genannte Höhe erzeugt, abgesichert gegen das Nullmodell (Kap. 7).
