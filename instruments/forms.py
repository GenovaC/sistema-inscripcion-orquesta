from django import forms
from django.forms import ModelForm
from .models import Instrument

class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = ['code', 'name']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'block w-full p-2.5 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: PERCUSION-001',
                'required': 'true' # Hace el campo HTML requerido
            }),
            'name': forms.TextInput(attrs={
                'class': 'block w-full p-2.5 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: Percusión',
                'required': 'true'
            }),
        }