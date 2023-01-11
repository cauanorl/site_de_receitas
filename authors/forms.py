from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        labels = {
            'first_name': _('Nome'),
            'last_name': _('Sobrenome'),
            'username': _('Nome de usuário'),
            'password': _('Senha'),
            'email': _('E-mail'),
        }
        fields = [
            'first_name', 'last_name',
            'email', 'username', 'password'
        ]
        help_texts = {
            'username': ''
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': '',
                'id': 'username_id',
                'name': ''
            }),
            'password': forms.PasswordInput(attrs={
                'class': '',
                'id': 'password_id',
                'name': ''
            })
            
        }

    password2 = forms.CharField(
        max_length=200,
        label=_('Repetir senha'),
        widget=forms.PasswordInput(attrs={
            'class': '',
            'id': 'password2_id',
            'name': '',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder({
            'first_name': _('Digite seu primeiro nome'),
            'last_name': _('Digite seu último nome'),
            'username': _('Digite seu nome de usuário'),
            'email': _('Digite seu email'),
            'password': _('Digite uma senha'),
            'password2': _('Repita a senha')
        })

    def add_placeholder(self, fields_and_values: dict = {}):
        for field, placeholder_value in fields_and_values.items():
            field_widget = self.fields.get(field).widget
            field_widget.attrs['placeholder'] = placeholder_value

    def clean_username(self, *args, **kwargs):
        username: str = self.cleaned_data.get('username')

        if username.isnumeric():
            self.add_error(
                'username',
                ValidationError(
                    _('Nome de usuário deve conter pelo menos uma letra'),
                    code="invalid"
                )
            )

        if len(username) < 6:
            self.add_error(
                'username',
                ValidationError(
                    _('Nome de usuário deve conter mais de 6 caracteres'),
                    code="min_length"
                )
            )

        return username

    def clean_password(self, *args, **kwargs):
        password: str = self.cleaned_data.get('password')

        if len(password) < 8:
            self.add_error(
                'password',
                ValidationError(
                    'A senha deve conter no minímo 8 caracteres',
                    code="invalid"
                ))

        return password

    def clean_password2(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            self.add_error(
                'password2',
                ValidationError(
                    _('As senhas não conferem'),
                    code="invalid"
                ))

        return password2
