from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import StudentForm
from .models import Student

@login_required
def create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student = form.save(commit=False)
            new_student.save()
            return redirect(reverse('students:new')) 
    else:
        form = StudentForm()
    return render(request, 'students/create_student.html', {'form': form})