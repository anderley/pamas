from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('formulario/', views.ShowForm.as_view(), name='formulario'),
    path('enviar-formulario/', views.enviar_formulario, name='send_form'),
    path('listar-envios/', views.ListSentForm.as_view(), name='list_sent_form'),
    path('listar-envios/<int:id>/cancelar/', views.cancelar_form, name='cancelar_sent_form'),
]
