from django.shortcuts import render

from .forms  import LoginForm


def login(request):
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'login.html', context=context)


def home(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')

    return login(request)