from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class EsqueceuForm(forms.Form):
    email = forms.EmailField(label='Email', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'formEsqueceu'
        self.helper.form_class = 'user'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Enviar', css_class='btn btn-primary btn-user btn-block'))


class CadastroUsuarioForm(forms.Form):
    nome = forms.CharField(label='Nome', required=False)
    sobre_nome = forms.CharField(label='Sobrenome', required=False)
    email = forms.EmailField(label='Email', required=False, widget=forms.TextInput(attrs={'type': 'email'}))
    confirmacao_email = forms.EmailField(label='Confirmação Email', required=False, widget=forms.TextInput(attrs={'type': 'email'}))
    senha = forms.CharField(label='Senha', required=False, widget=forms.PasswordInput())
    confirmacao_senha = forms.CharField(label='Confirmação Senha', required=False, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'formCadastroUsuario'
        self.helper.form_class = 'user'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Cadastar', css_class='btn btn-primary btn-user btn-block'))