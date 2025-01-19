# Generated by Django 5.0.3 on 2024-05-24 10:37

import utilisateurs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0005_enseignant_first_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eleve',
            name='profile_pic',
            field=models.ImageField(blank=True, default='media/Image/photo.jpg', upload_to=utilisateurs.models.path_and_rename, verbose_name='Profile Picture'),
        ),
    ]
