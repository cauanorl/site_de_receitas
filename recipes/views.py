from django.views.generic.base import TemplateView, View
from __localcode.main import make_recipe


class Home(TemplateView, View):
    template_name = 'recipes/pages/home.html'

    def get(self, request, *args, **kwargs):

        return self.render_to_response({
            'recipes': [make_recipe() for _ in range(16)],
            'is_list_page': True,
        })


class DetailRecipe(TemplateView, View):
    template_name = 'recipes/pages/detail.html'

    def get(self, request, pk, *args, **kwargs):
        return self.render_to_response({'recipe': make_recipe()})
