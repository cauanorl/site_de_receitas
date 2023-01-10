from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django import forms


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        labels = {
            'first_name': _('Nome'),
            'last_name': _('Sobrenome'),
            'username': _('Nome de usuário'),
            'password': _('Senha'),
            'email': _('Email'),
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

    def clean_username(self, *args, **kwargs): ...

    def clean_password(self, *args, **kwargs): ...

    def clean_password2(self, *args, **kwargs): ...

    def full_clean(self) -> None:
        return super().full_clean()
