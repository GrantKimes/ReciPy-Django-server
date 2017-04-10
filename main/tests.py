from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User 
from rest_framework.test import APIRequestFactory

from .models import Recipe, Ingredient, Profile, RecipeVote 
from . import views 

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
		response = views.add_to_user_saved_recipes(request)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'needs to be POST')


	def test_add_to_user_saved_recipes(self):
		request = self.factory.post('/save_recipe')
		request.user = self.user 
		request.POST = {'recipe_id': self.recipe1.id}

		response = views.add_to_user_saved_recipes(request) # First to add
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Added')
		self.assertIn(self.recipe1, self.user.profile.saved_recipes.all())

		response = views.add_to_user_saved_recipes(request) # Second to remove
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Removed')
		self.assertNotIn(self.recipe1, self.user.profile.saved_recipes.all())



class APITests(TestCase):
	def setUp(self):
		self.recipe1 = Recipe.objects.create(name='Chicken Rice', ingredient_list='chicken chicken rice bacon')
		self.factory = APIRequestFactory()
		self.user = User.objects.create_user(username='testguy', password='fdsajkl;')


	def test_api_list_recipes(self):
		request = self.factory.get('/api/recipes/')
		response = views.APIRecipeList.as_view()(request)
		self.assertContains(response, self.recipe1.name)


	def test_api_create_recipe(self):
		data = {
			'name': 'API Recipe',
			'ingredient_list': 'corn soup black-beans'
		}
		request = self.factory.post('/api/recipes/create', data, format='json')
		request.user = self.user 
		response = views.APIRecipeCreate.as_view()(request)

		r = Recipe.objects.get(name=data['name'])
		i = Ingredient.objects.get(raw_name='black-beans')
		self.assertEqual(response.status_code, 201) # created
		self.assertEqual(data['ingredient_list'], r.ingredient_list)
		self.assertEqual(r.id, 2)
		self.assertEqual(i.name, 'Black Beans')













