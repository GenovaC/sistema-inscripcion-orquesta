from django.contrib import admin
from .models import Student, EmergencyContact, StudentRelative

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentRelative)
admin.site.register(EmergencyContact)