from django.contrib import admin
from django.contrib.auth.models import User

from import_export.admin import ImportExportActionModelAdmin

from .models import UserProfile, UsuarioEnvioFormulario
from pagamentos.models import Pagamentos


class UsuarioEnvioFormularioAdmin(admin.ModelAdmin):
    list_display = ['user', 'num_formularios']


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Dados Complementares'


class UserAdmin(ImportExportActionModelAdmin):
    inlines = [UserProfileInline]
    list_display = ['email', 'first_name', 'last_name', 'whatsapp', 'comprou_algum_plano', 'is_staff']

    def comprou_algum_plano(self, obj):
        if Pagamentos.objects.filter(user=obj, status='pago'):
            return 'Sim'
        else:
            return 'Não'

    def whatsapp(self, obj):
        user = UserProfile.objects.get(user=obj)
        if user:
            return user.whatsapp


admin.site.register(UsuarioEnvioFormulario, UsuarioEnvioFormularioAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
