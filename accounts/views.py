from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django import forms
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label = "",
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo institucional',
            'required': 'required'
        })
    )
    password = forms.CharField(
        label = "",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'required': 'required'
        })
    )

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard:home')  

def profile(request):
    username = "Génova Castillo"
    return render(request, 'accounts/profile.html', {
        'username': username
    }) 

def signout(request):
    logout(request)
    return redirect('accounts:login')
    

    