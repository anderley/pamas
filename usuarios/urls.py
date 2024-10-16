from django.urls import path

from . import views

urlpatterns = [
    path('cadastrar', views.cadastro, name='cadastro_usuario'),
    path('esqueceu', views.esqueceu, name='esqueceu_usuario'),
]