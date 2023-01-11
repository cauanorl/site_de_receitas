from django.views.generic.base import View, TemplateView
from .forms import RegisterForm
from django.shortcuts import redirect


# Create your views here.
class RegisterView(TemplateView, View):
    template_name = 'authors/pages/register_view.html'

    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        self.form = RegisterForm(self.request.session.get('register_post'))

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'form': self.form,
        })
    
    def post(self, request, *args, **kwargs):
        self.request.session['register_post'] = request.POST
        self.request.session.save()

        return redirect('authors:register')