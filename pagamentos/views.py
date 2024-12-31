
import json
import mercadopago
import hmac
import hashlib
import base64
import urllib.parse
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from django.views.generic import ListView, TemplateView
from django.http import JsonResponse
from django.views import View

from notificacoes.models import Notificacoes
from pagamentos.models import Pagamentos
from planos.models import Planos
from usuarios.models import UsuarioEnvioFormulario


class PagamentosListView(LoginRequiredMixin, ListView):
    model = Pagamentos
    template_name = 'pagamentos/historico.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user
        ).order_by('-pk')


class PagamentoView(TemplateView):
    template_name = 'pagamentos/pagamento.html'

    def post(self, request, *args, **kwargs):
        data = {}

        plano = Planos.objects.get(id=self.request.POST.get('plano'))
        pagamento = Pagamentos.objects.create(
            user=self.request.user,
            plano_titulo=plano.titulo,
            plano_descricao=plano.descricao,
            plano_num_formularios=plano.num_formularios,
            plano_valor=plano.valor,
            status='pendente',
        )

        data['sucesso'], data['mensagem'], data['mercadopago_id'] = mercadopago_pagamento(self, self.request.POST, plano, pagamento.id) # noqa
        data['pagamento'] = pagamento.id

        if data['sucesso']:
            userEnvioFormulario, created = UsuarioEnvioFormulario.objects.get_or_create( # noqa
                user=self.request.user
            )
            if userEnvioFormulario:
                userEnvioFormulario.pagamento = pagamento
                userEnvioFormulario.num_formularios += pagamento.plano_num_formularios # noqa
                userEnvioFormulario.save()

            pagamento.status = 'pago'
            envia_email_e_cria_notificao(self.request, True)
        else:
            envia_email_e_cria_notificao(self.request, False)
        pagamento.mercadopago_id = data['mercadopago_id']
        pagamento.save()

        return render(request, self.template_name, data)


def envia_email_e_cria_notificao(request, paid):

    if paid:
        subject = '[PAMAS] Pagamento concluído'
        mensagem = 'Pagamento recebido com sucesso!'
    else:
        subject = '[PAMAS] Pagamento falhou'
        mensagem = 'Ocorreu um problema no seu pagamento!'

    try:
        html_message = render_to_string(
            'pagamentos/emails/mensagem.html',
            {
                'user_name': f'{request.user.first_name} {request.user.last_name}', # noqa
                'mensagem': f'{mensagem}',
            }
        )
        plain_message = strip_tags(html_message)

        send_mail(
            subject, plain_message, settings.EMAIL_HOST_USER, [request.user.email], html_message=html_message # noqa
        )

        Notificacoes(
            user=request.user,
            mensagem=f'Pagamento recebido do cliente: {request.user.email}', # noqa
            tipo=Notificacoes.Tipo.PAGAMENTO
        ).save()

        messages.success(request, f'Novo pagamento recebido do cliente: {request.user.email}') # noqa
    except Exception:
        messages.error(request, f'Erro no pagamento do cliente com o email: {request.user.email}') # noqa


def criando_cartao(self, sdk, data):
    vencimento = data.get('vencimento').split('/')
    cartao = data.get('cartao').replace(' ', '')

    # Dados do cartão
    card_data = {
        "card_number": cartao,
        "expiration_month": vencimento[0],
        "expiration_year": vencimento[1],
        "security_code": data.get('codigo'),
        "cardholder": {
            "name": data.get('nome'),
        },
        "email": self.request.user.email  # Email do titular do cartão
    }

    # Cria o token do cartão
    try:
        token_response = sdk.card_token().create(card_data)
        if token_response['status'] == 201:
            token = token_response['response']['id']
            print('status', token_response['status'], 'token', token)
            return True, token
        else:
            return False, "Erro ao gerar token: {}".format(token_response['response'])
    except Exception as e:
        return False, "Erro ao gerar token: {}".format(str(e))


def mercadopago_pagamento(self, data, plano, pagamento_id):
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    gerado, token_or_msg = criando_cartao(self, sdk, data)
    if gerado:

        payment_data = {
            "external_reference": pagamento_id,
            "transaction_amount": plano.valor,
            "description": plano.titulo,
            "installments": int(data.get('parcelas')),  # Número de parcelas
            "token": token_or_msg,
            "payer": {
                "email": self.request.user.email,
                "identification": {
                    "type": "CPF",
                    "number": data.get('cpf')
                }
            },
            "additional_info": {
                "items": [
                    {
                        "id": plano.id,
                        "title": plano.titulo,
                        "description": plano.descricao,
                        "quantity": 1,
                        "unit_price": plano.valor
                    }
                ],
            }
        }

        try:
            payment_response = sdk.payment().create(payment_data)
            if payment_response["status"] == 201:
                return True, "Pagamento realizado com sucesso!", payment_response["response"]["id"] # noqa
            else:
                return False, "Erro ao realizar o pagamento: {}".format(payment_response["response"]["message"]), None # noqa
        except: # noqa
            return False, "Erro inesperado!", None
    else:
        return False, token_or_msg, None

def criar_pagamento_pix(email_cliente, descricao, valor):
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    payment_data = {
        "transaction_amount": valor,  # Valor do pagamento
        "description": descricao,
        "payment_method_id": "pix",  # Método de pagamento Pix
        "payer": {
            "email": email_cliente  # Email do pagador
        }
    }

    # Cria o pagamento
    payment_response = sdk.payment().create(payment_data)
    return payment_response


def gerar_pix(request):
    plano_id = request.GET.get('plano_id')
    plano = Planos.objects.get(id=plano_id)

    pix_data = criar_pagamento_pix(request.user.email, plano.titulo, plano.valor)

    if pix_data:
        pix_vars = {
            'url': pix_data['response']['point_of_interaction']['transaction_data']['qr_code'], 
            'qrcode': pix_data['response']['point_of_interaction']['transaction_data']['qr_code_base64']
        }

        pagamento = Pagamentos.objects.create(
            user=request.user,
            plano_titulo=plano.titulo,
            plano_descricao=plano.descricao,
            plano_num_formularios=plano.num_formularios,
            plano_valor=plano.valor,
            status='pendente',
            mercadopago_id=pix_data['response']['id']
        )
    else:
        pix_vars = {}

    # Carrega o template que contém o HTML do Pix
    template = get_template('pagamentos/gerar_pix.html')  # Substitua pelo seu template
    return HttpResponse(template.render(pix_vars, request))
        

class PagamentosCallBackView(View):
    def post(self, request, *args, **kwargs):
        # Obtém o cabeçalho X-Signature
        xSignature = request.headers.get("x-signature")
        xRequestId = request.headers.get("x-request-id")

        # Processa a notificação
        notification = json.loads(request.body)
        payment_id = notification.get('id')

        # Valida a assinatura
        if not self.validate_signature(notification, xSignature, xRequestId):
            return JsonResponse({'status': 'error', 'message': 'Invalid signature'}, status=403)

        # Aqui você pode buscar o pagamento e atualizar o status no seu sistema
        sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        payment = sdk.payment().get(payment_id)

        if payment["status"] == 200:
            payment_data = payment["response"]
            status = payment_data['status']

            if status == 'approved':
                status = 'pago'
            elif status == 'pending':
                status = 'pendente'
            elif status == 'rejected':
                status = 'rejeitado'

            pagamento = Pagamentos.objects.filter(mercadopago_id=payment_id, status='pendente').first()
            if pagamento:
                pagamento.status = status
                pagamento.save()

                if pagamento.status == 'pago':
                    userEnvioFormulario, created = UsuarioEnvioFormulario.objects.get_or_create( # noqa
                        user=self.request.user
                    )
                    if userEnvioFormulario:
                        userEnvioFormulario.pagamento = pagamento
                        userEnvioFormulario.num_formularios += pagamento.plano_num_formularios # noqa
                        userEnvioFormulario.save()       

            return JsonResponse({'status': 'success', 'message': 'Payment processed'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to retrieve payment'}, status=400)


    def validate_signature(self, body, xSignature, xRequestId):

        # Extract the "data.id" from the query params
        dataID = body.get('data.id')

        # Separating the x-signature into parts
        parts = xSignature.split(",")

        # Initializing variables to store ts and hash
        ts = None
        hash = None

        # Iterate over the values to obtain ts and v1
        for part in parts:
            # Split each part into key and value
            keyValue = part.split("=", 1)
            if len(keyValue) == 2:
                key = keyValue[0].strip()
                value = keyValue[1].strip()
                if key == "ts":
                    ts = value
                elif key == "v1":
                    hash = value

        # Obtain the secret key for the user/application from Mercadopago developers site
        secret = settings.MERCADOPAGO_ASS_SECRET_WEBHOOK

        # Generate the manifest string
        manifest = f"id:{dataID};request-id:{xRequestId};ts:{ts};"

        # Create an HMAC signature defining the hash type and the key as a byte array
        hmac_obj = hmac.new(secret.encode(), msg=manifest.encode(), digestmod=hashlib.sha256)

        # Obtain the hash result as a hexadecimal string
        sha = hmac_obj.hexdigest()
        if sha == hash:
            # HMAC verification passed
            return True
        else:
            # HMAC verification failed
            return False