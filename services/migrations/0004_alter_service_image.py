# Generated by Django 5.0.3 on 2024-03-19 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_service_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='image',
            field=models.ImageField(upload_to='photos/%y/%m/%d'),
        ),
    ]
