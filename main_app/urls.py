from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('satellites/', views.satellites_index, name='satellites_index'),
    path('apod/', views.apod_index, name='apod_index')
]
