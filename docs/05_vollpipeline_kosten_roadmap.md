# 5. Vollpipeline, Kosten und Roadmap

## Architektur für alle vier Bücher

```text
e-rara PDF + IIIF + OCR/ALTO
          |
          v
Quellenmanifest und Seitenkonkordanz
          |
          +--> Text: Kapitel -> Passage -> A-Kandidat -> Review -> A-Regel
          |                         |
          |                         +--> Quervergleich -> B-Kandidat -> Review
          |
          +--> Bild: Seitentyp -> Regionen -> Geometrie/OCR -> Messvarianten
                                    |
                                    +--> Verhältnis-Hypothesen
                                    +--> Population/Statistik -> C1-Kandidat
          |
          v
SQLite (kanonisch) -> CSV/JSON -> Entscheidungsbaum/Generator
```

## Skalierungsschritte

1. Alle Seiten über IIIF-ID, physische Bildnummer, PDF-Seite und Druckseite
   konkordieren.
2. Kapitelkandidaten aus ALTO redaktionell normalisieren.
3. A-Kandidaten über sprachliche Marker (`si deve`, `deono`, `non si farà`,
   Maße und Verhältniswörter) regelbasiert markieren.
4. Jede Kandidatenpassage am Scan prüfen; OCR nie ungeprüft zitieren.
5. Abbildungsseiten deterministisch über Tintendichte, Linienlänge und OCR-Anteil
   vorsortieren.
6. Regionen zunächst durch Layoutanalyse, danach durch kleine manuelle Korrekturen
   segmentieren; Korrekturen als Annotationen speichern.
7. Architekturprimitive getrennt modellieren: Wand, Öffnung, Säule, Achse, Raum,
   Maßlinie, Text, Treppe, Gewölbe.
8. Für jede relevante Distanz alle plausiblen Messbezüge speichern.
9. C1-Populationen nach Bautyp, Zeichnungstyp und Bauteil definieren.
10. Erst nach Statistik und Review Regeln mit A/B verknüpfen.

## Kostenprinzip und Pilotschätzung

| Posten | Pilot | Voller Basislauf (339 PDF-Seiten) |
|---|---:|---:|
| Primärquelle, OCR, ALTO, IIIF | 0 EUR | 0 EUR |
| Open-Source-Software | 0 EUR | 0 EUR |
| externe KI-Aufrufe | 0 EUR | 0 EUR im deterministischen Basislauf |
| lokaler Speicher | ca. 130 MB Quelle plus Ableitungen | ca. 1-3 GB mit Renderings und Overlays |
| lokale Rechenzeit | Minuten | voraussichtlich unter wenigen Stunden auf einem aktuellen Rechner |
| menschliche Fachprüfung | nicht monetarisiert | größter Kosten- und Qualitätsfaktor |

Damit sind die laufenden **Servicekosten des Basislaufs 0 EUR**. Strom,
Geräteabschreibung und wissenschaftliche Arbeitszeit sind nicht null, werden aber
nicht künstlich als API-Kosten ausgegeben.

## Wann ein Modell gerechtfertigt wäre

Ein günstiges Vision-Modell ist erst sinnvoll, wenn deterministische Merkmale und
OCR eine Region nicht zuverlässig als Grundriss, Schnitt, Ansicht oder Detail
klassifizieren. Ein leistungsstarkes Modell ist nur für strittige Einzelfälle
vorgesehen. Vor jedem Batch gelten vier Prüfungen:

1. Kann eine nachvollziehbare Regel oder Geometrie dasselbe leisten?
2. Kann nur die schwierige Region statt der ganzen Seite gesendet werden?
3. Kann das Resultat gecacht und von Menschen stichprobenartig geprüft werden?
4. Bleibt die Modellaussage als Klassifikation/Interpretation markiert?

Weil der Pilot keine externen Modelle benötigt, wäre eine konkrete API-Schätzung
ohne festgelegten Anbieter, Modell, Bildauflösung und Zahl strittiger Regionen nur
Scheingenauigkeit. Die Pipeline protokolliert diese vier Größen, sobald ein solcher
Schritt tatsächlich aufgenommen wird.

## Entscheidungsbaum

`data/decision_tree.json` enthält einen ersten, maschinenlesbaren Pfad für private
Häuser. Er verweist ausschließlich auf Pilotregeln und beansprucht noch keine
Vollständigkeit des Gesamtwerks.

## Vorbereitung C2

Für die spätere gebaute Praxis sind zusätzlich nötig:

- Werk- und Bauteilidentität;
- Entwurfs-, Bau- und Umbauphase;
- Zuschreibung und Zuschreibungssicherheit;
- Quelle des Aufmaßes, Datum, Genauigkeit und Lizenz;
- heutiger versus palladianischer Zustand;
- Ausschluss späterer Bauteile aus der Regelstatistik.

Das aktuelle Schema lässt C2 als Evidenzklasse zu, füllt sie aber bewusst nicht.

