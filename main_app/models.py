from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User


# Create your models here.
class Apod(models.Model):
    title = models.CharField(max_length=100, default='APOD')      
    url = models.URLField(default='')
    date = models.DateField()
    explanation = models.TextField(max_length=3000)
    users = models.ManyToManyField(User, related_name='apods')
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Album(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    apod_photos = models.ManyToManyField(Apod)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Link users to album with foreign key -> then migrate

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('albums_detail', kwargs={'album_id': self.id})
    
    class Meta:
        ordering = ['name']


# class Constellation(models.Model):


class Satellite(models.Model):
    name = models.CharField(max_length=50)    
    type = models.CharField(max_length=50)    
    description = models.TextField(max_length=300)  


