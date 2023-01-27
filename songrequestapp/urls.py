from django.urls import path
from . import views

app_name = "songrequestapp"

urlpatterns = [
    # path("register/",views.register,name='register'),
    # path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    path('',views.index,name='index'),
    path("dashboard",views.dashboard,name='dashboard'),
    path("account", views.account, name="account"),
    path("account/change_username", views.change_username, name="change_username"),
    path("account/change_password", views.change_password, name="change_password"),
    path(r"^report_bug/$", views.bug_report, name="bug_report"),
    path("request_song",views.request_song, name='request_song'),
    path("request_song/skip_vote/<id>", views.skip_vote, name="skip_vote"),
    path("dashboard/next_song",views.next_song,name='next_song'),
    path("dashboard/songs_blacklist", views.songs_blacklist_page, name="songs_blacklist"),
    path("dashboard/songs_blacklist/add/<id>", views.add_song_to_blacklist, name="add_to_blacklist"), 
    path("dashboard/songs_blacklist/remove/<id>", views.remove_from_blacklist, name='remove_from_blacklist'),
    path("dashboard/history", views.songs_history, name="songs_history"),
    path(r"dashboard/clear_queue/$", views.clear_queue, name="clear_queue"),
    path(r'(?P<id>\d+)/$', views.song_delete, name="delete"), 
    path(r'(?P<id>\d+)/^$', views.song_delete_from_history, name="delete_from_history"), 
]