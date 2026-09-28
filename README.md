# Palladio-Code: wissenschaftlicher Pilot

Dieser Ordner enthält einen reproduzierbaren ersten Arbeitsdurchgang für einen
quellenkritischen, maschinenlesbaren Palladio-Code. Er ist bewusst vom älteren
Experiment `palladian-facades` getrennt: Dort wird Form generiert, hier werden
zunächst Quellen, Messungen, Interpretationen und Regelhypothesen sauber getrennt.

## Was der Pilot bereits leistet

- lokale Primärquelle: Andrea Palladio, *I quattro libri dell'architettura*,
  Venedig 1570, ETH-Bibliothek Zürich, Rar 439, Public Domain Mark;
- bibliografische und technische Provenienz samt Prüfsummen;
- relationales Datenmodell mit A-, B-, C1- und späterer C2-Fähigkeit;
- 20 überprüfte A-Regeln aus Buch I, Kap. XXI, XXIII und XXV;
- 4 ausdrücklich getrennte B-Rekonstruktionen mit Begründung und Konfidenz;
- 3 heterogene C1-Pilotzeichnungen (Grundriss, Ansicht, Ordnungsdetail);
- deterministische Bildvorverarbeitung, Linienerkennung, Symmetriemessung,
  Rohwertspeicherung und Verhältnis-Ranking;
- SQLite-, JSON- und CSV-Ausgaben;
- maschinelle Kapitelkandidaten aus dem bereitgestellten ALTO-OCR.
- automatischer Vollkorpuslauf über 338 OCR-Bildseiten (329 den vier Büchern
  zugeordnete Seiten und neun Vorsatz-/Paratextseiten): 704 unbestätigte
  Regelkandidaten, 177 mögliche Zeichnungsseiten sowie Themen-, Entwurfsphasen-,
  Verhältnis- und Prüfwarteschlangen.

Der Pilot behauptet noch **keine C1-Regel**. Drei Tafeln reichen nicht zur
statistischen Regelbildung; ihre Ergebnisse bleiben Messungen und
Proportionshypothesen.

Ebenso sind die 704 automatischen Textfundstellen **keine 704 Palladio-Regeln**.
Sie bilden eine nachprüfbare Kandidatenmenge. Erst der Abgleich mit dem Scan und
die redaktionelle Entscheidung können sie als A, B oder Nicht-Regel einstufen.

## Reproduzieren

Die mit Codex gebündelte Python-Laufzeit wurde verwendet. Im Projektordner:

```bash
make pilot
make test
```

Wenn Ollama und das lokale Modell `gemma4:12b` vorhanden sind, kann die
fortsetzbare, kostenfreie Modell-Vorsortierung ohne Cloud-Aufruf gestartet werden:

```bash
make local-review
```

Die Ergebnisse tragen ausdrücklich den Status `local_model_triage_unverified`
und ersetzen nicht den Quellenabgleich.

Für einen längeren lokalen Kontrolllauf werden zunächst verbliebene Lücken
einzeln geschlossen und anschließend alle Kandidaten mit einer unabhängigen,
strengeren Prüfanweisung ein zweites Mal beurteilt:

```bash
make overnight-review
```

Hauptausgaben:

- `output/palladio_code.sqlite`
- `output/csv/`
- `output/analysis/*_analysis.json`
- `output/analysis/*_overlay.png`
- `output/chapter_candidates.json`
- `output/full_corpus_summary.json`
- `output/automatic_review_queue.csv`
- `output/topic_index.json`
- `output/design_phase_index.json`
- `output/automatic_ratio_candidates.json`
- `output/pilot_summary.json`

## Wissenschaftlicher Einstieg

1. `docs/01_quelle_und_werkstruktur.md`
2. `docs/02_datenmodell_und_evidenzlogik.md`
3. `docs/03_pilotregeln_A_B.md`
4. `docs/04_c1_methodik_ergebnisse_grenzen.md`
5. `docs/05_vollpipeline_kosten_roadmap.md`
6. `docs/06_vollkorpus_erster_durchlauf.md`

## Lizenzhinweis

Der historische Scan ist gemeinfrei markiert. Der eigene Code und die eigenen
Metadaten sind für die weitere Forschung vorbereitet; vor einer öffentlichen
Veröffentlichung sollte im übergeordneten Repository noch eine explizite
Projektlizenz ergänzt werden.
