from django.utils.translation import gettext as _
from django.urls import path
from . import views


app_name = 'recipes'

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    
    path(
        _('recipes/search/'),
        views.SearchRecipes.as_view(),
        name="search",
    ),

    path(_('recipe/<int:id>/'), views.DetailRecipe.as_view(), name="detail"),

    path(
        _('recipe/category/<int:category_id>/'),
        views.FilterRecipesByCategory.as_view(),
        name="filter_by_category"
    ),
]
