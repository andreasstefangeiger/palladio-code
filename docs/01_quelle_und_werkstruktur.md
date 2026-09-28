# 1. Quelle und Werkstruktur

## Ausgewählte Primärquelle

Andrea Palladio: *I quattro libri dell'architettura di Andrea Palladio*.
Venedig: appresso Dominico de' Franceschi, 1570. Exemplar:
ETH-Bibliothek Zürich, Rar 439. Persistenter Identifikator:
https://doi.org/10.3931/e-rara-363. Das Digitalisat ist mit Public Domain Mark
gekennzeichnet und frei herunterladbar.

Die Quelle wurde gewählt, weil sie alle vier Bücher der Erstausgabe, hochauflösende
Seitenscans, OCR-Text, ALTO-XML und ein IIIF-Manifest aus einer wissenschaftlichen
Bibliothek verbindet. Für die Reproduzierbarkeit werden Scan und institutionelles
OCR unverändert lokal aufbewahrt.

## Drei Seitennummern, die nie vermischt werden dürfen

1. `physical_image_number`: Position des Blatts im ALTO/IIIF-Korpus.
2. `pdf_page`: technische, einsbasierte Seite der heruntergeladenen PDF-Datei.
3. `printed_page`: im Druck sichtbare Paginierung, die mit jedem Buch neu beginnt.

Im vorliegenden PDF ist `pdf_page = physical_image_number + 1`. Diese Relation ist
eine Eigenschaft genau dieser Ableitung und darf bei einem anderen Download nicht
vorausgesetzt werden. Quellenangaben der Regeln verwenden primär Buch, Kapitel und
gedruckte Seite; die PDF-Seite dient als reproduzierbarer Zugriffspfad.

## Bibliografische Makrostruktur

| Buch | Beginn im Korpus | Gedruckter Umfang | Kapitel | Hauptgegenstände |
|---|---:|---:|---:|---|
| I | phys. Bild 9 | 67 Seiten | XXIX | Baustoffe, Fundamente, Mauern, fünf Ordnungen, Räume, Höhen, Öffnungen, Treppen, Dächer |
| II | phys. Bild 73 | 66 [recte 78] Seiten | XVII | private Häuser in Stadt und Land, eigene Entwürfe, griechische und römische Haustypen, Villen |
| III | phys. Bild 153 | 46 Seiten plus 1 Blatt | XXI | Wege, Straßen, Brücken, Plätze, Basiliken, Xysten und Palästren |
| IV | phys. Bild 201 | 128 Seiten plus 3 Blätter | XXXI | Tempeltypen, Dekorum, Kompartiment, antike und neuere Tempelaufnahmen |

Die Korpusstruktur des Portals nennt außerdem Vorderdeckel auf Bild 1 und
Rückdeckel auf Bild 338; das heruntergeladene PDF umfasst 339 technische Seiten.

## Tafeln und Abbildungen

Die Ausgabe besitzt keine moderne, separat nummerierte Tafelserie. Holzschnitte,
Grundrisse, Ansichten, Schnitte, Maßketten und Details sind in die Paginierung
integriert; eine Druckseite kann mehrere Darstellungstypen enthalten. Ein
wissenschaftlich brauchbarer C1-Katalog muss daher mindestens zwei Ebenen führen:

- `drawing_page`: die publizierte Druckseite;
- `drawing_region`: der semantisch getrennte Grundriss, Schnitt, die Ansicht,
  Beschriftung, Maßkette oder das Detail innerhalb dieser Seite.

Eine bloße Anzahl „der Tafeln“ wäre ohne vorherige Segmentierungsregel nicht
reproduzierbar. Der Pilot katalogisiert deshalb zunächst drei Seiten und ihre
konfigurierten Untersuchungsregionen. Die vollständige Inventarisierung ist ein
Ausgabeschritt der späteren Gesamtpipeline, kein vorausgesetzter Bibliografiebefund.

## Bautypen und Themen aus dem Werk

Die erste werkinterne Typologie unterscheidet:

- private Häuser allgemein;
- Stadthäuser und Paläste;
- suburbane Häuser (Palladio ordnet Almericos Haus wegen Stadtnähe nicht den
  Villen zu);
- Villen und landwirtschaftliche Anlagen;
- antike griechische und römische Privathäuser;
- Straßen und Wege;
- Brücken;
- Plätze und die sie rahmenden Bauten;
- Basiliken;
- Xysten und Palästren;
- Tempel und Kirchen in mehreren Form- und Ordnungsarten.

Diese Liste ist kontrolliertes Startvokabular, keine abgeschlossene Ontologie.
Die maschinell aus ALTO gewonnenen Kapitelüberschriften werden in
`output/chapter_candidates.json` als **redaktionell zu prüfende Kandidaten**
ausgegeben.

## Quellenkritische Grenzen

- Das institutionelle OCR verwechselt häufig Lang-s, `f`, `s`, Ziffern und
  römische Zahlen. Es dient der Suche, nicht der endgültigen Transkription.
- Handschriftliche Einträge, Flecken, Durchscheinen und beschädigte Ränder werden
  vom Analyzer als Bildinformation erkannt und können Messungen beeinflussen.
- Palladios publizierte Zeichnung ist C1-Evidenz, nicht automatisch ein Aufmaß des
  gebauten Zustands.
- Die im Buch angegebene Maßzahl und die aus Pixeln gemessene Geometrie sind zwei
  getrennte Beobachtungen und müssen getrennt gespeichert werden.

