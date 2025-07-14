from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.list, name='list'),
    path('new', login_required(views.StudentWizard.as_view(views.FORMS)), name='new'),
    path('<int:id>', views.detail, name='detail'),
]
