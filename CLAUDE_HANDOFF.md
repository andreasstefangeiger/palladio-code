# Übergabe-Prompt für Claude Code: Palladio-Code

Du arbeitest an dem Projekt **Palladio-Code**.

Primäres Repository:
**https://github.com/andreasstefangeiger/palladio-code**

Zugehöriges älteres Fassadenexperiment:
**https://github.com/andreasstefangeiger/palladian-facades**

`palladio-code` ist der quellenkritische Forschungs- und Datenkern.
`palladian-facades` ist ein älterer SVG-Generator und darf als gestalterische
oder technische Ideenquelle untersucht werden. Entwickle eine nachvollziehbare
Integrationsstrategie zwischen beiden Repositories, aber verschiebe oder
überschreibe keine wissenschaftlichen Daten ungeprüft.

Bitte beginne nicht sofort mit einem großen Umbau. Untersuche zuerst das
Repository vollständig, lies die vorhandene Dokumentation und prüfe, was
tatsächlich reproduzierbar funktioniert. Arbeite anschließend selbstständig in
kleinen, nachvollziehbaren Ausbaustufen mit sauberen Commits beziehungsweise
Pull Requests.

## 1. Ziel des Projekts

Palladio-Code soll aus Andrea Palladios *I quattro libri dell'architettura*
(Venedig 1570) eine wissenschaftlich nachvollziehbare, maschinenlesbare und
interaktiv nutzbare Entwurfslogik erschließen. Langfristig soll daraus eine
ästhetisch anspruchsvolle Forschungssoftware entstehen, die drei Dinge
verbindet:

1. **Quellenkritische Wissensbasis:** Regeln, Belegstellen, Übersetzungen,
   Herleitungen und Unsicherheiten bleiben überprüfbar.
2. **Analysewerkzeug:** Textstellen, Zeichnungen, Maße, Verhältnisse und
   wiederkehrende Entwurfsentscheidungen können durchsucht und verglichen
   werden.
3. **Entwurfslabor:** Nutzer können Parameter verändern und sehen, welche
   palladianischen Regeln anwendbar sind, wo Varianten entstehen und wo ein
   Entwurf bewusst von der Quelle abweicht.

Die Software darf nicht so tun, als habe Palladio einen modernen Algorithmus
formuliert. Sie soll vielmehr sichtbar machen, was Quelle, Messung,
Interpretation, Rekonstruktion und Hypothese ist.

## 2. Vorhandener Stand

Das Repository enthält einen Python-Pilot mit SQLite als kanonischer Datenbasis.
Vorhanden sind unter anderem:

- Primärquelle, OCR und ALTO-Daten mit Provenienz;
- ein relationales Schema für Regeln, Quellen, Herleitungen, Zeichnungen,
  Regionen, Messungen und Verhältnis-Hypothesen;
- 20 redaktionell überprüfte A-Regeln;
- vier ausdrücklich als Rekonstruktionen markierte B-Regeln;
- drei explorativ untersuchte C1-Zeichnungen;
- zwölf Messungen und 24 Verhältnis-Hypothesen;
- ein automatischer Vollkorpuslauf über 338 OCR-Bildseiten;
- 704 automatische, **noch nicht wissenschaftlich bestätigte** Textkandidaten;
- 177 mögliche Zeichnungsseiten;
- 213 quantitative Maß- oder Verhältnis-Kandidaten;
- Themen-, Entwurfsphasen- und Prüfindizes;
- eine lokale Modellvorsortierung aller 704 Kandidaten:
  - 226 `probable_rule`
  - 194 `measurement_statement`
  - 270 `descriptive`
  - 14 `ocr_noise`
  - Status sämtlicher Ergebnisse: `local_model_triage_unverified`

Ein abgebrochener zweiter lokaler Kontrolllauf enthält nur 60 Datensätze in
`output/local_llm_review_pass2.jsonl`. Er ist unvollständig und darf weder als
Gesamtauswertung noch als Konsensprüfung verwendet werden.

Wichtig: Die 704 Kandidaten sind keine 704 bestätigten Palladio-Regeln. Der
bestätigte Bestand bleibt zunächst bei 20 A- und vier B-Regeln. Es gibt noch
keine behauptete C1-Regel.

Die großen Quell-PDFs und reproduzierbaren PNG-Ableitungen werden wegen ihrer
Größe nicht im Git-Repository gespeichert. `data/source/SOURCE_MANIFEST.md`
enthält DOI, Lizenzkennzeichnung und Prüfsummen. Die ALTO-OCR-Datei, die
kanonische SQLite-Datenbank sowie JSON- und CSV-Arbeitsstände sind dagegen im
Repository enthalten.

## 3. Zuerst lesen und prüfen

Lies mindestens:

- `README.md`
- `docs/01_quelle_und_werkstruktur.md`
- `docs/02_datenmodell_und_evidenzlogik.md`
- `docs/03_pilotregeln_A_B.md`
- `docs/04_c1_methodik_ergebnisse_grenzen.md`
- `docs/05_vollpipeline_kosten_roadmap.md`
- `docs/06_vollkorpus_erster_durchlauf.md`
- `schema.sql`
- `data/decision_tree.json`
- `src/palladio_code/`
- `tests/`
- `output/pilot_summary.json`
- `output/full_corpus_summary.json`
- `output/local_llm_review_summary.json`

Führe danach nur die leichten, vorhandenen Reproduktionstests aus. Starte keine
mehrstündigen lokalen Modellläufe, kein Ollama und keine rechenintensive
Vollanalyse ohne ausdrückliche Freigabe. Der Arbeitsrechner ist kein Server.

## 4. Unverhandelbare wissenschaftliche Regeln

Die Evidenzklassen müssen technisch und visuell getrennt bleiben:

- **A:** explizite, am Scan überprüfte Aussage Palladios mit genauer Fundstelle;
- **B:** nachvollziehbare Rekonstruktion mit Begründung, Herleitung und
  Konfidenz;
- **C1:** aus publizierten Zeichnungen abgeleitete Mess- oder Regelhypothese;
- **C2:** spätere gebaute Praxis; im Pilot noch nicht befüllt;
- **automatischer Kandidat:** maschineller Hinweis, niemals automatisch A oder B.

Weitere Grundsätze:

- OCR darf nicht ungeprüft als Zitat ausgegeben werden.
- Rohmessung, Sollverhältnis und Interpretation bleiben getrennte Datensätze.
- Eine geringe numerische Abweichung beweist keine historische Absicht.
- Jede Regelansicht muss Quelle, Status und Herleitung erkennen lassen.
- Bestehende Daten und Nutzeränderungen nicht überschreiben.
- Große Binärdateien und Quellenlizenzen vor einem Push prüfen; gegebenenfalls
  Git LFS und eine saubere Veröffentlichungsstrategie vorschlagen.

## 5. Gewünschte Ausbaustufen

### Ausbaustufe 0 – Repository- und Architekturprüfung

1. Prüfe Git-Status, Remote, Branches, Dateigrößen, Lizenzen und Reproduzierbarkeit.
2. Untersuche auch `palladian-facades` und dokumentiere, welche Teile als
   Oberfläche, SVG-Export oder historische Codebasis wiederverwendbar sind.
3. Erstelle einen kompakten Befund mit Risiken, technischen Schulden und
   empfohlener Zielarchitektur.
4. Lege einen priorisierten Umsetzungsplan mit klaren Abnahmekriterien vor.

### Ausbaustufe 1 – Solider Anwendungskern

Baue auf dem vorhandenen Python- und SQLite-Kern auf. Bevorzugte Richtung:

- Python/FastAPI als nachvollziehbare API-Schicht;
- SQLite zunächst beibehalten und sauber migrierbar machen;
- Pydantic-Modelle und versionierte API;
- TypeScript/React als moderne Benutzeroberfläche;
- automatisierte Tests für Datenmodell, API und zentrale UI-Flows;
- keine unnötige Microservice-Architektur.

Wenn du eine andere Architektur empfiehlst, begründe sie anhand des vorhandenen
Codes und der Forschungsanforderungen.

### Ausbaustufe 2 – Forschungsdashboard

Entwickle eine ruhige, hochwertige und wissenschaftlich lesbare Oberfläche mit:

- Werk-, Buch-, Kapitel- und Seitennavigation;
- Suche und Filterung nach Kategorie, Entwurfsphase, Evidenzklasse und Status;
- Regelkarten mit Originaltext, Übersetzung, Fundstelle, Herleitung und
  Unsicherheit;
- Scan- und OCR-Vergleich;
- Prüfwarteschlange für die 704 Kandidaten;
- Aktionen `bestätigen`, `zurückstellen`, `als Beschreibung markieren`,
  `OCR korrigieren` und `Kommentar hinzufügen`;
- lückenlosem Änderungsprotokoll und Export.

Die Gestaltung darf von venezianischem Papier, Kupferstich, Proportion und
Palladios typografischer Ruhe inspiriert sein, soll aber keine historisierende
Kulisse werden. Ziel ist eine elegante zeitgenössische Forschungsanwendung.

### Ausbaustufe 3 – Zeichnungs- und Verhältnisviewer

Baue einen Viewer für Tafeln und Regionen:

- Zoom, Pan und Overlays;
- Anzeige erkannter Linien, Achsen, Regionen und Messbezüge;
- Umschaltung zwischen Rohbild, Binärbild, Messoverlay und Interpretation;
- nachvollziehbare Maßdefinitionen wie Innenkante, Außenkante oder Achse;
- Vergleich gemessener Quotienten mit bekannten Verhältnis-Hypothesen;
- klare Warnung, dass Ähnlichkeit keine Absicht beweist.

### Ausbaustufe 4 – Palladio-Labor

Entwickle einen ersten kleinen, aber vollständigen vertikalen Prototyp für ein
interaktives Entwurfslabor. Beginne mit einem eng begrenzten Gegenstand, etwa
Raumproportion, Öffnung oder private Hausfassade:

- Nutzer gibt Maße, Bautyp und Randbedingungen ein.
- Das System zeigt anwendbare bestätigte A-Regeln und getrennte B-Hypothesen.
- Varianten werden geometrisch visualisiert.
- Jede Entscheidung verweist zurück auf ihre Evidenz.
- Abweichungen sind erlaubt und werden ausdrücklich sichtbar gemacht.
- Ausgabe als SVG/PNG sowie als maschinenlesbare Parameterdatei.

Nutze das ältere Projekt `palladian-facades` nur als mögliche Ideenquelle, nicht
als wissenschaftlich gleichwertige Datenbasis. Übernimm keinen Code ungeprüft.

### Ausbaustufe 5 – Qualität und Veröffentlichung

- Barrierefreiheit und responsive Darstellung;
- reproduzierbare Demo-Daten;
- klare Installations- und Entwicklungsanleitung;
- CI für Tests, Formatierung und Migrationen;
- Datenschutz- und Lizenzprüfung;
- keine Primärquellen oder große Binärdateien versehentlich in Releases;
- dokumentierter Export und Backup der redaktionellen Entscheidungen.

## 6. Arbeitsweise

Arbeite nicht alles auf einmal um. Gehe so vor:

1. Bestandsaufnahme und Plan;
2. kleinster funktionierender vertikaler Schnitt;
3. Tests und visuelle Prüfung;
4. Dokumentation;
5. sauberer Commit beziehungsweise Pull Request;
6. nächster Schnitt.

Vor jeder größeren Architekturentscheidung erkläre kurz Nutzen, Kosten und
Alternativen. Bewahre bestehende wissenschaftliche Semantik. Keine automatische
Hochstufung maschineller Ergebnisse zu A, B oder C1. Keine schweren lokalen
Rechenläufe ohne Zustimmung.

## 7. Erster konkreter Auftrag

Erledige zunächst nur Folgendes:

1. Analysiere Repository, Datenmodell, Pipeline und Dokumentation.
2. Führe die vorhandenen leichten Tests aus.
3. Formuliere eine Zielarchitektur und einen Umsetzungsplan für die fünf
   Ausbaustufen.
4. Implementiere anschließend den kleinsten überzeugenden vertikalen Schnitt:
   eine lokal startbare Webanwendung, die bestätigte Regeln und automatische
   Kandidaten aus SQLite liest, beide sichtbar trennt und eine Detailansicht mit
   Quelle, Status und Evidenzklasse bietet.
5. Ergänze Tests und eine kurze Startanleitung.
6. Zeige am Ende exakt, was geändert wurde, was getestet wurde, welche Annahmen
   offen sind und welche Ausbaustufe als Nächstes den größten Nutzen bringt.

Arbeite sorgfältig, quellennah und gestalterisch ambitioniert. Das Ziel ist
nicht bloß eine hübsche Oberfläche, sondern eine Software, in der Schönheit,
Nachvollziehbarkeit und wissenschaftliche Redlichkeit dieselbe Architektur
bilden.
