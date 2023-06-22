from django.contrib import admin

# Register your models here.
from .models import Album, Apod

admin.site.register(Album)
admin.site.register(Apod)