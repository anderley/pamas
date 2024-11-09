from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

from .models import Competencias, Grupos, Perguntas


class GruposResource(resources.ModelResource):

    class Meta:
        model = Grupos
        import_id_fields = ['nome']
        fields = ['id', 'nome', 'ativo']


class CompetenciasResource(resources.ModelResource):
    grupo = fields.Field(
        column_name='grupo',
        attribute='grupo',
        widget=ForeignKeyWidget(Grupos, field='nome')
    )

    class Meta:
        model = Competencias
        import_id_fields = ['nome']
        fields = ['id', 'nome', 'grupo', 'ativo']


class PerguntasResource(resources.ModelResource):
    competencia = fields.Field(
        column_name='competencia',
        attribute='competencia',
        widget=ForeignKeyWidget(Competencias, field='nome')
    )

    class Meta:
        model = Perguntas
        import_id_fields = ['descricao']
        fields = ['id', 'descricao',  'competencia', 'ativo']
