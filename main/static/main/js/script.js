

$(document).ready(function() {
	starRecipes();
	addIngredients();
});


function starRecipes() {
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
		});
	});
}

function addIngredients() {
	var ingredients = [];
	$('#addIngredientsButton').on('click', function() {
		console.log("clicked add ingredients");
		var currIngredient = $('#currentIngredient').val().trim();
		console.log(currIngredient);
		if (currIngredient == '') 
			return;

		// Add ingredient to list, display list
		ingredients.push(currIngredient);
		var ingredientList = '';
		for (var i = 0; i < ingredients.length; i++) {
			ingredientList += ingredients[i] + ', ';
		}
		ingredientList = ingredientList.substring(0, ingredientList.length-2);
		$('#ingredientList').text(ingredientList);

		// Clear text box 
		$('#currentIngredient').val('').focus();

	});

	$('#currentIngredient').keypress(function(event) {
		console.log("in keypress " + event.keyCode);
		if (event.keyCode == 13) {
			event.preventDefault();
			$('#addIngredientsButton').click();
		}
	});
}
















