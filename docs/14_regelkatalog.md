# 14. Regelkatalog der Quattro Libri

Stand: 17.11.2026 · Daten: `data/rules/register.json`, `data/rules/book1.json` bis `book4.json` ·
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
   Begründet Palladio eine Einzelentscheidung an einem Bau, wird das als
   `rationale` erfasst und bleibt von den allgemeinen Regeln unterschieden.
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
| I | 29 + Vorrede | vollständig, am Scan geprüft | 211 |
| II | 17 | vollständig, am Scan geprüft | 102 |
| III | 21 + Vorrede | vollständig, am Scan geprüft | 107 |
| IV | 31 + Vorrede | vollständig, am Scan geprüft | 126 |
| **zusammen** | 98 + 3 Vorreden | | **546** |

Die Zahlen schließen die Nachträge des zweiten Durchgangs ein (siehe unten).

## Buch I im Überblick

- **211 Einträge** (196 aus dem ersten, 15 aus dem zweiten Durchgang). Nach Art:
  63 Maßangaben, 45 Gebote, 27 Verfahren, 25 Grundsätze, 15 Spielräume,
  15 Vorzüge, 11 Begründungen, 10 Verbote.
- **Herkunft:** 165 von Palladio, 22 aus der Praxis der Antiken, 21 von Vitruv
  (genannt), 2 aus dem Brauch der Zeit, 1 von Alberti.
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

## Buch IV im Überblick

- **126 Einträge.** Nach Art: 38 Begründungen am einzelnen Bau, 32 Grundsätze,
  22 Gebote, 11 Verfahren, 10 Vorzüge, 10 Maßangaben, 2 Verbote, 1 Spielraum.
- **Herkunft:** 79 von Palladio, 24 aus der Praxis der Antiken, 20 von Vitruv
  (genannt), 3 aus dem Brauch der Zeit.
- **Theorieteil (Vorrede bis Kap. V):** 61 Regeln. 39 Zitate sind die schon am
  Scan geprüften Aussagen aus `data/book4/` (Vermerk in `note`).
- **Tempelkapitel (VI–XXXI):** 65 Einträge. Maße und Beschreibungen der Tempel
  bleiben Messdaten in `data/book4/`.
- **Nachtrag vom 16.11.2026.** Ein zweiter Durchgang suchte gezielt nach Stellen,
  an denen Palladio seine Rekonstruktion, eine Datierung oder die Auswahl eines
  Baus begründet. Er ergab 18 weitere Einträge. Die erste Fassung hatte sechs
  Rekonstruktionshinweise genannt und vier Kapitel ohne Eintrag geführt (X, XVIII,
  XXI, XXXI); beides ist damit überholt. Jedes Kapitel hat nun mindestens einen
  Eintrag.
- **Scanprüfung:** 87 Zitate wurden neu gelesen. Im ersten Durchgang wurden dabei
  46 Stellen des Entwurfs nach dem Druck korrigiert (Akzente, Apostrophe,
  Wortformen). Ein Beispiel: In IV.XXX.1 liest die OCR „quelli“, gedruckt ist
  „questi“. Die 18 Nachträge sind unmittelbar am Scan abgeschrieben.

### Was Buch IV für die Quellenkritik bringt

- **Palladio sagt, wie seine Tafeln entstanden sind.**
  - Die Gesamtgestalt hat er aus Resten und Fundamenten erschlossen
    (IV.Proemio.6), mit Vitruvs Hilfe (IV.Proemio.7).
  - Die Ornamente hat er an Fragmenten gemessen (IV.Proemio.8).
  - In 15 Fällen nennt er ausdrücklich, was er erschlossen, ergänzt, erfunden
    oder weggelassen hat. Beispiele:
    - die Cella des Mars Ultor, „di mia inuentione“ (IV.VII.2);
    - Vorhallen und Ornamente der Tempel von Sonne und Mond, „come mi sono
      imaginato“ (IV.X.1);
    - ein ganzer Tempel aus einer Flanke und Vitruv (IV.XV.6);
    - der Neptuntempel, von dem nichts mehr steht (IV.XXXI.2).

  Solche Tafelteile sind keine Bauaufnahme. Sie dürfen nicht als Messbefund für
  antike Proportionen zählen. Die vollständige Liste und ihre Folge für den
  Tafeltest stehen in docs/17 und `data/book4/reconstruction.json`.
- **Abweichungen von Vitruv mit Befund:**
  - Postamente: Palladio verwirft sie (IV.V.6). Nur Assisi hat welche (IV.XXVI.1).
  - Die ionische Basis Vitruvs kommt an keinem antiken Bau vor (IV.XIII.2).
  - Die Regel „kein Zahnschnitt unter Konsolen“ ist selten befolgt (IV.XV.2).
- **Spielraum und Urteil:**
  - Abweichen vom Gebrauch ist erlaubt, „pur che tal uariatione sia gratiosa,
    & habbia del naturale“ (IV.XXIIII.1).
  - Ein Gebälk unter ⅕ der Säulenlänge wird gelobt (IV.XV.4).
- **Wahrnehmung korrigiert das Maß:** Die inneren Säulen des Vortempels werden
  dünner gemacht, damit alle gleich dick erscheinen (IV.V.12).
- **Datierung nach dem Stil:** Das sind Palladios eigene Kriterien, nicht unsere:
  - augusteische Bauten sind „più sode“ (IV.XIX.1);
  - gute Ausführung weist auf die gute Zeit, schwächere auf eine spätere
    (IV.VI.2, IV.XXI.2, IV.XXIII.2);
  - ein Bauteil, das zum Ganzen stimmt, ist gleich alt (IV.XX.3).
- **Auswahl der Bauten:** Palladio nimmt auch auf, was er nicht für antik hält,
  und sagt es: das Baptisterium (IV.XVI.4), den Tempietto Bramantes (IV.XVII.1)
  und das Grabmal bei S. Agnese (IV.XXI.1).
- **Die Normen aus Buch I sind nicht der häufigste Wert der Tempel.** Für das
  Korinthische setzt Buch I 2 D Säulenabstand und ⅕ Gebälk. In Palladios eigenen
  Beschreibungen überwiegen 1½ D und ¼ (docs/17).
- **San Giorgio Maggiore** kommt zweimal vor:
  - die Kreuzform (IV.II.8);
  - Blätter unter den zu kurzen Säulenschäften des Portals, nach antikem Vorbild
    (IV.XVI.1, IV.XVI.2).

## Zweiter Durchgang durch Buch I bis III

Stand 17.11.2026. Wie in Buch IV wurden die drei ersten Bücher gezielt nach Stellen
durchsucht, an denen Palladio eine Einzelentscheidung, eine Rekonstruktion oder die
Auswahl eines Beispiels begründet.

- **Verfahren.** Ein Skript listete alle Zeilen, die kein Katalogeintrag abdeckt und
  die ein Merkmal tragen („perche“, „accioche“, „credo“, „inuentione“, „ho uoluto“,
  „doueua“ …). Das waren 60 Zeilen in Buch I, 45 in Buch II und 62 in Buch III,
  dazu einige weitere aus einer zweiten Merkmalsliste. Jede Stelle wurde im
  Zusammenhang gelesen.
- **Ergebnis.** 50 neue Einträge: 15 in Buch I, 24 in Buch II, 11 in Buch III. Alle
  sind am Scan gelesen. Im Entwurf nach der OCR waren 28 Stellen zu korrigieren,
  zum Beispiel „sia proportionata“ statt „habbia“ (II.XIIII.7) und „caminano“ statt
  „cambiano“ (II.XIIII.8).
- **Übersehene Regeln.** Drei Einträge sind keine Begründungen, sondern Regeln, die
  der erste Durchgang übersehen hatte: die Heizung der Antiken (I.XXVII.5), die
  Kühlung durch „Ventidotti“ in Costozza (I.XXVII.6) und die Verstärkung der
  Holzbrücken (III.VIII.5).

### Was der zweite Durchgang bringt

- **Die Zuordnung der Säulenabstände zu den Ordnungen ist Palladios Wahl.** Er sagt
  selbst: „Ne' quali ordini ho hauuto questo risguardo, accioche siano come
  vn'esempio di tutte queste maniere d'intercolunnij“ (I.XIII.14). Die Kopplung von
  Abstand und Säulenhöhe (I.XIII.8) ist also eine Ordnung zum Zeigen, keine Lehre
  Vitruvs. Das passt zum Befund aus docs/17: An den Tempeln, wie Palladio sie
  beschreibt, überwiegen andere Werte.
- **Woher die Profile stammen.** Die toskanischen Profile hat Palladio von der
  Arena in Verona und von Arena und Theater in Pola genommen (I.XIIII.9). Das
  Verfahren für die Schwellung der Säule ist seine eigene Erfindung, die Pietro
  Cattaneo übernahm (I.XIII.13).
- **Sein Studium der Antike.** Er nahm Vitruv zum Führer, maß die Reste „minutissimamente“
  und fand nichts, „che con ragione, & con bella proportione non fusse fatta“
  (I.Proemio.3). Das ist sein Urteil über den Befund, kein Maß.
- **Die Tafeln von Buch II zeigen auch Unfertiges.** Einige gezeichnete Bauten
  seien nicht fertig, aus dem Gebauten lasse sich aber das fertige Werk erkennen
  (II.III.7). Folgerung (B): Bei unvollendeten Bauten zeigen die Tafeln den Entwurf,
  nicht den Bestand. Das betrifft jede Messung an diesen Tafeln (docs/10).
- **Antike Häuser und Plätze sind Deutungen Vitruvs.** Das „atrio testudinato“ zeigt,
  „quel che ne credo“ (II.VII.5); die antike Villa soll zeigen, „come si debba
  intendere Vitruuio“ (II.XVI.6). Am griechischen Platz ergänzt Palladio Nischen,
  Basilika, Curia und Gefängnisse, obwohl Vitruv sie dort nicht nennt, und zwei
  Tempel nach dem Beispiel von Pola (III.XVII.4, III.XVII.5).
- **Begründungen an den eigenen Bauten.** Buch II hat jetzt 42 Begründungen. Sie
  nennen fast immer praktische Gründe:
  - Lage und Wasser: Der Palazzo Chiericati ist 5 Fuß angehoben, weil der Fluss
    nahe ist (II.III.9); anderswo liegen die Keller unter der Erde, weil der Bau
    hoch liegt (II.III.14).
  - Licht: Treppen und Säle werden so gelegt, dass sie Licht von oben erhalten
    (II.XV.7, II.XV.8).
  - Tragwerk: Säulen tragen Gewölbe und sichern den Raum darüber (II.III.11,
    II.XVII.9).
  - Proportion: Säulen im Saal, „accioche sia proportionata l'altezza alla
    larghezza“ (II.XIIII.7, II.XVII.7).

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

1. ~~Die Kapitel von Buch II bis IV nach demselben Verfahren lesen.~~ Erledigt:
   546 Einträge aus 101 Kapiteln, alle am Scan geprüft.
2. ~~San Giorgio Maggiore an vermessenen Plänen prüfen.~~ Erledigt mit Bertotti
   Scamozzi, *Le fabbriche e i disegni di Andrea Palladio*, Bd. IV, 1783
   (docs/15, docs/16).
3. ~~Die Regeln aus Buch I mit Buch IV abgleichen, ob die Säulenordnungen der
   Tempel den Maßen aus Buch I folgen.~~ Erledigt für Palladios Textangaben
   (docs/17). Offen: die Maßzahlen der Tafeln.
4. ~~IV.XVI.2 (Portal von San Giorgio) in die Kriterien von docs/16 aufnehmen.~~
   Erledigt; Bertottis Tafel VI bestätigt die Aussage.
5. ~~Die Tafelteile kennzeichnen, die Palladio als ergänzt oder erfunden
   bezeichnet.~~ Erledigt in `data/book4/reconstruction.json` (docs/17).
6. ~~Die Bücher I bis III ebenso gezielt nach Begründungen von Einzelentscheidungen
   durchsehen.~~ Erledigt (50 Einträge, siehe oben).
7. In der Gesamtauswertung von Buch II (docs/10) prüfen, welche gemessenen Bauten
   1570 unvollendet waren (II.III.7).
