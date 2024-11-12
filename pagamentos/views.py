import mercadopago
import requests
from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework import status
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from pagamentos.models import Pagamentos
from planos.models import Planos


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
            pagamento.status = 'pago'
        pagamento.mercadopago_id = data['mercadopago_id']
        pagamento.save()

        return render(request, self.template_name, data)


def criando_cartao(self, data):

    vencimento = data.get('vencimento').split('/')
    cartao = data.get('cartao').replace(' ', '')

    CLIENT_ID = settings.MERCADOPAGO_CLIENT_ID
    CLIENT_SECRET = settings.MERCADOPAGO_CLIENT_SECRET

    # Obtendo o access token
    auth_response = requests.post(
        'https://api.mercadopago.com/oauth/token',
        data={
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    )

    access_token = auth_response.json().get('access_token')

    card_data = {
        "card_number": cartao,
        "expiration_month": vencimento[0],
        "expiration_year": vencimento[1],
        "security_code": data.get('codigo'),
        "email": self.request.user.email,
        "cardholder": {
            "name": data.get('nome'),
        }
    }

    token_response = requests.post(
        'https://api.mercadopago.com/v1/card_tokens',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json=card_data
    )

    if token_response.status_code == 201:
        token = token_response.json().get('id')
        return True, token
    else:
        return False, "Erro ao gerar token:", token_response.json()


def mercadopago_pagamento(self, data, plano, pagamento_id):
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    gerado, token_or_msg = criando_cartao(self, data)
    if gerado:

        payment_data = {
            "external_reference": pagamento_id,
            "transaction_amount": plano.valor,
            "description": plano.titulo,
            "installments": 1,  # Número de parcelas
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


@csrf_exempt
def update_status(request):
    status = 'pago' if request.GET.get('status') == 'approved' else 'pendente'

    pagamento = Pagamentos.objects.get(
        id=request.GET.get('external_reference')
    )

    if pagamento:
        pagamento.status = status
        pagamento.save()
        # pagamento.user.plano_num_formularios = pagamento.plano_num_formularios  # noqa
        # pagamento.user.save()

    return JsonResponse({'success': 'ok'})
