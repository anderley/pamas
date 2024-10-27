import mercadopago
from django.conf import settings
from planos.models import Planos
from .models import Pagamentos
from django.views.generic import TemplateView
from django.shortcuts import render


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

        data['sucesso'], data['mensagem'], data['mercadopago_id'] = mercadopago_pagamento(self, self.request.POST, plano, pagamento.id)
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
        "transaction_amount": plano.valor,
        "external_reference": pagamento_id,
        "token": {
            'card_number': cartao,
            'card_expiration_month': vencimento[0],
            'card_expiration_year': vencimento[1],
            'security_code': data.get('codigo'),
            'cardholder_name': data.get('nome'),
            'identification_type': 'CPF',
            'identification_number': data.get('cpf')
        },
        "description": plano.descricao,
        "installments": 1,  # Número de parcelas
        "payment_method_id": "visa",  # Método de pagamento (ex: "visa", "master")
        "payer": {
            "email": self.request.user.email
        }
    }

    print(payment_data)

    try:
        payment_response = sdk.payment().create(payment_data)
        if payment_response["status"] == 201:

            return True, "Pagamento realizado com sucesso!", payment_response["response"]["id"]
        else:
            return False, "Erro ao realizar o pagamento: {}".format(payment_response["response"]["message"]), None
    except:
        return False, "Erro inesperado!", None