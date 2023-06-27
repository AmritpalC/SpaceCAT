from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Album, Apod, Satellite
from .forms import ApodForm, SavingForm

import requests, random
import environ
import time
from ratelimiter import RateLimiter

# New user
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# ? Import the login_required decorator
from django.contrib.auth.decorators import login_required
# to protect any function that requires a user to be logged in, add:
# @login_required above the function

# ? Authorisation for Class-based views - to be added when we have them
from django.contrib.auth.mixins import LoginRequiredMixin
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
  #passing apod to homepage
  apods = Apod.objects.all()
  random_apod = random.choice(apods)
  context['random_apod'] = random_apod
  
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
# def apod_index(request):
#   selected_date = request.GET.get('date')
#   if not selected_date:
#     return render(request, 'apod/index.html', { 'imageData': None })

#   url = f"{ROOT_URL}/planetary/apod?api_key={token}&date={selected_date}"
#   response = requests.get(url)
#   image_data = response.json()
#   # print(image_data)
#   return render(request, 'apod/index.html', { 'imageData': image_data })

# @login_required
# def apod_save(request):
#   print('HIT APODSAVE')
#   selected_date = request.GET.get('date')
#   print('SELECTEDDATE', selected_date)
#   if not selected_date:
#     return render(request, 'apod/index.html', { 'imageData': None })
  
#   try:
#     Apod.objects.get(date=selected_date)
#     print('APOD already saved')
#     return render(request, 'apod/index.html', { 'imageData': None, 'error': 'Picture already saved'})
#   except Apod.DoesNotExist:
#     url = f"{ROOT_URL}/planetary/apod?api_key={token}&date={selected_date}"
#     response = requests.get(url)
#     image_data = response.json()
#     print(image_data)
    
#     if image_data:
#       Apod.objects.create(
#         title=image_data['title'],
#         url=image_data['url'],
#         date=selected_date,
#         explanation=image_data['explanation']
#       )
#       return render(request, 'apod/index.html', { 'imageData': image_data })
#     else:
#       return render(request, 'apod/index.html', { 'imageData': None })

@login_required
def apod_detail(request, apod_id):
  apod = Apod.objects.get(id=apod_id)
  print(apod)
  return render(request, 'apod/detail.html', {
    'apod': apod
  })

@login_required
def apod_all(request):
  apods = Apod.objects.all()
  return render(request, 'apod/all.html', {
    'apods': apods
  })

@login_required
def apod_delete(request, apod_id):
  apod = Apod.objects.get(id=apod_id)
  if apod.users.count() > 1:
    apod.users.remove(request.user)
  else:
    apod.delete()
  return redirect('apod_all')
  

# ? Splitting API request from functions
# ! May revert back to above functions, passing selected_date as a context var in apod_index
@RateLimiter(max_calls=10, period=1)
def fetch_apod_data(selected_date):
  url = f"{ROOT_URL}/planetary/apod?api_key={token}&date={selected_date}"
  response = requests.get(url)
  return response.json()

def apod_index(request):
  selected_date = request.GET.get('date')
  print(selected_date)
  if not selected_date:
    return render(request, 'apod/index.html', { 'imageData': None })
  image_data = fetch_apod_data(selected_date)
  # print(image_data)
  return render(request, 'apod/index.html', { 'selected_date': selected_date, 'imageData': image_data })

@login_required
def apod_save(request):
  # print('HIT APODSAVE')
  selected_date = request.GET.get('date')
  # print('SELECTEDDATE =', selected_date)
  if not selected_date:
    return render(request, 'apod/index.html', { 'imageData': None })

  try:
    apod = Apod.objects.get(date=selected_date)
    if request.user in apod.users.all():
      print('APOD already saved by user')
      return render(request, 'apod/index.html', { 'imageData': None, 'message': 'Picture already saved' })
    else:
      apod.users.add(request.user)
      return render(request, 'apod/index.html', { 'message': 'Picture added to your photos!' })

  except Apod.DoesNotExist:
    image_data = fetch_apod_data(selected_date)
    
    if image_data:
      apod = Apod.objects.create(
        title=image_data['title'],
        url=image_data['url'],
        date=selected_date,
        explanation=image_data['explanation']
      )
      apod.users.add(request.user)
      return render(request, 'apod/index.html', { 'imageData': image_data, 'message': 'Picture added to your photos!' })
    else:
      return render(request, 'apod/index.html', { 'imageData': None })







# ? Albums
@login_required
def albums_index(request):
  albums = Album.objects.filter(user=request.user)
  return render(request, 'albums/index.html', {
    'albums': albums
  })

@login_required
def albums_detail(request, album_id):
  album = Album.objects.get(id=album_id)
  id_list = album.apod_photos.all().values_list('id')
  # add other bits after
  apod_photos_album_doesnt_have = Apod.objects.exclude(id__in=id_list)
  return render(request, 'albums/detail.html', {
    'album': album, 'apod_photos': apod_photos_album_doesnt_have
  })

# CBVs for Albums
class AlbumCreate(LoginRequiredMixin, CreateView):
  model = Album
  fields = ['name', 'description']

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user
    return super().form_valid(form)

class AlbumUpdate(LoginRequiredMixin, UpdateView):
  model = Album
  fields = ['name', 'description']

class AlbumDelete(LoginRequiredMixin, DeleteView):
  model = Album
  success_url = '/albums'

@login_required
def add_photo_to_album(request, album_id, apod_id):
  Album.objects.get(id=album_id).apod_photos.add(apod_id)
  return redirect('albums_detail', album_id=album_id)

@login_required             
def remove_photo_from_album(request, album_id, apod_id):
  Album.objects.get(id=album_id).apod_photos.remove(apod_id)
  return redirect('albums_detail', album_id=album_id)

#  ? Not using atm?!
@login_required 
def add_photo(request, album_id):
  form = ApodForm(request.POST)
  if form.is_valid():
    new_photo = form.save(commit=False)
    new_photo.album_id = album_id
    new_photo.save()
    return redirect('albums_index, album_id=album_id')
  pass

