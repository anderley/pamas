# import mercadopago
# from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from pagamentos.forms import PagamentoForm

from .models import Planos


class PlanosListView(LoginRequiredMixin, ListView):
    model = Planos
    template_name = 'planos/show.html'
    redirect_field_name = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['planos_active'] = 'active'

        return context


class PlanoDetailView(DetailView):
    model = Planos
    template_name = 'planos/detail.html'
    context_object_name = 'plano'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_pagamento'] = form_pagamento = PagamentoForm(plano_id=self.object.pk) # noqa

        # sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
        # payment_methods = sdk.payment_methods().list_all()
        # for method in payment_methods["response"]:
        #     print(f"ID: {method['id']}, Nome: {method['name']}")

        return context
