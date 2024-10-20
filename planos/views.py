from django.shortcuts import render
from django.views.generic import ListView

from .models import Planos


class List(ListView):
    model = Planos
    template_name = 'planos/show.html'
