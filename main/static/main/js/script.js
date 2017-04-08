

$(document).ready(function() {
	starRecipes();
	createRecipePage();
});

function createRecipePage() {
	addIngredients();
}


// For recipe list page
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
			url: '/save_recipe/',
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

// For create recipe page
function addIngredients() {
	var ingredientSet = new Set();
	var ingredients = [];

	// Add typed ingredient to list of ingredients
	$('#addIngredientsButton').on('click', function() {
		// If empty ingredient, don't do anything
		var currIngredient = $('#currentIngredient').val().trim();
		if (currIngredient == '') 
			return;

		// Add ingredient to ingredient set if ingredient is not already there
		if (! ingredientSet.has(currIngredient))
			ingredientSet.add(currIngredient);

		// Update html displaying ingredients
		var listHtml = '<ul class="fa-ul">';
		for (let ingredient of ingredientSet) {
			listHtml += '<li class="ingredient">'
				+ '<i class="fa fa-li fa-minus-circle"></i>'
				+ '<span>' + ingredient + '</span>'
				+ '</li>';
		}
		listHtml += '</ul>';

		$('#ingredientList').html(listHtml);


		// Clear text box and focus on it
		$('#currentIngredient').val('').focus();


		// Remove ingredient on click
		$('#ingredientList').on('click', 'li.ingredient', function() {
			var ingredient = $(this).find('span').text();
			ingredientSet.delete(ingredient);
			$(this).slideUp('fast');

			$('#currentIngredient').focus(); // Refocus on input box
		});

		// Color li on hover
		$('#ingredientList').on('mouseenter', 'li.ingredient', function() {
			$(this).find('i.fa-li').css('color', 'red');
		});
		$('#ingredientList').on('mouseleave', 'li.ingredient', function() {
			$(this).find('i.fa-li').css('color', 'black');
		});
	});



	// Allow enter to click add button
	$('#currentIngredient').keypress(function(event) {
		if (event.keyCode == 13) {
			event.preventDefault();
			$('#addIngredientsButton').click();
		}
	});
}
















