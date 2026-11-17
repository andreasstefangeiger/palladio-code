# 17. Tempel in Buch IV: Rekonstruktion und Säulenordnungen

Stand: 17.11.2026 · Daten: `data/book4/reconstruction.json`, `data/book4/orders.json`,
`data/book4/orders_plates.json`,
`data/rules/book4.json` · Auswertung: `make book4` → `output/book4/analysis.json`,
`output/book4/orders.json`, `output/book4/orders.md`

## Fragen

1. Welche Teile der Tempeltafeln sind nach Palladios eigenen Worten nicht am Bau
   gemessen?
2. Folgen die Säulenordnungen der Tempel, wie Palladio sie beschreibt, den Maßen aus
   Buch I?

## Quellen und Verfahren

- **Nur Palladios Text von 1570.** Jede Stelle ist am Scan gelesen (Klasse A).
- **Keine Tafelzahlen.** Die Maßzahlen der Tafeln sind hier nicht ausgewertet. Die
  einzige Ausnahme sind die elf Cella-Maße aus docs/13.
- **Normen aus dem Regelkatalog.** Verglichen wird mit Buch I, Kap. XIII–XVIII
  (docs/14).
- **Rohangabe, Norm und Deutung bleiben getrennt.** Eine Abweichung belegt keine
  Absicht.

## Teil 1: Was Palladio erschlossen, ergänzt oder erfunden hat

Palladio sagt in der Vorrede allgemein, wie die Tafeln entstanden sind:

- Die Gesamtgestalt ist aus Resten und Fundamenten erschlossen (IV.Proemio.6), mit
  Vitruvs Hilfe (IV.Proemio.7).
- Die Ornamente sind an Fragmenten gemessen: „non ui ho posto alcuna cosa del mio“
  (IV.Proemio.8).
- Statuen zeichnet er überall ein, weil Rom nach den Schriftquellen voll davon war
  (IV.VIII.4).

In den Tempelkapiteln nennt er 15 Fälle ausdrücklich:

| Kap. | Tempel | Status | Teil der Tafel | Fundstelle |
|---|---|---|---|---|
| VII | Marte Vendicatore | erfunden | Ornamente und Tabernakel in der Cella, „di mia inuentione“ | IV.VII.2 |
| VII | Marte Vendicatore | ergänzt | innere Basis und Kapitell, nach Fragmenten aus der Nähe | IV.VII.3 |
| VIII | Nerva Traiano | ergänzt | Tabernakel mit Statuen an den Cellawänden | IV.VIII.3 |
| IX | Antonino e Faustina | ergänzt | Statuen im Inneren | IV.IX.2 |
| X | Sole e Luna | erfunden | Vorhallen und innere Ornamente, „come mi sono imaginato“ | IV.X.1 |
| XII | Giove (Quirinale) | erschlossen | innere Portiken und offene Mitte | IV.XII.2, IV.XII.3 |
| XIIII | Vesta (Rom) | ergänzt | Gesims | IV.XIIII.2 |
| XV | Marte (piazza de' Preti) | erschlossen | der ganze Tempel außer einer Flanke, nach Ruinen und Vitruv | IV.XV.6 |
| XVIII | Giove Statore | erschlossen | Aspekt, Säulenstellung und Säulenzahl; drei Säulen stehen | IV.XVIII.1 |
| XIX | Giove Tonante | erschlossen | Rückseite des Grundrisses, nach Analogie | IV.XIX.2 |
| XXII | bei San Sebastiano | erschlossen | Säulen des Portikus, nach den Fundamenten | IV.XXII.2 |
| XXIIII | Castore e Polluce | weggelassen | Baukörper, weil nach Palladio modern | IV.XXIIII.2 |
| XXVII | Pola | erfunden | Ornamente der Tür | IV.XXVII.1, IV.XXVII.2 |
| XXX | Concordia | nicht antik | Cellamauern, später erneuert | IV.XXX.2 |
| XXXI | Nettuno | erschlossen | Grundriss und Aufriss; nichts steht aufrecht | IV.XXXI.1, IV.XXXI.2 |

Die Liste enthält nur, was Palladio selbst sagt. Wo er nichts sagt, ist damit nicht
bewiesen, dass eine Tafel reine Bauaufnahme ist.

### Folge für den Tafeltest aus docs/13

docs/13 prüft elf Cellae gegen die sieben Raumformen aus Buch I. Vier dieser Maße
beruhen nach Palladios Angaben auf einer Rekonstruktion:

| Tempel | Seitenverhältnis | nächste Form | Abweichung | Maß rekonstruiert? |
|---|---:|---|---:|---|
| Fortuna Virile | 1,530 | 3:2 | +2,0 % | nein |
| Maison Carrée | 1,466 | 3:2 | −2,3 % | nein |
| Assisi | 1,329 | 4:3 | −0,3 % | nein |
| Pola | 1,305 | 4:3 | −2,1 % | nein (nur die Tür ist erfunden) |
| Nerva Traiano | 1,091 | 1:1 | +9,1 % | nein (nur Tabernakel ergänzt) |
| Antonino e Faustina | 1,381 | √2 | −2,3 % | nein (nur Statuen ergänzt) |
| zweiter Tempel in Nîmes | 1,506 | 3:2 | +0,4 % | nein |
| Marte (piazza de' Preti) | 1,988 | 2:1 | −0,6 % | ja (IV.XV.6) |
| Giove Tonante | 1,644 | 5:3 | −1,4 % | ja (IV.XIX.2) |
| Concordia | 1,432 | √2 | +1,2 % | ja (IV.XXX.2) |
| Nettuno | 1,492 | 3:2 | −0,6 % | ja (IV.XXXI.1, IV.XXXI.2) |

| Gruppe | innerhalb 1 % | innerhalb 2 % | Zufall (1 % / 2 %) | p (1 % / 2 %) |
|---|---:|---:|---:|---:|
| alle elf (docs/13) | 4 von 11 | 7 von 11 | 15 % / 30 % | 0,07 / 0,02 |
| Maß nicht als rekonstruiert bezeichnet | 2 von 7 | 3 von 7 | 15 % / 30 % | 0,28 / 0,35 |
| Maß nach Palladio rekonstruiert | 2 von 4 | 4 von 4 | 15 % / 30 % | 0,11 / 0,008 |

- **Befund.** Die Nähe zu den sieben Formen kommt vor allem aus den vier Tempeln,
  die Palladio rekonstruiert hat. Bei den sieben übrigen liegt die Trefferzahl im
  Bereich des Zufalls.
- **Lesart (B).** Wo Palladio rekonstruiert, zeichnet er Verhältnisse, die seinen
  eigenen Raumformen nahekommen. Das stützt das Ergebnis aus docs/13: Die sieben
  Formen sind eine Regel seiner Entwurfspraxis und kein Kanon, den er an den
  antiken Tempeln abgelesen hat.
- **Vorbehalte.**
  - Vier und sieben Fälle sind sehr wenig. Der Unterschied zwischen den Gruppen ist
    ein Hinweis, kein Beweis.
  - Die Gruppen wurden nach der ersten Auswertung gebildet. Das Kriterium stammt
    aber aus Palladios Text und nicht aus den Maßen.
  - Was Palladio an den vier Tempeln am Ort messen konnte, etwa an Fundamenten,
    sagt er nicht im Einzelnen.

## Teil 2: Die Säulenordnungen

`data/book4/orders.json` enthält 43 Textangaben zu 23 Tempeln. Säulenabstand,
Säulenlänge und Gebälk stehen in Säulendurchmessern (D) oder als Anteil der
Säulenlänge. „spesse colonne“ ist nach IV.IIII.2 der Pyknostylos mit 1½ D.

| Kap. | Tempel | Ordnung | Säulenabstand (D) | Säule (D) | Gebälk | Basis |
|---|---|---|---|---|---|---|
| VI | Pace | korinthisch | – | 9,94 | 0,198 | – |
| VII | Marte Vendicatore | korinthisch | 1½ (Pyknostylos) | – | – | – |
| VIII | Nerva Traiano | korinthisch (erschlossen) | 1½ (Pyknostylos) | – | ¼ | attisch |
| IX | Antonino e Faustina | nicht genannt | 1½ (Pyknostylos) | – | ⅓ | attisch |
| XII | Giove (Quirinale) | korinthisch | 1½ (Pyknostylos) | – | ¼ | – |
| XIII | Fortuna Virile | ionisch | 2¼ | – | – | attisch |
| XIIII | Vesta (Rom) | korinthisch | 1½ | 11 | – | – |
| XV | Marte (piazza de' Preti) | korinthisch | 1½ | – | 1 : 5½ | attisch |
| XVI | Battistero di Costantino | komposit | – | – | – | attisch-ionisch |
| XVII | Tempietto (Bramante) | dorisch | – | – | – | – |
| XVIII | Giove Statore | korinthisch | 1½ (Pyknostylos) | – | ¼ | attisch-ionisch |
| XIX | Giove Tonante | nicht genannt | 1½ (Pyknostylos) | – | – | – |
| XX | Pantheon | korinthisch | – | – | – | attisch-ionisch |
| XXI | Bacco (S. Agnese) | komposit | – | – | – | attisch |
| XXIII | Vesta (Tivoli) | korinthisch | 2 | – | – | – |
| XXIIII | Castore e Polluce | korinthisch | zwischen 1½ und 2 | – | – | attisch |
| XXV | sotto Trevi | korinthisch | 1½ (Pyknostylos) | – | – | – |
| XXVI | Assisi | korinthisch | 2 | – | ⅕ „& qualche cosa di più“ | – |
| XXVII | Pola | nicht genannt | 2 (Mitte 2¼) | – | – | attisch |
| XXVIII | Maison Carrée | korinthisch | – | – | ¼ | attisch |
| XXIX | zweiter Tempel in Nîmes | komposit (erschlossen) | – | – | – | attisch-ionisch |
| XXX | Concordia | nicht genannt | unter 2 | – | – | attisch-ionisch |
| XXXI | Nettuno | nicht genannt | 1½ − 1/11 | – | – | – |

### Vergleich mit Buch I

| Merkmal | Norm in Buch I | Palladios Angaben zu den Tempeln |
|---|---|---|
| korinthisches Gebälk | ⅕ der Säulenhöhe (I.XVII.1, I.XVII.5) | viermal ¼; zweimal etwa ⅕; einmal 1 : 5½ |
| korinthischer Säulenabstand | 2 D (I.XVII.1) | achtmal enger; zweimal 2 D |
| korinthische Säule | 9½ D (I.XVII.1) | Pace 9,94 D; Vesta in Rom 11 D |
| ionischer Säulenabstand | 2¼ D (I.XVI.1) | Fortuna Virile 2¼ D |
| Basis | attisch; für Komposit auch attisch-ionisch (I.XVII.2, I.XVIII.2) | achtmal attisch; fünfmal attisch-ionisch |

- **Gebälk.** Buch I gibt ¼ nur der dorischen Ordnung (I.XV.10). An vier
  korinthischen Tempeln nennt Palladio ¼: Nerva, Giove auf dem Quirinal, Giove
  Statore und Maison Carrée. Nur Pace (10½ : 53 Fuß) und Assisi liegen bei ⅕. Der
  Tempel des Antoninus hat ⅓; seine Ordnung nennt Palladio nicht.
- **Säulenabstand.** 16 Tempel haben eine Angabe. Bei zwölf stehen die Säulen enger
  als 2 D, bei neun davon mit 1½ D. Palladio weiß das: Pyknostylos und
  Systylos seien erträglich bei großen Säulen, „come si vede in quasi tutti i Tempij
  Antichi“ (IV.IIII.4). Seinen Vorzug gibt er dem Eustylos (IV.IIII.7).
- **Säulenlänge.** Nach I.XIII.8 gehören zu 1½ D Abstand 10 D Länge. Der
  Vestatempel in Rom hat bei 1½ D aber 11 „teste“.
- **Basis.** Pantheon und Giove Statore sind korinthisch und haben eine
  attisch-ionische Basis. Buch I nennt sie nur für die Kompositordnung.
- **Namen.** Bei der Fortuna Virile nennt Palladio 2¼ D „Sistilos“. Nach IV.IIII
  heißt dieser Abstand Eustylos; der Systylos hat 2 D. Der Text widerspricht sich
  hier selbst.
- **Postamente.** Der zweite Tempel in Nîmes hat im Inneren Postamente von „poco
  più della terza parte“ der Säulenlänge. Buch I kennt mehr als ⅓ nur am
  Konstantinsbogen (I.XIX.2).

### Lesart (B)

- **Die korinthische Norm aus Buch I ist nicht der häufigste Wert der Tempel.** Am
  häufigsten beschreibt Palladio 1½ D Abstand und ¼ Gebälk. Buch I setzt 2 D und ⅕.
- **Palladio berichtet die Abweichungen ohne Tadel.** Das Gebälk von 1 : 5½ lobt er
  sogar (IV.XV.4).
- **Die Norm ist eine Auswahl.** Sie ordnet die Befunde nach Vitruv und nach
  eigenem Urteil und bildet nicht ihren Durchschnitt. Dazu passen:
  - der Vorzug des Eustylos (IV.IIII.7);
  - die Ablehnung der Postamente (IV.V.6);
  - die Regel zur Variation (IV.XXIIII.1).

## Teil 3: Gegenprobe an den Tafeln

Stand 17.11.2026 · Daten: `data/book4/orders_plates.json` · Auswertung:
`python -m palladio_code.temple_orders` → `output/book4/orders.json` (`plates`)

### Verfahren

- **Maßzahlen gelesen.** An zehn Tempeln wurden die gedruckten Maße am IIIF-Scan
  gelesen: Interkolumnium, Säulendurchmesser, Säulenhöhe und Gebälk, soweit
  beschriftet. Zu jeder Lesung sind Seite, Ausschnitt und Sicherheit vermerkt.
- **Zeichnung gemessen.** Unter den Aufrissen und in den Grundrissen stehen die
  Säulen als schraffierte Kreise. Durchmesser und lichte Abstände wurden
  automatisch gemessen (`measure_circles`). Das Verhältnis Abstand : Durchmesser
  ist maßstabsfrei.
- **Ableitung (B).** Wo der Durchmesser nicht sicher lesbar ist, wird er aus dem
  beschrifteten Abstand und dem gezeichneten Verhältnis berechnet.
- **Schwachstelle.** Durchmesser stehen oft in den schraffierten Kreisen und sind
  dort schwer lesbar. Diese Lesungen tragen die Sicherheit „niedrig“.

### Ergebnis

| Kap. | Tempel | Text | Abstand : D gezeichnet | Abstand : D aus Zahlen | Säule in D | Gebälk : Säule |
|---|---|---|---:|---:|---:|---:|
| VII | Marte Vendicatore | Pyknostylos | 1,55 | 1,35 | 10,3 (9,0) | 0,208 |
| VIII | Nerva Traiano | Pyknostylos, Gebälk ¼ | – | 1,58 | (9,8) | 0,234 |
| IX | Antonino e Faustina | Pyknostylos, Gebälk ⅓ | 1,51 | – | 9,3 | 0,238 |
| XII | Giove (Quirinale) | Pyknostylos, Gebälk ¼ | 1,56 | 1,50 | – | – |
| XIII | Fortuna Virile (ionisch) | 2¼ D | 1,97 (Mitte 2,19) | – | – | – |
| XV | Marte (piazza de' Preti) | 1½ D, Gebälk 1 : 5½ | 1,74 | 1,55 | 11,1 (9,8) | 0,180 |
| XIX | Giove Tonante | Pyknostylos | 1,73 (Mitte 2,13) | – | – | – |
| XXIIII | Castore e Polluce | zwischen 1½ und 2 D | 1,64 (Mitte 1,70) | 1,81 | 9,7 (10,7) | – |
| XXVI | Assisi | 2 D, Gebälk ⅕ „& qualche cosa di più“ | 1,79 (Mitte 1,93) | – | 9,4 | 0,191 |
| XXVIII | Maison Carrée | Gebälk ¼ | 1,54 (Mitte 2,08) | – | – | – |

„Säule in D“: aus dem abgeleiteten Durchmesser, in Klammern aus dem gelesenen.

- **Säulenabstand.**
  - Bei vier Tempeln mit „spesse colonne“ ist die Zeichnung nahe 1½ D:
    Antonino, Giove (Quirinal), Marte Vendicatore und die Seitenjoche der Maison
    Carrée.
  - Bei zwei Tempeln ist sie deutlich weiter: Marte (piazza de' Preti) und
    Giove Tonante, beide etwa 1¾ D.
  - Beim Marstempel ergeben die gedruckten Zahlen 1,55. Die Zeichnung ist dort
    also nicht im Maßstab der Zahlen gestochen, sofern der Durchmesser richtig
    gelesen ist (Sicherheit niedrig).
  - Fortuna Virile (Text: 2¼) und Assisi (Text: 2 D) sind enger gezeichnet,
    etwa 2 und 1¾ D an den Seitenjochen.
- **Gebälk.**
  - Beim Marstempel bestätigen die Zahlen den Text: 7 Fuß 4½ Zoll zu 41 Fuß, also
    1 : 5,6 („una delle cinque parti e meza“). Das zeigt, dass die Lesart der
    Tafeln trägt.
  - Nerva hat 0,234, nahe dem ¼ des Textes.
  - Beim Tempel des Antoninus nennt der Text ⅓. Die Tafel zeigt 9 Fuß 3½ Zoll zu
    39 Fuß, also etwa ¼ (0,238). Die Lesung ist sicher; ob die Maßlinie das ganze
    Gebälk umfasst, ist nicht sicher geprüft.
  - Mars Ultor hat ⅕ (10 : 48).
- **Säulenhöhe.** Die Werte liegen zwischen 9 und 11 Durchmessern. Buch I setzt
  für das Korinthische 9½. Wegen der unsicheren Durchmesser lässt sich daraus
  keine Regel ablesen.

### Lesart (B)

- **Zahlen, Zeichnung und Text sind drei verschiedene Quellen.** Sie stimmen oft
  überein, aber nicht immer.
- **„spesse colonne“ ist ein Name, kein genaues Maß.** Palladio nennt so auch Tempel,
  deren Zeichnung 1¾ D zeigt.
- **Die runden Worte des Textes können vom Befund abweichen.** Ein Beispiel ist das
  ⅓-Gebälk des Antoninus gegen etwa ¼ auf der Tafel.
- **Folge für die Forschung:** Für Proportionsfragen an Buch IV müssen Text, Zahl
  und Zeichnung getrennt ausgewiesen werden.

## Grenzen

- Teil 2 nutzt Palladios runde Worte („la quarta parte“). Teil 3 prüft zehn Tempel
  an den Tafeln. Bei Pantheon, Vesta (Tivoli und Rom), Giove Statore, sotto Trevi
  und den Tempeln in Nîmes und Pola sind die Tafelzahlen noch nicht gelesen.
- Gelesene Durchmesser in schraffierten Kreisen sind unsicher. Die
  Pixelmessung setzt voraus, dass Kreise und Abstände im selben Maßstab gestochen
  sind.
- Bei fünf Tempeln nennt der Text keine Ordnung. Bei Nerva und beim zweiten Tempel
  in Nîmes ist sie aus dem Wortlaut erschlossen.
- „spesse colonne“ ist mit 1½ D gleichgesetzt. Der Tempel des Neptun zeigt, dass der
  wirkliche Abstand davon abweichen kann (1½ − 1/11 D).
- Es sind wenige Fälle. Die Zählungen beschreiben Palladios Text, keine Statistik
  der antiken Architektur.
- Mehrere Tempel sind selbst Rekonstruktionen (Teil 1). Auch ihre Ordnungen sind
  dann Palladios Bild der Antike.
