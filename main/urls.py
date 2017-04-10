from django.conf.urls import url, include 
from django.contrib.auth import views as auth_views

from .views import recipes, users, api 


urlpatterns = [
	url(r'^$', recipes.home, name='home'),
	url(r'^recipes/$', recipes.RecipeList.as_view(), name='recipe_list'),
	url(r'^recipes/(?P<pk>[0-9]+)$', recipes.RecipeDetail.as_view(), name='recipe_detail'),
	url(r'^ingredients/$', recipes.IngredientList.as_view(), name='ingredient_list'),
	url(r'^ingredients/(?P<pk>[0-9]+)$', recipes.IngredientDetail.as_view(), name='ingredient_detail'),
	url(r'^create/$', recipes.create_recipe, name='create_recipe'),


	# Users
	url(r'^users/$', users.UserList.as_view(), name='user_list'),
	url(r'^users/(?P<slug>\w+)$', users.UserDetail.as_view(), name='user_detail'),
	url(r'^register/$', users.UserRegistrationView.as_view(), name='user_registration'),
	url(r'^login/$', auth_views.login, {'template_name': 'users/login.html'}, name='login'),
	url(r'^logout/$', users.logout_user, name='logout'),
	url(r'^delete_user/$', users.delete_user, name='delete_user'),

	url(r'^profile/$', users.update_profile, name='update_profile'),
	url(r'^profile/password/$', users.change_password, name='change_password'),

	url(r'^save_recipe/$', users.add_to_user_saved_recipes, name='save_recipe'),


	# API urls
	url(r'^api/$', api.Root),
	url(r'^api/recipes/$', api.RecipeList.as_view()),
	url(r'^api/recipes/create/$', api.RecipeCreate.as_view()),
	url(r'^api/recipes/save/$', api.SaveRecipe.as_view()),
	url(r'^api/recipes/like/$', api.LikeRecipe.as_view()),
	url(r'^api/recipes/dislike/$', api.DislikeRecipe.as_view()),
	url(r'^api/recipes/(?P<pk>[0-9]+)$', api.RecipeDetail.as_view()),
	url(r'^api/users/$', api.UserList.as_view(), name='api_users_list'),
	url(r'^api/users/(?P<pk>[0-9]+)$', api.UserDetail.as_view()),

	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

# url(r'^(?P<recipe_id>[0-9]+)/$', views.detail, name='detail'), 
# access captured group () in view method through self.args[0] or self.kwargs
