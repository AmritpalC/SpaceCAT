from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('albums_detail', kwargs={'album_id': self.id}) 


class Apod(models.Model):
    title = models.CharField(max_length=100, default='APOD')      
    url = models.URLField(default='')
    date = models.DateField()
    # album = models.ForeignKey(Album, on_delete=models.CASCADE)


# class Constellation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)


class Satellite(models.Model):
    name = models.CharField(max_length=50)    
    type = models.CharField(max_length=50)    
    description = models.TextField(max_length=300)  


