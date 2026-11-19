<?php
/**
 * Title: Vier Felder
 * Slug: palladio/vier-felder
 * Categories: palladio, text
 * Description: Eine gerade Zahl von Feldern, damit in der Mitte ein Zwischenraum liegt (W-ACHSE: I.XIII.9).
 * Keywords: felder, spalten, übersicht
 */
?>
<!-- wp:columns {"align":"wide","style":{"spacing":{"blockGap":{"left":"var:preset|spacing|40"},"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|60"}}}} -->
<div class="wp-block-columns alignwide" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--60)"><?php for ( $palladio_i = 1; $palladio_i <= 4; $palladio_i++ ) : ?><!-- wp:column -->
<div class="wp-block-column"><!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading"><?php echo esc_html( sprintf( /* translators: %d: field number */ _x( 'Feld %d', 'Pattern placeholder', 'palladio' ), $palladio_i ) ); ?></h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><?php echo esc_html_x( 'Zwei, drei Sätze. Alle Felder einer Reihe haben dasselbe Maß.', 'Pattern placeholder', 'palladio' ); ?></p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --><?php endfor; ?></div>
<!-- /wp:columns -->
