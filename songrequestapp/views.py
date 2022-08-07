from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from requests import request
from songrequestapp.forms import CustomUserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from .models import song
from .youtube_api import scrape_title, video_id, get_sec
from bson.objectid import ObjectId
# Create your views here.

client = MongoClient("mongodb+srv://shiro_47:cJOKjP8VgVrl0M7l@song-request.la9qn.mongodb.net/?retryWrites=true&w=majority")
db = client['song-request']

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

def index(request):
    return render(request, 'index.html', {})

@login_required(login_url='/accounts/login/')
def request_song(request):
    if request.method == 'POST':
        songs_blacklist=db["songs_blacklist"]
        try:
            if song.objects.get(song_url=request.POST["YouTube URL"]):
                return JsonResponse({"message":"ALREADY IN QUEUE"})
        except ObjectDoesNotExist:
            if songs_blacklist.find_one({"url": request.POST["YouTube URL"]})!=None or songs_blacklist.find_one({"title": scrape_title(request.POST["YouTube URL"])[0]})!=None:
                return JsonResponse({"message": "SONG IS BLACKLISTED"})
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
            "current_song_id": songs[0].id,
            "song_id":video_id(current_song_url),
                    }
        return render(request, 'dashboard.html', dict)
    except:
        return render(request, 'dashboard.html')

@user_passes_test(lambda u: u.is_superuser)
def songs_blacklist(request):
    songs_blacklist=db["songs_blacklist"]
    songs=[]
    for s in songs_blacklist.find():
        songs.append(s)
    dict={"songs":songs}
    return render(request, "songs_blacklist.html", dict)

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
    song_that_is_ready_to_be_deleted = get_object_or_404(song, id=id)
    if request.method == 'POST':
        song_that_is_ready_to_be_deleted.delete()

    return HttpResponseRedirect('/dashboard')

@user_passes_test(lambda u: u.is_superuser)
def add_song_to_blacklist(request, id): 
    Song = get_object_or_404(song, id=id)
    songs_blacklist=db["songs_blacklist"]
    if songs_blacklist.find_one({"url": Song.song_url})==None or songs_blacklist.find_one({"title": Song.song_title})==None:
        info={"url": Song.song_url, "title":Song.song_title, "duration":Song.song_duration, "thumbnail": Song.song_thumbnail}
        songs_blacklist.insert_one(info)
        Song.delete()

    return HttpResponseRedirect('/dashboard')


@user_passes_test(lambda u: u.is_superuser)
def remove_from_blacklist(request, id): 
    print('fsd')
    songs_blacklist=db["songs_blacklist"]
    songs_blacklist.delete_one({"_id": ObjectId(id)})
    return JsonResponse({"message":"DELETED"})

