from typing import List, Literal

from django.db.models import Count, ExpressionWrapper, FloatField, Sum

from .models import Competencias, Grupos, Textos


class GruposRepository:

    def get_media_repostas_grupo(
        self,
        formulario_id: int,
        tipo_impacto: Literal[Competencias.TipoImpacto]
    ) -> List[Grupos]:

        media_grupos = Grupos.objects.filter(
            competencias__tipo_impacto=tipo_impacto,
            competencias__perguntas__respostas__formulario_id=formulario_id
        ).annotate(
            media=ExpressionWrapper(
                Sum('competencias__perguntas__respostas__resposta')
                / Count('competencias'),
                output_field=FloatField()
            )
        )

        return media_grupos


class CompetenciasRepository:

    def get_total_repostas(
        self,
        formulario_id: int,
        tipo_performance: Literal[Competencias.TipoPerformance]
    ) -> int:
        result = Competencias.objects.filter(
            tipo_performance=tipo_performance,
            perguntas__respostas__formulario_id=formulario_id
        ).aggregate(
            total=Sum('perguntas__respostas__resposta')
        )

        return result['total']

    def get_media_forca(
        self,
        formulario_id: int
    ) -> int:
        result = Competencias.objects.filter(
            perguntas__respostas__formulario_id=formulario_id
        ).aggregate(
            total=Sum('perguntas__respostas__resposta')
        )

        return result['total']

    def get_forca_competencias(
        self,
        formulario_id: int,
        tipo_impacto: Literal[Competencias.TipoImpacto]
    ) -> List[str]:
        competencias = Competencias.objects.raw('''
            SELECT c.*
            FROM competencias c
            JOIN grupos g ON g.id = c.grupo_id
            JOIN perguntas p ON p.competencia_id = c.id
            JOIN respostas r ON r.pergunta_id = p.id
            JOIN (
                SELECT Sum(r.resposta) / Count(c.id) AS 'media',
                        g.id
                FROM competencias c
                JOIN grupos g ON g.id = c.grupo_id
                JOIN perguntas p ON p.competencia_id = c.id
                JOIN respostas r ON r.pergunta_id = p.id and r.formulario_id = %s # noqa
                WHERE c.tipo_impacto = %s
                GROUP  BY g.id
                ORDER  BY media DESC
                LIMIT  1
            ) max_g ON max_g.id = c.grupo_id
            ORDER  BY r.resposta DESC
            LIMIT  5
        ''', [formulario_id, tipo_impacto])

        return [
            c.nome.strip()
            for c in competencias
        ]

    def get_fraqueza_competencias(
        self,
        formulario_id: int,
        tipo_impacto: Literal[Competencias.TipoImpacto]
    ) -> List[str]:
        competencias = Competencias.objects.raw('''
            SELECT c.*
            FROM competencias c
            JOIN grupos g ON g.id = c.grupo_id
            JOIN perguntas p ON p.competencia_id = c.id
            JOIN respostas r ON r.pergunta_id = p.id
            JOIN (
                SELECT Sum(r.resposta) / Count(c.id) AS 'media',
                        g.id
                FROM competencias c
                JOIN grupos g ON g.id = c.grupo_id
                JOIN perguntas p ON p.competencia_id = c.id
                JOIN respostas r ON r.pergunta_id = p.id and r.formulario_id = %s # noqa
                WHERE c.tipo_impacto = %s
                GROUP  BY g.id
                ORDER  BY media
                LIMIT  1
            ) max_g ON max_g.id = c.grupo_id
            ORDER  BY r.resposta
            LIMIT  5
        ''', [formulario_id, tipo_impacto])

        return [
            c.nome
            for c in competencias
        ]


class TextosRepository:

    def get_resumos(
            self,
            secao: Textos.Secao,
            nivel: str,
            competencias: List[str]
    ) -> List:
        resumo = Textos.objects.filter(
            tipo=Textos.Tipo.RESUMO,
            secao=secao,
            nivel=nivel,
            competencia__in=competencias
        ).all()

        return resumo

    def get_textos(
            self,
            secao: Textos.Secao,
            nivel: str,
            competencias: List[str] = None
    ) -> List[Textos]:
        # print(secao, nivel, competencias)

        # return []
        filter = {
            'tipo': Textos.Tipo.LIVRO,
            'secao': secao,
            'nivel': nivel
        }
        if competencias:
            filter['competencia__in'] = competencias

        query = Textos.objects.filter(
            **filter
        )

        return query.all()
