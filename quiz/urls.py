from django.urls import path
from django.contrib.auth import views as auth_view

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_view.LoginView.as_view(template_name='quiz/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('formulario/cadastro/', views.ContatosCreateView.as_view(), name='formulario_cadastro'), # noqa
    path('formulario/cadastro/<pk>/editar', views.ContatosUpdateView.as_view(), name='formulario_cadastro_editar'), # noqa
    path('formulario/<pk>/', views.FormularioFormView.as_view(), name='formulario'), # noqa
    path('enviar-formulario/', views.enviar_formulario, name='send_form'),
    path('listar-envios/', views.ListSentFormsView.as_view(), name='list_sent_form'), # noqa
    path('listar-envios/<int:id>/cancelar/', views.cancelar_form, name='cancelar_sent_form'), # noqa
    path('pdf/viewer/', views.PdfTemplateView.as_view(), name='pdf-viewer'),
]
