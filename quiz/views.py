from django.shortcuts import render, redirect
from django.contrib.auth.views import  LoginView
from django.contrib.auth import logout
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import  settings
from django.contrib.auth.decorators import login_required, login_not_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from request_token.decorators import use_request_token
from request_token.models import RequestToken

from .forms  import (
    LoginForm,
    EnviarFormularioForm
)
from .models import (
    Perguntas,
    FomularioClientes,
)
from .decorators import use_request_token_check_expiration


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(redirect_field_name='login')
def home(request):
    return render(request, 'base.html')


@login_required(redirect_field_name='login')
def enviar_formulario(request):
    form = EnviarFormularioForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form = EnviarFormularioForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            request_token = RequestToken.objects.create_token(
                scope='mentorado',
                login_mode=RequestToken.LOGIN_MODE_NONE,
                data={
                    'user_id': request.user.id,
                    'client_email': email
                }
            )
            token = request_token.jwt()
            url = f'http://localhost:8000/formulario/?rt={token}'
            subject = '[PAMAS] Formulário'
            message = f'Segue o <a href="{url}">link</a> do formulário para preenchimento'
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])

                messages.success(request, 'Email enviado coom sucesso!')
                
                FomularioClientes(
                    user=request.user,
                    email=email,
                    token=token,
                    form_url=url
                ).save()
            except Exception as e:
                messages.error(request, f'Error no envio do email: {e}')

    return render(request, 'quiz/send_form.html', context=context)


@login_required(redirect_field_name='login')
def cancelar_form(request, id):
    form_client = FomularioClientes.objects.get(id=id)

    if form_client:
        form_client.status = 'Cancelado'
        form_client.save()

        messages.success(request, 'Formulário Cancelado com sucesso')

    return redirect('list_sent_form')


class Login(LoginView):
    form_class = LoginForm
    template_name = 'quiz/login.html'


class ShowForm(ListView):
    model = Perguntas
    paginate_by = 20
    template_name = 'quiz/show_form.html'

    @login_not_required
    @use_request_token_check_expiration
    @use_request_token(scope='mentorado')
    def get(self, request, *args, **kwargs):
        client_email = (
            request.token.data['client_email']
            if hasattr(request, 'token')
            else None
        )
        if not client_email:
            
            return render(request, '403.html')
        return super().get(request, *args, **kwargs)


class ListSentForm(LoginRequiredMixin, ListView):
    model = FomularioClientes
    paginate_by = 50
    template_name = 'quiz/list_sent_form.html'
    redirect_field_name = 'login'
