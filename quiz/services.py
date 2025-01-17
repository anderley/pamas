import base64
from datetime import datetime
from enum import Enum
from typing import List, Union

from django.template import engines
from html2image import Html2Image

from .helpers import PDFHelper
from .models import Competencias, Grupos
from .repositories import CompetenciasRepository, GruposRepository


class PDFService:
    grupos_repo = GruposRepository()
    competencias_repo = CompetenciasRepository()

    class ChartType(Enum):
        FORCA = 'Forca'
        FRAQUEZA = 'Fraqueza'

    def __get_pdf_config(
        self,
        data: Union[List[Grupos] | List[Competencias]],
        chart_type: ChartType,
        media: float
    ) -> dict:
        color = []
        find_color = False

        if chart_type == self.ChartType.FORCA:
            for d in data:
                if d.media == media and not find_color:
                    color.append(d.cod_cor)
                    find_color = True
                else:
                    color.append('#dddddd')
        else:
            for d in data:
                if d.media == media and not find_color:
                    color.append(d.cod_cor)
                    find_color = True
                else:
                    color.append('#dddddd')

        def get_data_vertical(
            data: Union[List[Grupos] | List[Competencias]],
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
                'color': color,
                'text': y,
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
            'layout': get_layout([0, 6], 340, 585)
        }

    def generate_grupo_chart_png(
        self,
        formulario_id: int
    ) -> List[str]:
        medias_gestao = self.grupos_repo.get_media_repostas_grupo(
            formulario_id, Competencias.TipoImpacto.GESTAO
        )
        maior_media = 0
        maior_grupo_gestao = None
        menor_media = 5
        menor_grupo_gestao = None

        for media_gestao in medias_gestao:
            if media_gestao.media > maior_media:
                maior_media = media_gestao.media
                maior_grupo_gestao = media_gestao.nome
            if media_gestao.media < menor_media:
                menor_media = media_gestao.media
                menor_grupo_gestao = media_gestao.nome

        pdf_config_forca = self.__get_pdf_config(
            medias_gestao, self.ChartType.FORCA, maior_media
        )
        pdf_config_fraqueza = self.__get_pdf_config(
            medias_gestao, self.ChartType.FRAQUEZA, menor_media
        )

        return PDFHelper.generate_base64_image(
            title='FORÇA',
            file_name='forca_gestao_chart',
            chart_type=PDFHelper.ChartType.BAR,
            **pdf_config_forca
        ), PDFHelper.generate_base64_image(
            title='Fraqueza',
            file_name='fraqueza_gestao_chart',
            chart_type=PDFHelper.ChartType.LINE,
            **pdf_config_fraqueza
        ), maior_grupo_gestao, menor_grupo_gestao

    def generate_equipes_chart_png(
        self,
        formulario_id: int
    ) -> List[str]:
        medias_equipes = self.grupos_repo.get_media_repostas_grupo(
            formulario_id, Competencias.TipoImpacto.EQUIPES
        )
        maior_media = 0
        maior_grupo_equipes = None
        menor_media = 5
        menor_grupo_equipes = None

        for media_equipes in medias_equipes:
            if media_equipes.media > maior_media:
                maior_media = media_equipes.media
                maior_grupo_equipes = media_equipes.nome
            if media_equipes.media < menor_media:
                menor_media = media_equipes.media
                menor_grupo_equipes = media_equipes.nome
        pdf_config_forca = self.__get_pdf_config(
            medias_equipes, self.ChartType.FORCA, maior_media
        )
        pdf_config_fraqueza = self.__get_pdf_config(
            medias_equipes, self.ChartType.FRAQUEZA, menor_media
        )

        return PDFHelper.generate_base64_image(
            title='FORÇA',
            file_name='forca_equipe_chart',
            chart_type=PDFHelper.ChartType.BAR,
            **pdf_config_forca
        ), PDFHelper.generate_base64_image(
            title='Fraqueza',
            file_name='fraqueza_equipe_chart',
            chart_type=PDFHelper.ChartType.LINE,
            **pdf_config_fraqueza
        ), maior_grupo_equipes, menor_grupo_equipes

    def generate_performance_chart_png(
        self,
        formulario_id: int,
        tipo_performance: Competencias.TipoPerformance
    ) -> List[str]:
        valor_ref = 120
        max_range = 260
        label_performance = 'PD'

        if Competencias.TipoPerformance.ENGAJAMENTO == tipo_performance:
            valor_ref = 70
            max_range = 160
            label_performance = 'PE'
        elif Competencias.TipoPerformance.ORGANIZACAO == tipo_performance:
            valor_ref = 110
            max_range = 230
            label_performance = 'PO'

        total_performance = self.competencias_repo.get_total_repostas(
            formulario_id, tipo_performance
        )
        performance = [
            {
                'nome': label_performance,
                'cor': '#fb18d6',
                'media': total_performance,
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
                'x': [valor_ref],
                'y': [
                    d['nome']
                    for d in performance
                ],
                'color': '#ffc000',
                'text': valor_ref
            },
            orientation=PDFHelper.BarChartType.HORIZONTAL,
            layout={
                'xaxis': {
                    'range': [0, max_range]
                },
                'width': 585,
                'height': 240,
                'margin': {
                    'l': 10,
                    'r': 10,
                    't': 60,
                    'b': 20,
                    'pad': 40,
                }
            }
        ), total_performance

    def generate_forca_chart_png(
        self,
        formulario_id: int
    ) -> str:
        media_forca = self.grupos_repo.get_media_repostas_grupo(
            formulario_id
        )
        pdf_config = self.__get_pdf_config(media_forca)

        return PDFHelper.generate_base64_image(
            title='Forca',
            file_name='forca_chart',
            **pdf_config
        )

    def _generate_painel_png(
        self,
        competencias: List[str]
    ) -> str:
        django_engine = engines['django']
        template = django_engine.from_string('''
            {% for competencia in competencias %}
                <p>{{ competencia }}</p>
            {% endfor %}
        ''')
        html = template.render({
            'competencias': competencias
        })
        css = '''
            html, body{background-color: #b4c6e7;padding-top:20px;}
            p{background-color:#44546a;color:#fff;border-radius:5px;font: 14px "Fira Sans", sans-serif;margin:15px auto;padding:10px 0;text-align:center;width:300px}
        '''
        str_time = datetime.now().strftime('%s')
        tmp_file_name = f'/tmp/painel_competencias_{str_time}.png'
        hti = Html2Image(
            size=(600, 400),
            custom_flags=[
                '--no-sandbox',
                '--headless',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-dev-shm-usage',
                '--hide-scrollbars'
            ]
        )
        hti.output_path = '/tmp/'
        hti.screenshot(
            html_str=html,
            css_str=css,
            save_as=tmp_file_name.split('/')[-1]
        )

        with open(tmp_file_name, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def generate_painel_forca_png(
        self,
        formulario_id: int,
        tipo_impacto: Competencias.TipoImpacto
    ) -> List:
        competencias = self.competencias_repo.get_forca_competencias(
            formulario_id, tipo_impacto
        )
        return self._generate_painel_png(competencias), competencias

    def generate_painel_fraqueza_png(
        self,
        formulario_id: int,
        tipo_impacto: Competencias.TipoImpacto
    ) -> list:
        competencias = self.competencias_repo.get_fraqueza_competencias(
            formulario_id, tipo_impacto
        )
        return self._generate_painel_png(competencias), competencias
