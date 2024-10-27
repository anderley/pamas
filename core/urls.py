from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    path('planos/', include('planos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('pagamentos/', include('pagamentos.urls')),
]
