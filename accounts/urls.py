from django.urls import path
from .views import CustomLoginView
from . import views


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('signout/', views.signout, name='logout'),
]
