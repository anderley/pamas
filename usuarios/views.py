from django.shortcuts import render

from .forms  import CadastroUsuarioForm, EsqueceuForm


def cadastro(request):
    form = CadastroUsuarioForm()
    context = {
        'form': form
    }
    return render(request, 'cadastro.html', context=context)


def esqueceu(request):
    form = EsqueceuForm()
    context = {
        'form': form
    }
    return render(request, 'esqueceu.html', context=context)
