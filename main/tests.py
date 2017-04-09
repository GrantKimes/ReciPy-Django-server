from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User 

from .models import Recipe, Ingredient, Profile, RecipeVote 
from . import views 

class RecipeTestCase(TestCase):
	def setUp(self):
		self.recipe1 = Recipe.objects.create(name='Chicken Rice', ingredient_list='chicken chicken rice bacon')

		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='testguy', password='fdsajkl;')

	def test_link_ingredients_on_recipe_save(self):
		r = Recipe.objects.get(name='Chicken Rice')
		self.assertEqual(r.ingredients.count(), 3)



	######################################################
	# views.add_to_user_saved_recipes
	######################################################
	def test_add_to_user_saved_recipes_fail_when_get(self):
		request = self.factory.get('/save_recipe')
		request.user = self.user 
		response = views.add_to_user_saved_recipes(request)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'needs to be POST')

	def test_add_to_user_saved_recipes_add(self):
		request = self.factory.post('/save_recipe')
		request.user = self.user 
		request.POST = {'recipe_id': self.recipe1.id}
		response = views.add_to_user_saved_recipes(request)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Added')
		self.assertIn(self.recipe1, self.user.profile.saved_recipes.all())

	def test_add_to_user_saved_recipes_remove(self):
		request = self.factory.post('/save_recipe')
		request.user = self.user 
		request.POST = {'recipe_id': self.recipe1.id}
		response = views.add_to_user_saved_recipes(request)
		response = views.add_to_user_saved_recipes(request) # Twice to add then remove

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Removed')
		self.assertNotIn(self.recipe1, self.user.profile.saved_recipes.all())

