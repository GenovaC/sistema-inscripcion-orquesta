from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import OrchestralProjectForm
from .models import OrchestralProject


@login_required
def list(request):
    projects = OrchestralProject.objects.all()
    
    if request.method == 'GET':
        return render(request, 'orchestral_projects/orchestral_projects_list.html', {
            'form': OrchestralProjectForm,
            'projects': projects
        }) 
    else:
        try:
            form = OrchestralProjectForm(request.POST)
            new_project = form.save(commit=False)
            new_project.save()
            return redirect(reverse('orchestral_projects:list'))
        except ValueError:
            return render(request, 'orchestral_projects/orchestral_projects_list.html', {
                'form': OrchestralProjectForm,
                'error': 'Ha habido un error al registrar el nuevo proyecto.'
            }) 

