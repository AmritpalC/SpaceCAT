from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("", views.home, name="home"),
    path('accounts/signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),

    path('satellites/', views.satellites_index, name='satellites_index'),

    path('apod/save', views.apod_save, name='apod_save'),
    path('apod/', views.apod_index, name='apod_index'),
    path('apod/<int:apod_id>', views.apod_detail, name='apod_detail'),
    path('apod/all', views.apod_all, name='apod_all'),
    path('apod/delete/<int:apod_id>', views.apod_delete, name='apod_delete'),


    path('albums', views.albums_index, name='albums_index'),
    path('albums/<int:album_id>', views.albums_detail, name='albums_detail'),
    path('albums/create', views.AlbumCreate.as_view(), name='albums_create'),
    path('albums/<int:pk>/update/', views.AlbumUpdate.as_view(), name='albums_update'),
    path('albums/<int:pk>/delete/', views.AlbumDelete.as_view(), name='albums_delete'),

    path('albums/<int:album_id>/add_photo_to_album/<int:apod_id>', views.add_photo_to_album, name='add_photo_to_album'),
    path('albums/<int:album_id>/remove_photo_from_album/<int:apod_id>', views.remove_photo_from_album, name='remove_photo_from_album'),



    path('albums/<int:album_id>/add_photo', views.add_photo, name='add_photo'),
]

urlpatterns += staticfiles_urlpatterns()