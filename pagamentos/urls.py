from django.urls import path

from .views import PagamentoView #, update_status

urlpatterns = [
    path('', PagamentoView.as_view(), name='pagamento'),
    # path('webhooks/', update_status, name='pagamento_callback'),
]
