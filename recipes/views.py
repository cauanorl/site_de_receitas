from django.views.generic.base import TemplateView, View
from django.http import HttpResponse

# Create your views here.
class Home(TemplateView, View):
    template_name = 'recipes/home.html'
    
    def get(self, request, *args, **kwargs):
        return self.render_to_response({'teste': 'home'})


class About(TemplateView, View):
    template_name: str = ''
    
    def get(self, request, *args, **kwargs):
        return HttpResponse("About")
