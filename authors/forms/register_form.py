from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

import re


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        labels = {
            'last_name': _('Sobrenome'),
            'email': _('E-mail'),
        }
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
            'required': 'Este campo é obrigatório',
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
            'required': _('Este campo é obrigatório'),
            'min_length': _('Primeiro nome deve conter mais que 2 caracteres'),
            'max_length': _('Nome deve conter no máximo 150 caracteres'),
        },
        widget=forms.TextInput(attrs={
            'placeholder': _('Digite seu primeiro nome'),
        })
    )

    last_name = forms.CharField(
        required=True,
        label="Sobrenome",
        max_length=150,
        min_length=2,
        error_messages={
            'required': _('Este campo é obrigatório'),
            'min_length': _('Sobrenome deve conter mais que 2 caracteres'),
            'max_length': _('Sobrenome deve conter no máximo 150 caracteres'),
        },
        widget=forms.TextInput(attrs={
            'placeholder': _('Digite seu primeiro nome'),
        })
    )

    password = forms.CharField(
        max_length=200,
        label=_('Senha'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Digite uma senha'),
        })
    )

    password2 = forms.CharField(
        max_length=200,
        label=_('Repetir senha'),
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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_already_exists = User.objects.filter(email=email).exists()

        if email_already_exists:
            self.add_error(
                'email',
                ValidationError(
                    _('Este email já foi cadastrado'),
                    code="invalid"
                )
            )

        if len(email) > 150:
            self.add_error(
                'email',
                ValidationError(
                    _('Email não deve conter mais de 150 caracteres'),
                    code="max_length"
                )
            )
        
        return email

    def clean_password(self, *args, **kwargs):
        password: str = self.cleaned_data.get('password')

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

    def clean(self):
        for field_name in self.required_fields:
            field = self.cleaned_data.get(field_name)
            field = '' if field is None else field
            if len(field) <= 1:
                self.add_error(
                    field_name,
                    ValidationError(
                        _('Este campo é obrigatório'),
                        code='required'
                    ))

        return super().clean()
