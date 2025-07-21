from django import forms
from django.forms import ModelForm
from .models import Instrument

class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = ['category', 'name']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'block w-full p-2.5 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-sm focus:ring-blue-500 focus:border-blue-500',
                'required': 'true' 
            }),
            'name': forms.TextInput(attrs={
                'class': 'block w-full p-2.5 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: Percusión',
                'required': 'true'
            }),
        }