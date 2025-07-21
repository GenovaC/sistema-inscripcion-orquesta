from django.db import models

# Create your models here.
class Instrument(models.Model):

    CATEGORY_CHOICES = [
        ('Wind',       'Viento'),
        ('String',     'Cuerdas'),
        ('Percussion', 'Percusión'),
        ('Other',      'Otros'),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
