from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

class Student(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('V', 'Venezolano/a'),
        ('E', 'Extranjero/a'),
    ]

    GENDER_CHOICES = [
        ('Femenine', 'Femenino'),
        ('Masculine', 'Masculino'),
    ]

    document_id = models.CharField(
        max_length=8,
        unique=True,  # Asumiendo que el document_id debe ser único
        help_text="Cédula o Pasaporte del estudiante."
    )
    nationality = models.CharField(
        max_length=1,
        choices=DOCUMENT_TYPE_CHOICES,
        help_text="Nacionalidad del estudiante ('V' para Venezolano, 'E' para Extranjero)."
    )
    names = models.CharField(
        max_length=30,
        help_text="Nombres del estudiante."
    )
    lastnames = models.CharField(
        max_length=30,
        help_text="Apellidos del estudiante."
    )
    born_date = models.DateField(
        help_text="Fecha de nacimiento del estudiante (debe tener más de 5 años)."
    )
    gender = models.CharField(
        max_length=10,  # Suficiente para "Femenine" o "Masculine"
        choices=GENDER_CHOICES,
        help_text="Género del estudiante."
    )
    address = models.TextField(
        max_length=300,
        help_text="Dirección del estudiante (máximo 300 caracteres)."
    )
    home_phone = models.CharField(
        max_length=11,
        blank=True,  # Permite que el campo esté en blanco en el formulario
        null=True,   # Permite que el campo sea NULL en la base de datos
        help_text="Número de teléfono de casa."
    )
    cellphone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        help_text="Número de teléfono celular."
    )
    email = models.EmailField(
        max_length=50,
       # unique=True,  # Asumiendo que el email debe ser único
        help_text="Correo electrónico del estudiante."
    )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"

    def clean(self):
        super().clean()

        # Validación para document_id:
        if not (3 <= len(self.document_id) <= 8):
            raise ValidationError({'document_id': 'El ID del documento debe tener entre 3 y 8 caracteres.'})

        # Validación para born_date:
        today = timezone.now().date()
        min_born_date = today - timezone.timedelta(days=5 * 365.25)  # Aproximación de 5 años
        if self.born_date and self.born_date > min_born_date:
            raise ValidationError({'born_date': 'El estudiante debe tener más de 5 años.'})

        # Validación para home_phone y cellphone (si no son nulos):
        if self.home_phone and not re.fullmatch(r'^\d{11}$', self.home_phone):
            raise ValidationError({'home_phone': 'El número de teléfono de casa debe ser una cadena de 11 dígitos numéricos.'})
        if self.cellphone and not re.fullmatch(r'^\d{11}$', self.cellphone):
            raise ValidationError({'cellphone': 'El número de celular debe ser una cadena de 11 dígitos numéricos.'})

    def __str__(self):
        return f"{self.names} {self.lastnames} ({self.document_id})"