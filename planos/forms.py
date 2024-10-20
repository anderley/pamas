from django import forms

from .models import Planos


class PlanosForm(forms.ModelForm):

    class Meta:
        model = Planos
        fields = ['titulo', 'descricao', 'num_formularios', 'valor']
