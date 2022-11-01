from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View

from .models import Category, Recipe


class Home(TemplateView, View):
    template_name = 'recipes/pages/home.html'

    def get(self, request, *args, **kwargs):
        recipes = Recipe.published.all()

        return self.render_to_response({
            'recipes': recipes,
            'title': 'Home',
        })


class DetailRecipe(TemplateView, View):
    template_name = 'recipes/pages/detail.html'

    def get(self, request, id, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=id, is_published=True)

        return self.render_to_response({
            'recipe': recipe,
            'is_detail_page': True,
        })


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
        query = self.request.GET.get('search')

        recipes = Recipe.published.filter(title__icontains=query)

        return self.render_to_response({
            'recipes': recipes,
            'title': f'Searching by {query}',
            'search': self.request.GET.get('search')
        })
