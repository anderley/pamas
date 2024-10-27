from django.shortcuts import render
from .models import Planos
from django.views.generic import ListView, DetailView


class List(ListView):
    model = Planos
    template_name = 'planos/show.html'

class PlanoDetailView(DetailView):
    model = Planos
    template_name = 'planos/detail.html'
    context_object_name = 'plano'