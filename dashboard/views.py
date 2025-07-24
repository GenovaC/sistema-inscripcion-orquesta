from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Q
from instruments.models import Instrument
from academic_period.models import AcademicPeriod, DetailAcademicInscription
from students.models import Student

@login_required
def home_dashboard(request):

    current_academic_period = AcademicPeriod.objects.filter(is_active=True).first()
    
    total_by_category = DetailAcademicInscription.objects.filter(
        id_academic_period__is_active=True
    ).aggregate(
        wind       = Count('id', filter=Q(id_instrument__category='Wind')),
        string     = Count('id', filter=Q(id_instrument__category='String')),
        percussion = Count('id', filter=Q(id_instrument__category='Percussion')),
        all        = Count('id')
    )

    # Acceso a los resultados
    wind_students       = total_by_category['wind']
    string_students     = total_by_category['string']
    percussion_students = total_by_category['percussion']
    all_students        = total_by_category['all']

    return render(request, 'dashboard/home.html', {
        'wind_students':           wind_students,
        'string_students':         string_students,
        'percussion_students':     percussion_students,
        'current_academic_period': current_academic_period,
        'all_students':            all_students
    })
