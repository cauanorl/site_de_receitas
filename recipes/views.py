from django.views.generic.base import TemplateView, View
from django.http import HttpResponse

# Create your views here.
class Home(TemplateView, View):
    template_name = 'recipes/pages/home.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'teste': 'home'})


class DetailRecipe(TemplateView, View):
    template_name = 'recipes/pages/detail.html'

    def get(self, request, pk, *args, **kwargs):
        return self.render_to_response({})
