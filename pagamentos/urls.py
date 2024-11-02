from django.urls import path
from .views import PagamentoView #, PagamentoCallback


urlpatterns = [
    path('', PagamentoView.as_view(), name='pagamento'),
    # path("webhooks/", PagamentoCallback.as_view(), name="pagamento_callback"),
]
