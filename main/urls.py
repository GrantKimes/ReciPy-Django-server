from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

# from .views import YummlyRecipeList, YummlyRecipeDetail, IngredientDetail, IngredientList

urlpatterns = [
	# ex: 
	url(r'^$', views.home, name='home'),

	# ex: recipes/
	url(r'^recipes/$', views.YummlyRecipeList.as_view(), name='recipe_list'),
	# ex: recipes/5
	url(r'^recipes/(?P<pk>[0-9]+)$', views.YummlyRecipeDetail.as_view(), name='recipe_detail'),

	# ex: ingredients/
	url(r'^ingredients/$', views.IngredientList.as_view(), name='ingredient_list'),
	# ex: ingredients/5
	url(r'^ingredients/(?P<pk>[0-9]+)$', views.IngredientDetail.as_view(), name='ingredient_detail'),

	# ex: users/
	url(r'^users/$', views.UserList.as_view(), name='user_list'),
	# ex: users/name
	url(r'^users/(?P<slug>\w+)$', views.UserDetail.as_view(), name='user_detail'),


	url(r'^register/$', views.UserRegistrationView.as_view(), name='user_registration'),
	url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
	url(r'^logout/$', views.logout_user, name='logout'),
	url(r'^delete_user/$', views.delete_user, name='delete_user'),

	url(r'^profile/$', views.update_profile, name='update_profile'),
	url(r'^profile/password/$', views.change_password, name='change_password'),

	url(r'^favorite_recipe/$', views.favorite_recipe, name='favorite_recipe'),

	# url(r'^create_recipe/$', views.UserRecipeCreate.as_view(), name='create_recipe'),
	url(r'^create_recipe/$', views.create, name='create_recipe'),



	# ex: /createRecipes/5/
	# url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'), 
	# access captured group () in view method through self.args[0] or self.kwargs
]