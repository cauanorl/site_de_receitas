from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, View
from .models import Category, Recipe


class Home(TemplateView, View):
    template_name = 'recipes/pages/home.html'

    def get(self, request, *args, **kwargs):
        recipes = Recipe.objects.filter(is_published=True).order_by('-id')

        return self.render_to_response({
            'recipes': recipes,
        })


class DetailRecipe(TemplateView, View):
    template_name = 'recipes/pages/detail.html'

    def get(self, request, id, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=id)

        return self.render_to_response({
            'recipe': recipe,
            'is_detail_page': True,
        })


class FilterRecipesByCategory(TemplateView, View):
    template_name = "recipes/pages/home.html"

    def get(self, request, category_id, *args, **kwargs):
        recipes = Recipe.objects.filter(category__id=category_id)
        category_name = get_object_or_404(Category, id=category_id).name
        
        return self.render_to_response({
            'recipes': recipes,
            'category_name': category_name
        })
