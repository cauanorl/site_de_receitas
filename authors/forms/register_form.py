from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

import re


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2'
        ]

    username = forms.CharField(
        required=True,
        label="Nome de usuário",
        max_length=150,
        min_length=6,
        error_messages={
            'required': ('Nome de usuário não pode estar em branco'),
            'max_length': _('Nome de usuário deve conter no máximo 150 caracteres'),
            'min_length': _('Nome de usuário deve conter mais de 6 caracteres'),
        },
        widget=forms.TextInput(attrs={
            'placeholder': _('Digite seu nome de usuário'),
        })
    )

    first_name = forms.CharField(
        required=True,
        label="Nome",
        max_length=150,
        min_length=2,
        error_messages={
            'required': _('Nome não pode estar em branco'),
            'min_length': _('Primeiro nome deve conter mais que 2 caracteres'),
            'max_length': _('Nome deve conter no máximo 150 caracteres'),
        },
        widget=forms.TextInput(attrs={
            'placeholder': _('Digite seu primeiro nome'),
        })
    )

    last_name = forms.CharField(
        required=True,
        label=_("Sobrenome"),
        max_length=150,
        min_length=2,
        error_messages={
            'required': _('Sobrenome não pode estar em branco'),
            'min_length': _('Sobrenome deve conter mais que 2 caracteres'),
            'max_length': _('Sobrenome deve conter no máximo 150 caracteres'),
        },
        widget=forms.TextInput(attrs={
            'placeholder': _('Digite seu primeiro nome'),
        })
    )

    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        max_length=150,
        validators=[EmailValidator(message=_("Formato de email inválido"))],
        widget=forms.EmailInput(attrs={"placeholder": "Digite seu E-mail"}),
        error_messages={"required": "Email não pode estar em branco"}
    )

    password = forms.CharField(
        max_length=200,
        label=_('Senha'),
        error_messages={"required": _("Senha não pode estar em branco")},
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Digite uma senha'),
        })
    )

    password2 = forms.CharField(
        max_length=200,
        label=_('Repetir senha'),
        error_messages={"required": _("As senhas não conferem")},
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Repita a senha'),
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.required_fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
        ]
        self.add_placeholder({
            'last_name': _('Digite seu último nome'),
            'email': _('Digite seu email'),
        })

    def add_placeholder(self, fields_and_values: dict = {}):
        for field, placeholder_value in fields_and_values.items():
            field_widget = self.fields.get(field).widget
            field_widget.attrs['placeholder'] = placeholder_value

    def clean_first_name(self):
        first_name: str | None = self.cleaned_data.get("first_name")

        return self.strip_string(first_name)

    def clean_last_name(self):
        last_name: str | None = self.cleaned_data.get("last_name")

        return self.strip_string(last_name)

    def clean_username(self):
        username: str | None = self.cleaned_data.get('username')

        return self.strip_string(username)

    def clean_email(self):
        email: str | None = self.cleaned_data.get('email')
        email_already_exists = User.objects.filter(email=email).exists()

        email = self.strip_string(email)

        if email == '':
            self.add_error(
                'email',
                ValidationError(
                    _('Email não pode estar em branco'),
                    code="required"
                ))

        if email_already_exists:
            self.add_error(
                'email',
                ValidationError(
                    _('Este email já foi cadastrado'),
                    code="invalid"
                )
            )

        return email

    def clean_password(self, *args, **kwargs):
        password: str | None = self.cleaned_data.get('password')

        password = self.strip_string(password)

        match = re.match(
            r'(?=^.{8,}$)((?=.*\d)(?=.*\w+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$',
            password,
            flags=re.IGNORECASE
        )

        if not match:
            self.add_error(
                'password',
                ValidationError(
                    _('A senha deve conter letras e números'),
                    code="invalid"
                ))

        if len(password) < 8:
            self.add_error(
                'password',
                ValidationError(
                    _('A senha deve conter no minímo 8 caracteres'),
                    code="invalid"
                ))

        return password

    def clean_password2(self, *args, **kwargs):
        password: str = self.cleaned_data.get('password')
        password2: str = self.cleaned_data.get('password2')

        password2 = self.strip_string(password2)

        if password != password2:
            self.add_error(
                'password2',
                ValidationError(
                    _('As senhas não conferem'),
                    code="invalid"
                )
            )

        return password2

    @staticmethod
    def strip_string(string: str | None):
        if string is None:
            string = ""
        else:
            string = string.strip()

        return string
