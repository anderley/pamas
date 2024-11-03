import mercadopago
from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework import status
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView


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


def mercadopago_pagamento(self, data, plano, pagamento_id):
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    vencimento = data.get('vencimento').split('/')
    cartao = data.get('cartao').replace(' ', '')

    payment_data = {
        "external_reference": pagamento_id,
        "transaction_amount": plano.valor,
        "token": {
                "card_number": cartao,  # Número do cartão (exemplo de cartão de teste)
                "security_code": data.get('codigo'),  # Código de segurança
                "card_expiration_month": vencimento[0],  # Mês de expiração
                "card_expiration_year": vencimento[1],  # Ano de expiração
                "cardholder_name": data.get('nome'),  # Nome do titular do cartão
                "identification_type": "CPF",  # Tipo de identificação (ex: "CPF", "CNPJ", "ID")
                "identification_number": data.get('cpf')  # Número de identificação
        },
        "description": plano.titulo,
        "installments": 1,  # Número de parcelas
        "payment_method_id": "visa",  # Método de pagamento (ex: "visa", "master") # noqa
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
            "payer": {
                "name": data.get('nome'),
                # "surname": "",
                # "phone": {
                #     "area_code": "11",
                #     "number": "987654321"
                # },
                # "address": {
                #     "street_name": "Rua Exemplo",
                #     "street_number": 123,
                #     "zip_code": "12345-678"
                # }
            }
        }
    }

    print(payment_data)

    try:
        payment_response = sdk.payment().create(payment_data)
        if payment_response["status"] == 201:

            return True, "Pagamento realizado com sucesso!", payment_response["response"]["id"] # noqa
        else:
            return False, "Erro ao realizar o pagamento: {}".format(payment_response["response"]["message"]), None # noqa
    except: # noqa
        return False, "Erro inesperado!", None
