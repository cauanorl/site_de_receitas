from django.urls import path
from . import views


app_name = 'authors'

urlpatterns = [
    path('', views.RegisterView.as_view(), name="none"),
]
