from django import forms

from django.shortcuts import redirect

from django.urls import reverse
from django.http import Http404

from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView

from django.utils.translation import gettext as _

from django.contrib import messages, auth
from django.contrib.auth.models import AbstractUser, User
from django.contrib.auth.mixins import LoginRequiredMixin

from recipes.views import AbstractPaginationListView
from recipes.models import Recipe

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
            messages.success(
                self.request, _("Sua conta foi criada com sucesso"))
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
                return redirect('authors:dashboard')

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


class DashboardView(AbstractPaginationListView):
    template_name = "authors/pages/dashboard.html"
    context_object_name = 'recipes'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse("authors:login"))

        self.set_pagination(self.get_queryset(), 'recipes', per_page=5)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Recipe.objects \
            .filter(author=self.request.user, is_published=False) \
            .order_by('-updated_at')


class DashboardRecipeEdit(DetailView):
    template_name = "authors/pages/dashboard_recipe.html"
    model = Recipe
    pk_url_kwarg = "recipe_id"
    context_object_name = "recipe"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()

        if obj.author != user or obj.is_published or not user.is_authenticated:
            raise Http404()

        return super().get(request, *args, **kwargs)
