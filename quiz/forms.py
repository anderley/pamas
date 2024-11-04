from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Contatos, FomularioClientes, Perguntas, Respostas


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Senha", required=False, widget=forms.PasswordInput()) # noqa

    class Meta:
        fields = [
            'username',
            'password',
        ]


class PerguntasForm(forms.ModelForm):

    class Meta:
        model = Perguntas
        fields = ['descricao', 'competencia']


class EnviarFormularioForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)


class ContatosForm(forms.ModelForm):

    class Meta:
        model = Contatos
        fields = ['nome_completo', 'email', 'telefone']


VALORES_RESPOSTA = [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
]


class RespostasForm(forms.ModelForm):
    resposta = forms.ChoiceField(
        choices=VALORES_RESPOSTA,
        widget=forms.RadioSelect,
        label=None,
        required=True
    )

    def __init__(self, form_cliente_id, *args, **kwargs):
        self.form_cliente_id = form_cliente_id

        print(form_cliente_id)

        super().__init__(*args, **kwargs)

    class Meta:
        model = Respostas
        fields = ['resposta']
        exclude = ['pergunta', 'formulario', 'created_at', 'updated_at']


class FormularioForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'page_obj' in self.initial:
            for pergunta in self.initial['page_obj']:
                query = Respostas.objects.filter(
                    pergunta__id=pergunta.id,
                    formulario__id=self.initial['formulario_id']
                )
                resposta = query.first().resposta if query.exists() else None

                self.fields[f'pergunta_{pergunta.id}'] = forms.ChoiceField(
                    choices=VALORES_RESPOSTA,
                    widget=forms.RadioSelect,
                    label=pergunta.descricao,
                    required=True,
                    error_messages={'required': 'Campo obrigatório'},
                    initial=resposta
                )

    def save(self):
        cleaned_data = self.clean()
        formulario_id = self.initial['formulario_id'] if 'formulario_id' in self.initial else None

        if formulario_id:
            for key in cleaned_data.keys():
                pergunta_id = key.split('_')[1]
                Respostas.objects.update_or_create(
                    formulario=FomularioClientes(id=formulario_id),
                    pergunta=Perguntas(id=pergunta_id),
                    defaults={
                        'formulario': FomularioClientes(id=formulario_id),
                        'pergunta': Perguntas(id=pergunta_id),
                        'resposta': cleaned_data[key]
                    }
                )
