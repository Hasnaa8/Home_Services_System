# Generated by Django 5.0.6 on 2024-08-22 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='rate',
            new_name='rating',
        ),
    ]