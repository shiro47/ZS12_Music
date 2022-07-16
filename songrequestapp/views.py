from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from django.urls import reverse
from songrequestapp.forms import CustomUserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import pymongo
from .models import song
from .youtube_api import scrape_title, video_id
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
def dashboard(request):
    songs= song.objects.all()
    current_song=songs[0].song_url
    song_id= song.objects.get(song_url=current_song)
    
    dict={"songs":songs,
        "current_song": current_song,
        "song_id":video_id(current_song),
                }
    if request.method == 'POST':
        print(song.objects.all())
        
        try:
            if song.objects.get(song_url=request.POST["YouTube URL"]):
                dict={"message":"ALREADY IN QUEUE",
                }
                return render(request, 'dashboard.html', dict)
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
                dict={"message":"SONG REQUESTED",
                }
                return render(request, 'dashboard.html', dict)
            else:
                dict={"message":"INVALID URL",
                }
                return render(request, 'dashboard.html', dict)
    return render(request, 'dashboard.html', dict)


    