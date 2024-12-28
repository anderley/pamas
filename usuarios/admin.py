from django.contrib import admin
from .models import UsuarioEnvioFormulario


class UsuarioEnvioFormularioAdmin(admin.ModelAdmin):
    list_display = ['user', 'num_formularios']


admin.site.register(UsuarioEnvioFormulario, UsuarioEnvioFormularioAdmin)
