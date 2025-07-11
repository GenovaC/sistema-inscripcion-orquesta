from django import forms
from .models import Student
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class StudentForm(forms.ModelForm):
    # Campos que requieren widgets específicos o validaciones adicionales a nivel de formulario
    age = forms.CharField(
        label="Edad",
        required=False, # No es requerido para la entrada del usuario
        widget=forms.TextInput(attrs={
            'readonly': 'readonly', # Campo de solo lectura
            'class': 'block w-full rounded-md border-0 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 bg-gray-100 cursor-not-allowed'
        }),
        help_text="Autocalculada a partir de la fecha de nacimiento."
    )

    class Meta:
        model = Student
        fields = [
             'document_id', 'nationality', 'names', 'lastnames', 'born_date',
             'gender', 'address', 'home_phone', 'cellphone', 'email'
        ]
        labels = {
            'document_id': 'Cédula/Pasaporte',
            'nationality': 'Nacionalidad',
            'names': 'Nombres',
            'lastnames': 'Apellidos',
            'born_date': 'Fecha de Nacimiento',
            'gender': 'Género',
            'address': 'Dirección',
            'home_phone': 'Teléfono de Casa',
            'cellphone': 'Celular',
            'email': 'Correo Electrónico',
        }
        help_texts = {
            'document_id': 'Cédula del estudiante sin puntos ni espacios.',
            'nationality': 'Venezolano (V) o Extranjero (E).',
            'names':       'Máximo 30 caracteres.',
            'lastnames':   'Máximo 30 caracteres.',
            'born_date':   'Selecciona la fecha de nacimiento del estudiante.',
            'gender':      'Selecciona Femenino o Masculino.',
            'address':     'Dirección de residencia del estudiante.',
            'home_phone':  'Número telefónico residencial.',
            'cellphone':   'Número telefónico personal.',
            'email':       'Correo electrónico del estudiante.',
        }
        widgets = {
            'document_id': forms.TextInput(attrs={
                'placeholder': 'Ej: 1234567',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'nationality': forms.Select(attrs={
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'names': forms.TextInput(attrs={
                'placeholder': 'Ej: Juan',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'lastnames': forms.TextInput(attrs={
                'placeholder': 'Ej: Pérez',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'gender': forms.Select(attrs={
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'address': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ej: Calle Principal, Casa #10',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'home_phone': forms.TextInput(attrs={
                'placeholder': 'Ej: 02861234567',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'cellphone': forms.TextInput(attrs={
                'placeholder': 'Ej: 04121234567',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Ej: correo@ejemplo.com',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'born_date':   forms.DateInput(attrs={
                'type': 'date',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            })
        }

     # Sobreescribir el constructor para calcular la edad al cargar el formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.born_date:
            today = timezone.now().date()
            age = today.year - self.instance.born_date.year - ((today.month, today.day) < (self.instance.born_date.month, self.instance.born_date.day))
            self.fields['age'].initial = age # Asigna la edad calculada al campo 'age'

    def clean_document_id(self):
        document_id = self.cleaned_data.get('document_id')
        if not (3 <= len(document_id) <= 8):
            raise ValidationError('El ID del documento debe tener entre 3 y 8 caracteres.')
        return document_id

    def clean_born_date(self):
        born_date = self.cleaned_data.get('born_date')
        if born_date:
            today = timezone.now().date()
            min_born_date = today - timezone.timedelta(days=5 * 365.25)
            if born_date > min_born_date:
                raise ValidationError('El estudiante debe ser mayor de 5 años.')
        return born_date

    def clean_home_phone(self):
        home_phone = self.cleaned_data.get('home_phone')
        if home_phone and not re.fullmatch(r'^\d{11}$', home_phone):
            raise ValidationError('El número de teléfono de casa debe tener 11 dígitos.')
        return home_phone

    def clean_cellphone(self):
        cellphone = self.cleaned_data.get('cellphone')
        if cellphone and not re.fullmatch(r'^\d{11}$', cellphone):
            raise ValidationError('El número de celular debe tener 11 dígitos.')
        return cellphone