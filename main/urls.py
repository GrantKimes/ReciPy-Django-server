from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
	url(r'^$', views.home, name='home'),

	url(r'^recipes/$', views.RecipeList.as_view(), name='recipe_list'),
	# ex: recipes/5
	url(r'^recipes/(?P<pk>[0-9]+)$', views.RecipeDetail.as_view(), name='recipe_detail'),

	url(r'^ingredients/$', views.IngredientList.as_view(), name='ingredient_list'),
	# ex: ingredients/5
	url(r'^ingredients/(?P<pk>[0-9]+)$', views.IngredientDetail.as_view(), name='ingredient_detail'),

	url(r'^users/$', views.UserList.as_view(), name='user_list'),
	url(r'^users/(?P<slug>\w+)$', views.UserDetail.as_view(), name='user_detail'),


	# User management
	url(r'^register/$', views.UserRegistrationView.as_view(), name='user_registration'),
	url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
	url(r'^logout/$', views.logout_user, name='logout'),
	url(r'^delete_user/$', views.delete_user, name='delete_user'),

	url(r'^profile/$', views.update_profile, name='update_profile'),
	url(r'^profile/password/$', views.change_password, name='change_password'),

	url(r'^save_recipe/$', views.add_to_user_saved_recipe, name='save_recipe'),

	# url(r'^create_recipe/$', views.UserRecipeCreate.as_view(), name='create_recipe'),
	url(r'^create/$', views.create_recipe, name='create_recipe'),



	# API urls
	url(r'^api_recipes/$', views.APIRecipeList.as_view()),
	url(r'^api_recipes/(?P<pk>[0-9]+)$', views.APIRecipeDetail.as_view()),


]

# url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'), 
# access captured group () in view method through self.args[0] or self.kwargs
