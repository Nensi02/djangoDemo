# forms.py
from django import forms
from .models import Services, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required')
    password = forms.CharField(widget=forms.PasswordInput)

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'description', 'status']
