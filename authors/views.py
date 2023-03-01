from django.views.generic.base import View, TemplateView
from django.utils.translation import gettext as _
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django import forms
from django.contrib import messages, auth
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, LoginForm


class RegisterView(TemplateView, View):
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
            messages.success(self.request, _("Sua conta foi criada com sucesso"))
            auth.login(self.request, user)
            return redirect('recipes:home')

        return self.render_to_response({'form': form})


class LoginView(TemplateView, View):
    template_name = 'authors/pages/login.html'

    def get(self, *args, **kwargs):
        form = LoginForm()
        if self.request.user.is_authenticated:
            return redirect('recipes:home')
        return self.render_to_response({'form': form})
    
    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(
                self.request, username=username, password=password)

            if user:
                auth.login(self.request, user)
                return redirect('recipes:home')

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


class LogoutView(LoginRequiredMixin, View):
    login_url = "authors:login"
    redirect_field_name = 'next'

    def get(self, *args, **kwargs):
        auth.logout(self.request)

        return redirect("recipes:home")
