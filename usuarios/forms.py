from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class EsqueceuForm(forms.Form):
    email = forms.EmailField(label='Email', required=False)


class CadastroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label='Nome', required=True)
    last_name = forms.CharField(label='Sobrenome', required=True)
    email = forms.EmailField(label='Email', required=True, widget=forms.TextInput(attrs={'type': 'email'})) # noqa
    password1 = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput()) # noqa
    password2 = forms.CharField(label='Confirmação Senha', required=True, widget=forms.PasswordInput()) # noqa

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(CadastroUsuarioForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
    password = forms.CharField(
        label='Senha',
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': (
            'Por favor, informe o email correto %(email)s e senha. Ambos os '
            'campos podem ser case-sensitive.'
        ),
        'inactive': 'Esta conta está inactiva.',
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields = {
            'email': self.fields['email'],
            'password': self.fields['password']
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    class Meta:
        model = User
        fields = ['email', 'password']
