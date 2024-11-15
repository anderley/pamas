from django.urls import path

from . import views

urlpatterns = [
    path('cadastrar/', views.CadastroView.as_view(), name='cadastro_usuario'),
    path('esqueceu/', views.password_reset_request, name='esqueceu_usuario'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete')
]