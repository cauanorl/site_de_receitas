import os

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from recipes.models import Recipe


def delete_cover(instance: Recipe) -> None:
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        pass


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_instance = sender.objects.filter(pk=instance.pk).first()
    delete_cover(old_instance)


@receiver(pre_save, sender=Recipe)
def recipe_cover_save(sender, instance, **kwargs):
    old_instance = sender.objects.filter(pk=instance.pk).first()

    if old_instance is None:
        return

    is_new_image = old_instance.cover != instance.cover

    if is_new_image:
        delete_cover(old_instance)
