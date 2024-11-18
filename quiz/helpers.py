import base64
import plotly.graph_objs as go

from enum import Enum
from datetime import datetime
from typing import List, Dict


class PDFHelper:

    class BarChartType(Enum):
        VERTICAL = 'v'
        HORIZONTAL = 'h'

    @staticmethod
    def generate_bar_chart_image(
        title: str,
        file_name: str,
        orientation: BarChartType,
        data: dict,
        refereces: dict=None,
        layout: dict=None,
    ) -> str:
        fig_media_gestao = go.Figure()
        
        if refereces:
            fig_media_gestao.add_trace(go.Bar(
                showlegend=False,
                x=refereces['x'],
                y=refereces['y'],
                marker_color=refereces['color'],
                orientation=orientation.value
            ))

        fig_media_gestao.add_trace(go.Bar(
            showlegend=False,
            x=data['x'],
            y=data['y'],
            marker_color=data['color'],
            text=data['text'],
            textposition='outside',
            orientation=orientation.value
        ))
        fig_media_gestao.update_layout(
            title=title,
            bargroupgap=0.2,
            **layout
        )
        str_time = datetime.now().strftime('%s')
        tmp_file_name = f'/tmp/{file_name}_{str_time}.png'
        
        fig_media_gestao.write_image(tmp_file_name)

        return tmp_file_name
    
    @staticmethod
    def generate_base64_image(
        title: str,
        file_name: str,
        data: dict,
        orientation: BarChartType=BarChartType.VERTICAL,
        refereces: dict=None,
        layout: dict=None,
    ) -> str:
        tmp_file_name = PDFHelper.generate_bar_chart_image(
            title, file_name, orientation, data, refereces, layout
        )

        with open(tmp_file_name, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    
    
