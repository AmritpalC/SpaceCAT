from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User

# Create your models here.
class Constellation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)