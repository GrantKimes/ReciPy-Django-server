from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User 
from rest_framework.test import APIRequestFactory

from .models import Recipe, Ingredient, Profile, RecipeVote 
from .views import recipes, users, api 

class RecipeTests(TestCase):
	def setUp(self):
		self.recipe1 = Recipe.objects.create(name='Chicken Rice', ingredient_list='chicken chicken rice bacon')
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='testguy', password='fdsajkl;')


	def test_link_ingredients_on_recipe_save(self):
		r = Recipe.objects.get(name='Chicken Rice')
		self.assertEqual(r.ingredients.count(), 3)


	def test_add_to_user_saved_recipes_fail_when_get(self):
		request = self.factory.get('/save_recipe')
		request.user = self.user 
		response = users.add_to_user_saved_recipes(request)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'needs to be POST')


	def test_add_to_user_saved_recipes(self):
		request = self.factory.post('/save_recipe')
		request.user = self.user 
		request.POST = {'recipe_id': self.recipe1.id}

		response = users.add_to_user_saved_recipes(request) # First to add
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Added')
		self.assertIn(self.recipe1, self.user.profile.saved_recipes.all())

		response = users.add_to_user_saved_recipes(request) # Second to remove
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Removed')
		self.assertNotIn(self.recipe1, self.user.profile.saved_recipes.all())



class APITests(TestCase):
	def setUp(self):
		self.recipe1 = Recipe.objects.create(name='Chicken Rice', ingredient_list='chicken chicken rice bacon')
		self.initial_num_recipes = 1
		self.factory = APIRequestFactory()
		self.user = User.objects.create_user(username='testguy', password='fdsajkl;')
		self.new_recipe_data = { 'name': 'API Recipe', 'ingredient_list': 'corn soup black-beans' }
		self.like_recipe_data = { 'recipe_id': self.recipe1.id }



	def test_api_list_recipes(self):
		request = self.factory.get('/api/recipes/')
		response = api.RecipeList.as_view()(request)
		self.assertContains(response, self.recipe1.name)


	########################################################
	# Create recipes
	########################################################
	def test_api_create_recipe(self):
		request = self.factory.post('/api/recipes/create', self.new_recipe_data, format='json')
		request.user = self.user 
		response = api.RecipeCreate.as_view()(request)

		r = Recipe.objects.get(name=self.new_recipe_data['name'])
		i = Ingredient.objects.get(raw_name='black-beans')
		self.assertEqual(response.status_code, 201) # created
		self.assertEqual(r.id, self.initial_num_recipes+1) # One more recipe than before
		self.assertEqual(i.name, 'Black Beans') # Proper ingredient list parsing
		self.assertEqual(r.creator, self.user) 
		self.assertTrue(r.is_user_recipe)


	def test_api_create_recipe_fail_when_not_authenticated(self):
		request = self.factory.post('/api/recipes/create', self.new_recipe_data, format='json')
		response = api.RecipeCreate.as_view()(request)
		self.assertEqual(response.status_code, 403) # forbidden
		self.assertEqual(Recipe.objects.all().count(), self.initial_num_recipes) # Didn't create


	########################################################
	# Like and dislike
	########################################################
	def test_api_save_recipe(self):
		request = self.factory.post('/api/recipes/save', self.like_recipe_data, format='json')
		request.user = self.user 
		self.assertEqual(self.user.profile.saved_recipes.count(), 0)
		response = api.SaveRecipe.as_view()(request)
		self.assertEqual(response.status_code, 200) # ok
		self.assertContains(response, 'Processed save request')
		self.assertEqual(self.user.profile.saved_recipes.count(), 1)


	def test_api_unsave_recipe_when_already_saved(self):
		request = self.factory.post('/api/recipes/save', self.like_recipe_data, format='json')
		request.user = self.user 
		response = api.SaveRecipe.as_view()(request)
		self.assertEqual(self.user.profile.saved_recipes.count(), 1)
		request = self.factory.post('/api/recipes/save', self.like_recipe_data, format='json')
		request.user = self.user 
		response = api.SaveRecipe.as_view()(request)
		self.assertEqual(self.user.profile.saved_recipes.count(), 0)


	########################################################
	# Like and dislike
	########################################################
	def test_api_like_recipe(self):
		request = self.factory.post('/api/recipes/like', self.like_recipe_data, format='json')
		request.user = self.user 
		self.assertEqual(self.user.profile.liked_recipes.count(), 0)
		response = api.LikeRecipe.as_view()(request)
		self.assertEqual(response.status_code, 200) # ok
		self.assertContains(response, 'Processed like request')
		self.assertEqual(self.user.profile.liked_recipes.count(), 1)


	def test_api_dislike_recipe(self):
		request = self.factory.post('/api/recipes/dislike', self.like_recipe_data, format='json')
		request.user = self.user 
		self.assertEqual(self.user.profile.disliked_recipes.count(), 0)
		response = api.DislikeRecipe.as_view()(request)
		self.assertEqual(response.status_code, 200) # ok
		self.assertContains(response, 'Processed dislike request')
		self.assertEqual(self.user.profile.disliked_recipes.count(), 1)


	def test_api_unlike_recipe_already_liked(self):
		request = self.factory.post('/api/recipes/like', self.like_recipe_data, format='json')
		request.user = self.user 
		response = api.LikeRecipe.as_view()(request)
		self.assertEqual(self.user.profile.liked_recipes.count(), 1)
		request = self.factory.post('/api/recipes/like', self.like_recipe_data, format='json')
		request.user = self.user 
		response = api.LikeRecipe.as_view()(request)
		self.assertEqual(self.user.profile.liked_recipes.count(), 0)


	def test_api_like_recipe_remove_from_disliked(self):
		request = self.factory.post('/api/recipes/dislike', self.like_recipe_data, format='json')
		request.user = self.user 
		response = api.DislikeRecipe.as_view()(request)
		self.assertEqual(self.user.profile.liked_recipes.count(), 0)
		self.assertEqual(self.user.profile.disliked_recipes.count(), 1)
		request = self.factory.post('/api/recipes/like', self.like_recipe_data, format='json')
		request.user = self.user 
		response = api.LikeRecipe.as_view()(request)
		self.assertEqual(self.user.profile.liked_recipes.count(), 1)
		self.assertEqual(self.user.profile.disliked_recipes.count(), 0)


	def test_api_like_recipe_fail_when_not_authenticated(self):
		request = self.factory.post('/api/recipes/like', self.like_recipe_data, format='json')
		response = api.LikeRecipe.as_view()(request)
		self.assertEqual(response.status_code, 403) # forbidden
		self.assertEqual(self.user.profile.liked_recipes.count(), 0) # Didn't count as like


	def test_api_like_recipe_fail_on_get_request(self):
		request = self.factory.get('/api/recipes/like', self.like_recipe_data, format='json')
		request.user = self.user 
		response = api.LikeRecipe.as_view()(request)
		self.assertEqual(response.status_code, 405) # method not allowed
		self.assertEqual(self.user.profile.liked_recipes.count(), 0) # Didn't count as like





