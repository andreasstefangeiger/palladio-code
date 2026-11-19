<?php
/**
 * Title: Eingang mit Mitte
 * Slug: palladio/mitte
 * Categories: palladio, featured
 * Description: Eine Hauptachse in der Mitte, auf die alles antwortet (W-ACHSE: I.XXI.2, I.XXV.8).
 * Keywords: mitte, eingang, hero, titel
 */
?>
<!-- wp:group {"align":"wide","style":{"spacing":{"padding":{"top":"var:preset|spacing|80","bottom":"var:preset|spacing|80"},"blockGap":"var:preset|spacing|40"}},"layout":{"type":"constrained"}} -->
<div class="wp-block-group alignwide" style="padding-top:var(--wp--preset--spacing--80);padding-bottom:var(--wp--preset--spacing--80)"><!-- wp:heading {"textAlign":"center","level":6} -->
<h6 class="wp-block-heading has-text-align-center"><?php echo esc_html_x( 'Willkommen', 'Pattern placeholder', 'palladio' ); ?></h6>
<!-- /wp:heading -->

<!-- wp:heading {"textAlign":"center","level":1,"fontSize":"huge"} -->
<h1 class="wp-block-heading has-text-align-center has-huge-font-size"><?php echo esc_html_x( 'Klar, wahr, schön', 'Pattern placeholder', 'palladio' ); ?></h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"align":"center","fontSize":"large"} -->
<p class="has-text-align-center has-large-font-size"><?php echo esc_html_x( 'Ein Satz, der sagt, worum es auf dieser Seite geht.', 'Pattern placeholder', 'palladio' ); ?></p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button -->
<div class="wp-block-button"><a class="wp-block-button__link wp-element-button"><?php echo esc_html_x( 'Weiterlesen', 'Pattern placeholder', 'palladio' ); ?></a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:group -->
