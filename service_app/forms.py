# forms.py
from django import forms
from .models import Services

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'description', 'status']
