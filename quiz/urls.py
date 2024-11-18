from django.urls import path

from usuarios import views as auth_view

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_view.CustomLoginView.as_view(), name='login'), # noqa
    path('logout/', views.logout_view, name='logout'),
    path('formulario/instrucoes/', views.InstrucoesTemplateView.as_view(), name='formulario_instrucoes'), # noqa
    path('formulario/cadastro/', views.ContatosCreateView.as_view(), name='formulario_cadastro'), # noqa
    path('formulario/cadastro/<pk>/editar', views.ContatosUpdateView.as_view(), name='formulario_cadastro_editar'), # noqa
    path('formulario/<pk>/', views.FormularioFormView.as_view(), name='formulario'), # noqa
    path('enviar-formulario/', views.enviar_formulario, name='send_form'),
    path('listar-envios/', views.ListSentFormsView.as_view(), name='list_sent_form'), # noqa
    path('listar-envios/<int:id>/cancelar/', views.cancelar_form, name='cancelar_sent_form'), # noqa
    path('pdf/viewer/<pk>/', views.PdfViewerTemplateView.as_view(), name='pdf-viewer'), # noqa
    path('pdf/<pk>/download/', views.PdfView.as_view(), name='pdf-download'), # noqa
]
