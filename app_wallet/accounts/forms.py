from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CreateAccountForm(UserCreationForm):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Login'}))
	password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
	email = forms.CharField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Email'})) 

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'email']

class LoginForm(AuthenticationForm):
	username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Login'}))
	password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))