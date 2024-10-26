from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Planos


class List(LoginRequiredMixin, ListView):
    model = Planos
    template_name = 'planos/show.html'
    redirect_field_name = 'login'
