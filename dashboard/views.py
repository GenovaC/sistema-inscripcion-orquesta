from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home_dashboard(request):
    return render(request, 'dashboard/home.html')