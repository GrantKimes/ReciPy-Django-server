import pprint
import logging
logger = logging.getLogger('main')
import json
from urllib.request import Request as url_request
import facebook # Facebook API sdk

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AdminPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.conf import settings

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from social_django.models import UserSocialAuth

from .models import YummlyRecipe, Ingredient
from .forms import UserForm, UserRegistrationForm, UserInfoForm, ProfileInfoForm



def home(request):
	context = {}
	logger.debug(request.user.username)
	return render(request, 'main/home.html', context)


# Yummly Recipes
############################################################

class YummlyRecipeList(ListView):
	model = YummlyRecipe
	template_name = 'main/yummlyrecipe_list.html'

	#queryset = YummlyRecipe.objects.order_by('name')

	# YummlyRecipe models to pass to template
	def get_queryset(self):
		return YummlyRecipe.objects.order_by('name')[:20]


	# Other values to pass to template
	def get_context_data(self, **kwargs):
		context = super(YummlyRecipeList, self).get_context_data(**kwargs)

		context['total_recipe_count'] = YummlyRecipe.objects.count()
		return context


class YummlyRecipeDetail(DetailView):
	model = YummlyRecipe
	template_name = 'main/yummlyrecipe_detail.html'

	context_object_name = 'recipe'


# Ingredients
############################################################

class IngredientList(ListView):
	model = Ingredient
	template_name = 'main/ingredient_list.html'

	def get_queryset(self):
		return Ingredient.objects.order_by('name')

class IngredientDetail(DetailView):
	model = Ingredient
	template_name = 'main/ingredient_detail.html'

	# context_object_name = 'ingredient'



# Users
############################################################

class UserList(ListView):
	model = User
	template_name = 'main/user_list.html'

	def get_queryset(self):
		return User.objects.all()

class UserDetail(DetailView):
	model = User
	template_name = 'main/user_detail.html'
	slug_field = 'username' # slug is in url, ex: users/<username>

	# def get_queryset(self):
	# 	return User.objects.filter(username=)


# class UserFormView(View):
# 	form_class = UserForm 
# 	template_name = 'main/registration_form.html'

# 	# Display blank form for new user registering
# 	def get(self, request):
# 		form = self.form_class(None)
# 		context = { 'form': form }
# 		return render(request, self.template_name, context)

# 	# Process submitted form, add user if valid
# 	def post(self, request):
# 		form = self.form_class(request.POST)

# 		if form.is_valid():
# 			user = form.save(commit=False) # Creates object from form data, but doesn't save to db

# 			# Clean and normalize data
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password']

# 			user.set_password(password)
# 			user.save()



class UserRegistrationView(FormView):
	form_class = UserRegistrationForm
	template_name = 'users/register.html'
	success_url = '/' # reverse('main:home')

	def form_valid(self, form):
		form.save()
		return redirect('/login')
		# user = form.save(commit=False)
		# username = form.cleaned_data.get('username')
		# password = form.cleaned_data.get('password')
		# user.set_password(password)
		# user.save()
		# user = authenticate(username=username, password=password)

		# if user is not None:
		# 	if user.is_active:
		# 		login(request, user)
		# 		return redirect(self.success_url)

	# def post(self, request):
	# 	form = self.form_class(request.POST or None)
	# 	if form.is_valid():
	# 		user = form.save(commit=False)
	# 		username = form.cleaned_data.get('username')
	# 		password = form.cleaned_data.get('password')
	# 		user.set_password(password)
	# 		user.save()
	# 		user = authenticate(username=username, password=password)

	# 		if user is not None:
	# 			if user.is_active:
	# 				login(request, user)


	def get_context_data(self, **kwargs):
		# Call the base implementation first to get a context
		context = super(UserRegistrationView, self).get_context_data(**kwargs)

		# logger.debug(vars(context['form']))
		# for field in context['form']:
		# 	logger.debug(vars(field))
		
		return context


# def login_user(request):
# 	return render(request, 'users/login.html')

def logout_user(request):
	logout(request)
	return redirect('/')



# Page for a user to view and update their profile
@login_required
def update_profile(request):
	user = request.user
	template_name = 'users/update_profile.html'
	context = {}

	if request.method == 'POST':
		user_form = UserInfoForm(request.POST, instance=user)
		profile_form = ProfileInfoForm(request.POST, instance=user.profile)
		context['user_form'] = user_form
		context['profile_form'] = profile_form
		# profile_form['bio'].css_classes('form-control')

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated.')
			return redirect('home')
		else:
			messages.error(request, 'Please correct the errors below.')

	else: 
		# Display form with existing info 
		user_form = UserInfoForm(instance=user)
		profile_form = ProfileInfoForm(instance=user.profile)
		context['user_form'] = user_form
		context['profile_form'] = profile_form

		try: 
			facebook_login = user.social_auth.get(provider='facebook')
			# logger.debug(vars(facebook_login))
			# logger.debug(facebook_login.extra_data)

			oauth_token = facebook_login.extra_data['access_token']
			# logger.debug(oauth_token)
			graph = facebook.GraphAPI(access_token=oauth_token)
			# logger.debug(graph)
			profile = graph.get_object("me")
			# logger.debug(profile)

			picture = graph.get_connections("me", "picture")
			context['profile_picture_url'] = picture['url']


		except UserSocialAuth.DoesNotExist:
			facebook_login = None

		can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
		context['facebook_login'] = facebook_login
		context['can_disconnect'] = can_disconnect

	return render(request, template_name, context)



# AJAX request to favorite a recipe
@login_required
def favorite_recipe(request):
	response_data = {}
	if request.method == 'POST':
		recipe_id = request.POST.get('recipe_id')
		try:
			recipe = YummlyRecipe.objects.get(id=recipe_id)
		except YummlyRecipe.DoesNotExist:
			recipe = None

		user_profile = request.user.profile

		# Like the recipe. If it is already liked, unlike it. 
		if user_profile.liked_recipes.filter(pk=recipe.pk).exists():
			user_profile.liked_recipes.remove(recipe)
			response_data['success_message'] = 'Removed recipe %s from %s\'s liked recipes' % (recipe_id, request.user.username)
		else:
			user_profile.liked_recipes.add(recipe)
			response_data['success_message'] = 'Added recipe %s to %s\'s liked recipes' % (recipe_id, request.user.username)

	else:
		response_data['error_message'] = 'Submission type needs to be POST.'
	
	return JsonResponse(response_data)




@login_required
def change_password(request):
	if request.user.has_usable_password():
		PasswordForm = PasswordChangeForm
	else:
		PasswordForm = AdminPasswordChangeForm

	if request.method == 'POST':
		form = PasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Your password was successfully updated.')
			return redirect('home')
		else:
			messages.error(request, 'Please correct the errors below.')
	else:
		form = PasswordForm(request.user)

	return render(request, 'users/change_password.html', {'form': form } )










