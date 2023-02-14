from django.views.generic.base import View, TemplateView
from django.utils.translation import gettext as _
from django.shortcuts import redirect

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import AbstractUser

from .forms import RegisterForm


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
            login(self.request, user)
            return redirect('recipes:home')

        return self.render_to_response({'form': form})


class LoginView(TemplateView, View):
    template_name = 'authors/pages/login.html'

    def get(self, *args, **kwargs):
        return self.render_to_response({})
    
    def post(self, *args, **kwargs):
        return self.render_to_response({})
