from django import forms

from .models import Planos


class PlanosForm(forms.ModelForm):

    class Meta:
        model = Planos
        fields = [
            'titulo', 'descricao', 'cod_cor',
            'imagem', 'num_formularios', 'valor', 'parcelas'
        ]
