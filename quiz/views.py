from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import  LoginView
from django.contrib.auth import logout

from .forms  import LoginForm


class Login(LoginView):
    form_class = LoginForm
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    print(f'user: {request.user.is_authenticated}')
    if request.user.is_authenticated:
        return render(request, 'base.html')

    return redirect('login')