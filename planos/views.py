from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Planos
from django.views.generic import ListView, DetailView


class List(LoginRequiredMixin, ListView):
    model = Planos
    template_name = 'planos/show.html'
    redirect_field_name = 'login'


class PlanoDetailView(DetailView):
    model = Planos
    template_name = 'planos/detail.html'
    context_object_name = 'plano'
