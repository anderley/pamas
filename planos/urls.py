from django.urls import path
from .views import PlanosListView, PlanoDetailView


urlpatterns = [
    path('', PlanosListView.as_view(), name='planos'),
    path('<int:pk>/', PlanoDetailView.as_view(), name='planos_detail'),
]
