# 3. Produkte

Was aus der Forschung entsteht, in drei Gruppen: wissenschaftliche Texte, Werkzeuge,
Gestaltung. Zu jedem Produkt: Stand, was fehlt, wer als Nächstes am Zug ist.

## 3.1 Wissenschaftliche Texte

### P1 Hausarbeit „Die Architekturtheorie Andrea Palladios am Beispiel der Basilika San Giorgio Maggiore“, Fassung 2026

- **Stand:** Entwurf V3 als Word-Datei, Methode vorn, Kosmologie über das Umfeld,
  21 Kriterien im Vergleich. Etwa 41.500 Zeichen. Du schreibst ihn persönlich aus.
- **Liegt nicht im Repositorium.** Deine Arbeit bleibt privat.
- **Am Zug: du.**
  - Seitenzahlen ergänzen: Beltramini, Goethe, Oechslin, Forssman, Kruft, Lücke,
    Wittkower;
  - einen Beleg für die Statuen der Fassade und für Wandfarbe und Boden finden;
  - die eigenen Messungen am Plan nach Canales neu machen;
  - entscheiden: Haramein-Passage, Titel, Umfang;
  - prüfen: Datierung 1564 oder 1565, das UNESCO-Jahr der Villen, und ob Palladio
    die Fassade von San Francesco della Vigna entwarf.

### P2 Aufsätze

- **Stand:** vorgeschlagen, nicht freigegeben.
- **Vorschläge:**
  1. Methode: Nullmodell und Raummaße aus Buch II (etwa Nexus Network Journal oder
     Architectural Histories);
  2. Quellenkritik: Tempeltafeln in Buch IV, Selbstauskunft, Text, Zahl und
     Zeichnung (etwa Annali di architettura);
  3. Fallstudie San Giorgio.
- **Am Zug: du** (Freigabe, Reihenfolge, Sprache).

### P3 Regelkatalog als offener Datensatz

- **Stand:** Die Daten sind fertig (546 Regeln, am Scan geprüft). Veröffentlichung
  vorgeschlagen, nicht begonnen.
- **Fehlt:** eine Lizenz für Code und Daten; ein Ort mit DOI (etwa Zenodo); eine
  kurze Datenbeschreibung.
- **Am Zug: du** (Lizenz und Freigabe).

## 3.2 Werkzeuge

### P4 Entwurfskern und Entwurfslabor

- **Stand:** Prototyp.
  - Der Entwurfskern (`src/palladio_code/design.py`) entwirft einen Villenblock in
    acht Schritten.
  - Das Entwurfslabor (`app/dist/palladio-labor.html`) ist eine Datei für das iPad:
    Raumtiefen werden mit dem Pencil gezogen, zu jedem Schritt erscheinen Regelkarten.
- **Fehlt:** weitere Bautypen und die Fassade.
- **Detailfrage:** Das Labor spielt Raumverhältnisse als Klang. Palladio nennt aber
  keine musikalischen Intervalle (docs/19). Soll der Klang bleiben, deutlich als
  Gestaltung gekennzeichnet, oder entfallen?

### P5 Forschungsanwendung nach dem Übergabeplan

- **Stand:** nicht begonnen.
- **Plan** (CLAUDE_HANDOFF.md): Webanwendung mit Regelkarten, Suche, Scanvergleich,
  Prüfwarteschlange für die 704 Kandidaten, Tafelviewer.
- **Der Forschungskern ist inzwischen weiter als der Plan:** Der Katalog wurde von
  Hand gebaut statt über die Prüfwarteschlange.
- **Am Zug: du.** Ob und wann diese Anwendung noch gebraucht wird.

## 3.3 Gestaltung (Deutungsschicht D)

### P6 Gestaltungsrichtlinie

- **Stand:** Entwurf (docs/18). 13 Übertragungen von Palladios Regeln auf Webseiten,
  jede mit Fundstelle, Stärke und Grenze; 5 verworfene Übertragungen.
- **Am Zug: du.** Freigabe oder Änderungen.

### P7 WordPress-Theme „Palladio“

**Was es ist.** Ein Theme ist das Kleid einer WordPress-Seite: Schrift, Farben,
Abstände, Seitenvorlagen und Muster. Inhalte enthält es nicht. Unser Theme setzt die
Gestaltungsrichtlinie (P6) um.

**Was fertig ist.**

- **Ordner:** `products/wordpress/palladio` mit allem, was WordPress ab 6.6 braucht.
  Schrift und Bilder liegen im Theme, es lädt nichts von fremden Servern.
- **Geprüft** sind die Einstellungsdateien, die Blockauszeichnung, die PHP-Syntax und
  eine Musterseite im Browser (`output/web/specimen.html`).

**Was nicht fertig ist.**

- **Nie in WordPress getestet.** Das Theme lief noch nie in einem echten WordPress.
  In der Cloud wurde der Download von WordPress von einer Sicherheitsprüfung
  gestoppt. Auf deinen Rechner kann diese Cloud-Sitzung nicht zugreifen.
- **Keine Inhalte.** Es gibt noch keine Homepage-Inhalte: weder Startseite noch
  Seitenstruktur noch Texte.
- **Kein Ort.** Wo die Seite später liegt (Anbieter, Adresse), ist offen. Ebenso
  Impressum und Datenschutzerklärung.

**Wie es weitergeht**, in dieser Reihenfolge:

1. **Testen.** Zwei Wege:
   - **Auf deinem Rechner:** Du richtest Local ein. Dann arbeitet eine
     Claude-Sitzung im Desktop-App auf deinem Rechner: Sie verknüpft den
     Theme-Ordner mit der Local-Seite und prüft alle Vorlagen.
   - **In der Cloud:** Du erlaubst ausdrücklich, WordPress hier herunterzuladen.
     Das ist schneller, aber weniger echt.
2. **Inhalte festlegen:** Welche Seiten braucht die Homepage? Zum Beispiel
   Projekt, Regeln, Bauten, Labor, Über mich.
3. **Ort wählen:** Anbieter und Adresse, Impressum, Datenschutz.
4. **Später, wenn gewünscht:** das Theme im WordPress-Verzeichnis anbieten. Das
   Theme steht bereits unter GPL.

**Am Zug: du**, mit der Wahl des Testwegs.
