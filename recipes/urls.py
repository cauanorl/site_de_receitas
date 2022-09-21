from django.utils.translation import gettext as _
from django.urls import path
from . import views


app_name = 'recipes'

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
]
