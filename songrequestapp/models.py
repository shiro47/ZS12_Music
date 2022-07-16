from django.db import models
from  embed_video.fields  import  EmbedVideoField

# Create your models here.

class  song(models.Model):
	song_url= EmbedVideoField()
	song_title = models.TextField(default='No title')
	song_duration= models.TextField(default='')
	song_thumbnail= models.TextField(default='')