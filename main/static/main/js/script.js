

$(document).ready(function() {
	recipeListPage();
	createRecipePage();
});

function recipeListPage() {
	var defaultClass = 'btn-default';
	var saveClass = 'btn-info';
	var likeClass = 'btn-primary';
	var dislikeClass = 'btn-danger';

	$('div.likeDislikeSaveButtons button').on('click', function() {
		var url = '';

		if ($(this).hasClass('save')) {
			url = '/api/recipes/save/';
			updateSaveCount(this);
			$(this).toggleClass(saveClass).toggleClass(defaultClass);
		}
		else if ($(this).hasClass('like')) {
			url = '/api/recipes/like/';
			$(this).toggleClass(likeClass).toggleClass(defaultClass);
			$(this).next('button').removeClass(dislikeClass).addClass(defaultClass);
		}
		else if ($(this).hasClass('dislike')) {
			url = '/api/recipes/dislike/';
			$(this).toggleClass(dislikeClass).toggleClass(defaultClass);
			$(this).prev('button').removeClass(likeClass).addClass(defaultClass);
		}
		else {
			return;
		}

		var recipeId = this.getAttribute('data-recipe-id');

		$.ajax({
			url: url,
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

	function updateSaveCount(button) {
		var numSaves = Number(button.getAttribute('data-num-saves'));
		console.log("numSaves: " + numSaves);
		if ($(button).hasClass(saveClass)) { // Was saved, now clicked to toggle not saved
			numSaves--;
		}
		else if ($(button).hasClass(defaultClass)) { // Now saved, 1 more save count
			numSaves++;
		}
		$(button).find('span').text(numSaves);
		button.setAttribute('data-num-saves', numSaves);
	}

	$('[data-toggle="popover"]').popover({
		container: 'body',
		placement: 'bottom',
		html: true,
		trigger: 'click'
	});
}

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
	let slideTime = 300;

	// Add typed ingredient to list of ingredients
	$('#addIngredientsButton').on('click', function() {
		// If empty ingredient, don't do anything
		var currIngredient = $('#id_currentIngredient').val().trim().toLowerCase().split(' ').join('-');
		if (currIngredient == '') return;
		$('#id_currentIngredient').val('').focus();

		// If ingredient not yet added, add it
		for (let ingredient of ingredients) {
			if (currIngredient == ingredient) return;
		}
		ingredients.unshift(currIngredient);
		$('#id_ingredient_list').val(ingredients.join(' '));

		// Animate new element being added, slide down
		var newlyAdded = $('#ingredient-list-group').prepend('<li class="ingredient list-group-item" data-raw-name="'+currIngredient+'">'
			+ currIngredient.capitalize()
			+ '<i class="fa fa-minus-circle pull-right"></i></li>')
			.find('li').first();
		newlyAdded.hide().slideDown(slideTime).addClass('list-group-item-success')
			.queue(function() { $(this).removeClass('list-group-item-success').dequeue(); });
	});

	// Remove ingredient on click, slide up
	$('#ingredient-list-group').on('click', 'li.ingredient', function() {
		var ingredient = $(this).data('raw-name');
		ingredients.splice(ingredients.indexOf(ingredient), 1);
		$(this).addClass('list-group-item-danger').slideUp(slideTime);
		$('#id_currentIngredient').focus(); 
	});

	// Allow enter in ingredients to click add button
	$('#id_currentIngredient').keypress(function(event) {
		if (event.keyCode == 13) {
			// event.preventDefault();
			$('#addIngredientsButton').click();
			return false;
			// return false;
		}
	});
	$('#id_name').keypress(function(event) {
		if (event.keyCode == 13) {
			console.log("Preventing form submission on enter");
			// event.preventDefault();
			return false;
		}
	});
}









String.prototype.capitalize = function() {
	var splitStr = this.toLowerCase().split('-');
	for (var i = 0; i < splitStr.length; i++) {
		splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);
	}
	return splitStr.join(' ');
}






