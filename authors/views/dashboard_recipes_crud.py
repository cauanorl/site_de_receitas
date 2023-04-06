from django.shortcuts import redirect

from django.urls import reverse

from django.http import Http404

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from recipes.views import AbstractPaginationListView
from recipes.models import Recipe

from ..forms import RecipeForm


@method_decorator(login_required, name="dispatch")
class DashboardView(AbstractPaginationListView):
    template_name = "authors/pages/dashboard.html"
    context_object_name = 'recipes'

    def get(self, request, *args, **kwargs):

        self.set_pagination(self.get_queryset(), 'recipes', per_page=5)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Recipe.objects \
            .filter(author=self.request.user, is_published=False) \
            .order_by('-updated_at')


# TODO: Mudar para a UpdateView or FormView
@method_decorator(login_required, name="dispatch")
class DashboardRecipeEdit(DetailView):
    template_name = "authors/pages/dashboard_recipe.html"
    model = Recipe
    pk_url_kwarg = "recipe_id"
    context_object_name = "recipe"
    extra_context = {}
    form_class = RecipeForm

    def get(self, request, *args, **kwargs):
        user = self.request.user
        obj = self.get_object()

        if obj.author != user or obj.is_published or not user.is_authenticated:
            raise Http404()

        form = self.form_class(instance=obj)

        self.extra_context.update({'form': form})
        return super().get(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        obj = self.get_object()
        form = self.form_class(
            data=self.request.POST,
            files=self.request.FILES,
            instance=obj
        )

        if form.is_valid() and self.request.user.is_authenticated:
            form.save()
            messages.success(
                self.request, _("Sua receita foi atualizada com sucesso!"))

        return self.render_to_response({
            'form': form,
            'recipe': obj
        })


# TODO: Mudar para a FormView
@method_decorator(login_required, name="dispatch")
class DashboardRecipeCreate(TemplateView):
    template_name = "authors/pages/dashboard_recipe.html"
    form_class = RecipeForm

    def get(self, *args, **kwargs):
        form = self.form_class()

        return self.render_to_response({"form": form})

    def post(self, *args, **kwargs):
        form = self.form_class(
            data=self.request.POST,
            files=self.request.FILES
        )

        if form.is_valid():
            recipe: Recipe = form.save(commit=False)

            recipe.author = self.request.user
            recipe.are_preparation_time_html = False

            recipe.save()
            messages.success(self.request, _("Receita criada com sucesso!"))

            return redirect(reverse("authors:dashboard"))

        messages.error(
            self.request, _("Ocorreu um erro na criação da receita"))

        return self.render_to_response({"form": form})


# TODO: Mudar para DeleteView
@method_decorator(login_required, name="dispatch")
class DashboardRecipeDelete(DetailView):
    model = Recipe
    pk_url_kwarg = 'recipe_id'

    def post(self, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user

        if not obj:
            raise Http404()

        if obj.author == user:
            obj.delete()
            messages.success(
                self.request, "Sua receita foi apagada com sucesso")

        return redirect(reverse("authors:dashboard"))
