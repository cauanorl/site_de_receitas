from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ['id', 'title', 'author', "category", 'is_published']
    search_fields = ['title', "author", "category", "id", "description"]
    list_filter = [
        "is_published",
        "category",
        'are_the_preparation_steps_html']
    list_per_page = 20
    list_editable = ['is_published']
    list_display_links = ['id', 'title', 'author']
    date_hierarchy = "updated_at"
    prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ("author",)
    ordering = ['-updated_at']

    fieldsets = (
        (_("Receita"), {
            'fields': (
                'title',
                "description",
                'category',
                "preparation_steps",
                "cover",
                ("preparation_time", "preparation_time_unit"),
                ("servings", "servings_unit"),
                'author',
            ),
            "description": _("Essa é uma receita feita por um usuário")
        }),
        (_('Outros campos'), {
            'classes': ('collapse',),
            'fields': (
                'is_published',
                "are_the_preparation_steps_html",
                'slug'
            ),
        }),
    )
