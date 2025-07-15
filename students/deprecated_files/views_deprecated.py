from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Student
from django.forms import formsets
from formtools.wizard.views import SessionWizardView
from .forms import PersonalDataForm, AcademicSocioeconomicDataForm, LegalParentDataForm, RelativeDataForm
from academic_period.forms import DetailAcademicInscription
from datetime import date
from django import forms

FORMS = [
    ("inscription_data", DetailAcademicInscription),
    ("personal_data", PersonalDataForm),
    ("legal_parent_data", LegalParentDataForm),
    ("relative_data", RelativeDataForm),
    ("academic_socioeconomic_data", AcademicSocioeconomicDataForm),
]

TEMPLATES = {
    "inscription_data": "students/student_wizard_form_inscription_data.html",
    "personal_data": "students/student_wizard_form_personal_data.html",
    "academic_socioeconomic_data": "students/student_wizard_form_academic_data.html",
    "legal_parent_data": "students/student_wizard_form_legal_parent_data.html",
    "relative_data": "students/student_wizard_form_relative_data.html",
}

class StudentWizard(SessionWizardView):

    # Para determinar qué plantilla HTML se debe renderizar para el paso actual del formulario.
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]      
    
    # Proporciona datos adicionales al contexto de la plantilla que se está renderizando para el paso actual
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)         # Obtener contexto base de la clase padre
        context['wizard_title'] = "Inscribir nuevo estudiante"
        context['step_titles'] = {
            'inscription_data': 'Datos de Inscripción',
            'personal_data': 'Datos Personales',
            'academic_socioeconomic_data': 'Datos Académicos y Socioeconómicos',
            'legal_parent_data': 'Representante Legal',
            'relative_data': 'Otro familiar'
        }
        return context
    
    #Para pasar argumentos adicionales al constructor de cada formulario en cada paso
    # Importante: La instancia del modelo se comparte en los formularios.
    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        # Se verifica si ya existe un atributo instance en la vista del wizard. 
        # Si no existe (como la primera vez que carga el wizard), se crea una nueva instancia vacía del modelo Student        
        if not hasattr(self, 'instance'):
            self.instance = Student()

        # Si ya existe (en pasos siguientes), se reutiliza la misma instancia.
        # La instancia del Student (nueva o existente) se pasa como el argumento 'instance' a cada ModelForm en cada paso.
        kwargs['instance'] = self.instance      
        return kwargs

    # Este método es invocado cuando se completan todos los pasos del wizard y el último formulario ha sido validado.
    # form_list es una lista de todas las instancias de formulario, en orden, de cada paso del wizard. 
    # Cada formulario en esta lista ya ha pasado su propia validación de formulario.
    def done(self, form_list, **kwargs):
        new_student = self.instance     # Recupera la instancia del modelo Student que se ha estado construyendo        
        
        for form in form_list:
            # Asegura que todos los cleaned_data de cada formulario se copian explícitamente a la instancia final
            # Se excluye la edad porque no es un dato del modelo 'Student'.
            for field_name, value in form.cleaned_data.items():
                if hasattr(new_student, field_name) and field_name != 'age':
                    setattr(new_student, field_name, value)

        try:
            new_student.full_clean()   # Crítico. ejecuta todas las validaciones definidas a nivel del modelo 
            new_student.save()
            
            return redirect(reverse('students:list'))
            
        except Exception as e:
            print(f"Error saving student: {e}")
            import traceback
            traceback.print_exc() # For detailed debugging
            # Falta definir cómo gestionar el error
            return render(self.request, 'students/error_saving_student.html', {'error': str(e), 'data': new_student.__dict__})

@login_required
def list(request):
    students = Student.objects.all()
    all_students_count = Student.objects.count()
    venezuelan_students_count = Student.objects.filter(nationality='V').count()
    foreigners_students_count = Student.objects.filter(nationality='E').count()
    
    return render(request, 'students/student_list.html', {
        'students': students,
        'all_students': all_students_count,
        'venezuelan_students': venezuelan_students_count,
        'foreigners_students': foreigners_students_count
    })

@login_required
def detail(request, id):
    student = get_object_or_404(Student, id=id)

    # Calcular la edad
    today = date.today()
    born = student.born_date
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    student.calculated_age = age

    return render(request, 'students/student_detail.html', {'student': student}) 