from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('formulario/', views.Show.as_view(), name='formulario'),
    path('enviar-formulario/', views.enviar_formulario, name='send_form'),
]
