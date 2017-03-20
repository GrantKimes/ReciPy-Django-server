

$(document).ready(function() {


	var starredIcon = 'fa-star';
	var unstarredIcon = 'fa-star-o';
	$('ul.favorites-list li i.fa').on('click', function(event) {

		var recipeId = this.getAttribute('data-recipe-id');

		// Update favorite count 
		var countSpan = $(this).siblings().find('span.favorite_count');
		if ($(this).hasClass(unstarredIcon)) {
			var count = Number(countSpan.text());
			countSpan.text(count + 1);
		}
		else {
			var count = Number(countSpan.text());
			countSpan.text(count - 1);
		}

		// Toggle filled and unfilled star icon
		$(this).toggleClass(starredIcon).toggleClass(unstarredIcon);
		
		//console.log("csrf_token: " + window.CSRF_TOKEN);

		$.ajax({
			url: '/favorite_recipe/',
			datatype: 'json',
			type: 'POST',
			data: {
				recipe_id: recipeId,
				csrfmiddlewaretoken: window.CSRF_TOKEN,
			},

			success: function(response) {
				console.log(response);
			},

			error: function(xhr, textStatus, error) {
				console.log(xhr.status + ': ' + textStatus + ' - ' + xhr.responseText);
			},

			// complete: function(xhr, textStatus) {

			// },
		});
	});
});