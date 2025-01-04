from django.contrib import admin

from .models import Pagamentos


class PagamentosAdmin(admin.ModelAdmin):
    search_fields = ['plano_titulo', 'user__nome_first', 'plano_descricao', 'mercadopago_id']
    list_filter = ['status', ]
    list_display = [
        '__str__', 'mercadopago_id', 'plano_titulo',
        'plano_descricao', 'plano_num_formularios',
        'plano_valor', 'status', 'modificado', 'criado']


admin.site.register(Pagamentos, PagamentosAdmin)
