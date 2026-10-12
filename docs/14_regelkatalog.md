# 14. Regelkatalog der Quattro Libri

Stand: 12.10.2026 · Daten: `data/rules/register.json`, `data/rules/book1.json` ·
Werkzeug: `python -m palladio_code.catalogue {status|check|dump BUCH KAPITEL}` ·
Scanbelege: `python -m palladio_code.proofs data/rules/book1.json --out …`

## Ziel

Der Katalog soll alle Regeln Palladios enthalten, und zwar aus allen vier Büchern,
nicht nur aus einzelnen Kapiteln. Jede Regel ist

- am Druck von 1570 belegt (Buch, Kapitel, Seite, italienisches Zitat, am Scan
  gelesen),
- deutsch wiedergegeben,
- nach Art und Herkunft eingeordnet,
- mit maschinenlesbaren Werten versehen, wo Palladio Zahlen nennt.

Die Wissenschaft hat Vorrang. Vollständigkeit wird über das Kapitelregister geprüft:
Jedes der 101 Kapitel trägt einen Status (`open`, `read`, `extracted`, `checked`).

## Verfahren

1. **Kapitelregister.** Alle Kapitelanfänge sind in der ALTO-Texterkennung
   verortet: Buch I mit 29 Kapiteln und Vorrede, Buch II mit 17, Buch III mit 21
   und Vorrede, Buch IV mit 31 und Vorrede.
2. **Lesen.** Jedes Kapitel wird ganz gelesen (`catalogue dump`). Ob eine Stelle
   eine Regel ist, entscheide ich am Wortlaut, nicht nach einem Suchtreffer.
   Erfasst werden Gebote, Verbote, Spielräume, Vorzüge, Verfahren,
   Maßangaben als Norm und allgemeine Grundsätze. Beschreibungen einzelner Bauten
   kommen nicht in den Katalog; sie werden als Messdaten geführt (Buch II, IV).
3. **Herkunft.** Jede Regel ist einer Quelle zugeordnet:
   - `palladio`: Palladios eigene Regel;
   - `vitruvius`: Palladio gibt Vitruv wieder, der genannt ist;
   - `antichi`: die Praxis der Antiken als Vorbild;
   - `alberti`: Palladio gibt Alberti wieder;
   - `custom`: der Brauch seiner Zeit.
4. **Scanprüfung.** Jedes Zitat wird am IIIF-Ausschnitt des Drucks gelesen und
   korrigiert. Erst danach erhält es die Klasse A. Text außerhalb des Ausschnitts
   steht in eckigen Klammern.
5. **Geltungsbereich.** `scope` gibt an, wofür eine Regel gilt: `all`, `villa`,
   `private_house` usw. Für Buch I gilt nach Palladio selbst `all`
   (Vorrede S. 6: „precetti, che vniuersali sono, & si deono osseruare in tutti
   gli edificij così publici, come priuati“).

## Stand

| Buch | Kapitel | Status | Regeln |
|---|---:|---|---:|
| I | 29 + Vorrede | vollständig, am Scan geprüft | 196 |
| II | 17 | offen (Höhen und Raummaße bereits in `data/book2/`) | – |
| III | 21 + Vorrede | offen (Basilika in `data/book4/`) | – |
| IV | 31 + Vorrede | Theorieteil in `data/book4/`, Tempelkapitel offen | – |

## Buch I im Überblick

- **196 Regeln.** Nach Art: 63 Maßangaben, 45 Gebote, 25 Grundsätze,
  23 Verfahren, 15 Spielräume, 15 Vorzüge, 10 Verbote.
- **Herkunft:** 153 von Palladio, 21 von Vitruv (genannt), 20 aus der Praxis der
  Antiken, je eine von Alberti und aus dem Brauch der Zeit.
- **Schwerpunkte:**
  - Säulenordnungen: 55 Regeln;
  - Baustoffe: 27;
  - Fundamente: 15;
  - Treppen: 12;
  - Öffnungen: 11;
  - Mauern: 11;
  - Missbräuche: 7.
- **Zahlen zum Rechnen:** 89 Regeln haben maschinenlesbare Werte, z. B.
  - Mörtel 3 : 1;
  - Fundament doppelt so dick wie die Mauer;
  - Dachfirst 2/9 der Spannweite;
  - Stufen 4–6 Zoll hoch;
  - Gebälk ¼ bzw. ⅕ der Säulenhöhe;
  - Modul = unterer Säulendurchmesser.

### Was für die Proportionsfrage neu hinzukommt

- **Das Maßsystem ist relativ.** Palladio lehnt ortsgebundene Einheiten (Elle,
  Fuß, Palm) für die Ordnungen ab. Alles wird im **Modul** gemessen, dem unteren
  Säulendurchmesser zu 60 Minuten (I, XIII, S. 16).
- **Säulenhöhe und Säulenabstand hängen zusammen.** Je enger die Säulen stehen,
  desto schlanker sind sie: 7, 8, 9, 9½ und 10 Durchmesser bei Abständen von über
  3, 3, 2¼, 2 und 1½ Durchmessern (I, XIII, S. 16). Die Zuordnung zu den fünf
  Ordnungen ist Palladios eigene.
- **Wahrnehmung korrigiert das Maß.** Hohe Säulen verjüngen sich weniger, „essendo
  che l'altezza da se faccia l'effetto del diminuire per la distanza“
  (I, XIII, S. 15).
- **Die Natur ist der Maßstab.** Säulen verjüngen sich wie Bäume, Basen scheinen
  unter der Last gequetscht, und Triglyphen zeigen Balkenköpfe. Was der Natur der
  Dinge widerspricht, entfernt sich „dal uero, buono, e bel modo di fabricare“
  (I, XX, S. 51).
- **Quadrat und Doppelquadrat kehren wieder:**
  - Metope 1:1;
  - ionische Bogenöffnung zwei Quadrate hoch, korinthische und komposite 2½;
  - Säle höchstens zwei Quadrate.
- **Regeln mit Spielraum und Urteil:**
  - Für Haupttüren gibt es „certa, e determinata regola“ nicht (I, XXV).
  - Für Kassettendecken ebenso wenig (I, XXII).
  - Manche Gewölbehöhen unterliegen keiner Regel (I, XXIII).
  - Die Antiken „variarono“, aber ohne die „regole vniuersali, & necessarie
    dell'Arte“ zu verlassen (I, XX).

## Spätere Produkte (Deutungsschicht, getrennt vom Katalog)

Zwei Anwendungen sind vorgesehen. Beide bauen auf dem Katalog auf, gehören aber
nicht in ihn.

1. **Gestaltungsrichtlinie für die Homepage.**
2. **WordPress-Template „Palladio“.**

Die Übertragung einer Bauregel auf eine Webseite ist eine Deutung. Sie kommt in
eine eigene Datei, die jede Übertragung auf die Regel-IDs zurückführt und als
Deutung kennzeichnet. Geeignete Kandidaten aus Buch I:

| Bauregel (Fundstelle) | mögliche Übertragung |
|---|---|
| Modul als relatives Grundmaß (I.XIII.12) | eine Basisgröße, aus der alle Abstände und Schriftgrade abgeleitet werden |
| sieben Raumformen (I.XXI.5) | Seitenverhältnisse für Bilder, Karten und Raster: 1:1, 4:3, √2, 3:2, 5:3, 2:1 |
| Gebälk ⅕ der Säule, Gliederung 4 : 3 : 5 (I.XVI.7) | Verhältnis von Kopfbereich, Inhalt und Fuß |
| Säulenhöhe nach Säulenabstand (I.XIII.8) | Zeilenlänge und Zeilenabstand gekoppelt: je dichter, desto schlanker |
| Symmetrie, Achsen übereinander (I.XXI.4, I.XXV.8) | Spaltenraster mit durchgehenden Achsen |
| gleiche Fenster in einem Geschoss (I.XXV.6) | ein Bildmaß pro Ebene, unabhängig vom Inhalt |
| Mitte als „più bella parte“, auf die alles antwortet (I.XXI.2) | eine Hauptachse und ein Zentrum je Seite |
| keine gesprengten Giebel, keine Kartuschen ohne Funktion (I.XX) | kein Ornament ohne Aufgabe |
| Treppe: Zugang sichtbar, Weg zeigt das Schönste, führt in weite Räume (I.XXVIII.2) | Navigation |

## Nächste Schritte

1. Die Kapitel von Buch II bis IV nach demselben Verfahren lesen.
2. San Giorgio Maggiore an vermessenen Plänen prüfen. Bertotti Scamozzi,
   *Le fabbriche e i disegni di Andrea Palladio*, Bd. IV, 1783, gemeinfrei,
   enthält Grundriss, Schnitt und Ansicht mit Maßen.
3. Die Regeln aus Buch I mit Buch IV abgleichen, ob die Säulenordnungen der Tempel
   den Maßen aus Buch I folgen.
