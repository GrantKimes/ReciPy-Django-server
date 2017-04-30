import json
from urllib.request import Request as url_request
import facebook # Facebook API sdk
import logging
logger = logging.getLogger('main')

# Django 
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from django.contrib import messages 
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity

# Django extensions
from social_django.models import UserSocialAuth
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework import generics
from rest_framework import permissions 
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse as api_reverse

# Local
from main.models import Recipe, Ingredient
from main.forms import RecipeCreateForm
from main.serializers import RecipeSerializer, RecipeDetailSerializer, UserSerializer, UserDetailSerializer, RecipeCreateSerializer


def home(request):
	context = {}

	if request.user.is_authenticated:
		profile = request.user.profile 
		liked_recipes = profile.liked_recipes.all()
		disliked_recipes = profile.disliked_recipes.all()

		recommended_recipes = Recipe.objects.filter(related_recipes__in=liked_recipes).distinct().exclude(id__in=liked_recipes).exclude(id__in=disliked_recipes)
		context['recommended_recipes'] = recommended_recipes
	return render(request, 'main/home.html', context)


def about(request):
	return render(request, 'main/about.html', {})


class Search(View):
	template_name = 'main/search_results.html'

	def get(self, request):
		query = str(request.GET.get('q', ''))
		context = {
			# 'searched_recipes': Recipe.objects.filter(name__search=query)[:8],
			# 'searched_recipes_count': Recipe.objects.filter(name__search=query).count(),
			'searched_recipes': Recipe.objects.annotate(similarity=TrigramSimilarity('name', query)).filter(similarity__gt=0.3).order_by('-similarity')[:16],
			# 'searched_users': User.objects.annotate(search=SearchVector('username', 'email')).filter(search=query),
			'searched_users': User.objects.annotate(similarity=TrigramSimilarity('username', query)).filter(similarity__gt=0.3).order_by('-similarity')[:16],
			'query_string': query,
		}


		if request.user.is_authenticated:
			context['saved_recipes'] = request.user.profile.saved_recipes.all()
			context['liked_recipes'] = request.user.profile.liked_recipes.all()
			context['disliked_recipes'] = request.user.profile.disliked_recipes.all()
		return render(request, self.template_name, context)


############################################################
# Recipes
############################################################

class RecipeList(View):
	template_name = 'main/recipe_list.html'

	def get(self, request):
		context = {
			'total_recipe_count': Recipe.objects.count(),
			'recent_user_recipes': Recipe.objects.filter(is_user_recipe=True).order_by('-date_created')[:8],
			'most_saved_yummly_recipes': Recipe.objects.filter(is_yummly_recipe=True).annotate(num_saves=Count('profiles_saved')).order_by('-num_saves')[:8],
		}
		if request.user.is_authenticated:
			context['saved_recipes'] = request.user.profile.saved_recipes.all()
			context['liked_recipes'] = request.user.profile.liked_recipes.all()
			context['disliked_recipes'] = request.user.profile.disliked_recipes.all()
		return render(request, self.template_name, context)



class RecipeDetail(DetailView):
	model = Recipe
	template_name = 'main/recipe_detail.html'
	context_object_name = 'recipe'

	def get_context_data(self, **kwargs):
		context = super(RecipeDetail, self).get_context_data(**kwargs)
		recipe = self.get_object()
		context['flavors'] = [
			{ 'name': 'salty', 'value': int(recipe.salty * 100) },
			{ 'name': 'bitter', 'value': int(recipe.bitter * 100) },
			{ 'name': 'sour', 'value': int(recipe.sour * 100) },
			{ 'name': 'sweet', 'value': int(recipe.sweet * 100) },
			{ 'name': 'meaty', 'value': int(recipe.meaty * 100) },
			{ 'name': 'piquant', 'value': int(recipe.piquant * 100) },
		]
		if self.request.user.is_authenticated:
			context['saved_recipes'] = self.request.user.profile.saved_recipes.all()
			context['liked_recipes'] = self.request.user.profile.liked_recipes.all()
			context['disliked_recipes'] = self.request.user.profile.disliked_recipes.all()
		return context


@method_decorator(login_required, name='dispatch')
class RecipeCreate(View):
	def get(self, request):
		form = RecipeCreateForm()
		return render(request, 'main/user_recipe_create.html', {'form': form})

	def post(self, request):
		form = RecipeCreateForm(request.POST, request.FILES)
		if form.is_valid():
			r = Recipe()
			r.name = form.cleaned_data['name']
			r.ingredient_list = form.cleaned_data['ingredient_list']
			r.instructions = form.cleaned_data['instructions']
			r.photo = request.FILES['photo']
			r.is_user_recipe = True
			r.creator = request.user.profile
			r.save()

			messages.success(request, "Recipe created.")
			return redirect('recipe_detail', pk=r.id)
		else:
			messages.error(request, "Invalid input, correct errors below.")
			return render(request, 'main/user_recipe_create.html', {'form': form})


############################################################
# Ingredients
############################################################

class IngredientList(ListView):
	model = Ingredient
	template_name = 'main/ingredient_list.html'

	def get_queryset(self):
		return Ingredient.objects.order_by('name')[:100]

class IngredientDetail(DetailView):
	model = Ingredient
	template_name = 'main/ingredient_detail.html'

	# context_object_name = 'ingredient'

