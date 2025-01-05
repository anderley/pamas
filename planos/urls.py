from django.urls import path

from .views import PlanoDetailView, PlanosListView

urlpatterns = [
    path('', PlanosListView.as_view(), name='planos'),
    path('detalhes/', PlanosListView.as_view(), name='planos_detail'),
    path('<int:pk>/', PlanoDetailView.as_view(), name='planos_checkout'),
]
