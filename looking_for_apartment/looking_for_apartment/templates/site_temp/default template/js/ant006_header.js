/*! version : 1.0.0 */

jQuery( document ).ready(function($) {

	// menu toggle
	$('.ant006_header-toggle').on('click', function() {
		$('.ant006_header-container').slideToggle(500);
	});

	$('nav.ant006_header-container > ul > li.menu-item-has-children').on('click', function() {
		$(this).find('.sub-menu').slideToggle(0);
	});

});