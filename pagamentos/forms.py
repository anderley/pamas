from django import forms


class PagamentoForm(forms.Form):

    cartao = forms.CharField(label="Número do Cartão", required=True, max_length=19,
        widget=forms.TextInput(attrs={
            'placeholder': '0000 0000 0000 0000',
            'class': 'form-control',
        })
    )
    nome = forms.CharField(label="Nome complemento", required=True, help_text='Conforme aparece no cartão.') # noqa
    vencimento = forms.CharField(label="Data de vencimento", required=True, help_text='Mês / Ano', max_length=5,
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/AA',
            'class': 'form-control',
        })) # noqa
    codigo = forms.CharField(label="Código de segurança", required=True, help_text="CVV") # noqa
    cpf = forms.CharField(label="CPF", required=True)
    plano = forms.CharField(widget=forms.HiddenInput(), required=False)

    fields = ['cartao', 'nome', 'vencimento', 'codigo', 'cpf', 'plano']

    def __init__(self, *args, **kwargs):
        plano_id = kwargs.pop('plano_id', None)
        super().__init__(*args, **kwargs)
        if plano_id:
            self.fields['plano'].initial = plano_id
