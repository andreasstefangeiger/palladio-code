# 13. Buch IV: Hat der Sakralbau eine eigene Proportionslehre?

Stand: 08.10.2026 · Daten: `data/book4/` · Auswertung: `make book4` →
`output/book4/analysis.json`, `output/book4/matrix.md` · Scanbelege:
`python -m palladio_code.proofs data/book4/text_statements.json --out output/book4/proofs`

## Frage und These

These von A. S. Geiger: Palladio entwickelt seine Proportionslehre nur einmal, in
Buch I, und sie gilt auch für den Sakralbau. Buch IV gibt für Tempel und Kirchen nur
eine Liste von Kriterien (Ort, Form, Decorum, Material, Licht …) und lobt den Kreis.
Eine neue, systematische Proportionstheorie enthält es nicht.

## Vorgehen

1. **Text.** Alle Aussagen zu Maß und Proportion in Buch IV wurden gesucht:
   Volltextsuche nach Proportionswörtern und Rückverweisen, dazu die vollständige
   Lektüre der Vorrede und der Kap. I–V. Daraus wurden 39 Stellen erfasst, zusammen
   mit den Gegenstellen in Buch I (Kap. I, XXIII) und Buch III (Kap. XIX).
   Jede Stelle ist am Scan geprüft; 14 Lesefehler der Texterkennung wurden
   korrigiert (`data/book4/text_statements.json`).
2. **Matrix.** Jedes Thema aus Buch I ist dem gegenübergestellt, was Buch IV dazu
   sagt (`data/book4/matrix.json`). Klasse A heißt: Die Beziehung steht so im Text.
   Klasse B heißt: Sie ist unsere Deutung mehrerer A-Stellen.
3. **Tafeln.** Aus Palladios Grundrissen der antiken Tempel wurden die Maße der
   Cella gelesen (`data/book4/plate_readings.json`). Sie wurden gegen die sieben
   Formen aus Buch I, Kap. XXI und gegen das Nullmodell aus Kap. 7 geprüft.

## Ergebnis 1: Die These trifft zu

- **Der Grundsatz steht einmal, in Buch I, und gilt für jedes Gebäude.** Buch I,
  Kap. I, S. 6–7: „La bellezza risulterà dalla bella forma, e dalla corrispondenza
  del tutto alle parti, delle parti fra loro, e di quelle al tutto“. Die drei
  Anforderungen gelten „in ciascuna fabrica“.
- **Buch IV wiederholt diesen Grundsatz nur und verlangt mehr Sorgfalt.**
  - Vorrede, S. 3: Wenn man irgendwo mit „bella misura, e proportione“ bauen
    solle, dann gewiss bei den Tempeln. Für Wohnhäuser wende man große Sorgfalt
    auf, für Kirchen eine „molto maggiore“.
  - Kap. V, S. 9: Was „in tutte le fabriche“ gilt, sei „con estrema cura … ne i
    Tempij“ zu beachten.
- **Wo Buch IV Zahlen nennt, sind es Verweise oder Vitruvs Kanon.**
  - Für Säulenordnungen, Interkolumnien, Gebälke, Kapitelle und die Ausführung
    verweist Palladio auf Buch I (u. a. S. 8, 9, 61, 98).
  - Für die Seitenschiffe der Kirchen verweist er auf die Basiliken in Buch III
    (S. 10).
  - Die Tempelregeln selbst kennzeichnet er als Vitruvs: in der Vorrede (S. 3–4),
    in Kap. III (S. 7) und in Kap. V (S. 9–10, „cosi compartisse Vitruuio“,
    „come ci insegna Vitruuio“).
- **Neu in Buch IV sind Begründungen, keine Maße.**
  - Decorum: Jede Säulenordnung gehört zu bestimmten Göttern (S. 6).
  - Kosmologie: Sonne und Mond erhalten Rundtempel, „perche continuamente
    intorno al Mondo si girano“ (S. 6).
  - Theologie des Kreises: Der Kreis zeige „la Vnità, la infinita Essenza, la
    Vniformità, & la Giustitia di DIO“ (S. 6).
  - Das Kreuz als Bild des Kreuzesholzes, mit San Giorgio Maggiore als Beispiel
    (S. 6–7).
  - Das Pantheon, „di figura del Mondo“, ist so hoch wie sein Durchmesser (S. 73).
- **Palladios eigene Gliederung ist eine Liste.** „E tanto basti hauer detto del
  Decoro, de gli aspetti, delle maniere, & del compartimento de i Tempij“ (S. 10).

## Ergebnis 2: Zwei Präzisierungen

1. **Die Übertragung der Raumregeln auf Kirchen steht nicht im Text.** Palladio
   sagt nirgends, dass die sieben Raumformen (I, XXI) oder die Höhenregeln
   (I, XXIII) für Kirchen gelten. Seine Rückverweise auf Buch I betreffen nur
   Ordnungen und Ausführung. Dass die Raumlehre im Sakralbau gilt, ist deshalb
   eine gut begründete Rekonstruktion (Klasse B). Sie stützt sich auf den
   allgemeinen Grundsatz in Buch I, Kap. I und Buch IV, Kap. V (Klasse A).
2. **Vitruvs Tempelkanon liegt außerhalb der sieben Formen.** Der Kanon, den
   Palladio übernimmt (S. 10), sieht so aus: Der Tempel ist doppelt so lang wie
   breit, das sind 2:1, eine der sieben Formen. Die Cella nimmt 5 von 8 Teilen
   der Länge ein, die Mauern eingerechnet; das ergibt 5:4, und 5:4 gehört nicht
   zu den sieben Formen.

## Ergebnis 3: Die Tempeltafeln

| Tempel | S. | Cella (Fuß) | Verhältnis | nächste Form | Abw. | Lesung |
|---|---:|---|---:|---|---:|---|
| Fortuna Virile | 49 | 18 9/12 × 28¾ | 1,530 | 3:2 | +2,0 % | sicher |
| Maison Carrée, Nîmes | 112 | 29 × 42½ | 1,466 | 3:2 | −2,3 % | Bruch unsicher |
| Assisi | 104 | 38 × 50½ | 1,329 | 4:3 | −0,3 % | sicher |
| Pola | 108 | 19 11/12 × 26 | 1,305 | 4:3 | −2,1 % | sicher |
| Nerva Traiano | 25 | 49½ × 54 | 1,091 | 1:1 | +9,1 % | Länge bis zur Säulenstellung |
| Antonino e Faustina | 33 | 48½ × 67 | 1,381 | √2 | −2,3 % | sicher |
| Marte (piazza de' Preti) | 56 | 42½ × 84½ | 1,988 | 2:1 | −0,6 % | sicher |
| Giove Tonante | 71 | 29½ × 48½ | 1,644 | 5:3 | −1,4 % | sicher |
| zweiter Tempel in Nîmes | 119 | 29 8½/12 × 44¾ | 1,506 | 3:2 | +0,4 % | sicher |
| Concordia | 125 | 47½ × 68 | 1,432 | √2 | +1,2 % | Bruch unsicher |
| Nettuno | 129 | 44¼ × 66 | 1,492 | 3:2 | −0,6 % | Bruch unsicher |

- **Vier von elf Cellae liegen innerhalb von 1 % an einer der sieben Formen.**
  Der Zufall erwartet 15 %, die Irrtumswahrscheinlichkeit beträgt p = 0,07. Innerhalb
  von 2 % sind es sieben von elf (Zufall 30 %, p = 0,02). Wegen der unsicheren Brüche
  liegen die Zahlen zwischen 3 und 4 bzw. zwischen 6 und 7 Treffern.
- **Keine Cella liegt in der Nähe von 5:4, auch Assisi und Pola nicht.** Für diese
  beiden schreibt Palladio selbst „la quarta parte più della larghezza“ (S. 103,
  107), seine Tafeln zeigen aber im Innenmaß 1,33 und 1,31. Vitruv rechnet die
  Mauern ein, die Innenmaße der Tafeln tun das nicht. Text und Tafel müssen sich
  deshalb nicht widersprechen; die gezeichneten Innenräume liegen aber näher an 4:3.
- **Lesart.** In Palladios eigenen Entwürfen (Buch II) haben 54 % der Hauptzimmer
  genau eine der sieben Formen (Kap. 10). Bei den antiken Tempeln, wie er sie
  vermessen und ergänzt hat, ist die Tendenz deutlich schwächer. Die sieben Formen
  sind also eine Regel seiner eigenen Entwurfspraxis. Als Kanon aus den Tempeln
  der Antike abgelesen hat er sie nicht, und in Buch IV wendet er sie auch nicht an.
- **Kontrollmessung.** Bei vier Tafeln wurde das gezeichnete Rechteck zusätzlich
  vermessen (Fortuna Virile, Maison Carrée, Assisi, Pola). Es weicht höchstens 0,8 %
  von Palladios Zahlen ab.

## Bedeutung für San Giorgio Maggiore

- Palladio führt San Giorgio in Buch IV, Kap. II, S. 7 als Beispiel der Kreuzform an.
  Nach der Volltextsuche ist sie die einzige eigene Kirche, die er im Traktat nennt.
- Dass die Raumlehre aus Buch I für San Giorgio gilt, ist eine gut begründete
  Lesart (B), aber keine Aussage Palladios. Prüfen ließe sie sich am vermessenen
  Bau (Corpus Palladianum, Laserscan wie beim Redentore), und zwar gegen das
  Nullmodell.
- Für die Seitenschiffe nennt Palladio selbst den Maßstab: die Basilika
  (III, XIX, S. 38). Dort ist der Mittelraum 2:1, und die Seitengänge haben ein
  Drittel der Mittelbreite.

## Matrix (Kurzfassung)

| Thema | Befund | Klasse |
|---|---|---|
| Grundsatz: Schönheit aus Proportion | gleicher Grundsatz; für Tempel „con estrema cura“ | A |
| Wohnhaus und Kirche | dieselbe Sorgfalt, nur größer; Kirche: Würde statt Bequemlichkeit | A |
| Raumformen | kein Verweis auf die sieben Formen; Vitruvs Cella 5:4 außerhalb | A |
| Höchstens zwei Quadrate | 2:1 bei Tempel und Basilika, als Vitruv-Kanon | B |
| Raumhöhen | Höhenregeln aus Buch I fehlen in Buch IV | A |
| Säulenordnungen | Verweis auf Buch I; Palladios Urteil (Eustylos, keine Postamente) | A |
| Gemeinsames Maß | in Buch IV ausdrücklich: „modulo, cioè misura“ | A |
| Öffnungen | eine Beobachtung im Rahmen von Buch I | A |
| Kirchen und Basiliken | Verweis auf Buch III | A |
| Decorum, Kosmologie, Theologie | nur Buch IV; begründen die Form, nicht ihre Maße | A |
| Herkunft der Tempelregeln | Vitruv, ausdrücklich genannt | A |
| Urteil und Spielraum | in beiden Büchern („secondo il suo giudicio“; Abweichung von Vitruv) | A |

Die vollständige Matrix mit allen Belegnummern steht in `output/book4/matrix.md`.

## Grenzen

- Elf Tempel sind eine kleine Stichprobe. Der Test ist schwach, und es gibt sechs
  mögliche Zielformen.
- Drei Brüche sind nicht sicher lesbar. Bei Nerva reicht die Längenlinie nur bis zur
  Säulenstellung vor der Rückwand.
- Ausgeschlossen sind: Rundbauten, Raumgruppen, Cellae mit Apsiden und Nischen, der
  Tempel des Iuppiter Stator (Länge unleserlich) und Tafeln ohne Grundriss
  (`excluded` in den Daten).
- Die antiken Bauten sind Palladios Rekonstruktionen („sono andato conietturando“,
  Vorrede). Gemessen wird also Palladios Bild der Antike.
- Die Volltextsuche nutzt die e-rara-Texterkennung und kann Stellen übersehen. Alle
  39 zitierten Stellen sind am Scan geprüft.
