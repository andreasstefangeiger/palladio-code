# 9. Buch II: Höhenangaben gegen die Maße der Holzschnitte

Stand: 30.09.2026 · Tafelmaße: `data/book2/plate_readings.json` · Test:
`python -m palladio_code.heights` → `output/book2/height_tests.json`

## Vorgehen

Für zehn Bauten mit Höhenangaben im Text (Kap. 8) wurden die Raummaße auf den
Holzschnitten am Scan gelesen (IIIF, volle Auflösung). Gedruckte Zahlen zählen;
spätere Bleistiftnotizen auf einzelnen Scanseiten (z. B. S. 5) werden ignoriert.
Jede Lesung hat eine Sicherheitsstufe (hoch/mittel/niedrig). Die Tabellen von
Howard/Longair und Mitrović wurden nicht verwendet.

Jeder Befund wird gegen eine Zufallserwartung gestellt (½-Fuß-Raster wie im
Nullmodell, Kap. 7).

## Befund A: Genannte Höhen in Fuß

| Bau | Raum (Tafel) | Höhe (Text) | beste Regel aus I.23 | Abw. | Zufall |
|---|---|---:|---|---:|---:|
| Mocenigo, Marocco | 26 × 16 | 21 | 1. Verfahren = 21 | 0 % | 9,5 % |
| Barbarano | Quadrat 16 | 21½ | Breite + ⅓ = 21⅓ | 0,8 % | 9,1 % |
| Barbarano | 24 × 19 (unsicher) | 21½ | 1. Verfahren = 21½ | 0 % | 15 % |
| Trissino (Entwurf) | 40 × 20, **Flachdecke** | 27 | 3. Verfahren = 26⅔ | 1,3 % | 15 % |
| Trissino (Entwurf) | 20 × 18, **gewölbt** | 18 | Höhe = Breite | 0 % | 15 % |
| Mocenigo, Marocco | Kammern 16 × 10 | 17 | keine | 31 % | – |
| Garzadore (Entwurf) | Kammern 18½ × 16 (korrigiert, Kap. 11) | 16 | Höhe = Breite | 0 % | 9 % |

**Lesart:** Einzelne Treffer sind mit 9–15 % Zufallsrate nur schwache Belege. Die
Kammerhöhen (17 und 16 Fuß) folgen keiner Regel aus Buch I; sie ergeben sich
offenbar aus den Nachbarräumen und Zwischengeschossen. Bei Trissino vertauscht
Palladio die Regeln: die Flachdecke erhält ein Gewölbemittel, der gewölbte Raum
die Flachdeckenregel. Mitrović (1990) hat diesen Fall bereits bemerkt; er ist
hier am Scan bestätigt.

## Befund B: Gleiche Höhe von Langraum und Quadratraum

Wo Palladio für einen Langraum das Verfahren nennt und daneben ein Quadratraum
gleicher Breite liegt, ergibt das Verfahren nahezu die Höhe des Quadratraums
(Breite + ⅓):

| Bau | Langraum | Verfahren | Höhe | Quadratraum | Abw. | Zufall |
|---|---|---|---:|---:|---:|---:|
| Chiericati | 30 × 18 | 1. (arithm.) | 24 | 24 | 0 % | 2,8 % |
| Cornaro | 26½ × 16 | 1. (arithm.) | 21¼ | 21⅓ | 0,4 % | 3,1 % |
| Pisani, Montagnana | 28 × 16 | 2. (geom.) | 21,17 | 21⅓ | 0,8 % | 6,2 % |
| Mocenigo, Marocco | 26 × 16 | 1. (arithm.) | 21 | 21⅓ | 1,6 % | 9,4 % |

Bei unabhängiger Wahl der Raumlänge wäre dieses Zusammentreffen in allen vier
Bauten mit etwa 5 · 10⁻⁶ zu erwarten. **Nachtrag (Kap. 10):** Berücksichtigt man
Palladios Vorliebe für 5:3 und 2:1, ist das Zusammentreffen nicht mehr auffällig
(p ≈ 0,2); siehe dort. Palladio sagt es für Chiericati und Mocenigo
auch ausdrücklich („tanto alti quanto ... le maggiori“).

**Wichtige Einschränkung:** Das Nullmodell nimmt beliebige Raumlängen an. Wer ohnehin
5:3 bevorzugt, erhält mit dem ersten Verfahren automatisch die Quadrathöhe, denn
(5/3 + 1)/2 = 4/3. Chiericati (30 × 18) ist exakt 5:3. Der Befund belegt deshalb,
dass Raumform und Höhenverfahren zusammen gewählt wurden, nicht, welches von
beiden zuerst kam.

## Befund C: Das Verhältnis 7:4 als Partner des geometrischen Mittels (Hypothese)

Howard/Longair (1982, 134) hielten es für unwahrscheinlich, dass Palladio mit
Absicht 7:4 wählte. Der Text zeigt: Der einzige 7:4-Raum, für den Palladio das
Verfahren nennt (Pisani, Montagnana), erhält das **zweite** (geometrische) Mittel.
Dessen Höhe ist √(7/4) · Breite = 1,323 · Breite, weniger als 1 % unter 4/3. Damit
wäre 7:4 genau die Raumform, die mit dem geometrischen Mittel dieselbe Höhe wie ein
benachbarter Quadratraum erreicht, so wie 5:3 mit dem arithmetischen Mittel.

Gegenprobe Cornaro: Der Text nennt 7:4 und das erste Verfahren; das ergäbe 22 statt
21⅓ (3,1 % Abweichung). Die Tafel zeigt aber 26½ × 16, also fast 5:3, und damit
21¼. Text und Tafel widersprechen sich hier; die Tafel passt zur gleichen Höhe.

Status: **B-Hypothese**, gestützt auf einen Fall mit genanntem Verfahren und einen
Widerspruch zwischen Text und Tafel. Nicht als Regel Palladios zu behaupten.

## Befund D: Geschosshöhen

Im Entwurf S. 71 ergibt das genannte erste Verfahren für die 30 × 18-Räume 24 Fuß.
Mit den Textangaben für die Obergeschosse folgt 24 → 20 → 18: der erste Schritt
entspricht genau der Sechstelregel aus Buch I (5/6), der zweite nicht (9/10). Das
Erdgeschoss ist dabei erschlossen, nicht genannt.

## Grenzen

- Die Tafelmaße sind Lesungen mit Unsicherheit; bei Barbarano ist eine Zahl
  beschädigt.
- Zehn Bauten, kleine Fallzahlen. Die Zufallsraten sind heuristische Schranken.
- Die Holzschnitte zeigen, was Palladio veröffentlichte, nicht was gebaut wurde.

## Nächste Schritte

1. Alle übrigen Grundrisse von Buch II lesen (vollständiger eigener Datensatz).
2. Befund C an allen Räumen mit 7:4 und 5:3 prüfen, wo ein Quadratraum anschließt.
3. Abgleich unserer Lesungen mit Howard/Longair und Mitrović erst danach, als
   unabhängige Kontrolle.
