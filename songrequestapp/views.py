from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from requests import request
from songrequestapp.forms import CustomUserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
import pymongo
from datetime import datetime
from datetime import timedelta
from .models import song
from .youtube_api import scrape_title, video_id, get_sec
# Create your views here.

def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))


# client = pymongo.MongoClient('mongodb+srv://username:password@HOSTNAME/DATABASE_NAME?authSource=admin&tls=true&tlsCAFile=<PATH_TO_CA_FILE>')

# #Define Db Name
# dbname = client['admin']

# #Define Collection
# collection = dbname['mascot']

# mascot_1={
#     "name": "Sammy",
#     "type" : "Shark"
# }

# collection.insert_one(mascot_1)

# mascot_details = collection.find({})

# for r in mascot_details:
#     print(r['name'])


def index(request):
    return render(request, 'index.html', {})

@login_required(login_url='/accounts/login/')
def request_song(request):
    if request.method == 'POST':
        try:
            if song.objects.get(song_url=request.POST["YouTube URL"]):
                return JsonResponse({"message":"ALREADY IN QUEUE"})
        except ObjectDoesNotExist:
            if "www.youtube.com" in request.POST["YouTube URL"] or "youtu.be" in request.POST["YouTube URL"]:
                url= request.POST["YouTube URL"]
                data=scrape_title(url)
                Song=song()
                Song.song_url=url
                Song.song_title=data[0]
                Song.song_duration= data[1]
                Song.song_thumbnail= data[2]
                Song.save()
                return JsonResponse({"message":"SONG REQUESTED"})
            else:
                return JsonResponse({"message":"INVALID URL"})
    return render(request, 'request_song.html')


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    try:
        songs= song.objects.all()
        current_song_title=songs[0].song_title
        current_song_url=songs[0].song_url
        current_time = datetime.now()
        sec=0
        songs_play_times=[]
        for x in songs:
            if x==songs[0]:
                songs_play_times.append(current_time.strftime('%H:%M:%S'))
                time1= x.song_duration
                sec+= get_sec(time1)
            time1= x.song_duration
            sec+= get_sec(time1)
            estimated_time=current_time+timedelta(seconds=sec)
            songs_play_times.append(estimated_time.strftime('%H:%M:%S'))
        dict={"songs":zip(songs,songs_play_times),
            "current_song_url": current_song_url,
            "current_song_title": current_song_title,
            "song_id":video_id(current_song_url),
                    }
        return render(request, 'dashboard.html', dict)
    except:
        return render(request, 'dashboard.html')

@user_passes_test(lambda u: u.is_superuser)
def next_song(request):
    try:
        songs= song.objects.all()
        songs[0].delete()
        return redirect(reverse("songrequestapp:dashboard"))
    except IndexError:
        return render(request, 'dashboard.html')


@user_passes_test(lambda u: u.is_superuser)
def song_delete(request, id):
    card_that_is_ready_to_be_deleted = get_object_or_404(song, id=id)
    if request.method == 'POST':
        card_that_is_ready_to_be_deleted.delete()

    return HttpResponseRedirect('/dashboard')