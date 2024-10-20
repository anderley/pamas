from django.contrib import admin

from .models import (
    Grupos,
    Competencias,
    Perguntas,
    Textos
)
from .forms import  PerguntasForm


class GruposAdmin(admin.ModelAdmin):
    list_display = ['nome']


class CompetenciasAdmin(admin.ModelAdmin):
    list_display=['nome', 'grupo']


class PerguntasAdmin(admin.ModelAdmin):
    form = PerguntasForm
    list_display=['descricao', 'competencia', 'grupo']


class TextosAdmin(admin.ModelAdmin):
    list_display = ['texto', 'competencia']


admin.site.register(Grupos, GruposAdmin)
admin.site.register(Competencias, CompetenciasAdmin)
admin.site.register(Perguntas, PerguntasAdmin)
admin.site.register(Textos, TextosAdmin)
