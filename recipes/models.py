from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from tag.models import Tag


class PublishedManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True).order_by('-id')

        return qs


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    objects = models.Manager()
    published = PublishedManager()

    title = models.CharField(max_length=150, verbose_name=_("Title"))
    description = models.CharField(max_length=165, verbose_name=_("Description"))
    slug = models.SlugField(unique=True)
    preparation_time = models.PositiveIntegerField(verbose_name=_("Preparation time"))
    preparation_time_unit = models.CharField(
        choices=[
            ('M', _('Minutes')),
            ('H', _('Hours')),
        ], max_length=1)

    servings = models.PositiveIntegerField()
    servings_unit = models.CharField(
        max_length=65,
        choices=[
            ("O", _("Person")),  # One
            ("M", _("People"))  # Many
        ]
    )
    preparation_steps = models.TextField()
    are_the_preparation_steps_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        default=False,
        verbose_name=_("published"))
    cover = models.ImageField(upload_to="recipes/covers/%Y/%m/%d/", verbose_name=_("Image"))

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes")

    tags = GenericRelation(
        Tag,
        related_query_name="recipes",
        object_id_field="target_id",
        content_type_field="target_ct",
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("recipes:detail", kwargs={"id": self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + f"-{self.pk}"

        return super().save(*args, **kwargs)
