# Generated by Django 4.2.5 on 2023-09-24 06:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0004_rename_user_id_allowedproducts_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watchedlessons',
            unique_together={('lesson', 'watcher')},
        ),
    ]
