

$(document).ready(function() {


	var starredIcon = 'fa-star-o';
	var unstarredIcon = 'fa-star';
	$('ul.favorites-list li i.fa').on('click', function(event) {
		var recipeId = this.getAttribute('data-recipe-id');
		console.log("Clicked star for recipe #" + recipeId);
		$(this).toggleClass(starredIcon).toggleClass(unstarredIcon);
		
		console.log("csrf_token: " + window.CSRF_TOKEN);

		$.ajax({
			url: '/favorite_recipe/',
			datatype: 'json',
			type: 'POST',
			data: {
				recipe_id: recipeId,
				csrfmiddlewaretoken: window.CSRF_TOKEN,
			},

			success: function(response) {
				console.log("Success");
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