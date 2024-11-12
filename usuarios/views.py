from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import CadastroUsuarioForm, EsqueceuForm, CustomAuthenticationForm


class CadastroView(SuccessMessageMixin, CreateView):
    form_class = CadastroUsuarioForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/cadastro.html'
    success_message = 'Cadastro finalizado com sucesso'


def esqueceu(request):
    form = EsqueceuForm()
    context = {
        'form': form
    }
    return render(request, 'usuarios/esqueceu.html', context=context)


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('home')
