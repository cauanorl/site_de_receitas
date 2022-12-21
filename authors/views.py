from django.views.generic.base import View, TemplateView


# Create your views here.
class RegisterView(TemplateView, View):
    template_name = 'authors/pages/register_view.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            
        })
