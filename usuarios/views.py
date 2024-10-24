from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms  import CadastroUsuarioForm, EsqueceuForm


class Cadastro(CreateView):
    form_class = CadastroUsuarioForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/cadastro.html'


def esqueceu(request):
    form = EsqueceuForm()
    context = {
        'form': form
    }
    return render(request, 'usuarios/esqueceu.html', context=context)
