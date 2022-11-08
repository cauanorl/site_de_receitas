from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Category, Recipe


class Home(ListView):
    template_name = 'recipes/pages/home.html'
    queryset = Recipe.published.all()
    extra_context = {'title': 'Home'}
    context_object_name = 'recipes'


class DetailRecipe(DetailView):
    template_name = 'recipes/pages/detail.html'
    model = Recipe
    pk_url_kwarg: str = 'id'
    extra_context = {'is_detail_page': True}

    def get_object(self):
        obj = super().get_object()
        if not obj.is_published == True:
            raise Http404

        return obj


class FilterRecipesByCategory(TemplateView, View):
    template_name = "recipes/pages/home.html"

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        recipes = Recipe.published.filter(category__id=category_id)
        category_name = category.name

        return self.render_to_response({
            'recipes': recipes,
            'title': f'{category_name} - category',
            'category_name': category_name,
        })


class SearchRecipes(TemplateView, View):
    template_name = 'recipes/pages/home.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '').strip()

        if not query:
            return redirect('recipes:home')
        
        recipes = Recipe.published.filter(title__icontains=query)

        return self.render_to_response({
            'recipes': recipes,
            'title': f'Searching for {query}',
            'search': query
        })
