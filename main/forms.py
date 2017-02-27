from django.contrib.auth.models import User
from django import forms 
from django.contrib.auth.forms import UserCreationForm 

from .models import Profile

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


# class UserRegistrationForm(forms.ModelForm):
# 	password = forms.CharField(widget=forms.PasswordInput)

# 	class Meta:
# 		model = User
# 		fields = ['username', 'password'] 

# 		# widgets = {
# 		# 	'username': forms.TextInput(attrs={'class': 'form-control'}),
# 		# }


class UserInfoForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class ProfileInfoForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio',)