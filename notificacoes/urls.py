from django.urls import path

from . import views

urlpatterns = [
    path('', views.NotificacoesJsonView.as_view(), name='notificacoes'),
    path('all/', views.NotificacoesListView.as_view(), name='all_notificacoes'), # noqa
    path('viewed/', views.set_viewed_notificacao, name='set_viewed_notificacao'), # noqa
]
