from django.urls import path
from . import views


urlpatterns = [
    path('instruments/', views.list, name='list'),
    #path('instruments/create', views.create, name='new'),
]
