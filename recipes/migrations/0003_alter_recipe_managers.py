# Generated by Django 4.1.1 on 2022-10-04 00:01

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220929_1356'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='recipe',
            managers=[
                ('published', django.db.models.manager.Manager()),
            ],
        ),
    ]
