from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

# Create your models here.
class Constellation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class Satellite(models.Model):
    name = models.CharField(max_length=50)    
    type = models.CharField(max_length=50)    
    description = models.TextField(max_length=300)  
    
class Apod(models.Model):
    name = models.CharField(max_length=50)      
    image = models.CharField(max_length=50)
    description = models.TextField(max_length=300)  
    date = models.DateField()   

class Album(models.Model):
    name = models.CharField(max_length=100) 
    date = models.DateField()

