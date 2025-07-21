from django import forms
from django.forms import ModelForm
from .models import AcademicPeriod, DetailAcademicInscription
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


class AcademicPeriodDataForm(forms.ModelForm):

    class Meta:
        model = AcademicPeriod
        fields = [
            'first_year', 'final_year'
        ]
        labels = {
            'first_year':  'Año inicial',
            'final_year':  'Año final'        
        }
        help_texts = {
            'first_year':  'Seleccione el año inicial del período',
            'final_year':  'Seleccione el año final del período'   
        }
        widgets = {   
            'first_year': forms.NumberInput(attrs={
                'placeholder': 'Ej: 2025',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }), 
            'final_year': forms.NumberInput(attrs={
                'placeholder': 'Ej: 2026',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            })
        }

    def clean_final_year(self):
        first_year = self.cleaned_data.get('first_year')
        final_year = self.cleaned_data.get('final_year')
        if first_year & final_year:
            if final_year != first_year + 1:
                raise ValidationError("El año final debe ser exactamente un año mayor que el año inicial.")

class DetailAcademicInscriptionForm(forms.ModelForm):

    class Meta:
        model = DetailAcademicInscription
        fields = [
            'id_orchestral_project', 'id_instrument', 'id_academic_period', 'inscription_date',
            'type'
        ]
        labels = {
            'id_orchestral_project':  'Proyecto Orquestal',
            'id_instrument':          'Instrumento',
            'id_academic_period':     'Período Académico',
            'inscription_date':       'Fecha de Inscripción',
            'type':                   'Tipo de Inscripción'            
        }
        help_texts = {
            'id_orchestral_project':  'Seleccione un proyecto académico',
            'id_instrument':          'Seleccione un instrumento',
            'id_academic_period':     'Seleccione el período académico',
            'inscription_date':       'Seleccione la fecha de inscripción',
            'type':                   'Seleccione el tipo de inscripción'  
        }
        widgets = {
            'id_orchestral_project': forms.Select(attrs={
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'id_instrument': forms.Select(attrs={
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'id_academic_period': forms.Select(attrs={
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'type': forms.Select(attrs={
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'inscription_date':   forms.DateInput(attrs={
                'type': 'date',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            })
        }

    def clean_inscription_date(self):
        inscription_date = self.cleaned_data.get('inscription_date')
        if inscription_date and inscription_date > timezone.now().date():
            raise ValidationError("La fecha de inscripción no puede ser futura.")
        return inscription_date
  