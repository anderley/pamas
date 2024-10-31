from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Planos
from django.views.generic import ListView, DetailView
from pagamentos.forms import PagamentoForm
from pagamentos.models import Pagamentos
from quiz.decorators import use_request_token_check_expiration


class PlanosListView(LoginRequiredMixin, ListView):
    model = Planos
    template_name = 'planos/show.html'
    redirect_field_name = 'login'


class PlanoDetailView(DetailView):
    model = Planos
    template_name = 'planos/detail.html'
    context_object_name = 'plano'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_pagamento'] = form_pagamento = PagamentoForm(plano_id=self.object.pk)
        return context
