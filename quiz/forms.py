from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", required=False)
    password = forms.CharField(label="Senha", required=False, widget=forms.PasswordInput())

    class Meta:
        fields = (
			'username',
			'password',
		)
