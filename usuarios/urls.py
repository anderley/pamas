from django.urls import path

from . import views

urlpatterns = [
    path('cadastrar/', views.CadastroView.as_view(), name='cadastro_usuario'),
    path('esqueceu/', views.esqueceu, name='esqueceu_usuario'),
]