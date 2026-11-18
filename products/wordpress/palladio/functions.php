<?php
/**
 * Palladio theme functions.
 *
 * The design values live in theme.json, generated from data/interpretation/web.json
 * (python -m palladio_code.webdesign). This file only loads the stylesheet and the patterns' category.
 *
 * @package Palladio
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Theme setup: translations and editor styles.
 */
function palladio_setup() {
	load_theme_textdomain( 'palladio', get_template_directory() . '/languages' );
	add_theme_support( 'editor-styles' );
	add_editor_style( 'style.css' );
}
add_action( 'after_setup_theme', 'palladio_setup' );

/**
 * Front-end stylesheet (only the rules theme.json cannot express).
 */
function palladio_enqueue_styles() {
	wp_enqueue_style(
		'palladio-style',
		get_stylesheet_uri(),
		array(),
		wp_get_theme()->get( 'Version' )
	);
}
add_action( 'wp_enqueue_scripts', 'palladio_enqueue_styles' );

/**
 * Pattern category for the patterns in /patterns.
 */
function palladio_pattern_categories() {
	register_block_pattern_category(
		'palladio',
		array(
			'label'       => __( 'Palladio', 'palladio' ),
			'description' => __( 'Muster nach den Regeln der Quattro Libri.', 'palladio' ),
		)
	);
}
add_action( 'init', 'palladio_pattern_categories' );
