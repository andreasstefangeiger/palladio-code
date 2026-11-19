# Forschungsprojekt Palladio-Code: Überblick

Stand: 19.11.2026

Diese Mappe ordnet das Projekt in drei Teile:

1. **Gegenstand** ([1_gegenstand.md](1_gegenstand.md)): woran wir arbeiten, also Quellen
   und Bestände.
2. **Forschungsfragen** ([2_forschungsfragen.md](2_forschungsfragen.md)): was wir wissen
   wollen, was beantwortet ist und was offen bleibt.
3. **Produkte** ([3_produkte.md](3_produkte.md)): was daraus entsteht, also Texte,
   Werkzeuge und Gestaltung.

Die Einzelheiten stehen in `docs/01` bis `docs/19`. Diese Mappe sagt, wo was steht
und wie weit es ist.

## Auf einen Blick

Stand: **erreicht** · **weitgehend** (Kern fertig, Einzelheiten offen) · **begonnen** ·
**vorgeschlagen** (noch nicht freigegeben) · **nicht begonnen**

### Gegenstand

| Baustein | Stand | Ort |
|---|---|---|
| Quattro Libri 1570, Text: Regelkatalog | erreicht: 546 Regeln aus 101 Kapiteln, alle am Scan gelesen | docs/14 |
| Quattro Libri, Tafeln Buch II | erreicht: 86 Raummaße aus 32 Bauten | docs/08–11 |
| Quattro Libri, Tafeln Buch IV | weitgehend: 17 Tempel, einige Zahlen unlesbar | docs/13, 17 |
| San Giorgio Maggiore, gebaut | weitgehend: eine Bauaufnahme (Bertotti, 18. Jh.) | docs/15, 16 |
| Palladios Umfeld | begonnen: 4 Quellen, 19 Stellen | docs/19 |
| 704 automatische Textkandidaten | offen: nicht mit dem Katalog abgeglichen | docs/06 |

### Forschungsfragen

| Frage | Stand | Ort |
|---|---|---|
| M Was beweist ein Proportionstreffer? | beantwortet | docs/07 |
| F1 Folgen Palladios Bauten in Buch II seinen Regeln? | beantwortet | docs/08–11 |
| F2 Gibt es eine eigene Lehre für Kirchen? | beantwortet: nein | docs/13 |
| F3 Welche Regeln stellt Palladio auf, wie begründet er sie? | beantwortet | docs/14 |
| F4 Tempel in Buch IV: gemessen oder rekonstruiert? | weitgehend | docs/17 |
| F5 San Giorgio: Theorie und Praxis | weitgehend | docs/15, 16 |
| F6 Welche Kosmologie liegt zugrunde? | begonnen | docs/19 |
| F7 Lässt sich die Entwurfsweise als Prozess fassen? | begonnen | docs/12 |

### Produkte

| Produkt | Stand | Ort |
|---|---|---|
| Hausarbeit San Giorgio, Fassung 2026 | Entwurf V3, bei dir | nicht im Repositorium |
| Aufsätze | vorgeschlagen | – |
| Regelkatalog als offener Datensatz | vorgeschlagen; Lizenz fehlt | data/rules |
| Entwurfslabor | Prototyp | app/, docs/12 |
| Forschungsanwendung nach Übergabeplan | nicht begonnen | CLAUDE_HANDOFF.md |
| Gestaltungsrichtlinie | Entwurf | docs/18 |
| WordPress-Theme „Palladio“ | gebaut, nie in WordPress getestet | products/wordpress/palladio |

## Was du entscheiden musst

1. **Hausarbeit:** Seitenzahlen ergänzen, eigene Messungen neu machen, Umfang und
   Haramein-Passage klären (Einzelheiten in 3_produkte.md).
2. **WordPress:** Wo wird das Theme getestet, auf deinem Rechner (Local) oder in der
   Cloud mit deiner Erlaubnis? Danach: welche Inhalte die Seite bekommt und wo sie
   später liegt.
3. **Lizenz** für Code und Daten. Ohne sie lässt sich nichts veröffentlichen.
4. **Nächster Forschungsschritt**, einer von dreien:
   - das Umfeld weiterlesen (Alberti, Barbaro 1567, Giorgis Denkschrift);
   - die 704 automatischen Kandidaten mit dem Katalog abgleichen;
   - Aufsatz 1 beginnen (Methode und Nullmodell).

## Belegordnung (gilt überall)

| Klasse | Bedeutung |
|---|---|
| A | Palladios Wortlaut, am Scan gelesen, mit Fundstelle |
| B | Rekonstruktion mit Begründung |
| C1 | Messung oder Hypothese an Palladios Tafeln |
| C2 | gebaute Praxis (bisher: San Giorgio nach Bertotti) |
| D | Deutung, als solche gekennzeichnet (Kosmologie, Gestaltung) |
| automatisch | maschineller Hinweis, nie von selbst A oder B |

Rohmaß, Zielverhältnis und Deutung bleiben getrennt. Eine kleine Abweichung beweist
keine Absicht.
