from django import forms

from planos.models import Planos


class PagamentoForm(forms.Form):

    PARCELAS_CHOICES = [(i, str(i)) for i in range(1, 13)]

    cartao = forms.CharField(
        label="Número do Cartão", required=True,
        max_length=19, widget=forms.TextInput(attrs={
            'placeholder': '0000 0000 0000 0000',
            'class': 'form-control',
        })
    )
    nome = forms.CharField(label="Nome complemento", required=True, help_text='Conforme aparece no cartão.') # noqa
    vencimento = forms.CharField(
        label="Data de vencimento", required=True, help_text='Mês / Ano',
        max_length=7, widget=forms.TextInput(attrs={
            'placeholder': 'MM/AAAA',
            'class': 'form-control',
        })) # noqa
    codigo = forms.CharField(label="Código de segurança", required=True, help_text="CVV") # noqa
    cpf = forms.CharField(label="CPF", required=True)
    plano = forms.CharField(widget=forms.HiddenInput(), required=False)
    parcelas = forms.ChoiceField(
        choices=PARCELAS_CHOICES, label='Número de Parcelas'
    )

    fields = ['cartao', 'nome', 'vencimento', 'codigo', 'cpf', 'plano']

    def __init__(self, *args, **kwargs):
        plano_id = kwargs.pop('plano_id', None)
        super().__init__(*args, **kwargs)
        if plano_id:
            plano = Planos.objects.get(id=plano_id)
            self.fields['plano'].initial = plano_id
            self.fields['parcelas'].choices = [
                (i, str(i)) for i in range(1, plano.parcelas + 1)
            ]
