# Generated by Django 5.0.3 on 2024-05-07 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_profile_users_wishlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='users_wishlist',
            new_name='users_favourite',
        ),
    ]