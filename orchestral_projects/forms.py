from django import forms
from django.forms import ModelForm
from .models import OrchestralProject


class OrchestralProjectForm(ModelForm):
    class Meta:
        model = OrchestralProject
        fields = ['code', 'name']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'block w-full p-2.5 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: INICIAL-001',
                'required': 'true' # Hace el campo HTML requerido
            }),
            'name': forms.TextInput(attrs={
                'class': 'block w-full p-2.5 text-gray-900 border border-gray-300 rounded-lg bg-gray-50 text-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Ej: Orquesta Sinfónica Juvenil',
                'required': 'true'
            }),
        }