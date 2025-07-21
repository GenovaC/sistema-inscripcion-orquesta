from django import forms
from django.forms import ModelForm
from .models import Student, EmergencyContact, StudentRelative
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from django.utils import timezone
import re

class PersonalDataForm(forms.ModelForm):
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
            'document_id', 'has_document_id', 'nationality', 'names', 'lastnames', 'born_date',
            'gender', 'address', 'home_phone', 'cellphone', 'email', 'allergies', 'regular_medical_treatment', 'medical_report'
        ]
        labels = {
            'document_id':               'Cédula/Pasaporte',
            'has_document_id':           '¿Tiene Documento de Identidad?',       
            'nationality':               'Nacionalidad',
            'names':                     'Nombres',
            'lastnames':                 'Apellidos',
            'born_date':                 'Fecha de Nacimiento',
            'gender':                    'Género',
            'address':                   'Dirección',
            'home_phone':                'Teléfono de Casa',
            'cellphone':                 'Celular',
            'email':                     'Correo Electrónico',
            'allergies':                 'Alergias', 
            'regular_medical_treatment': '¿Se somete a algún tratamiento médico regular?', 
            'medical_report':            '¿Presenta informe médico?',
        }
        help_texts = {
            'document_id':                  'Cédula del estudiante sin puntos ni espacios.',
            'has_document_id':              'Marque si el estudiante tiene documento de identidad',    
            'nationality':                  'Venezolano (V) o Extranjero (E).',
            'names':                        'Máximo 30 caracteres.',
            'lastnames':                    'Máximo 30 caracteres.',
            'born_date':                    'Selecciona la fecha de nacimiento del estudiante.',
            'gender':                       'Selecciona Femenino o Masculino.',
            'address':                      'Dirección de residencia del estudiante.',
            'home_phone':                   'Número telefónico residencial.',
            'cellphone':                    'Número telefónico personal.',
            'email':                        'Correo electrónico del estudiante.',
            'allergies':                    'Indique las alergias del estudiante. Dejar en blanco si no tiene o se desconocen.', 
            'regular_medical_treatment':    'Indique si el estudiante toma tratamiento médico regular. Dejar en blanco en caso contrario.', 
            'medical_report':               'Indique datos del informe médico del estudiante. Dejar en blanco en caso contrario'
        }
        widgets = {
            'document_id': forms.TextInput(attrs={
                'placeholder': 'Ej: 1234567',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'has_document_id': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
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
            }),                        
            'allergies': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Ej: Alergia a los AINES',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),    
            'regular_medical_treatment': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Ej: Broncodilatadores',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),     
            'medical_report': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Ej: Diagnóstico de asma',
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

    #  --- lógica para document_id y has_document_id (en el clean() general) ---
    def clean(self):
        cleaned_data = super().clean() # <--- LLAMA AL CLEAN ORIGINAL
        
        document_id = cleaned_data.get('document_id')
        has_document_id = cleaned_data.get('has_document_id') 

        if has_document_id:
            if not document_id:
                raise ValidationError('Debe ingresar la cédula o pasaporte del estudiante si marcó que tiene uno.')
            elif document_id.upper() == 'N/A':
                raise ValidationError('El documento de identidad no puede ser N/A si marcó que el estudiante tiene uno.')
            else: # Verificar unicidad si tiene Cédula y no es 'N/A'
                # Excluye el estudiante actual si estás en un formulario de edición
                # Para un formulario de creación, esto simplemente busca si existe otro
                if self.instance and self.instance.pk: # Si es un formulario de edición
                    if Student.objects.filter(document_id=document_id).exclude(pk=self.instance.pk).exists():
                        raise ValidationError('Ya existe un estudiante con este número de documento. Debe ser único.')
                else:  # Si es un formulario de creación
                    if Student.objects.filter(document_id=document_id).exists():
                        raise ValidationError('Ya existe un estudiante con este número de documento.')
                    elif not (7 <= len(document_id) <= 8):
                        raise ValidationError('La cédula no cumple con el formato esperado.')
        else:
            cleaned_data['document_id'] = 'N/A'
            
        return cleaned_data # Siempre devuelve los datos limpios    

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

class AcademicSocioeconomicDataForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'academic_institution_name', 'academic_institution_address', 'academic_degree', 'academic_institution_type', 'housing_type', 'housing_condition', 'number_people_living_housing'
        ]
        labels = {
            'academic_institution_name':    'Nombre del plantel', 
            'academic_institution_address': 'Dirección del plantel', 
            'academic_degree':              'Grado/Año', 
            'academic_institution_type':    'Tipo de plantel', 
            'housing_type':                 'Tipo de vivienda', 
            'housing_condition':            'La vivienda es', 
            'number_people_living_housing': 'N° de personas que viven en el hogar', 
        }
        help_texts = {
            'academic_institution_name':    'Nombre del Plantel Educativo', 
            'academic_institution_address': 'Dirección del Plantel Educativo.', 
            'academic_degree':              'Grado académico', 
            'academic_institution_type':    'Tipo de Plantel (Privado, Mixto, etc.)', 
            'housing_type':                 'Tipo de Vivienda (Casa, Edificio, Apartamento, Quinta, etc.)', 
            'housing_condition':            'Estado de la Vivienda (Propia, Alquilada, etc.)', 
            'number_people_living_housing': 'Cantidad de personas que habitan en la Vivienda', 
        }
        widgets = {
            
            'academic_institution_name': forms.TextInput(attrs={
                'placeholder': 'Ej: U.E. Colegio Integral',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'academic_institution_address': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Ej: Calle Principal, Edificio #10',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),            
            'academic_degree': forms.TextInput(attrs={
                'placeholder': 'Ej: 5to grado',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),          
            'academic_institution_type': forms.TextInput(attrs={
                'placeholder': 'Ej: Privado',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),       
            'housing_type': forms.TextInput(attrs={
                'placeholder': 'Ej: Apartamento',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),       
            'housing_condition': forms.TextInput(attrs={
                'placeholder': 'Ej: Alquilado',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),     
            'number_people_living_housing': forms.NumberInput(attrs={
                'placeholder': 'Ej: 4',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            })
        }
    
    def clean_number_people_living_housing(self):
        number_people_living_housing = self.cleaned_data.get('number_people_living_housing')
        if number_people_living_housing < 1:
            raise ValidationError('Debe indicar un valor válido de personas que residen en el hogar.')
        return number_people_living_housing
    
class LegalParentDataForm(forms.ModelForm):
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
        model = StudentRelative
        fields = [ 'relationship', 'fullname', 'born_date', 'marital_status', 'document_id', 'nationality',  'marital_status', 'profession', 'address', 'home_phone', 'cellphone',  'email', 'workplace', 'job_title', 'office_phone' ]

        labels = {
            'relationship':   'Parentesco',
            'fullname':       'Nombre completo',
            'born_date':      'Fecha de Nacimiento',
            'marital_status': 'Estado Civil',
            'document_id':    'Cédula',
            'nationality':    'Nacionalidad',
            'profession':     'Profesión',
            'address':        'Dirección',
            'home_phone':     'Teléfono de Habitación', 
            'cellphone':      'Teléfono Celular', 
            'email':          'Correo Electrónico',
            'workplace':      'Lugar de Trabajo',
            'job_title':      'Cargo',
            'office_phone':   'Teléfono de Oficina',
        }
        help_texts = {
            'relationship':   'Parentesco',
            'fullname':       'Máximo 60 caracteres',
            'born_date':      'Selecciona la fecha de nacimiento del representante',
            'marital_status': 'Seleccione el estado civil.',
            'document_id':    'Cédula sin puntos ni espacios',
            'nationality':    'Venezolano (V) o Extranjero (E).',
            'profession':     'Profesión u Oficio del representante',
            'address':        'Dirección de Habitación (solo si es diferente a la del beneficiario).',
            'home_phone':     'Teléfono de Habitación (solo si es diferente a la del beneficiario).', 
            'cellphone':      'Número telefónico personal', 
            'email':          'Correo Electrónico',
            'workplace':      'Lugar de Trabajo',
            'job_title':      'Cargo de trabajo (si aplica)',
            'office_phone':   'Teléfono de Oficina (si aplica)'
        }
        widgets = {
            'relationship': forms.TextInput(attrs={
                'placeholder': 'Ej: Madre',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'fullname': forms.TextInput(attrs={
                'placeholder': 'Ej: Sandra Pérez',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'born_date':   forms.DateInput(attrs={
                'type': 'date',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),   
            'marital_status': forms.Select(attrs={
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'document_id': forms.TextInput(attrs={
                'placeholder': 'Ej: 1234567',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'nationality': forms.Select(attrs={
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
            'profession': forms.TextInput(attrs={
                'placeholder': 'Ej: Licenciado en Educación',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),          
            'workplace': forms.TextInput(attrs={
                'placeholder': 'Ej: Colegio Integral',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),          
            'job_title': forms.TextInput(attrs={
                'placeholder': 'Ej: Profesor Contratado',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),            
            'office_phone': forms.TextInput(attrs={
                'placeholder': 'Ej: 04121234567',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
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
        if not (7 <= len(document_id) <= 8):
            raise ValidationError('El ID del documento debe tener entre 7 y 8 caracteres.')
        return document_id

    def clean_born_date(self):
        born_date = self.cleaned_data.get('born_date')
        if born_date:
            today = timezone.now().date()
            min_born_date = today - timezone.timedelta(days=18 * 365.25)
            if born_date > min_born_date:
                raise ValidationError('El representante legal debe ser mayor de 18 años.')
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

    def clean_office(self):
        office_phone = self.cleaned_data.get('office_phone')
        if office_phone and not re.fullmatch(r'^\d{11}$', office_phone):
            raise ValidationError('El número de celular debe tener 11 dígitos.')
        return office_phone
        

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = [ 'fullname', 'relationship', 'cellphone']
        
        labels = {
            'fullname':     'Nombre Completo',
            'relationship': 'Parentesco',
            'cellphone':    'Teléfono'
        }
        help_texts = {
            'fullname':     'Ingrese el nombre completo del contacto de emergencia',
            'relationship': 'Ingrese el parentesco',
            'cellphone':    'Ingrese solo números sin guiones ni espacios'
        }
        widgets = {
            'fullname': forms.TextInput(attrs={
                'placeholder': 'Ej: Nombre completo',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'relationship': forms.TextInput(attrs={
                'placeholder': 'Ej: Abuelo',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            }),
            'cellphone': forms.TextInput(attrs={
                'placeholder': 'Ej: 04120000000',
                'class': 'block w-full rounded-md border-1 py-1.5 px-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-500 focus:ring-3 focus:ring-inset focus:ring-indigo-400 sm:text-sm sm:leading-6'
            })
        }

    def cellphone(self):
        cellphone = self.cleaned_data.get('cellphone')
        if cellphone and not re.fullmatch(r'^\d{11}$', cellphone):
            raise ValidationError('El número de teléfono debe tener 11 dígitos.')
        return cellphone


# Create a formset for 3 emergency contacts
EmergencyContactFormSet = formset_factory(EmergencyContactForm, extra=0, min_num=3, validate_min=True)