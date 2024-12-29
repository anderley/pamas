import os
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import (CreateView, FormView, ListView, TemplateView,
                                  UpdateView)
from django_weasyprint import WeasyTemplateResponseMixin
from pytz import timezone
from request_token.models import RequestToken
from weasyprint import HTML

from core.utils.email_utils import EmailUtils
from notificacoes.models import Notificacoes

from .decorators import (check_contato, timeout_form,
                         use_request_token_check_expiration)
from .forms import ContatosForm, EnviarFormularioForm, FormularioForm
from .models import (Competencias, Contatos, FomularioClientes, Perguntas,
                     Textos)
from .repositories import TextosRepository
from .services import PDFService
from usuarios.models import UsuarioEnvioFormulario


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
            token: str = request_token.jwt()
            link_form = f'{settings.SITE_URL}/formulario/instrucoes/?rt={token}' # noqa

            user = UsuarioEnvioFormulario.objects.filter(user=request.user).first()
            if user and user.num_formularios > 0:
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
                    user.num_formularios = user.num_formularios - 1
                    user.save()
                except Exception as e:
                    messages.error(request, f'Error no envio do email: {e}')
            else:
                messages.error(request, f'Você não possui mais disparos de email, contrate um novo plano.')

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

    @use_request_token_check_expiration(scope='mentorado')
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return render(request, '404.html')

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

        paginator = Paginator(
            Perguntas.objects.filter(ativo=True).order_by('id').all(),
            20
        )
        timeout = form_cliente.iniciado + timedelta(minutes=settings.TIMEOUT_FORMULARIO) # noqa
        tz_sao_paulo = timezone('America/Sao_Paulo')
        self.initial['formulario_id'] = pk
        self.initial['timeout'] = timeout.astimezone(tz_sao_paulo).isoformat()
        self.initial['paginator'] = paginator
        self.initial['page_obj'] = paginator.page(page)

        return super().get(request, *args, **kwargs)

    @timeout_form
    def post(self, request, pk, *args, **kwargs):
        form = self.get_form()
        is_finalizar = request.GET['finalizar'] \
            if 'finalizar' in request.GET else False

        if form.is_valid():
            self.success_url = request.get_full_path()

            if is_finalizar:
                self.success_url = reverse_lazy(
                    'formulario_finalizar', kwargs={
                        'pk': pk
                    }
                )

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


def _load_pdf_context(
    context: dict,
    formulario_id: int,
    contato: Contatos
):
    pdf_serivce = PDFService()
    textos_repo = TextosRepository()

    context['user_name'] = contato.nome_completo

    forca_gestao_png, fraqueza_gestao_png, \
        maior_grupo_gestao, menor_grupo_gestao = \
        pdf_serivce.generate_grupo_chart_png(formulario_id)

    context['forca_gestao_png'] = forca_gestao_png
    context['fraqueza_gestao_png'] = fraqueza_gestao_png
    context['maior_grupo_gestao'] = maior_grupo_gestao
    context['menor_grupo_gestao'] = menor_grupo_gestao
    painel_forcas_gestao_png, principais_forcas_gestao = \
        pdf_serivce.generate_painel_forca_png(
            formulario_id, Competencias.TipoImpacto.GESTAO
        )
    context['painel_forcas_gestao_png'] = painel_forcas_gestao_png
    painel_fraquezas_gestao_png, principais_fraquezas_gestao = \
        pdf_serivce.generate_painel_fraqueza_png(
            formulario_id, Competencias.TipoImpacto.GESTAO
        )
    context['painel_fraquezas_gestao_png'] = painel_fraquezas_gestao_png
    context['forca_gestao_resumos'] = textos_repo.get_resumos(
        Textos.Secao.FORCAS, maior_grupo_gestao, principais_forcas_gestao
    )
    context['fraqueza_gestao_resumos'] = textos_repo.get_resumos(
        Textos.Secao.FRAQUEZAS,
        menor_grupo_gestao,
        principais_fraquezas_gestao
    )
    context['forca_gestao_textos'] = textos_repo.get_textos(
        Textos.Secao.GESTAO, maior_grupo_gestao, principais_forcas_gestao
    )
    context['fraqueza_gestao_textos'] = textos_repo.get_textos(
        Textos.Secao.GESTAO,
        menor_grupo_gestao,
        principais_fraquezas_gestao
    )

    forca_equipes_png, fraqueza_equipes_png, \
        maior_grupo_equipes, menor_grupo_equipes = \
        pdf_serivce.generate_equipes_chart_png(formulario_id)

    context['forca_equipes_png'] = forca_equipes_png
    context['fraqueza_equipes_png'] = fraqueza_equipes_png
    context['maior_grupo_equipes'] = maior_grupo_equipes
    context['menor_grupo_equipes'] = menor_grupo_equipes
    painel_forcas_gestao_png, principais_forcas_equipes = \
        pdf_serivce.generate_painel_forca_png(
            formulario_id, Competencias.TipoImpacto.EQUIPES
        )
    painel_forcas_equipes_png, principais_forcas_equipes = \
        pdf_serivce.generate_painel_forca_png(
            formulario_id, Competencias.TipoImpacto.EQUIPES
        )
    context['painel_forcas_equipes_png'] = painel_forcas_equipes_png
    painel_fraquezas_equipes_png, principais_fraquezas_equipes = \
        pdf_serivce.generate_painel_fraqueza_png(
            formulario_id, Competencias.TipoImpacto.EQUIPES
        )
    context['painel_fraquezas_equipes_png'] = painel_fraquezas_equipes_png

    context['forca_equipes_resumos'] = textos_repo.get_resumos(
        Textos.Secao.FORCAS, maior_grupo_equipes, principais_forcas_equipes
    )
    context['fraqueza_equipes_resumos'] = textos_repo.get_resumos(
        Textos.Secao.FRAQUEZAS,
        menor_grupo_equipes,
        principais_fraquezas_equipes
    )
    context['forca_equipes_textos'] = textos_repo.get_textos(
        Textos.Secao.EQUIPES,
        maior_grupo_equipes,
        principais_forcas_equipes
    )
    context['fraqueza_equipes_textos'] = textos_repo.get_textos(
        Textos.Secao.EQUIPES,
        menor_grupo_equipes,
        principais_fraquezas_equipes
    )

    performance_engajamento_png, performance_engajamento_pontos = \
        pdf_serivce.generate_performance_chart_png(
            formulario_id, Competencias.TipoPerformance.ENGAJAMENTO
        )
    context['performance_engajamento_png'] = performance_engajamento_png # noqa
    context['performance_engajamento_pontos'] = performance_engajamento_pontos # noqa

    nivel = None

    if 0 <= performance_engajamento_pontos <= 28:
        nivel = 'Muito Insatisfatório'
    elif 29 <= performance_engajamento_pontos <= 56:
        nivel = 'Insatisfatório'
    elif 57 <= performance_engajamento_pontos <= 84:
        nivel = 'Satisfatório'
    elif 85 <= performance_engajamento_pontos <= 112:
        nivel = 'Bom'
    elif 113 <= performance_engajamento_pontos <= 140:
        nivel = 'Excelente'

    context['performance_engajamento_textos'] = textos_repo \
        .get_textos(Textos.Secao.ENGAJAMENTO, nivel)

    performance_desempenho_png, performance_desempenho_pontos = \
        pdf_serivce.generate_performance_chart_png(
            formulario_id, Competencias.TipoPerformance.DESEMPENHO
        )
    context['performance_desempenho_png'] = performance_desempenho_png
    context['performance_desempenho_pontos'] = performance_desempenho_pontos # noqa

    if 0 <= performance_desempenho_pontos <= 48:
        nivel = 'Muito Insatisfatório'
    elif 49 <= performance_desempenho_pontos <= 96:
        nivel = 'Insatisfatório'
    elif 97 <= performance_desempenho_pontos <= 144:
        nivel = 'Satisfatório'
    elif 145 <= performance_desempenho_pontos <= 192:
        nivel = 'Bom'
    elif 193 <= performance_desempenho_pontos <= 240:
        nivel = 'Excelente'

    context['performance_desempenho_textos'] = textos_repo \
        .get_textos(Textos.Secao.DESEMPENHO, nivel)

    performance_organizacao_png, performance_organizacao_pontos = \
        pdf_serivce.generate_performance_chart_png(
            formulario_id, Competencias.TipoPerformance.ORGANIZACAO
        )
    context['performance_organizacao_png'] = performance_organizacao_png # noqa
    context['performance_organizacao_pontos'] = performance_organizacao_pontos # noqa

    if 0 <= performance_organizacao_pontos <= 44:
        nivel = 'Muito Insatisfatório'
    elif 45 <= performance_organizacao_pontos <= 88:
        nivel = 'Insatisfatório'
    elif 89 <= performance_organizacao_pontos <= 132:
        nivel = 'Satisfatório'
    elif 133 <= performance_organizacao_pontos <= 176:
        nivel = 'Bom'
    elif 177 <= performance_organizacao_pontos <= 220:
        nivel = 'Excelente'

    context['performance_organizacao_textos'] = textos_repo \
        .get_textos(Textos.Secao.ORGANIZACAO, nivel)


class PdfViewerTemplateView(WeasyTemplateResponseMixin, TemplateView):
    template_name = 'quiz/pdf/template.html'

    def get_context_data(self, pk, **kwargs):
        contato = Contatos.objects.get(
            email=FomularioClientes.objects.filter(
                id=pk
            ).values('email')[0]['email']
        )
        context = super().get_context_data(**kwargs)

        _load_pdf_context(context, pk, contato)

        return context


def _generate_pdf(
    formulario_id: int,
) -> str:
    template_name = 'quiz/pdf/template.html'
    base_url = settings.SITE_URL
    context = {}
    contato = Contatos.objects.get(
        email=FomularioClientes.objects.filter(
            id=formulario_id
        ).values('email')[0]['email']
    )

    _load_pdf_context(context, formulario_id, contato)

    ts = datetime.now().strftime('%s')
    pdf_name = f"/tmp/{contato.nome_completo.replace(' ', '_')}_{formulario_id}_{ts}.pdf" # noqa
    html_template = get_template(template_name).render(context=context)

    HTML(
        string=html_template,
        base_url=base_url
    ).write_pdf(
        target=pdf_name
    )

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='us-east-1'
    )
    document_name = os.path.basename(pdf_name)

    try:
        s3_client.upload_file(
            pdf_name, settings.AWS_STORAGE_BUCKET_NAME,
            document_name, ExtraArgs={'ACL': 'public-read'}
        )
    except ClientError as e:
        print(e)

    return document_name, pdf_name


class InstrucoesTemplateView(TemplateView):
    template_name = 'quiz/instrucoes.html'

    @timeout_form
    @use_request_token_check_expiration(scope='mentorado')
    def get(self, request, *args, **kwargs):
        return super().get(request, args, kwargs)


class FormularioFinalizarView(TemplateView):
    template_name = 'quiz/finish_form.html'

    def get(self, request, pk, *args, **kwargs):
        form_cliente = FomularioClientes.objects.get(id=pk)

        if form_cliente:
            self.extra_context = {
                'email': form_cliente.email
            }
            file_name, file_path = _generate_pdf(pk)

            form_cliente.status = FomularioClientes.Status.FINALIZADO
            form_cliente.documento = file_name
            form_cliente.save()

            data_envio = form_cliente.created_at.strftime(settings.DATE_FORMAT_DEFAULT) # noqa

            Notificacoes(
                user=form_cliente.user,
                mensagem=f'Formulario enviado para o email: {form_cliente.email} na data {data_envio}, finalizado',  # noqa
                tipo=Notificacoes.Tipo.INFORMATIVA
            ).save()

            contato = Contatos.objects.get(
                email=FomularioClientes.objects.filter(
                    id=pk
                ).values('email')[0]['email']
            )

            EmailUtils.send_email_pdf(
                form_cliente.email, [form_cliente.user.email],
                file_path, contato.nome_completo
            )

            messages.success(request, 'Email enviado com sucesso!')

            Notificacoes(
                user=form_cliente.user,
                mensagem=f'Resultado gerado e enviado para o email: {form_cliente.email}',  # noqa
                tipo=Notificacoes.Tipo.INFORMATIVA
            ).save()

        return super().get(request, args, kwargs)
