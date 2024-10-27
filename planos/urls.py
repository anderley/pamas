from django.urls import path
from .views import List, PlanoDetailView


urlpatterns = [
    path('', List.as_view(), name='planos'),
    path('<int:pk>/', PlanoDetailView.as_view(), name='planos_detail'),
]
