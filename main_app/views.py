from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Album, Apod, Satellite
from .forms import ApodForm, SavingForm

import requests
import environ

# New user
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# ? Import the login_required decorator
from django.contrib.auth.decorators import login_required
# to protect any function that requires a user to be logged in, add:
# @login_required above the function

# ? Authorisation for Class-based views - to be added when we have them
# from django.contrib.auth.mixins import LoginRequiredMixin
# importing above, we then add this to the class function like this e.g.
# class CatCreate(LoginRequiredMixin, CreateView):

# Initialising env
env = environ.Env()
environ.Env.read_env()

# Create your views here.
def home(request):
  # Current Time and Location api
  api_key = '7f8e23bcf09d466893f5ac68bfb5b53b'  # IP Geolocation API key
  url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}'

  response = requests.get(url)
  data = response.json()

  current_datetime = data['time_zone']['current_time']
  location = data['country_code2']
  city = data['city']

  context = {
      'current_datetime': current_datetime.split('.')[0],
      'location': location,
      'city': city
  }
  return render(request, 'home.html', context)
# Root URL for APIs
ROOT_URL = env('ROOT_URL')

# APOD Key
token = env('APOD_KEY')

# Sign up 
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# Create your views here.

def about(request):
  return render(request, 'about.html')

def satellites_index(request):
  satellites = Satellite.objects.all()
  return render(request, 'satellites/index.html', {
    'satellites': satellites
  })


# ? APODs

def apod_index(request):
  selected_date = request.GET.get('date')
  if not selected_date:
    return render(request, 'apod/index.html', { 'imageData': None })

  url = f"{ROOT_URL}/planetary/apod?api_key={token}&date={selected_date}"
  response = requests.get(url)
  image_data = response.json()
  # print(image_data)
  return render(request, 'apod/index.html', { 'imageData': image_data })

def apod_detail(request, apod_id):
  apod = Apod.objects.get(id=apod_id)
  print(apod)
  return render(request, 'apod/detail.html', {
    'apod': apod
  })

def apod_all(request):
  apods = Apod.objects.all()
  return render(request, 'apod/all.html', {
    'apods': apods
  })

def apod_delete(request, apod_id):
  apod = Apod.objects.get(id=apod_id)
  apod.delete()
  return redirect('apod_all')
  
def apod_save(request):
  print('HIT APODSAVE')
  selected_date = request.GET.get('date')
  print('SELECTEDDATE', selected_date)
  if not selected_date:
    return render(request, 'apod/index.html', { 'imageData': None })
  
  try:
    Apod.objects.get(date=selected_date)
    print('APOD already saved')
    return render(request, 'apod/index.html', { 'imageData': None, 'error': 'Picture already saved'})
  except Apod.DoesNotExist:
    url = f"{ROOT_URL}/planetary/apod?api_key={token}&date={selected_date}"
    response = requests.get(url)
    image_data = response.json()
    print(image_data)
    
    if image_data:
      Apod.objects.create(
        title=image_data['title'],
        url=image_data['url'],
        date=selected_date,
        explanation=image_data['explanation']
      )
      return render(request, 'apod/index.html', { 'imageData': image_data })
    else:
      return render(request, 'apod/index.html', { 'imageData': None })


# ? Albums

def albums_index(request):
  albums = Album.objects.all()
  return render(request, 'albums/index.html', {
    'albums': albums
  })

def albums_detail(request, album_id):
  album = Album.objects.get(id=album_id)
  id_list = album.apod_photos.all().values_list('id')
  # add other bits after
  apod_photos_album_doesnt_have = Apod.objects.exclude(id__in=id_list)
  return render(request, 'albums/detail.html', {
    'album': album, 'apod_photos': apod_photos_album_doesnt_have
  })

# CBVs for Albums
class AlbumCreate(CreateView):
  model = Album
  fields = ['name', 'description']

class AlbumUpdate(UpdateView):
  model = Album
  fields = ['name', 'description']

class AlbumDelete(DeleteView):
  model = Album
  success_url = '/albums'

def add_photo_to_album(request, album_id, apod_id):
  Album.objects.get(id=album_id).apod_photos.add(apod_id)
  return redirect('albums_detail', album_id=album_id)
                    
def remove_photo_from_album(request, album_id, apod_id):
  Album.objects.get(id=album_id).apod_photos.remove(apod_id)
  return redirect('albums_detail', album_id=album_id)

def add_photo(request, album_id):
  form = ApodForm(request.POST)
  if form.is_valid():
    new_photo = form.save(commit=False)
    new_photo.album_id = album_id
    new_photo.save()
    return redirect('albums_index, album_id=album_id')
  pass

