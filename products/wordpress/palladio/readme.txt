=== Palladio ===
Contributors: palladio-code
Requires at least: 6.6
Tested up to: 6.8
Requires PHP: 7.4
Stable tag: 0.1.0
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Ein Blocktheme nach Regeln aus Andrea Palladios „I quattro libri dell'architettura“ (Venedig 1570).

== Description ==

Palladio übersetzt einige Regeln der Quattro Libri in Gestaltungsregeln für Webseiten. Jede Übertragung
ist eine Deutung und auf Fundstellen im Regelkatalog des Projekts zurückgeführt
(data/interpretation/web.json; docs/18_gestaltungsrichtlinie.md im Repository palladio-code).

* Ein relatives Grundmaß: der Modul (Zeilenhöhe) und seine Minuten (1/60). I.XIII.11
* Schriftgrade aus den drei Mitteln von 1 und 2: 4/3, √2, 3/2. I.XXIII.3–6
* Bildformate aus den sieben Raumformen: 1:1, √2, 4:3, 3:2, 5:3, 2:1. I.XXI.5
* Eine Mitte je Seite, durchgehende Achsen. I.XXI.2, I.XXV.8
* Kein Ornament ohne Aufgabe: keine Schatten, Verläufe oder Zierrahmen. I.XX
* Farben aus dem Scan des Drucks von 1570, zu einem warmen Weiß aufgehellt. IV.II.12

theme.json wird erzeugt: `python -m palladio_code.webdesign`. Bitte nicht von Hand ändern.

== Changelog ==

= 0.1.0 =
* Erste Fassung.

== Copyright ==

Palladio WordPress Theme, (C) 2026 Palladio-Code.
Palladio is distributed under the terms of the GNU GPL v2 or later.

This theme bundles the following third-party resources:

EB Garamond (variable, Latin and Latin Extended subsets, woff2 from the Fontsource package
@fontsource-variable/eb-garamond 5.3.0)
Copyright 2017 The EB Garamond Project Authors (https://github.com/octaviopardo/EBGaramond12)
License: SIL Open Font License, Version 1.1 (assets/fonts/eb-garamond/OFL.txt)

Images assets/images/rotonda-alzato-4-3.jpg and assets/images/rotonda-pianta-1-1.jpg
Andrea Palladio, I quattro libri dell'architettura, Venetia 1570, Libro II, p. 19 (Villa Almerico, "La Rotonda").
Scan: ETH-Bibliothek Zürich, Rar 439, e-rara.ch, DOI 10.3931/e-rara-363. Public Domain Mark 1.0.
Colours: sampled from the same scan (Libro IV, pp. 5, 9, 55) and lightened.
