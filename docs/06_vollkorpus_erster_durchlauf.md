# Vollkorpus: erster automatischer Durchlauf

## Ergebnisstatus

Der erste automatische Durchlauf über den vollständigen historischen Buchkörper
ist durchgeführt. Verarbeitet wurden 338 OCR-Bildseiten. Davon sind 329 den vier
Büchern zugeordnet: Buch I 64, Buch II 80, Buch III 48 und Buch IV 137 Seiten;
neun weitere Seiten gehören zum Vorsatz beziehungsweise Paratext. Die technisch
zusätzliche 339. PDF-Seite ist eine vorgeschaltete Container- beziehungsweise
Einbandseite und gehört nicht zum erschlossenen historischen Bildseitenkorpus.

Der Lauf erzeugte 704 automatische Textkandidaten für mögliche Regeln oder
maßbezogene Aussagen (Buch I: 264; II: 137; III: 140; IV: 163) und markierte 177
Seiten als mögliche zeichnungsdominante oder gemischte Seiten (I: 30; II: 36;
III: 16; IV: 95).

Damit ist die Erfassung durchgeführt, die wissenschaftliche Prüfung aber noch
nicht abgeschlossen. `automatic_unverified_candidate` ist eine eigene
Evidenzstufe und darf weder mit Quellenklasse A noch mit einer rekonstruierten
B-Regel gleichgesetzt werden. Die bereits einzeln geprüften 20 A- und vier
B-Regeln bleiben der bestätigte Bestand.

## Was die Pipeline liefert

- eine vollständige Seitentabelle mit Buchzuordnung, OCR-Umfang und Bildmaßen;
- eine priorisierte Prüfwarteschlange aller Textkandidaten;
- Themen- und Entwurfsphasenindizes;
- eine Teilmenge quantitativer Verhältnis- und Maßkandidaten;
- eine buchweise Rangliste möglicher Zeichnungsseiten;
- SQLite-, JSON- und CSV-Ausgaben mit reproduzierbaren Identifikatoren.

Die Textsuche ist bewusst auf hohe Wiederauffindbarkeit ausgerichtet. Sie erkennt
normative, konditionale, finale und quantitative sprachliche Marker. Daher sind
auch beschreibende Maßangaben und einzelne OCR-Fehler enthalten. Jede Beförderung
zur A-Regel verlangt den Abgleich mit dem Seitenbild, die korrekte Segmentierung
des Satzes, eine Quellenangabe und die dokumentierte redaktionelle Entscheidung.

## Stichprobenprüfung

Eine manuelle Sichtung von 32 hoch bewerteten Textfundstellen ergab 29 plausible
Prüfkandidaten. Das entspricht 90,6 Prozent in dieser gezielt ausgewählten
Spitzengruppe, ist aber ausdrücklich keine Schätzung der Genauigkeit für alle 704
Fundstellen. Unter den vier jeweils höchst gerankten Bildseiten waren drei
eindeutige Architekturzeichnungen; die Titel- und Schmuckseite von Buch III
wurde ebenfalls erkannt. Das zeigt sowohl die Brauchbarkeit der Vorauswahl als
auch die Notwendigkeit einer semantischen Nachprüfung.

## Nächster wissenschaftlicher Arbeitsschritt

Nun folgt keine neue technische Erschließung, sondern die redaktionelle
Validierung: Kandidat für Kandidat wird als A, B oder Nicht-Regel entschieden;
Zeichnungsseiten werden nach Grundriss, Ansicht, Schnitt, Detail und Paratext
klassifiziert. Erst danach können Häufigkeiten, wiederkehrende Verhältnisse und
Entscheidungslogiken werkweit behauptet werden.

## Fußnote zur späteren Verwertung

> **Verwertungsperspektive (nach Abschluss der Quellenarbeit):** Aus dem
> Palladio-Code können zwei eigenständige Anwendungen hervorgehen. **A –
> Software:** eine Weiterentwicklung der Palladio-Fassaden zu einem interaktiven,
> quellengebundenen Entwurfs- und Analyseinstrument, das Regeln nicht nur
> anwendet, sondern ihre Herkunft, Evidenz und Abweichung sichtbar macht. **B –
> Roman:** Auf einer Reise durch Venedig und Venetien begegnet ein kosmologisch
> denkender Philosoph – begleitet von Platon, dem *Timaios* und Talebs moderner
> Lehre vom Unvorhersehbaren – einer schönen Architektin auf den Spuren
> Palladios. Zwischen Kosmos und Fassade, Maß und Zufall entsteht eine Anziehung,
> in der geistige und körperliche Nähe Formen derselben wechselseitigen
> Befruchtung werden. Der Roman wäre nicht bloß Illustration der Forschung,
> sondern ihr sinnliches Gegenbild: Erkenntnis erhält Körper, Architektur wird
> zur Begegnung, und das Maß bewährt sich erst dort, wo das Leben es überschreitet.
