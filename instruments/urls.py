from django.urls import path
from . import views


urlpatterns = [
    path('/', views.list, name='list'),
    #path('instruments/create', views.create, name='new'),
]
