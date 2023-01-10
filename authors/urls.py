from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name = 'authors'

urlpatterns = [
    path(_('register/'), views.RegisterView.as_view(), name="register"),
]
