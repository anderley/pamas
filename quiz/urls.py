from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('formulario/cadastro/', views.CreateContatosView.as_view(), name='formulario_cadastro'),
    path('formulario/', views.FormListView.as_view(), name='formulario'),
    path('enviar-formulario/', views.enviar_formulario, name='send_form'),
    path('listar-envios/', views.ListSentFormsView.as_view(), name='list_sent_form'),
    path('listar-envios/<int:id>/cancelar/', views.cancelar_form, name='cancelar_sent_form'),
]
