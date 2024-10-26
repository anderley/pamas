<<<<<<< HEAD
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

=======
from django.shortcuts import render
>>>>>>> c2b95db (planos e mercadopago)
from .models import Planos
from django.views.generic import ListView, DetailView


class List(LoginRequiredMixin, ListView):
    model = Planos
    template_name = 'planos/show.html'
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    redirect_field_name = 'login'
=======

class PlanoDetailView(DetailView):
    model = Planos
    template_name = 'planos/detail.html'
    context_object_name = 'plano'
>>>>>>> c2b95db (planos e mercadopago)
=======
    redirect_field_name = 'login'
>>>>>>> 83c9d93 (chore: envio de link com token de expiração)
=======
    redirect_field_name = 'login'
>>>>>>> 83c9d93 (chore: envio de link com token de expiração)
