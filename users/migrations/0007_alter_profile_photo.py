# Generated by Django 5.0.3 on 2024-04-30 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='default.jfif', upload_to='static/images/profiles/'),
        ),
    ]