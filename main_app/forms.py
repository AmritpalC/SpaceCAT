from django.forms import ModelForm
from .models import Apod

class ApodForm(ModelForm):
    class Meta:
        model = Apod
        fields = ['title', 'date', 'url']
