# 15. San Giorgio Maggiore an Palladios eigenen Regeln

Stand: 12.10.2026 · Daten: `data/san_giorgio/bertotti_scamozzi.json` ·
Auswertung: `python -m palladio_code.san_giorgio` → `output/san_giorgio/analysis.json`

## Quelle

Palladio hat von San Giorgio keinen Plan veröffentlicht; in den Quattro Libri nennt
er die Kirche nur als Beispiel der Kreuzform (IV, II, S. 7).

Die älteste veröffentlichte Bauaufnahme mit Maßen stammt von Ottavio Bertotti
Scamozzi: *Le fabbriche e i disegni di Andrea Palladio*, Bd. IV, Taf. V–VIII,
Vicenza 1776–1783. Bertotti hat die Bauten selbst vermessen. Benutzt wurde die
gemeinfreie Genueser Ausgabe von 1846 (hg. von Celestino Foppiani), die der
Vicentiner Ausgabe folgt. Das Digitalisat stellt die Bibliothek des Politecnico di
Torino bereit.

Evidenzklasse **C2**: gebaute Praxis, gemessen im 18. Jahrhundert.

Bertotti gibt die Maße in vicentinischen Fuß und Zoll an (Fuß : Zoll, 12 Zoll =
1 Fuß). Jede verwendete Zahl wurde mit der Maßleiste der Tafel geprüft
(0–60 Fuß = 709 px): Beschriftung und gezeichnete Strecke stimmen auf etwa 1 %
überein.

## Bertotti hat die Frage schon gestellt

> „Vi saranno indubitabilmente giuste proporzioni fra la lunghezza, la larghezza ed
> altezza; ma non ho potuto rinvenirle. Solamente conobbi che la navata principale è
> lunga sino alla tribuna quasi due larghezze.“ (S. 22)

In der Anmerkung rechnet er Palladios Verfahren aus Buch I, Kap. XXIII nach:

- Das arithmetische Mittel ergäbe für das Mittelschiff etwa 51 Fuß, das
  kontraharmonische 56⅘ Fuß.
- Ausgeführt sind „quasi 62 piedi“; im Haupttext nennt er „intorno a piedi 61“.

## Ergebnis

| Raum | Maße (Fuß) | Verhältnis | nächste der sieben Formen |
|---|---|---:|---|
| Mittelschiff bis zur Vierung | 68,6 × 34½ | 1,99 | 2:1 (−0,6 %) |
| Vierung | 34½ × 34,3 | 1,01 | 1:1 (+0,6 %) |
| Querhausarm ohne Apsis | 34½ × 34¼ | 1,01 | 1:1 (+0,7 %) |
| Presbyterium | 41⅓ × 31⅙ | 1,33 | 4:3 (−0,5 %) |
| Mönchschor mit Apsis (nach Palladios Tod) | 57¼ × 34¼ | 1,67 | 5:3 (+0,3 %) |

Die Länge des Mittelschiffs ist nicht beschriftet; sie ist mit der Maßleiste
gemessen. Bertotti nennt „quasi due larghezze“. Der Kuppelkreis der Vierung ist
ebenfalls gemessen. Alle übrigen Zahlen sind Bertottis Beschriftungen.

| Regel Palladios (Fundstelle) | San Giorgio (Bertotti) | Befund |
|---|---|---|
| Saal höchstens zwei Quadrate (I.XXI.3); Basilika: Mittelraum zwei Quadrate (III, XIX) | Mittelschiff 1,99 Breiten | erfüllt |
| Seitenschiffe der Kirchen wie bei der Basilika: ⅓ des Mittelraums (IV, V → III, XIX) | Seitenschiffe 0,53 der Mittelschiffbreite | **nicht erfüllt**: etwa ½ (Bertotti: „la metà“) |
| Kreis und Quadrat die vollkommensten Formen; Kreuzform (IV, II) | quadratische Vierung mit Kuppel, quadratische Querhausarme mit Halbkreisapsiden | erfüllt |
| Kompositsäule 10 Moduln, Gebälk ⅕ (I.XVIII) | innen 10¼ Durchmesser, Gebälk ⅕; Fassade knapp 10, Gebälk ⅕ | erfüllt |
| Postament der Kompositordnung ⅓ der Säule, der korinthischen ¼ (I.XVIII, I.XIX) | innen ¼, Fassade knapp ⅓ | Fassade erfüllt; innen das korinthische Maß |
| Bogenöffnung der Kompositordnung 2½ Quadrate hoch (I.XVIII) | Arkaden der Seitenschiffe 2½ Breiten | erfüllt |
| Gewölbehöhe nach einem der drei Mittel, sonst Urteil des Architekten (I.XXIII) | ≈ 61–62 Fuß; die Mittel ergäben 46–52 | keines der drei Mittel: Urteil |

**Lesart:**

- **Raumformen.** Die Haupträume aus Palladios Bauzeit folgen auf 1 % genau den
  Formen aus Buch I, Kap. XXI:
  - Mittelschiff 2:1;
  - Vierung und Querhausarme 1:1;
  - Presbyterium 4:3.

  Rein rechnerisch ist das bei 15 % Zufallsrate je Raum sehr unwahrscheinlich
  (p ≈ 0,0005). Die Treffer sind aber nicht unabhängig: Eine Kuppel verlangt eine
  quadratische Vierung, und die Querhausarme haben die Breite des Mittelschiffs.
  Der p-Wert ist deshalb nur ein Hinweis.
- **Säulenordnungen.** Die Kompositordnung folgt im Wesentlichen den Maßen aus
  Buch I.
- **Zwei klare Abweichungen:**
  - Die Seitenschiffe sind etwa halb so breit wie das Mittelschiff. Die
    Basilikaregel, auf die Palladio die Kirchen ausdrücklich verweist, verlangt ein
    Drittel.
  - Das Mittelschiffgewölbe ist höher als jedes der drei Mittel. Für diesen Fall
    lässt Palladio selbst Raum: „altre altezze … secondo il suo giudicio“.

Die übrigen Kriterien der Theorie prüft docs/16: Ort, Kreuzform, Fassade, Kuppel,
Material, Farbe, Licht und Decorum. Dort sind auch die Fassade (Taf. VIII) und die
Kuppel (Taf. VI) vermessen.

## Was nicht von Palladio stammt

Bertotti (S. 21, Anm. b; S. 23, nach Temanza) überliefert:

- 1579 war das Innere fertig.
- Der Chor und die Fassade wurden erst nach Palladios Tod (1580) „con
  l'assistenza d'altro maestro“ gebaut, die Fassade „sul principio del
  susseguente secolo XVII“.

Für die Fassade gibt Bertotti selbst musikalische Verhältnisse an:

- Seitenflügel zu Mittelteil „si accosti a una seconda maggiore“ (9:8);
- Höhe zu Breite des Mittelteils „una sesta minore“ (8:5).

Die Fassade ist als Ausführung nach Palladios Modell zu behandeln, nicht als sein
eigener Bau.

## Grenzen

- Das ist eine einzige Aufnahme aus dem 18. Jahrhundert, in einer nachgestochenen
  Ausgabe. Eine moderne Bauaufnahme (Corpus Palladianum, Laserscan) wäre die
  nötige Gegenprobe.
- Bei einer Ziffer ist die Lesung unsicher (Seitenschiff 18:5 oder 18:3); am
  Befund ändert das nichts.
- Welche Fluchten Bertotti jeweils misst (Pfeilerkern, Pilaster, Wandvorlage), lässt
  sich an der Tafel nur ungefähr bestimmen. Die Verhältnisse sind deshalb auf etwa
  ±1 % genau.
- Die Auswahl der Räume folgt dem Grundriss: alle Haupträume, der Chor getrennt.
