import os

from django.shortcuts import get_object_or_404, redirect

from django.http import Http404

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.core.paginator import Paginator

from django.db.models import Q

from utils.pagination import make_pagination_range

from tag.models import Tag
from .models import Category, Recipe


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class AbstractPaginationRecipesListView(ListView):
    extra_context = {}

    def get_queryset(self):
        qs = Recipe.published.all()
        qs = qs.select_related("author", "category")
        qs = qs.prefetch_related("tags", "author__profile")

        return qs

    def set_pagination(
            self, queryset, context_object_name='object',
            number_of_pages=4, per_page=9, *args, **kwargs):

        paginator = Paginator(queryset, per_page)
        current_page = int(self.request.GET.get('page', 1))

        page_obj = paginator.get_page(current_page)
        page_range = make_pagination_range(
            page_range=paginator.page_range,
            number_of_pages=number_of_pages,
            current_page=current_page
        )

        self.extra_context.update({
            context_object_name: page_obj,
            'page_obj': page_obj,
            'page_range': page_range,
        })


class Home(AbstractPaginationRecipesListView):
    template_name = 'recipes/pages/home.html'
    extra_context = {'title': 'Home'}

    def get(self, *args, **kwargs):
        self.set_pagination(
            super().get_queryset(), 'recipes', per_page=PER_PAGE)
        return super().get(*args, **kwargs)


class DetailRecipe(DetailView):
    template_name = 'recipes/pages/detail.html'
    model = Recipe
    pk_url_kwarg: str = 'id'
    extra_context = {'is_detail_page': True}

    def get_object(self):
        obj = super().get_object()
        if not obj.is_published:
            raise Http404()

        return obj


class FilterRecipesByCategory(AbstractPaginationRecipesListView):
    template_name = "recipes/pages/home.html"

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        recipes = Recipe.published\
            .filter(category__id=category_id)\
            .select_related("author", "category")

        category_name = category.name

        self.set_pagination(recipes, 'recipes', per_page=PER_PAGE)

        self.extra_context.update({
            'title': f'{category_name} - category',
            'category_name': category_name,
        })

        return super().get(request, *args, **kwargs)


class SearchRecipes(AbstractPaginationRecipesListView):
    template_name = 'recipes/pages/home.html'
    extra_context = {'title': 'Searching'}

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q', '').strip()

        if not query:
            return qs

        self.extra_context.update({
            'title': f'Searching for "{query}"',
            'search': query,
        })

        return qs.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
        )

    def get(self, *args, **kwargs):
        if not self.request.GET.get('q'):
            return redirect('recipes:home')

        self.set_pagination(self.get_queryset(), 'recipes', per_page=PER_PAGE)

        return super().get(*args, **kwargs)


class TagListView(AbstractPaginationRecipesListView):
    template_name = 'recipes/pages/tag.html'
    extra_context = {'title': 'Searching'}

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(tags__slug=self.kwargs.get("slug", ''))

        title = Tag.objects.get(slug=self.kwargs.get('slug', ''))

        self.extra_context.update({
            'title': f'{title}'
        })

        return qs

    def get(self, *args, **kwargs):

        self.set_pagination(self.get_queryset(), 'recipes', per_page=PER_PAGE)

        return super().get(*args, **kwargs)
