from django.urls import path

from .views import PlanoDetailView, PlanosListView

urlpatterns = [
    path('', PlanosListView.as_view(), name='planos'),
    path('<int:pk>/', PlanoDetailView.as_view(), name='planos_detail'),
]
