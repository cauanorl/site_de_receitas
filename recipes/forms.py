from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput({
        'class': 'password',
    }))

    class Meta:
        ...
