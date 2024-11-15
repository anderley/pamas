from datetime import datetime, timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, FormView, ListView, TemplateView,
                                  UpdateView)
from pytz import timezone
from request_token.models import RequestToken

from core.utils.email_utils import EmailUtils
from notificacoes.models import Notificacoes

from .decorators import (check_contato, timeout_form,
                         use_request_token_check_expiration)
from .forms import ContatosForm, EnviarFormularioForm, FormularioForm
from .models import Contatos, FomularioClientes, Perguntas


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(redirect_field_name='login')
def home(request):
    return render(request, 'base_site.html')


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
            link_form = f'{settings.SITE_URL}/formulario/instrucoes/?rt={token}' # noqa

            try:
                EmailUtils.send_email_form(email, link_form, request.user)

                FomularioClientes(
                    user=request.user,
                    email=email,
                    token=token,
                    form_url=link_form
                ).save()
                Notificacoes(
                    user=request.user,
                    mensagem=f'Formulario enviado com sucesso para o email: {email}', # noqa
                    tipo=Notificacoes.Tipo.INFORMATIVA
                ).save()

                messages.success(request, 'Email enviado com sucesso!')
            except Exception as e:
                messages.error(request, f'Error no envio do email: {e}')

    return render(request, 'quiz/send_form.html', context=context)


@login_required(redirect_field_name='login')
def cancelar_form(request, id):
    form_cliente = FomularioClientes.objects.get(id=id)

    if form_cliente:
        form_cliente.status = FomularioClientes.Status.CANCELADO
        form_cliente.save()
        Notificacoes(
            user=request.user,
            mensagem=f'Formulario enviado para o email: {form_cliente.email}, foi cancelado', # noqa
            tipo=Notificacoes.Tipo.ALERTA
        ).save()

        messages.success(request, 'Envio cancelado com sucesso')

    return redirect('list_sent_form')


class ContatosCreateView(CreateView):
    form_class = ContatosForm
    template_name = 'quiz/cad_contato.html'

    @use_request_token_check_expiration
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, '404.html')

        token = request.GET['rt']
        form_cliente = FomularioClientes.objects.get(token=token)

        if form_cliente:
            form_cliente.status = FomularioClientes.Status.ACESSADO
            form_cliente.save()

            self.initial['formulario_id'] = form_cliente.id
            self.initial['user_id'] = form_cliente.user.id
            self.initial['email'] = form_cliente.email

            query_contato = Contatos.objects.filter(email=form_cliente.email)

            if query_contato.exists():
                contato = query_contato.get()
                request.session['formulario_id'] = form_cliente.id

                return redirect('formulario_cadastro_editar', contato.pk)

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('formulario', kwargs={
            'pk': self.initial['formulario_id']
        })


class ContatosUpdateView(UpdateView):
    form_class = ContatosForm
    model = Contatos
    template_name = 'quiz/cad_contato.html'

    def get_success_url(self):
        if self.request.user.is_authenticated:
            redirect(self.request, '404.html')

        return reverse_lazy('formulario', kwargs={
            'pk': self.request.session['formulario_id']
        })


class FormularioFormView(FormView):
    form_class = FormularioForm
    template_name = 'quiz/show_form.html'

    @timeout_form
    @check_contato
    def get(self, request, pk, *args, **kwargs):
        page = request.GET['page'] if 'page' in request.GET else 1
        page = page if page and int(page) > 0 else 1
        form_cliente = FomularioClientes.objects.get(id=pk)

        if (
            form_cliente
            and form_cliente.status in [
                FomularioClientes.Status.ENVIADO,
                FomularioClientes.Status.ACESSADO
            ]
        ):
            form_cliente.status = FomularioClientes.Status.PREENCHENDO
            form_cliente.iniciado = datetime.now()
            form_cliente.save()
            data_envio = form_cliente.created_at.strftime(settings.DATE_FORMAT_DEFAULT) # noqa
            Notificacoes(
                user=form_cliente.user,
                mensagem=f'Formulario enviado para o email: {form_cliente.email} na data {data_envio}, iniciou o preenchimento',  # noqa
                tipo=Notificacoes.Tipo.INFORMATIVA
            ).save()

        pagination = Paginator(
            Perguntas.objects.filter(ativo=True).order_by('id').all(),
            20
        )
        timeout = form_cliente.iniciado + timedelta(minutes=settings.TIMEOUT_FORMULARIO) # noqa
        tz_sao_paulo = timezone('America/Sao_Paulo')
        self.initial['formulario_id'] = pk
        self.initial['timeout'] = timeout.astimezone(tz_sao_paulo).isoformat()
        self.initial['paginator'] = pagination
        self.initial['page_obj'] = pagination.page(page)

        return super().get(request, *args, **kwargs)

    @timeout_form
    def post(self, request, pk, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.success_url = request.get_full_path()
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(**self.initial)

        return context


class ListSentFormsView(LoginRequiredMixin, ListView):
    model = FomularioClientes
    paginate_by = 50
    template_name = 'quiz/list_sent_form.html'
    redirect_field_name = 'login'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class PdfFaceTemplateView(TemplateView):
    template_name = 'quiz/pdf/face.html'


class PdfPagesTemplateView(TemplateView):
    template_name = 'quiz/pdf/pages.html'


class InstrucoesTemplateView(TemplateView):
    template_name = 'quiz/instrucoes.html'
