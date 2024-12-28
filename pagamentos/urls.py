from django.urls import path

from . import views

urlpatterns = [
    path('', views.PagamentoView.as_view(), name='pagamento'),
    path('all/', views.PagamentosListView.as_view(), name='all_pagamentos'), # noqa
    path('gerar_pix/', views.gerar_pix, name='gerar_pix'),
    # path('webhooks/', views.update_status, name='pagamento_callback'),
]
