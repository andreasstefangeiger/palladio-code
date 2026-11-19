<?php
/**
 * Title: Zwei Räume: Bild und Text
 * Slug: palladio/zwei-raeume
 * Categories: palladio, text
 * Description: Zwei gleiche Spalten; das Bild im Format 4:3, einer der sieben Raumformen (W-FORMEN: I.XXI.5).
 * Keywords: bild, text, spalten
 */
?>
<!-- wp:columns {"align":"wide","style":{"spacing":{"blockGap":{"left":"var:preset|spacing|50"},"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|60"}}}} -->
<div class="wp-block-columns alignwide" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--60)"><!-- wp:column {"verticalAlignment":"center"} -->
<div class="wp-block-column is-vertically-aligned-center"><!-- wp:image {"aspectRatio":"4/3","scale":"cover","sizeSlug":"full"} -->
<figure class="wp-block-image size-full"><img src="<?php echo esc_url( get_template_directory_uri() . '/assets/images/rotonda-alzato-4-3.jpg' ); ?>" alt="<?php echo esc_attr_x( 'Villa Almerico, „La Rotonda“: Aufriss aus Palladios Quattro Libri, Buch II, 1570', 'Image alt text', 'palladio' ); ?>" style="aspect-ratio:4/3;object-fit:cover"/><figcaption class="wp-element-caption"><?php echo esc_html_x( 'Palladio, I quattro libri, 1570, Buch II, S. 19', 'Image caption', 'palladio' ); ?></figcaption></figure>
<!-- /wp:image --></div>
<!-- /wp:column -->

<!-- wp:column {"verticalAlignment":"center"} -->
<div class="wp-block-column is-vertically-aligned-center"><!-- wp:heading -->
<h2 class="wp-block-heading"><?php echo esc_html_x( 'Ein Raum für das Bild, einer für das Wort', 'Pattern placeholder', 'palladio' ); ?></h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><?php echo esc_html_x( 'Beide Spalten sind gleich breit. Rechts entspricht links, wie in Palladios Grundrissen.', 'Pattern placeholder', 'palladio' ); ?></p>
<!-- /wp:paragraph --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->
