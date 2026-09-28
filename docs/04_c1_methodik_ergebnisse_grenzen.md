# 4. C1-Methodik, Ergebnisse und Grenzen

## Pilotkorpus

1. Buch II, S. 19: Grundriss des Hauses von Paolo Almerico (Planregion der
   gemischten Plan-/Schnittseite).
2. Buch II, S. 17: von Palladio ausdrücklich als halbe Fassade bezeichnete
   Ansicht des Palazzo Valmarana.
3. Buch I, S. 43: korinthisches Kapitell, Gebälk, Untersicht und Maßketten.

## Deterministische Pipeline

1. PDF-Seite mit Poppler auf 200 dpi rendern.
2. Hintergrund durch morphologisches Closing normalisieren.
3. Otsu-Binarisierung ohne manuell erzwungenen Schwellwert.
4. geringe Scanrotation aus Hough-Linien schätzen und korrigieren.
5. konfigurierte, normalisierte Untersuchungsregion ausschneiden.
6. horizontale, vertikale und diagonale Liniensegmente erkennen.
7. Ausdehnung zusammenhängender Tintenkomponenten bestimmen.
8. Spiegelüberlappung an horizontaler und vertikaler Mittelachse berechnen.
9. Rohquotienten gegen Palladios sechs rechteckige Raumverhältnisse und zwei
   explorative Verhältnisse ranken.
10. JSON, Overlay, Binärbild, SQLite und CSV ausgeben.

Kein Sprach- oder Vision-Modell wird benutzt.

## Was vollautomatisch funktioniert

- reproduzierbares Rendering und Pixelkoordinaten;
- Hintergrundnormalisierung und Binarisierung;
- kleine Schiefstandskorrektur;
- grobe Linienorientierung;
- rein bildliche Ausdehnungs- und Symmetriestatistiken;
- Verhältnis-Ranking mit Abweichung;
- unveränderte Rohwertspeicherung und Export.

## Was halbautomatisch ist

- Auswahl der relevanten Druckseite;
- Festlegung einer normalisierten ROI, etwa nur der Grundriss in S. 19;
- Zuordnung der Seite zu `ground_plan`, `elevation` oder `detail`;
- Auswahl der architektonisch plausiblen Messbezüge.

Die ROI steht transparent in `config/pilot.json`; sie ist kein verborgenes
Nachjustieren auf ein erwünschtes Verhältnis.

## Was menschliche Kontrolle erfordert

- Unterscheidung von Wandinnenkante, Wandachse und Außenkante;
- Trennung von Maßlinien, Baukanten, Schraffur, Schrift und Flecken;
- Zuordnung erkannter Rechtecke zu tatsächlichen Räumen;
- Interpretation von Maßziffern und ihrem Bezug;
- Prüfung, ob eine Asymmetrie architektonisch, drucktechnisch oder durch die
  publizierte Halbansicht verursacht ist;
- jede Beförderung einer Messung zum C1-Regelkandidaten.

## Warum noch keine C1-Regel entsteht

Die automatischen Kennwerte messen derzeit Bildstruktur, nicht zuverlässig lichte
Raummaße. Besonders `ink_component_extent` kann Seitenrahmen und Beschriftungen
enthalten. `dominant_line_median` kann in einer Ordnungszeichnung Ornament- und
Maßlinien statt Bauteilgrenzen erfassen. Eine geringe Abweichung zu 4:3 wäre unter
diesen Bedingungen nur eine Proportionshypothese.

Ein C1-Regelkandidat wird erst angelegt, wenn:

- eine semantisch homogene Population definiert ist;
- mindestens die Bezugslinie und Region geprüft sind;
- n, Treffer, Mittelwert, Median, Standardabweichung, mittlere Sollabweichung und
  Ausreißer berechnet sind;
- konkurrierende Verhältnisse und Alternativerklärungen dokumentiert sind.

## Typische Fehlerquellen

- Scan- und Druckverzerrung;
- gebogene Buchseite und nichtlineare Skalierung;
- ungleiche Linienbreite;
- Durchscheinen der Rückseite;
- Flecken, Randverlust und handschriftliche Notizen;
- perspektivisch oder diagrammatisch gemeinte Linien;
- Seitenrahmen, die fälschlich als Gebäudegrenze erscheinen;
- Textziffern, die Komponentenbildung und Symmetrie stören;
- kombinierte Darstellungen auf einer Druckseite;
- Palladios Halbansichten, die nicht als vollständige Fassaden gemessen werden
  dürfen.

