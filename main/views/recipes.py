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
from main.forms import UserForm, UserRegistrationForm, UserInfoForm, ProfileInfoForm
from main.serializers import RecipeSerializer, RecipeDetailSerializer, UserSerializer, UserDetailSerializer, RecipeCreateSerializer


def home(request):
	context = {}

	if request.user.is_authenticated:
		profile = request.user.profile 
		liked_recipes = profile.liked_recipes.all()
		disliked_recipes = profile.disliked_recipes.all()

		recommended_recipes = Recipe.objects.filter(related_recipes__in=liked_recipes).exclude(id__in=liked_recipes).exclude(id__in=disliked_recipes)[:4]
		context['recommended_recipes'] = recommended_recipes
	return render(request, 'main/home.html', context)


def about(request):
	return render(request, 'main/about.html', {})


############################################################
# Recipes
############################################################

@method_decorator(login_required, name='dispatch')
class RecipeList(ListView):
	model = Recipe
	template_name = 'main/recipe_list.html'

	# Recipe models to pass to template
	def get_queryset(self):
		return Recipe.objects.order_by('name')[:20]


	# Other values to pass to template
	def get_context_data(self, **kwargs):
		context = super(RecipeList, self).get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context['saved_recipes'] = self.request.user.profile.saved_recipes.all()
			context['liked_recipes'] = self.request.user.profile.liked_recipes.all()
			context['disliked_recipes'] = self.request.user.profile.disliked_recipes.all()
		context['total_recipe_count'] = Recipe.objects.count()
		return context


@method_decorator(login_required, name='dispatch')
class RecipeDetail(DetailView):
	model = Recipe
	template_name = 'main/recipe_detail.html'
	context_object_name = 'recipe'

	def get_context_data(self, **kwargs):
		context = super(RecipeDetail, self).get_context_data(**kwargs)
		recipe = self.get_object()
		context['flavor_percent'] = {
			'bitter': int(recipe.bitter * 100),
			'meaty': int(recipe.meaty * 100),
			'salty': int(recipe.salty * 100),
			'sour': int(recipe.sour * 100),
			'sweet': int(recipe.sweet * 100),
			'piquant': int(recipe.piquant * 100),
		}
		context['saved_recipes'] = self.request.user.profile.saved_recipes.all()
		context['liked_recipes'] = self.request.user.profile.liked_recipes.all()
		context['disliked_recipes'] = self.request.user.profile.disliked_recipes.all()
		return context



@login_required
def create_recipe(request):
	context = {}
	return render(request, 'main/user_recipe_create.html', context)


############################################################
# Ingredients
############################################################

@method_decorator(login_required, name='dispatch')
class IngredientList(ListView):
	model = Ingredient
	template_name = 'main/ingredient_list.html'

	def get_queryset(self):
		return Ingredient.objects.order_by('name')

@method_decorator(login_required, name='dispatch')
class IngredientDetail(DetailView):
	model = Ingredient
	template_name = 'main/ingredient_detail.html'

	# context_object_name = 'ingredient'

