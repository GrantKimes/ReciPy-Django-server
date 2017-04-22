from django.contrib.auth.models import User
from django import forms 
from django.contrib.auth.forms import UserCreationForm 

from .models import Profile, Recipe 


class RecipeCreateForm(forms.ModelForm):
	# ingredient_list	= forms.CharField(widget=forms.HiddenInput)
	instructions 	= forms.CharField(widget=forms.Textarea)
	photo 			= forms.ImageField(label="Select a photo", help_text="Help text")

	class Meta:
		model = Recipe 
		fields = ['name', 'ingredient_list', 'instructions', 'photo']




class UserForm(forms.ModelForm):
 	password = forms.CharField(widget=forms.PasswordInput)

 	class Meta:
 		model = User 
 		fields = ['username', 'email', 'password']


class UserRegistrationForm(UserCreationForm):
	# email = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ['username'] # password already include twice for confirmation

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		# user.email = self.cleaned_data['email']
		user.username = self.cleaned_data['username']

		if commit:
			user.save()
		return user 


class UserInfoForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class ProfileInfoForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio',)