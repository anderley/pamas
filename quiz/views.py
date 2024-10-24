from django.shortcuts import render, redirect
from django.contrib.auth.views import  LoginView
from django.contrib.auth import logout
from django.views.generic import ListView

from .forms  import (
    LoginForm,
    EnviarFormularioForm
)
from .models import Perguntas


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    user = request.user

    if user.is_authenticated and not user.is_superuser:
        return render(request, 'base.html')

    return redirect('login')


def enviar_formulario(request):
    form = EnviarFormularioForm()
    context = {
        'form': form
    }
    return render(request, 'quiz/send_form.html', context=context)


class Login(LoginView):
    form_class = LoginForm
    template_name = 'quiz/login.html'


class  Show(ListView):
    model = Perguntas
    paginate_by = 20
    template_name = 'quiz/show_form.html'
