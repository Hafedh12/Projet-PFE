# Generated by Django 5.0.3 on 2024-04-18 12:12

import django.db.models.deletion
import programmes.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id_cours', models.AutoField(primary_key=True, serialize=False)),
                ('nom_cours', models.CharField(max_length=10)),
                ('video', models.FileField(blank=True, null=True, upload_to=programmes.models.save_cours, verbose_name='Video')),
                ('fichier', models.FileField(blank=True, upload_to=programmes.models.save_cours, verbose_name='fichier')),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('créer_par', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id_exercice', models.AutoField(primary_key=True, serialize=False)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField()),
                ('finish_time', models.DateTimeField()),
                ('fichier', models.FileField(blank=True, upload_to=programmes.models.save_exercice, verbose_name='exercice')),
                ('créer_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id_solution', models.AutoField(primary_key=True, serialize=False)),
                ('type_fichier', models.CharField(max_length=100)),
                ('date_ajout', models.DateTimeField(auto_now_add=True)),
                ('fichier', models.FileField(blank=True, upload_to=programmes.models.save_solution, verbose_name='solution')),
                ('créer_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('exercice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programmes.exercice')),
            ],
        ),
    ]
