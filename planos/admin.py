from django.contrib import admin

from .forms import PlanosForm
from .models import Planos


class PlanosAdmin(admin.ModelAdmin):
    form = PlanosForm
    list_display = [
        'titulo', 'descricao', 'cod_cor',
        'imagem', 'num_formularios', 'valor'
    ]


admin.site.register(Planos, PlanosAdmin)
