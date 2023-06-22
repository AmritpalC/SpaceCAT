from django.shortcuts import render, redirect
import requests
from .models import Satellite

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


# Create your views here.
def home(request):
    # Current Time and Location api
    api_key = 'd34af97fcf764abfaf83458dfc0014bb'  # IP Geolocation API key
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

def about(request):
  return render(request, 'about.html')

def satellites_index(request):
  satellites = Satellite.objects.all()
  return render(request, 'satellites/index.html', {
    'satellites': satellites
  })




