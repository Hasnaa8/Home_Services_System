# Generated by Django 5.0.2 on 2024-04-27 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_rename_is_craftsman_customer_craftsman_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='media\\photos'),
        ),
    ]
