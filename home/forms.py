from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", required=False)
    senha = forms.CharField(label="Senha", required=False, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'formLogin'
        self.helper.form_class = 'user'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Entrar', css_class='btn btn-primary btn-user btn-block'))