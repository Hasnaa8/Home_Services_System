# Generated by Django 5.0.2 on 2024-04-27 17:56

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_alter_customer_options_alter_customer_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customer',
            new_name='Profile',
        ),
    ]