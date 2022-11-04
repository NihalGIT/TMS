from django.db import models

# Create your models here.
class Collection(models.Model):
    lieu=models.CharField(max_length=100)
    longitude=models.DecimalField(max_digits=20, decimal_places=10)
    latitude=models.DecimalField(max_digits=20, decimal_places=10)
class Distance(models.Model):
    lieu_1=models.CharField(max_length=100)
    lieu_2=models.CharField(max_length=100)
    dist=models.DecimalField(max_digits=20, decimal_places=10)
class inf(models.Model):
    matrice=models.CharField(max_length=300)
    dim=models.IntegerField()
class bound(models.Model):
        cost=models.DecimalField(max_digits=20, decimal_places=10)
        chemin=models.CharField(max_length=300)
