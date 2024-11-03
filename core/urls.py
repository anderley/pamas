from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    path('planos/', include('planos.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('pagamentos/', include('pagamentos.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
