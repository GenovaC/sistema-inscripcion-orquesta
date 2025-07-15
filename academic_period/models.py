from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class AcademicPeriod(models.Model):
    first_year = models.PositiveIntegerField()
    final_year = models.PositiveIntegerField()

    def clean(self):
        if self.final_year != self.first_year + 1:
            raise ValidationError("El año final debe ser exactamente un año mayor que el año inicial.")

    def __str__(self):
        return f"{self.first_year}-{self.final_year}"

    class Meta:
        verbose_name = "Período Académico"
        verbose_name_plural = "Períodos Académicos"
        ordering = ["-first_year"]


class DetailAcademicInscription(models.Model):
    TYPE_CHOICES = [
        ('New admission', 'Nuevo ingreso'),
        ('Re-entry', 'Reingreso'),
        ('Data update', 'Actualización de datos'),
        ('Re-enrollment', 'Reinscripción regular'),
    ]

    id_student            = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    id_orchestral_project = models.ForeignKey('orchestral_projects.OrchestralProject', on_delete=models.CASCADE)
    id_instrument         = models.ForeignKey('instruments.Instrument', on_delete=models.CASCADE)
    id_academic_period    = models.ForeignKey('academic_period.AcademicPeriod', on_delete=models.CASCADE)
    inscription_date      = models.DateField()
    type                  = models.CharField(max_length=30, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Detalle de Inscripción Académica"
        verbose_name_plural = "Detalles de Inscripción Académica"
        #unique_together es porque un estudiante no puede estar inscrito 2 veces en el mismo período académico 
        unique_together = ('id_student', 'id_academic_period')
        ordering = ['-inscription_date']

    def clean(self):
        super().clean()
        
        # Validación: fecha no puede ser futura
        if self.inscription_date > timezone.now().date():
            raise ValidationError("La fecha de inscripción no puede ser futura.")
        
        # Validación: tipo debe estar en las opciones (redundante si usas choices)
        if self.type not in dict(self.TYPE_CHOICES):
            raise ValidationError("Tipo de inscripción inválido.")

    def __str__(self):
        return f"{self.id_student} - {self.id_academic_period} ({self.type})"

