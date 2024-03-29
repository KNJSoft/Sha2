from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Fichier(models.Model):
    nom=models.CharField(max_length=200)
    path=models.FileField(upload_to="fichiers")
    hash=models.CharField(max_length=1024)
    user=models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    date_creation=models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    texte=models.TextField()
    hash=models.CharField(max_length=1024)