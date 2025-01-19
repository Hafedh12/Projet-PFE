from django.db import models
from django.contrib.auth.models import User
import os
from django.urls import reverse


def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.profile_pic:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.user.username, ext)
    return os.path.join(upload_to, filename)
class Eleve(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=path_and_rename, verbose_name="Profile Picture", blank=True,default='media/Images/photo.jpg')
    id_eleve = models.AutoField(primary_key=True)
    date_de_naissance = models.DateField()
    anomalie = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=path_and_rename, verbose_name="Profile Picture", blank=True)
    id_enseignant = models.AutoField(primary_key=True)
    numero_telephone = models.BigIntegerField()
    first_login = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username



