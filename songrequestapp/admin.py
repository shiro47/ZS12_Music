from django.contrib import admin
from  embed_video.admin  import  AdminVideoMixin
from .models  import  song

# Register your models here.

class  songAdmin(AdminVideoMixin, admin.ModelAdmin):
	pass

admin.site.register(song, songAdmin)