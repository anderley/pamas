from django.urls import path

from . import views

urlpatterns = [
    path('cadastrar/', views.Cadastro.as_view(), name='cadastro_usuario'),
    path('esqueceu/', views.esqueceu, name='esqueceu_usuario'),
]