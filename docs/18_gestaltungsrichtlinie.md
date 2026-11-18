# 18. Gestaltungsrichtlinie „Palladio“

Stand: 18.11.2026 · Daten: `data/interpretation/web.json` · Erzeugung: `make web` →
`output/web/tokens.json`, `output/web/specimen.html`,
`products/wordpress/palladio/theme.json`, `products/wordpress/palladio/styles/notte.json`
· Theme: `products/wordpress/palladio/` · Tests: `tests/test_webdesign.py`,
`tests/test_theme_markup.py`

## Status

Diese Richtlinie ist eine **Deutung (Klasse D)**. Sie sagt nicht, was Palladio
meinte. Sie sagt, wie dieses Projekt einige seiner Regeln für Webseiten verwendet.

- Jede Übertragung nennt die Einträge des Regelkatalogs (docs/14), auf die sie sich
  stützt. Diese Einträge sind Klasse A und am Scan geprüft.
- Jede Übertragung sagt, wie eng sie ist, und wo sie endet.
- Verworfene Übertragungen bleiben mit Grund im Protokoll.
- Was ohne Regel gewählt ist, steht als freie Wahl da.
- Nichts fließt in den Katalog zurück. `validate()` prüft, dass jede genannte
  Regel-ID im Katalog steht.

| Stärke | Bedeutung |
|---|---|
| eng | dieselbe Struktur: ein Verhältnis oder Verfahren wird unverändert übernommen |
| lose | nur der Gedanke wird übertragen; die Zahlen sind eigene Wahl |
| frei | Gestaltungsentscheidung ohne Regel Palladios |

## Übersicht

| ID | Übertragung | Fundstellen | Stärke |
|---|---|---|---|
| W-MODUL | Ein relatives Grundmaß | I.XIII.11, I.I.5 | eng |
| W-ABSTAENDE | Abstände aus den Säulenstellungen | I.XIII.4, I.XIII.6, IV.IIII.7 | lose |
| W-FORMEN | Sieben Raumformen als Bildformate | I.XXI.5, I.XXI.3 | eng |
| W-MITTEL | Schriftgrade aus den drei Mitteln | I.XXIII.3–6 | eng |
| W-DECORUM | Große Glieder in großen Bauten | II.I.4, II.II.6 | lose |
| W-OTTICA | Die Wahrnehmung korrigiert das Maß | I.XIII.2, IV.V.12 | lose |
| W-ACHSE | Eine Mitte, durchgehende Achsen | I.XXI.2, I.XXI.4, I.XXV.8, I.XIII.9 | lose |
| W-FENSTER | Ein Bildmaß je Reihe | I.XXV.6 | eng |
| W-ORNAMENT | Kein Ornament ohne Aufgabe | I.XX.3, I.XX.5, I.XX.8, I.XX.11 | lose |
| W-TREPPE | Navigation wie eine gute Treppe | I.XXVIII.2, I.XXVIII.3 | lose |
| W-SERVIZI | Dienende Teile verborgen, aber erreichbar | II.II.2 | lose |
| W-BIANCO | Weiß, ruhige Bilder, angemessenes Licht | IV.II.12, IV.II.13, I.XXV.12 | lose |
| W-VARIAZIONE | Abweichung mit Anmut | IV.XXIIII.1, I.XX.7 | eng |

## Die Übertragungen

### W-MODUL · Ein relatives Grundmaß · eng

**Palladio.** Keine Elle, kein Fuß, kein Palm, sondern ein Maß aus der Säule selbst:
der Modul, unterer Durchmesser = 60 Minuten. „potrà ciascuno facendo il Modulo
maggiore, e minore secondo la qualità della fabrica seruirsi delle proportioni“
(I.XIII.11). Schönheit entsteht aus der Entsprechung der Teile untereinander und
zum Ganzen (I.I.5).

**Web.** Alle Längen gehen von einem Modul aus: der Zeilenhöhe des Fließtexts. Feine
Maße in Minuten (1/60 Modul). Angaben in rem, damit die Einstellung des Lesers
gilt. Pixel nur für Haarlinien (1px).

**Werte.** Modul 1,594–1,781 rem (1,5 × Grundschrift). Token
`--wp--custom--palladio--modulo`, `--wp--custom--palladio--minuto`.

**Grenze.** Palladios Modul ist der Säulendurchmesser, hier ist es die Zeilenhöhe.
Gleich ist das Prinzip, nicht der Gegenstand.

### W-ABSTAENDE · Abstände aus den Säulenstellungen · lose

**Palladio.** Säulenabstände von 1½, 2, 2¼ und 3 Durchmessern (I.XIII.4). Am
meisten schätzten die Antiken 2¼ (I.XIII.6); Eustylos ist die schönste und
eleganteste Tempelart (IV.IIII.7).

**Web.** Die Abstandsskala besteht aus ¼, ½, 1, 1½, 2, 2¼, 3 und 4 Moduln.
Abschnitte einer Seite stehen 2¼ Moduln auseinander, große Abschnitte 3 Moduln.

**Werte.** WordPress-Abstände `10` bis `80`; `60` = 2¼ Moduln (Eustylos).

**Grenze.** Übernommen sind nur die Zahlen. Die Säulenstellung selbst wird nicht
übertragen (R-INTERCOLUMNIO).

### W-FORMEN · Sieben Raumformen als Bildformate · eng

**Palladio.** „Le più belle e proportionate maniere di stanze […] sono sette“: rund
(selten), Quadrat, Diagonale des Quadrats, 4 : 3, 3 : 2, 5 : 3, 2 : 1 (I.XXI.5). Säle
nicht länger als zwei Quadrate (I.XXI.3).

**Web.** Bilder, Karten und Felder haben eines der sechs rechteckigen Formate.
Nichts ist breiter als 2 : 1. Der Kreis ist selten und Porträts vorbehalten.

**Werte.** Seitenverhältnisse im Editor: 1:1, √2:1, 4:3, 3:2, 5:3, 2:1. Der Test
vergleicht sie mit dem Nullmodell `PALLADIO_I21` (docs/07).

**Grenze.** Palladio meint Grundrisse von Räumen, hier sind es Bildflächen. Die
Verhältnisse sind dieselben.

### W-MITTEL · Schriftgrade aus den drei Mitteln · eng

**Palladio.** Drei Verfahren, die Höhe eines Raums aus Länge und Breite zu finden:
arithmetisch, geometrisch, harmonisch (I.XXIII.3–5). Man wählt jeweils das, mit dem
Räume verschiedener Größe „i uolti egualmente alti“ und doch proportionierte
Gewölbe erhalten (I.XXIII.6).

**Web.** Zwischen 1 und 2 liegen die drei Mittel 3/2, √2 und 4/3. Sie sind die
Stufen der Schriftskala: auf schmalen Bildschirmen 4/3, auf breiten 3/2, dazwischen
gleitend.

**Werte.**

| Grad | Name | rem (schmal–breit) | Zeilenabstand | Laufweite |
|---|---|---|---|---|
| small | Klein | 0,797–0,891 | 1,5 | 0 |
| medium | Text | 1,063–1,188 | 1,5 | 0 |
| large | Groß | 1,417–1,781 | 1,386 | 0 |
| x-large | Sehr groß | 1,889–2,672 | 1,297 | −0,005 em |
| xx-large | Titel | 2,519–4,008 | 1,229 | −0,010 em |
| huge | Eingang | 3,358–6,012 | 1,177 | −0,015 em |

h1 = Titel, h2 = Sehr groß, h3 = Groß, h4 und h5 = Text, h6 = Klein. Die Stufe unter
dem Text hat an beiden Enden 4/3, damit kleine Schrift nicht schrumpft.

**Grenze.** Die drei Mittel sind mathematisch dieselben. Dass Schriftgrade wie
Raumhöhen gewählt werden, ist Deutung.

### W-DECORUM · Große Glieder in großen Bauten · lose

**Palladio.** „ne gli edificij grandi; ui siano membri grandi; ne' piccioli, piccioli,
e ne i mediocri, mediocri“ (II.I.4). Große, mittlere und kleine Räume entsprechen
einander (II.II.6).

**Web.** Modul und Schriftgrade wachsen mit der Bildschirmbreite (22–80 rem),
innerhalb fester Grenzen. Eine Seite hat große, mittlere und kleine Abschnitte, die
einander entsprechen.

**Grenze.** Ein Bildschirm ist kein Bau. Übertragen ist der Gedanke der
Angemessenheit.

### W-OTTICA · Die Wahrnehmung korrigiert das Maß · lose

**Palladio.** Hohe Säulen verjüngen sich weniger, weil die Entfernung selbst
verjüngt (I.XIII.2). Innere Säulen werden etwas dünner gemacht, damit alle gleich
erscheinen (IV.V.12).

**Web.** Je größer die Schrift, desto geringer der Zeilenabstand im Verhältnis und
desto enger die Laufweite. So erscheinen große und kleine Grade gleich ruhig.

**Grenze.** Die Zahlen der Korrektur sind eigene Wahl.

### W-ACHSE · Eine Mitte, durchgehende Achsen · lose

**Palladio.** Jedes wohlgeordnete Haus hat „nel mezo, & nella più bella parte loro
alcuni luoghi: ne' quali rispondono, & riescono tutti gli altri“ (I.XXI.2). Rechts
gleich links (I.XXI.4), Leer über Leer, Voll über Voll (I.XXV.8). An Fronten eine
gerade Säulenzahl, damit in der Mitte ein Joch liegt (I.XIII.9).

**Web.** Jede Seite hat eine Hauptachse in der Mitte. Ränder links und rechts sind
gleich. Alle Abschnitte nutzen dieselben zwei Breiten, so dass Kanten übereinander
stehen. Raster haben eine gerade Spaltenzahl.

**Werte.** Textbreite 33,75 rem, breite Abschnitte 50,625 rem.

**Grenze.** Text neben Bild ist erlaubt, wenn die Achse der Seite bleibt.

### W-FENSTER · Ein Bildmaß je Reihe · eng

**Palladio.** „le finestre deono essere tutte vguali nel loro ordine, ò solaro“,
obwohl die Räume groß, mittel und klein sind (I.XXV.6).

**Web.** In einer Reihe oder Galerie haben alle Bilder dasselbe Format, unabhängig
vom Motiv.

### W-ORNAMENT · Kein Ornament ohne Aufgabe · lose

**Palladio.** Zu tadeln ist, was sich von der Natur der Dinge entfernt (I.XX.3).
Jeder Teil des Gesimses muss einen Zweck haben (I.XX.5). Ornamente nicht zu weit
auskragen lassen (I.XX.8). Gesimse in Proportion zu den Säulen (I.XX.11).

**Web.** Keine Schatten, Verläufe oder Zierrahmen. Linien nur, wo sie trennen.
Überschriften stehen in Proportion zum Text (W-MITTEL). Links sind unterstrichen,
weil man sie sonst nicht erkennt.

### W-TREPPE · Navigation wie eine gute Treppe · lose

**Palladio.** Der Zugang zur Treppe ist umso lobenswerter, je weniger er versteckt
ist; am besten zeigt der Weg „la più bella parte della casa“, und er ist „manifesta,
e facile da trouarsi“. Oben führt die Treppe in weite, schöne Räume (I.XXVIII.2).
Gute Treppen sind hell, weit und bequem, nie unter 4 Fuß, damit zwei Personen
einander ausweichen können (I.XXVIII.3).

**Web.** Die Navigation ist sofort sichtbar, kurz und führt zum wichtigsten Inhalt.
Ziele sind mindestens 2¾ rem hoch und stehen ½ Modul auseinander.

**Werte.** `--wp--custom--palladio--ziel` = 2,75 rem.

### W-SERVIZI · Dienende Teile verborgen, aber erreichbar · lose

**Palladio.** Wie am Körper liegen im Haus die ansehnlichen Teile offen, die dienenden
möglichst verborgen; ohne sie könnten die schönen nicht bestehen (II.II.2).

**Web.** Impressum, Datenschutz, Anmeldung und Ähnliches stehen klein im Fuß der
Seite, nie im Kopf.

### W-BIANCO · Weiß, ruhige Bilder, angemessenes Licht · lose

**Palladio.** „Tra tutti i colori niuno è, che si conuenga più à i Tempij, della
bianchezza“ (IV.II.12). Keine Bilder, die von der Betrachtung ablenken (IV.II.13).
Fenster geben nicht mehr und nicht weniger Licht als nötig (I.XXV.12).

**Web.** Grund ein warmes Weiß, Schrift dunkle Druckfarbe, keine Signalfarben.
Bilder ordnen sich dem Text unter. Weder reines Weiß noch reines Schwarz;
Kontrast mindestens 7 : 1.

**Grenze.** Palladio spricht vom Tempel, nicht vom Wohnhaus und nicht von
Bildschirmen.

### W-VARIAZIONE · Abweichung mit Anmut · eng

**Palladio.** „non è uietato all'Architetto partirsi alcuna uolta dall'uso commune,
pur che tal uariatione sia gratiosa, & habbia del naturale“ (IV.XXIIII.1). Auch die
Antiken variierten, ohne die allgemeinen Regeln zu verlassen (I.XX.7).

**Web.** Jede Regel dieser Richtlinie darf gebrochen werden, wenn es dem Inhalt
dient. Die Abweichung wird benannt.

## Verworfene Übertragungen

| ID | Idee | Fundstellen | Warum nicht |
|---|---|---|---|
| R-INTERCOLUMNIO | Säulenabstand als Spaltenabstand im Raster | I.XIII.6, I.XIII.8 | Im Bau ist der Raum zwischen den Säulen 1½- bis 3-mal so breit wie die Säule. Im Raster ist der Inhalt der Raum und der Abstand die Wand. 2¼ Spaltenbreiten Abstand wären widersinnig. |
| R-SAEULENHOEHE | Säulenhöhe nach Säulenabstand (je enger, desto schlanker) als Kopplung von Zeilenlänge und Zeilenabstand | I.XIII.8 | Der Zeilenabstand bestimmt hier den Modul, und die Textbreite ist in Moduln gemessen. Hinge der Zeilenabstand von der Textbreite ab, wäre das Grundmaß zirkulär. |
| R-GEBAELK | Gebälk ⅕ der Säule, Architrav : Fries : Gesims = 4 : 3 : 5, als Kopf, Inhalt und Fuß der Seite | I.XVI.7, I.XVII.5 | Eine Seite trägt keine Last, und ihr Kopf richtet sich nach dem Inhalt. Das wäre Zahlensymbolik. |
| R-ORDINI | Die festeste Ordnung nach unten: schwerer Fuß, leichter Kopf | I.XII.1 | Eine Seite wird von oben gelesen; der Titel braucht Gewicht. |
| R-MITTELJOCH | Das mittlere Joch etwas weiter: breiterer mittlerer Abstand in Galerien | I.XIII.9 | Am Bildschirm wirkt ein ungleicher Abstand wie ein Fehler. Übernommen ist nur die gerade Spaltenzahl (W-ACHSE). |

Docs/14 hatte das Gebälk und die Kopplung von Säulenhöhe und Abstand als Kandidaten
genannt. Beide sind hier verworfen (R-GEBAELK, R-SAEULENHOEHE).

## Freie Wahl

| Was | Wert | Grund |
|---|---|---|
| Grundschrift | 1,0625–1,1875 rem, gleitend | Lesbarkeit der Garamond am Bildschirm |
| Zeilenabstand des Fließtexts | 1,5 | typografische Konvention; bestimmt den Modul |
| Schrift | EB Garamond (Georg Duffner, Octavio Pardo; SIL OFL 1.1) | Renaissance-Antiqua mit Kursive; Vorlagen von Garamont und Granjon aus dem 16. Jh. Dieselbe Type wie 1570 ist das nicht. |
| Textbreite | 20 Moduln bei mittlerer Grundschrift = 33,75 rem | etwa 65 Zeichen je Zeile |
| Breite Abschnitte | Textbreite × 3/2 = 50,625 rem | eine der sieben Formen; eigene Wahl |
| Nachtvariante „Notte“ | Druckfarbe als Grund, Papier als Schrift | keine Regel Palladios |

## Farben

Die Farben sind am Scan gemessen, nicht erfunden: e-rara-Exemplar der ETH-Bibliothek
(Rar 439), Buch IV, S. 5, 9 und 55 (phys. 205, 209, 255), Satzspiegel. Druckfarbe =
Median der dunkelsten 2 %, Papier = Median der helleren Hälfte; über die drei Seiten
der Median je Farbkanal.

| Name | Tag | Nacht | Herleitung (Tag) |
|---|---|---|---|
| Calce (Grund) | `#f7f5f0` | `#282621` | Papier, zu ¾ mit Weiß gemischt |
| Inchiostro (Schrift) | `#424037` | `#ece8dc` | Druckfarbe des Scans |
| Carta (Papier) | `#dfd8c5` | `#38362f` | Papier des Scans |
| Pietra (Nebentext) | `#66645c` | `#aca697` | Druckfarbe, zu ⅕ mit Calce gemischt |
| Linea (Haarlinie) | `#cac8c2` | `#56524a` | Druckfarbe, zu ¾ mit Calce gemischt |

Kontrast Schrift/Grund: Tag 9,54 : 1, Nacht 12,34 : 1. Nebentext/Grund: Tag 5,44 : 1,
Nacht 6,23 : 1. Der Test verlangt mindestens 7 : 1 und 4,5 : 1.

**Vorbehalt.** Das ist die Farbe des heutigen Scans: gealtertes Papier, ein
bestimmter Scanner. Die Farbe des Drucks von 1570 ist es nicht.

## Bilder

Das Theme bringt zwei Ausschnitte aus Buch II, S. 19 (phys. 91, Villa Almerico,
„La Rotonda“) mit: Aufriss im Format 4 : 3, Grundriss im Format 1 : 1. Quelle ist
derselbe Scan (DOI 10.3931/e-rara-363, Public Domain Mark 1.0).

## Das Theme

`products/wordpress/palladio/` ist ein Blocktheme für WordPress ab 6.6.

- `theme.json` und `styles/notte.json` werden erzeugt. Nicht von Hand ändern.
- Vorlagen: Startseite, Beitrag, Seite, Seite „Mitte“, Archiv, Suche, 404.
- Muster: „Eingang mit Mitte“ (eine Hauptachse, W-ACHSE), „Zwei Räume: Bild und
  Text“ (Aufriss der Rotonda, 4 : 3), „Vier Felder“ (gerade Zahl, die Mitte ist ein
  Zwischenraum, I.XIII.9).
- Schrift und Bilder liegen im Theme. Es lädt nichts von fremden Servern.

Musterseite: `output/web/specimen.html` zeigt alle Werte im Browser. Sie lädt
Schrift und Bilder aus dem Theme-Ordner.

**Nicht geprüft.** Das Theme ist noch nicht in einer laufenden WordPress-Installation
getestet. Geprüft sind die JSON-Verweise, die Blockauszeichnung, die PHP-Syntax und
die Darstellung der Musterseite bei 390, 1200 und 1440 Pixel Breite.

## Neu erzeugen

```
make web
make test
```
