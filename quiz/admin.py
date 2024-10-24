from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Grupos,
    Competencias,
    Perguntas,
    Textos,
    FomularioClientes
)
from .forms import  PerguntasForm


class GruposAdmin(ImportExportModelAdmin):
    list_display = ['nome']


class CompetenciasAdmin(ImportExportModelAdmin):
    list_display=['nome', 'grupo']


class PerguntasAdmin(ImportExportModelAdmin):
    form = PerguntasForm
    list_display=['descricao', 'competencia', 'grupo']


class TextosAdmin(ImportExportModelAdmin):
    list_display = ['texto', 'competencia']


class FomularioClientesAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email', 'token', 'form_url']


admin.site.register(Grupos, GruposAdmin)
admin.site.register(Competencias, CompetenciasAdmin)
admin.site.register(Perguntas, PerguntasAdmin)
admin.site.register(Textos, TextosAdmin)
admin.site.register(FomularioClientes, FomularioClientesAdmin)
