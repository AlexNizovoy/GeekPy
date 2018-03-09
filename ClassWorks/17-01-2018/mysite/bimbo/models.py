from django.db import models

# Create your models here.
class Project(models.Model):
    photo = models.BinaryField()
    name = models.CharField(max_length=200)
    blurb = models.CharField(max_length=200)
    goal = models.CharField(max_length=200)
    pledged = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    usd_pledged = models.FloatField()
