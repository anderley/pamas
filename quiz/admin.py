from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .forms import PerguntasForm
from .models import (Competencias, Contatos, FomularioClientes, Grupos,
                     Perguntas, Textos, Respostas)
from .resources import CompetenciasResource, GruposResource, PerguntasResource


class GruposAdmin(ImportExportModelAdmin):
    resource_class = GruposResource
    list_display = ['id', 'nome', 'ativo', 'created_at', 'updated_at']

    class Media:
        css = {
            'all': ['css/custom_admin.min.css']
        }


class CompetenciasAdmin(ImportExportModelAdmin):
    resource_class = CompetenciasResource
    search_fields = ['grupo']
    list_display = ['id', 'nome', 'grupo', 'ativo', 'created_at', 'updated_at']

    class Media:
        css = {
            'all': ['css/custom_admin.min.css']
        }


class PerguntasAdmin(ImportExportModelAdmin):
    resource_class = PerguntasResource
    form = PerguntasForm
    search_fields = ['competencia']
    list_display = ['id', 'descricao', 'competencia', 'grupo', 'ativo', 'created_at', 'updated_at'] # noqa

    class Media:
        css = {
            'all': ('css/custom_admin.min.css',)
        }


class TextosAdmin(ImportExportModelAdmin):
    list_display = ['texto', 'competencia', 'ativo', 'created_at', 'updated_at'] # noqa


class FomularioClientesAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email', 'status', 'token', 'form_url', 'created_at', 'updated_at'] # noqa


class ContatosAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'email', 'telefone', 'created_at', 'updated_at'] # noqa


class RespostasAdmin(admin.ModelAdmin):
    list_display = ['formulario', 'pergunta', 'resposta', 'created_at', 'updated_at'] # noqa


admin.site.register(Grupos, GruposAdmin)
admin.site.register(Competencias, CompetenciasAdmin)
admin.site.register(Perguntas, PerguntasAdmin)
admin.site.register(Textos, TextosAdmin)
admin.site.register(FomularioClientes, FomularioClientesAdmin)
admin.site.register(Contatos, ContatosAdmin)
admin.site.register(Respostas, RespostasAdmin)
