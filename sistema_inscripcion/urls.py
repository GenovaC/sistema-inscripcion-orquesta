"""
URL configuration for sistema_inscripcion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Autenticación y usuarios
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # CRUD de estudientes
    path('students', include(('students.urls', 'students'), namespace='students')),
    
    # Panel de visualización
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')), 

    # CRUD de instrumentos
    path('instruments', include(('instruments.urls', 'instruments'), namespace='instruments')),

    # CRUD de proyectos orquestales
    path('orchestral_projects', include(('orchestral_projects.urls', 'orchestral_projects'), namespace='orchestral_projects')),

]