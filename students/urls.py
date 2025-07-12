from django.urls import path
from . import views


urlpatterns = [
    path('/create', views.create, name='new'),
    path('/list', views.list, name='list'),
    path('/<int:id>', views.detail, name='detail'),
]
