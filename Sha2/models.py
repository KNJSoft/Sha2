from django.db import models

# Create your models here.
class Fichier(models.Model):
    nom=models.CharField(max_length=200)
    path=models.FileField(upload_to="fichiers")
    hash=models.CharField(max_length=1024)

class Message(models.Model):
    texte=models.TextField()
    hash=models.CharField(max_length=1024)