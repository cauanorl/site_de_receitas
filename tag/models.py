from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
import string
from random import SystemRandom


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    target_ct = models.ForeignKey(
        ContentType,
        related_name="tags",
        on_delete=models.CASCADE
    )
    target_id = models.CharField(max_length=300)
    target = GenericForeignKey("target_ct", "target_id")

    def get_object(self, *args, **kwargs):
        model = self.target_ct.model_class()
        object = model.objects.get(id=self.target_id)

        return object

    def __str__(self):
        return f"Tag: {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f"{self.name}-{self.pk}{rand_letters}")

        return super().save(*args, **kwargs)
