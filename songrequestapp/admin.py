from django.contrib import admin
from .models  import  song, songs_blacklist, songs_play_history

# Register your models here.

admin.site.register(song)
admin.site.register(songs_blacklist)
admin.site.register(songs_play_history)