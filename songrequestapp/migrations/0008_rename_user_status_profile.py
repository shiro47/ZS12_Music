# Generated by Django 4.1.5 on 2023-02-09 01:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('songrequestapp', '0007_user_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_status',
            new_name='Profile',
        ),
    ]
