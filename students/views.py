from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from formtools.wizard.views import SessionWizardView
from .models import Student, EmergencyContact
from academic_period.models import DetailAcademicInscription, AcademicPeriod
from instruments.models import Instrument
from orchestral_projects.models import OrchestralProject
from .forms import PersonalDataForm, AcademicSocioeconomicDataForm, LegalParentDataForm, RelativeDataForm, EmergencyContactForm, EmergencyContactFormSet 
from academic_period.forms import DetailAcademicInscriptionForm
from datetime import date

FORMS = [
    ("personal_data", PersonalDataForm),
    ("inscription_data", DetailAcademicInscriptionForm),
    ("legal_parent_data", LegalParentDataForm),
    ("relative_data", RelativeDataForm),
    ("academic_socioeconomic_data", AcademicSocioeconomicDataForm),
    ("emergency_contact", EmergencyContactFormSet)
]

TEMPLATES = {
    "emergency_contact": "students/student_wizard_form_emergency_contact.html",
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
    
     # --- MÉTODO PARA PASAR DATOS A LOS SELECTORES DEL INSCRIPTION_DATA_TEMPLATE ---
    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        # Si estamos en el paso de inscripción, ajustamos los querysets
        if step == 'inscription_data':
            # Ejemplos de filtros, si llegan a ser necesarios:
            # form.fields['id_orchestral_project'].queryset = OrchestralProject.objects.filter(is_active=True)
            # form.fields['id_instrument'].queryset = Instrument.objects.order_by('name')
            # form.fields['id_academic_period'].queryset = AcademicPeriod.objects.filter(is_current=True)

            # Actualmente solo se obtienen todos los objetos.
            form.fields['id_orchestral_project'].queryset = OrchestralProject.objects.all()
            form.fields['id_instrument'].queryset         = Instrument.objects.all()
            form.fields['id_academic_period'].queryset    = AcademicPeriod.objects.all()

        return form
    
    # Proporciona datos adicionales al contexto de la plantilla que se está renderizando para el paso actual
    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)         # Obtener contexto base de la clase padre
        context['wizard_title'] = "Inscribir nuevo estudiante"
        context['step_titles'] = {
            'inscription_data':            'Datos de Inscripción',
            'personal_data':               'Datos Personales',
            'academic_socioeconomic_data': 'Datos Públicos',
            'legal_parent_data':           'Representante Legal',
            'relative_data':               'Otro familiar',
            'emergency_contact':           'Contactos de Emergencia' 
        }
        return context
    
    def render_next_step(self, form):
        # self.storage.data contiene todos los datos limpios de los pasos anteriores
        # y también información sobre el paso actual y el siguiente.
        
        # Acceder a los datos de los pasos ya completados
        all_collected_data = self.storage.data.get('step_data', {})
        print("\n--- Datos Recopilados al Pasar al Siguiente Paso ---")
        for step_name, cleaned_data_dict in all_collected_data.items(): # <--- CAMBIO AQUÍ
            # cleaned_data_dict es directamente el diccionario de datos
            print(f"Paso: {step_name}")
            print(f"  Datos: {cleaned_data_dict}") # <--- CAMBIO AQUÍ
        print("---------------------------------------------------\n")
        
        return super().render_next_step(form)

    def done(self, form_list, **kwargs):
        # form_list es una lista de los formularios válidos de cada paso
        # Puedes acceder a los datos de cada paso usando get_cleaned_data_for_step()

        # 1. Obtener todos los datos del estudiante 
        student_data = {}
        for step_name in ["personal_data", "academic_socioeconomic_data", "legal_parent_data", "relative_data"]: 
            step_data = self.get_cleaned_data_for_step(step_name)
            if step_data: 
                student_data.update(step_data)
    
        # 2. Eliminar 'age' si existe en los datos recolectados ya que ese dato era solo lectura, no está en el modelo
        # Se debe hacer DESPUÉS de recopilar todos los datos, pero ANTES de crear el Student.
        if 'age' in student_data:
            del student_data['age']

        # 3. Obtener los datos del detalle de inscripción y contactos de emergencia
        detail_inscription_data = self.get_cleaned_data_for_step("inscription_data")
        # emergency_contacts es una lista de diccionarios si el formset es válido
        emergency_contacts_data_list = self.get_cleaned_data_for_step("emergency_contact")

        # 4. Intentar crear AMBOS objetos dentro de un único bloque try-except para manejar la dependencia.
        student_instance = None 
        
        try:
            #5. Crear la instancia del estudiante
            student_instance = Student.objects.create(**student_data)

            #6. Crear la instancia de DetailAcademicInscription SY Y SOLO SI el Student fue creado con éxito
            if detail_inscription_data:
                DetailAcademicInscription.objects.create(id_student=student_instance, **detail_inscription_data)
                
                # 6.1 Crear cada contacto de emergencia asociado al estudiante
                if emergency_contacts_data_list: # Confirmar que hay data
                    for contact_data in emergency_contacts_data_list:
                        # Only create if the form data is not empty (e.g., all fields were filled)
                        # This check is important if you allow less than 3 forms to be submitted (e.g., extra=3, min_num=0)
                        # With min_num=3, all 3 forms are expected to have data if valid.
                        if any(contact_data.values()): # Check if any value in the dict is not empty/None
                            EmergencyContact.objects.create(id_student=student_instance, **contact_data)

        # Este bloque captura errores tanto de la creación del estudiante como de la inscripción.        
        except Exception as e:
            
            print(f"Error during student or inscription creation: {e}")
            import traceback
            traceback.print_exc() # Para depuración detallada

            # Opcional: Si el estudiante se creó pero falló la inscripción,
            # se puede implementar más adelante una distinción en el mensaje de error.
            return render(self.request, 'students/error_saving_student.html', {'error': str(e), 'data': str(e)})

        # Opcional: limpiar los datos del wizard de la sesión/cookies
        self.storage.reset()        

        # 7. Redirigir a una página de éxito
        return redirect(reverse('students:list'))

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