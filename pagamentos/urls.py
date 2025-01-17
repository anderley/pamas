from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.PagamentoView.as_view(), name='pagamento'),
    path('all/', views.PagamentosListView.as_view(), name='all_pagamentos'), # noqa
    path('gerar_pix/', views.gerar_pix, name='gerar_pix'),
    path('mercadopago/', csrf_exempt(views.PagamentosCallBackView.as_view()), name='mercadopago_callback'), # noqa
]
