from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.conf import settings
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import CadastroUsuarioForm, EsqueceuForm, CustomAuthenticationForm


class CadastroView(SuccessMessageMixin, CreateView):
    form_class = CadastroUsuarioForm
    success_url = reverse_lazy('login')
    template_name = 'usuarios/cadastro.html'
    success_message = 'Cadastro finalizado com sucesso'


def password_reset_request(request):
    form = EsqueceuForm()
    if request.method == "POST":
        email = request.POST.get("email")
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Redefinição de Senha"
                email_template_name = "emails/password_reset_email.txt"
                context = {
                    "email": user.email,
                    'domain': settings.SITE_URL,
                    'site_name': 'PAMAS',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user)
                }
                email = render_to_string(email_template_name, context)
                send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email])
            messages.success(request, "Um email foi enviado com instruções para redefinir sua senha.")
            return redirect("esqueceu_usuario")
        else:
            messages.error(request, "Nenhum usuário encontrado com esse email.")
    return render(request, "usuarios/password_reset.html", {'form': form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'usuarios/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'usuarios/password_reset_complete.html'


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('home')

