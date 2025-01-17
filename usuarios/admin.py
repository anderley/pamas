from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, UsuarioEnvioFormulario


class UsuarioEnvioFormularioAdmin(admin.ModelAdmin):
    list_display = ['user', 'num_formularios']


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Dados Complementares'


class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]


admin.site.register(UsuarioEnvioFormulario, UsuarioEnvioFormularioAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
