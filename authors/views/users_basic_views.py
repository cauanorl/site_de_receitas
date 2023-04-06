from django import forms

from django.shortcuts import redirect

from django.views.generic.base import TemplateView

from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator

from django.contrib import messages, auth
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.decorators import login_required

from ..forms import RegisterForm, LoginForm


class RegisterView(TemplateView):
    template_name = 'authors/pages/register_view.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('recipes:home')

        form = RegisterForm()

        return self.render_to_response({
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=self.request.POST)

        if form.is_valid():
            user: AbstractUser = form.save(commit=False)
            user.set_password(self.request.POST.get('password'))
            user.save()
            messages.success(
                self.request, _("Sua conta foi criada com sucesso"))
            auth.login(self.request, user)
            return redirect('recipes:home')

        return self.render_to_response({'form': form})


class LoginView(TemplateView):
    form_class = LoginForm
    template_name = 'authors/pages/login.html'

    def get(self, *args, **kwargs):
        form = self.form_class()
        if self.request.user.is_authenticated:
            return redirect('recipes:home')
        return self.render_to_response({'form': form})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(
                self.request, username=username, password=password)

            if user:
                auth.login(self.request, user)
                return redirect('authors:dashboard')

            # TODO: Mudar essas válidações para o form.py
            if not User.objects.filter(username=username).exists():
                form.add_error(
                    'username',
                    forms.ValidationError(
                        "Esse nome de usuário não existe", code="invalid"))
            else:
                form.add_error(
                    'password',
                    forms.ValidationError(
                        "Sua senha está incorreta", code="invalid"))
        else:
            messages.error(self.request, 'Erro ao validar o formulário')

        return self.render_to_response({'form': form})


@method_decorator(login_required, name="dispatch")
class LogoutView(TemplateView):

    def get(self, *args, **kwargs):
        auth.logout(self.request)

        return redirect("recipes:home")
