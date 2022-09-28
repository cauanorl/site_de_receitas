from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.PositiveIntegerField()
    preparation_time_unit = models.CharField(
        choices=[
            ('M', _('Minutes')),
            ('H', _('Hours')),
        ], max_length=1)

    servings = models.PositiveIntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to="recipes/covers/%Y/%m/%d/")

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes")
    
    def __str__(self):
        return self.title
