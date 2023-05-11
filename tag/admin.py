from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'target']
    list_display_links = ['id', 'name', 'target']
    search_fields = ["id", "name"]
    list_per_page = 10
    ordering = ['-id', 'name']
    prepopulated_fields = {"slug": ("name",)}
