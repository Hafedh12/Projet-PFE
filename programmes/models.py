from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from utilisateurs.models import Enseignant, Eleve
import os
from django.urls import reverse



def save_cours(instance, filename):
    upload_to = 'Resources/'
    ext = filename.split('.')[-1]
    if instance.id_cours:
        filename = 'Cours/{}/{}.{}'.format(instance.nom_cours, instance.nom_cours, ext)
    else:
        filename = 'Cours/{}/{}'.format(instance.nom_cours, filename)
    return os.path.join(upload_to, filename)

def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

class Cours(models.Model):
    id_cours = models.AutoField(primary_key=True)
    slug = models.SlugField(null=True, blank=True)
    nom_cours = models.CharField(max_length=20, unique=True)
    fichier = models.FileField(upload_to=save_cours, verbose_name="fichier")
    date_ajout = models.DateTimeField(auto_now_add=True)
    créer_par = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cours {self.id_cours} / {self.nom_cours}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"cours-{self.nom_cours}-{self.id_cours}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.fichier:
            delete_file(self.fichier.path)
        parent_dir = os.path.dirname(self.fichier.path)
        if not os.listdir(parent_dir):
            os.rmdir(parent_dir)
        super().delete(*args, **kwargs)


def save_exercice(instance, filename):
    upload_to = 'Resources/'
    ext = filename.split('.')[-1]
    if instance.nom_exercice:
        filename = 'Exercice/{}/{}.{}'.format(instance.nom_exercice, instance.nom_exercice, ext)
    else:
        filename = 'Exercice/{}/{}'.format(instance.nom_exercice, filename)
    return os.path.join(upload_to, filename)

def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

class Exercice(models.Model):
    id_exercice = models.AutoField(primary_key=True)
    nom_exercice = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(null=True, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    créer_par = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    fichier = models.FileField(upload_to=save_exercice, verbose_name="exercice", blank=True)

    def __str__(self):
        return f"Exercice {self.nom_exercice}"

    def get_absolute_url(self):
        return reverse('exercice_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"exercice-{self.nom_exercice}-{self.id_exercice}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.fichier:
            delete_file(self.fichier.path)
        parent_dir = os.path.dirname(self.fichier.path)
        if not os.listdir(parent_dir):
            os.rmdir(parent_dir)
        super().delete(*args, **kwargs)
def save_solution(instance, filename):
    upload_to = 'Resources/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.exercice:
        filename = 'Solution/solution {}/solution {}.{}'.format(instance.exercice.nom_exercice, instance.exercice.nom_exercice, ext)
    return os.path.join(upload_to, filename)

def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

class Solution(models.Model):
    slug = models.SlugField(null=True, blank=True)
    id_solution = models.AutoField(primary_key=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    créer_par = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to=save_solution, verbose_name="solution", blank=True)

    def __str__(self):
        return f"Solution {self.exercice.nom_exercice}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"solution-{self.exercice.nom_exercice}-{self.id_solution}")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.fichier:
            delete_file(self.fichier.path)
        parent_dir = os.path.dirname(self.fichier.path)
        if not os.listdir(parent_dir):
            os.rmdir(parent_dir)
        super().delete(*args, **kwargs)
def delete_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

def save_reponce(instance, filename):
    upload_to = 'Resources/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.exercice:
        filename = 'Reponse/Reponsee {}/créer par {}.{}'.format(instance.exercice.nom_exercice, instance.créer_par.username, ext)
    return os.path.join(upload_to, filename)

class Status(models.Model):
    slug = models.SlugField(null=True, blank=True)
    id_status = models.AutoField(primary_key=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    créer_par = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to=save_reponce, verbose_name="reponce", blank=True)

    def __str__(self):
        return f"Reponce {self.exercice.nom_exercice}/créer par {self.créer_par.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.exercice.nom_exercice)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.fichier:
            delete_file(self.fichier.path)
        parent_dir = os.path.dirname(self.fichier.path)
        if not os.listdir(parent_dir):
            os.rmdir(parent_dir)
        super().delete(*args, **kwargs)


