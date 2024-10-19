from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class EsqueceuForm(forms.Form):
    email = forms.EmailField(label='Email', required=False)


class CadastroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label='Nome', required=True)
    last_name = forms.CharField(label='Sobrenome', required=True)
    email = forms.EmailField(label='Email', required=True, widget=forms.TextInput(attrs={'type': 'email'}))
    password1 = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirmação Senha', required=True, widget=forms.PasswordInput())

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

        print(user)
        
        if commit:
            user.save()
            
        return user