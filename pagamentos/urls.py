from django.urls import path
from .views import PagamentoView


urlpatterns = [
    path('', PagamentoView.as_view(), name='pagamento'),
]
