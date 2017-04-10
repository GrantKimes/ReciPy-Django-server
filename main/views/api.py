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



############################################################
# API Views
############################################################

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': api_reverse('api_users_list', request=request, format=format),
	})

class APIRecipeList(generics.ListAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeSerializer

class APIRecipeCreate(generics.CreateAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeCreateSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def perform_create(self, serializer):
		serializer.save(creator=self.request.user, is_user_recipe=True)

class APIRecipeDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeDetailSerializer 

class APIUserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class APIUserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer 

