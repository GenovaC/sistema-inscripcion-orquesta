from django.urls import path
from . import views


urlpatterns = [
    path('', views.list, name='list'),
    #path('create', views.create, name='new'),
]
