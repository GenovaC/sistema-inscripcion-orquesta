from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from .models import Student
from datetime import date

@login_required
def create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student = form.save(commit=False)
            new_student.save()
            return redirect(reverse('students:list')) 
    else:
        form = StudentForm()
    return render(request, 'students/student_create.html', {'form': form})


@login_required
def list(request):
    students = Student.objects.all()
    all_students_count = Student.objects.count()
    venezuelan_students_count = Student.objects.filter(nationality='V').count()
    foreigners_students_count = all_students_count - venezuelan_students_count
    
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