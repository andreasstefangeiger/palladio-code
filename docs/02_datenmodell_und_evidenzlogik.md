# 2. Datenmodell und Evidenzlogik

## Grundentscheidung

Das Modell ist relational normalisiert. Eine einzige breite Tabelle wäre bequem
für CSV, würde aber mehrere Quellen pro Regel, mehrere Messvarianten pro Region und
mehrere Verhältnis-Hypothesen pro Rohmessung schlecht abbilden. SQLite ist daher
die kanonische Form; CSV wird als Export erzeugt.

## Entitäten

| Entität | Aufgabe |
|---|---|
| `rules` | Aussage, Evidenzklasse, Phase, Kategorie, Bedingung, Zweck, Konfidenz |
| `rule_sources` | beliebig viele genaue Belegstellen mit Original und Übersetzung |
| `rule_derivations` | nachvollziehbare Herleitung einer B-Regel aus anderen Regeln |
| `drawings` | publizierte C1-Seite mit Buch-, Kapitel-, Seiten- und Bildbezug |
| `drawing_regions` | semantische Teilregion mit Geometrie und Prüfflag |
| `measurements` | unveränderter Rohwert plus Messmethode und Bezugslinie |
| `ratio_hypotheses` | getrenntes Ranking möglicher Sollverhältnisse |
| `c1_rule_candidates` | erst für ausreichend große, definierte Populationen |
| `c1_candidate_support` | messungsgenaue Evidenz eines Kandidaten |

Die SQL-Definition steht in `schema.sql`. Die View `rules_flat` erleichtert den
Export, ohne die normalisierte Quelle aufzugeben.

## Harte Evidenzregeln

- A-Regeln besitzen genaue Quelle und keine numerische Konfidenz: Sie sind als
  explizite Aussagen klassifiziert, nicht probabilistisch „mehr oder weniger A“.
- B-Regeln besitzen Begründung, Konfidenz und `derived_from`-Relationen.
- Eine C1-Messung wird nicht allein wegen geringer Abweichung zur C1-Regel.
- Eine Verhältnis-Hypothese speichert immer den gemessenen Quotienten, Sollwert,
  Abweichung und Ursprung des Sollwerts.
- `within_pilot_tolerance` bedeutet nur „innerhalb des vorläufigen Fensters von
  4 %“, nicht „von Palladio beabsichtigt“.
- C2 bleibt im Schema vorhanden, wird im Pilot aber nicht befüllt.

## Messbezüge

Das Feld `reference_line` ist obligatorischer methodischer Kontext. Spätere
Regionen sollen unter anderem getrennt führen:

- lichte Innenkante;
- Wandinnenkante;
- Wandachse;
- Wandaußenkante;
- Säulenachse;
- Gesamtbegrenzung.

Die Pilotautomatik verwendet noch keine dieser architektonisch semantischen
Bezugslinien. Ihre automatischen `ink_component_extent`- und
`dominant_line_median`-Werte sind ausdrücklich explorative Bildmessungen und
fordern menschliche Prüfung.

## Lebenszyklus einer Aussage

```text
Quelle -> Transkription -> A-Regel
       -> wiederholte/verkettete Evidenz -> B-Hypothese -> geprüfte B-Regel

Zeichnung -> Region -> Rohmessung -> Verhältnis-Hypothese
          -> definierte Vergleichspopulation -> C1-Regelkandidat
          -> Statistik + Alternativerklärungen + Review -> C1-Regel
```

Quelle, Messung, Interpretation, Hypothese und Regel bleiben somit technisch
unterschiedliche Datensätze.

