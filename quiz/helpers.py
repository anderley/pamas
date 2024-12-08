import base64
from datetime import datetime
from enum import Enum

import plotly.graph_objs as go


class PDFHelper:

    class ChartType(Enum):
        BAR = 'Bar'
        LINE = 'Line'

    class BarChartType(Enum):
        VERTICAL = 'v'
        HORIZONTAL = 'h'

    @staticmethod
    def generate_bar_chart_image(
        title: str,
        file_name: str,
        orientation: BarChartType,
        data: dict,
        refereces: dict = None,
        layout: dict = None,
    ) -> str:
        fig_bar_chart = go.Figure()

        if refereces:
            fig_bar_chart.add_trace(go.Bar(
                showlegend=False,
                x=refereces['x'],
                y=refereces['y'],
                text=refereces['text'],
                textposition='outside',
                marker_color=refereces['color'],
                orientation=orientation.value
            ))

        fig_bar_chart.add_trace(go.Bar(
            showlegend=False,
            x=data['x'],
            y=data['y'],
            marker_color=data['color'],
            text=data['text'],
            textposition='outside',
            orientation=orientation.value
        ))
        fig_bar_chart.update_layout(
            title={
                'text': title,
                'font': {
                    'family': 'Arial',
                    'size': 20,
                    'weight': 800
                },
                'y': 0.85,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            bargroupgap=0.2,
            **layout
        )
        str_time = datetime.now().strftime('%s')
        tmp_file_name = f'/tmp/{file_name}_{str_time}.png'

        fig_bar_chart.write_image(tmp_file_name)

        return tmp_file_name

    @staticmethod
    def generate_line_chart_image(
        title: str,
        file_name: str,
        data: dict,
        layout: dict = None,
    ) -> str:
        fig_line_chart = go.Figure()

        fig_line_chart.add_trace(go.Scatter(
            showlegend=False,
            x=data['x'],
            y=data['y'],
            mode='lines+markers+text',
            marker_color=data['color'],
            text=data['text'],
            textposition='middle center',
            line={
                'color': '#dddddd',
                'width': 6
            },
            marker={
                'size': 30
            },
        ))
        fig_line_chart.update_layout(
            title={
                'text': title,
                'font': {
                    'family': 'Arial',
                    'size': 20,
                    'weight': 800
                },
                'y': 0.85,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            **layout
        )
        str_time = datetime.now().strftime('%s')
        tmp_file_name = f'/tmp/{file_name}_{str_time}.png'

        fig_line_chart.write_image(tmp_file_name)

        return tmp_file_name

    @staticmethod
    def generate_base64_image(
        title: str,
        file_name: str,
        data: dict,
        chart_type: ChartType = ChartType.BAR,
        orientation: BarChartType = BarChartType.VERTICAL,
        refereces: dict = None,
        layout: dict = None,
    ) -> str:
        tmp_file_name = None

        if chart_type == PDFHelper.ChartType.BAR:
            tmp_file_name = PDFHelper.generate_bar_chart_image(
                title, file_name, orientation, data, refereces, layout
            )
        else:
            tmp_file_name = PDFHelper.generate_line_chart_image(
                title, file_name, data, layout
            )

        with open(tmp_file_name, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
