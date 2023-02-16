from django.db import models
from django.contrib.auth.models import User
from  embed_video.fields import EmbedVideoField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class song(models.Model):
	song_url= EmbedVideoField()
	song_title = models.TextField(default='No title')
	song_duration= models.TextField(default='')
	song_thumbnail= models.TextField(default='')
	skip_requests = models.IntegerField(default=0)
 
class songs_play_history(models.Model):
	song_url= EmbedVideoField()
	song_title = models.TextField(default='No title')
	song_duration= models.TextField(default='')
	song_thumbnail= models.TextField(default='')
 
class songs_blacklist(models.Model):
	song_url= EmbedVideoField()
	song_title = models.TextField(default='No title')
	song_duration= models.TextField(default='')
	song_thumbnail= models.TextField(default='')
 
class bug_report(models.Model):
    reported_by=models.CharField(max_length=255, default="")
    description=models.TextField(default='')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    requests = models.IntegerField(default=0)
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()