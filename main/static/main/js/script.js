

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

	// Add typed ingredient to list of ingredients
	$('#addIngredientsButton').on('click', function() {
		var currIngredient = $('#currentIngredient').val().trim();
		console.log(currIngredient);
		if (currIngredient == '') 
			return;

		// Add ingredient to list, display list
		ingredients.push(currIngredient);
		var ingredientListText = '<ul class="fa-ul">';
		for (var i = 0; i < ingredients.length; i++) {
			ingredientListText += '<li id="' + ingredients[i] + '" class="ingredient">'
				+ '<i class="fa fa-li fa-minus-circle" onclick="removeIngredient("' + ingredients[i] + '");" ></i>' 
				+ ingredients[i] 
				+ '</li>';
		}
		ingredientListText += '</ul>';
		//ingredientListText = ingredientListText.substring(0, ingredientListText.length-2);
		$('#ingredientList').html(ingredientListText);

		// Clear text box 
		$('#currentIngredient').val('').focus();

	});

	function removeIngredient(ingredientName) {
		console.log(ingredientName);
		var ingredient_li = $('#' + ingredientName); 
		var index = ingredients.indexOf(ingredientName);
		ingredients.splice(index, 1);
		ingredient_li.fadeOut('slow');
		console.log("finshed removing");
	}

	// Remove ingredient when the minus sign is clicked
	/*$('li.ingredient i.fa').on('click', function() {
		var ingredient_li = $(this).parent('li');
		var index = ingredients.indexOf(ingredient_li.text())
	});*/

	// Allow enter to click add button
	$('#currentIngredient').keypress(function(event) {
		if (event.keyCode == 13) {
			event.preventDefault();
			$('#addIngredientsButton').click();
		}
	});
}
















