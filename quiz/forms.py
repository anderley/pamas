from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Perguntas, Contatos


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Senha", required=False, widget=forms.PasswordInput())

    class Meta:
        fields = (
			'username',
			'password',
		)


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
