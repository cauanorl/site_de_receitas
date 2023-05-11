from django.urls import path
from django.utils.translation import gettext as _
from . import views


app_name = 'authors'

urlpatterns = [
    path(_('register/'), views.RegisterView.as_view(), name="register"),
    path(_('login/'), views.LoginView.as_view(), name="login"),
    path(_('logout/'), views.LogoutView.as_view(), name="logout"),
    path(_('dashboard/'), views.DashboardView.as_view(), name="dashboard"),

    path(
        _('dashboard/recipe/create/'),
        views.DashboardRecipeCreate.as_view(),
        name="dashboard_recipe_create"
    ),

    path(
        _('dashboard/recipe/edit/<int:recipe_id>/'),
        views.DashboardRecipeEdit.as_view(),
        name="dashboard_recipe_edit"
    ),

    path(
        _('dashboard/recipe/delete/<int:recipe_id>/'),
        views.DashboardRecipeDelete.as_view(),
        name="dashboard_recipe_delete"
    ),

    path("profile/<int:id>/", views.ProfileView.as_view(), name="profile")
]
