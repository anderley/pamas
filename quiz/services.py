from typing import List, Union

from .repositories import GruposRepository, CompetenciasRepository
from .models import Competencias, Grupos
from .helpers import PDFHelper

class PDFService:
    grupos_repo = GruposRepository()
    competencias_repo = CompetenciasRepository()

    def __get_pdf_config(
        self,
        data: Union[List[Grupos]|List[Competencias]],
    ) -> dict:
        
        def get_data_vertical(
            data: Union[List[Grupos]|List[Competencias]],
        ) -> dict:
            y = [
                d.media
                for d in data
            ]
            return {
                'x': [
                    d.nome
                    for d in data
                ],
                'y': y,
                'color': [
                    d.cod_cor
                    for d in data
                ],
                'text': y,
            }
    
        def get_references(
            data: Union[List[Grupos]|List[Competencias]],
            value: List[int]
        ) -> dict:
            return {
                'x': [
                    mg.nome
                    for mg in data
                ],
                'y': value,
                'color': '#F0E68C'
            }
        
        def get_layout(
            range: List[int],
            height: int,
            width: int
        ) -> dict:
            return {
                'yaxis': {
                    'range': range
                },
                'width': width,
                'height': height,
                'margin': {
                    'l': 10,
                    'r': 10,
                    't': 60,
                    'b': 20,
                    'pad': 20,
                }
            }
        
        return {
            'data': get_data_vertical(data),
            'refereces': get_references(
                data, [3, 3, 3, 3]
            ),
            'layout': get_layout([0,6], 340, 585)
        }

    def generate_grupo_chart_png(
        self,
        formulario_id: int
    ) -> str:
        media_gestao = self.grupos_repo.get_media_repostas_grupo(
            formulario_id, Competencias.TipoImpacto.GESTAO
        )
        pdf_config = self.__get_pdf_config(media_gestao)

        return PDFHelper.generate_base64_image(
            title='Valor Referência x Valor Real',
            file_name='grupo_chart',
            **pdf_config
        )
        
    def generate_equipes_chart_png(
        self,
        formulario_id: int
    ) -> str:
        media_equipes = self.grupos_repo.get_media_repostas_grupo(
            formulario_id, Competencias.TipoImpacto.EQUIPES
        )
        pdf_config = self.__get_pdf_config(media_equipes)

        return PDFHelper.generate_base64_image(
            title='Valor Referência x Valor Real',
            file_name='grupo_chart',
            **pdf_config
        )

    def generate_performance_chart_png(
        self,
        formulario_id: int
    ) -> str:
        total_desempenho = self.competencias_repo.get_total_repostas(
            formulario_id, Competencias.TipoPerformance.DESEMPENHO
        )
        total_engajamento = self.competencias_repo.get_total_repostas(
            formulario_id, Competencias.TipoPerformance.ENGAJAMENTO
        )
        total_organizacao = self.competencias_repo.get_total_repostas(
            formulario_id, Competencias.TipoPerformance.ORGANIZACAO
        )
        performance = [
            {
                'nome': f'{Competencias.TipoPerformance.DESEMPENHO}',
                'cor': '#fb18d6',
                'media': total_desempenho,
            },
            {
                'nome': f'{Competencias.TipoPerformance.ENGAJAMENTO}',
                'cor': '#fb18d6',
                'media': total_engajamento,
            },
            {
                'nome': f'{Competencias.TipoPerformance.ORGANIZACAO}',
                'cor': '#fb18d6',
                'media': total_organizacao
            }
        ]
        x = [
            p['media']
            for p in performance
        ]
        return PDFHelper.generate_base64_image(
            title='Valor Referência x Valor Real',
            file_name='performance_chart',
            data={
                'x': x,
                'y': [
                    d['nome']
                    for d in performance
                ],
                'color': [
                    d['cor']
                    for d in performance
                ],
                'text': x,
            },
            refereces={
                'x': [120, 70, 110],
                'y': [
                    d['nome']
                    for d in performance
                ],
                'color': '#F0E68C',
            },
            orientation=PDFHelper.BarChartType.HORIZONTAL,
            layout={
                'xaxis': {
                    'range': [0,260]
                },
                'width': 585,
                'height': 340,
                'margin': {
                    'l': 10,
                    'r': 10,
                    't': 60,
                    'b': 20,
                    'pad': 10,
                }
            }
        )
