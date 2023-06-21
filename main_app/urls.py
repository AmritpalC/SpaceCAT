from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),

    path('satellites/', views.satellites_index, name='satellites_index'),

    path('apod/', views.apod_index, name='apod_index'),

    path('albums', views.albums_index, name='albums_index'),
    path('albums/<int:album_id>', views.albums_detail, name='albums_detail'),
    path('albums/create', views.AlbumCreate.as_view(), name='albums_create'),
    path('albums/<int:pk>/update/', views.AlbumUpdate.as_view(), name='albums_update'),
    path('albums/<int:pk>/delete/', views.AlbumDelete.as_view(), name='albums_delete'),


    path('albums/<int:album_id>/add_photo', views.add_photo, name='add_photo'),
]
