from typing import Literal

from django.db.models import ExpressionWrapper, Sum, Count, FloatField

from .models import Grupos, Competencias


class GruposRepository:

    def get_media_repostas_grupo(
        self,
        formulario_id: int,
        tipo_impacto: Literal[Competencias.TipoImpacto]
    ):

        media_grupos = Grupos.objects.filter(
            competencias__tipo_impacto=tipo_impacto,
            competencias__perguntas__respostas__formulario_id=formulario_id
        ).annotate(
            media=ExpressionWrapper(
                Sum('competencias__perguntas__respostas__resposta') / Count('competencias'),
                output_field=FloatField()
            )
        )

        return media_grupos


class CompetenciasRepository:

    def get_total_repostas(
        self,
        formulario_id: int,
        tipo_performance: Literal[Competencias.TipoPerformance]
    ):
        result = Competencias.objects.filter(
            tipo_performance=tipo_performance,
            perguntas__respostas__formulario_id=formulario_id
        ).aggregate(
            total=Sum('perguntas__respostas__resposta')
        )

        return result['total']
