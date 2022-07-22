from django.urls import path
from . import views

app_name = "songrequestapp"

urlpatterns = [
    path('',views.index,name='index'),
    path("register/",views.register,name='register'),
    path("dashboard",views.dashboard,name='dashboard'),
    path("request_song",views.request_song, name='request_song'),
    path("dashboard/next_song",views.next_song,name='next_song'),
    path(r'(?P<id>\d+)/$', views.song_delete, name="delete"), 
]