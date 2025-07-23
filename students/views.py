from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from formtools.wizard.views import SessionWizardView
from .models import Student, EmergencyContact, StudentRelative
from academic_period.models import DetailAcademicInscription, AcademicPeriod
from instruments.models import Instrument
from orchestral_projects.models import OrchestralProject
from .forms import PersonalDataForm, AcademicSocioeconomicDataForm, LegalParentDataForm, EmergencyContactForm, EmergencyContactFormSet 
from academic_period.forms import DetailAcademicInscriptionForm
from .utils import calculate_age

FORMS = [
    ("personal_data", PersonalDataForm),
    ("inscription_data", DetailAcademicInscriptionForm),
    ("legal_parent_data", LegalParentDataForm),
    ("relative_data", LegalParentDataForm),
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

    # Esta función determina qué template HTML se debe renderizar para el paso actual del formulario.
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]      
    
    # Método para inyectar un atributo adicional/temporal a un step, para luego usarlo en el formulario
    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == 'relative_data':  
            legal_parent_data = self.get_cleaned_data_for_step('legal_parent_data')
            dni_legal_parent = legal_parent_data.get('document_id')
            kwargs['document_id_legal_parent'] = dni_legal_parent
        
        return kwargs

    # --- MÉTODO PARA PASAR DATOS A LOS SELECTORES DEL INSCRIPTION_DATA_TEMPLATE ---
    def get_form(self, step=None, data=None, files=None):
        form = super().get_form(step, data, files)

        # Si estamos en el paso de inscripción, ajustamos los querysets
        if step == 'inscription_data':
            # Ejemplos de filtros adicionales por si llegan a ser necesarios más adelante:
            # form.fields['id_academic_period'].queryset = AcademicPeriod.objects.filter(is_current=True)

            # Actualmente solo se obtienen todos los objetos.
            form.fields['id_orchestral_project'].queryset = OrchestralProject.objects.all()
            form.fields['id_instrument'].queryset         = Instrument.objects.all()
            form.fields['id_academic_period'].queryset    = AcademicPeriod.objects.all()

        return form
    
    # Método que proporciona datos adicionales al contexto de la plantilla que se está renderizando para el paso actual
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
    
    # Método para imprimir en consola lo que se va recopilando al pasar cada step. Solo es informativo.
    def render_next_step(self, form):
        # contiene todos los datos limpios de los pasos anteriores, también información sobre el paso actual y el siguiente.        

        # Acceder a los datos de los pasos ya completados
        all_collected_data = self.storage.data.get('step_data', {})
        print("\n--- Datos Recopilados al Pasar al Siguiente Paso ---")
        for step_name, cleaned_data_dict in all_collected_data.items(): 
            # cleaned_data_dict es directamente el diccionario de datos
            print(f"Paso: {step_name}")
            print(f"  Datos: {cleaned_data_dict}") 
        print("---------------------------------------------------\n")
        
        return super().render_next_step(form)

    # Método para guardar el estudiante, se llama al completar todo el formulario wizard
    def done(self, form_list, **kwargs):
        # form_list es una lista de los formularios válidos de cada paso, no se usa porque hay 
        # formularios de distintas entidades por lo que se requiere un tratamiento distinto.
        # Para acceder a los datos de cada paso se usa: get_cleaned_data_for_step()

        # 1. Obtener todos los datos del estudiante 
        student_data = {}
        for step_name in ["personal_data", "academic_socioeconomic_data"]: 
            step_data = self.get_cleaned_data_for_step(step_name)
            if step_data: 
                student_data.update(step_data)
    
        # 2. Eliminar 'age' si existe en los datos recolectados ya que ese dato era solo lectura, no está en el modelo
        # Se debe hacer DESPUÉS de recopilar todos los datos, pero ANTES de crear el Student.
        if 'age' in student_data:
            del student_data['age']

        # 3. Obtener los datos del detalle de inscripción, familiares y contactos de emergencia
        detail_inscription_data = self.get_cleaned_data_for_step("inscription_data")

        legal_parent_data = self.get_cleaned_data_for_step("legal_parent_data")
        if 'age' in legal_parent_data:
            del legal_parent_data['age']

        relative_data = self.get_cleaned_data_for_step("relative_data")        
        if 'age' in relative_data:
            del relative_data['age']

        emergency_contacts_data_list = self.get_cleaned_data_for_step("emergency_contact") # emergency_contacts es una lista de diccionarios si el formset es válido

        # 4. Intentar crear los objetos dentro de un único bloque try-except para manejar la dependencia.
        student_instance = None 
        
        try:

            # Usar una transacción para asegurar la atomicidad de la operación.  
            # Si ocurre un error en cualquier punto dentro de este bloque todas las operaciones de base de datos 
            # realizadas dentro de la transacción se revertirán. O se guarda todo correctamente, o no se guarda nada.
            with transaction.atomic():

                # 5. Crear los familiares
                # Crear el representante legal o actualizar el registro por document_id si ya existe
                legal_parent_instance, created_legal = StudentRelative.objects.update_or_create(
                    document_id = legal_parent_data['document_id'],
                    defaults = legal_parent_data
                )

                print(f"\n --------- Representante Legal {'creado' if created_legal else 'actualizado'}: {legal_parent_instance}")

                # Crear el familiar o actualizar el registro por document_id si ya existe
                relative_instance, created_relative = StudentRelative.objects.update_or_create(
                    document_id = relative_data['document_id'],
                    defaults = relative_data
                )

                print(f"\n --------- Familiar {'creado' if created_relative else 'actualizado'}: {relative_instance}")

                # 5.1 Asignar las instancias de familiares a los datos del estudiante
                student_data['id_legal_parent'] = legal_parent_instance
                student_data['id_relative'] = relative_instance

                #6. Crear la instancia del estudiante
                student_instance = Student.objects.create(**student_data)
                print(f"\n --------- Estudiante creado: {student_instance}")

                #7. Crear la instancia de DetailAcademicInscription 
                if detail_inscription_data:
                    DetailAcademicInscription.objects.create(id_student=student_instance, **detail_inscription_data)
                    
                    # 7.1 Crear cada contacto de emergencia asociado al estudiante
                    if emergency_contacts_data_list: 
                        for contact_data in emergency_contacts_data_list:
                             # Asegurar de que el diccionario no esté vacío antes de crear
                            if any(contact_data.values()): 
                                EmergencyContact.objects.create(id_student=student_instance, **contact_data)

            # Opcional: limpiar los datos del wizard de la sesión/cookies
            self.storage.reset()        

            # 8. Redirigir a una página de éxito
            return redirect(reverse('students:list'))
        
        # 9. Este bloque captura errores de la creación del estudiante, de la inscripción y/o los familiares       
        except Exception as e:
            
            print(f"Error durante la creación del estudiante: {e}")
            import traceback
            traceback.print_exc() # Para depuración detallada

            # Opcional: Si el estudiante se creó pero falló la inscripción,
            # se puede implementar más adelante una distinción en el mensaje de error.
            return render(self.request, 'students/error_saving_student.html', {'error': str(e), 'data': str(e)})

        

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
    legal_parent = student.id_legal_parent  # Esto es una instancia de StudentRelative
    relative = student.id_relative          # También es una instancia de StudentRelative
    inscriptions = DetailAcademicInscription.objects.filter(id_student=student)
    emergency_contacts = EmergencyContact.objects.filter(id_student=student)

    # Calcular las edades
    student.calculated_age = calculate_age(student.born_date)
    legal_parent.calculated_age = calculate_age(legal_parent.born_date)
    relative.calculated_age = calculate_age(relative.born_date)

    return render(request, 'students/student_detail.html', {
        'student':            student,
        'legal_parent':       legal_parent,
        'relative':           relative,
        'inscriptions':       inscriptions,
        'emergency_contacts': emergency_contacts
    }) 