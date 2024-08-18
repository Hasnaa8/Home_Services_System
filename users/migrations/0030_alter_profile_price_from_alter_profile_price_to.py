# Generated by Django 5.0.6 on 2024-06-14 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0029_alter_fav_options_alter_fav_fav_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='price_from',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='price_to',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]