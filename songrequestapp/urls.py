from django.urls import path
from . import views

app_name = "songrequestapp"

urlpatterns = [
    path('',views.index,name='index'),
    path("register/",views.register,name='register'),
    path("dashboard",views.dashboard,name='dashboard'),
    path("request_song",views.request_song, name='request_song'),
    path("dashboard/next_song",views.next_song,name='next_song'),
    path("dashboard/songs_blacklist", views.songs_blacklist, name="songs_blacklist"),
    path("dashboard/songs_blacklist/remove/<id>", views.remove_from_blacklist, name='remove_from_blacklist'),
    path(r'(?P<id>\d+)/$', views.song_delete, name="delete"), 
    path(r'(?P<id>\d+)/^$', views.add_song_to_blacklist, name="add_to_blacklist"), 
]