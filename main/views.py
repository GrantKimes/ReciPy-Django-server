import pprint
import logging
logger = logging.getLogger('main')

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView


from .models import YummlyRecipe, Ingredient
from .forms import UserForm, UserRegistrationForm



def home(request):
	context = {}
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


def login_user(request):
	return render(request, 'users/login.html')

def logout_user(request):
	logout(request)
	return redirect('/')





















