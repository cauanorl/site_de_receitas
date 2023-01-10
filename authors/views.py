from django.views.generic.base import View, TemplateView
from .forms import RegisterForm


# Create your views here.
class RegisterView(TemplateView, View):
    template_name = 'authors/pages/register_view.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()

        return self.render_to_response({
            'form': form,
        })
    
    def post(self, request, *args, **kwargs):
        form = RegisterForm(data=request.POST)

        return self.render_to_response({
            'form': form            
        })
