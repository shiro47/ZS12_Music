from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from pymongo import MongoClient
from datetime import datetime
from datetime import timedelta
from .forms import SignupForm
from .tokens import account_activation_token
from .models import song, songs_play_history, songs_blacklist
from .youtube_api import scrape_title, video_id, get_sec
from django.contrib.auth.forms import PasswordChangeForm
from bson.objectid import ObjectId
from .consumers import WSConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
# Create your views here.

client = MongoClient("mongodb+srv://shiro_47:cJOKjP8VgVrl0M7l@song-request.la9qn.mongodb.net/?retryWrites=true&w=majority")
db = client['song-request']
channel_layer = get_channel_layer()



#   ____  _____ ____ ___ ____ _____ _____ ____  
#  |  _ \| ____/ ___|_ _/ ___|_   _| ____|  _ \ 
#  | |_) |  _|| |  _ | |\___ \ | | |  _| | |_) |
#  |  _ <| |__| |_| || | ___) || | | |___|  _ < 
#  |_| \_\_____\____|___|____/ |_| |_____|_| \_\
                                              

# def register(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid() and form.cleaned_data.get('email').endswith("@uczen.eduwarszawa.pl"):
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Activate your blog account.'
#             message = render_to_string('registration/acc_active_email.html', {
#                 'user': user,
#                 'domain': current_site.domain,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#             to_email = form.cleaned_data.get('email')
#             email = EmailMessage(
#                         mail_subject, message, to=[to_email]
#             )
#             email.send()
#             return HttpResponse('Please confirm your email address to complete the registration')
#     else:
#         form = SignupForm()
#     return render(request, 'registration/register.html', {'form': form})

# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         # return redirect('home')
#         return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
#     else:
#         return HttpResponse('Activation link is invalid!')


def index(request):
    return render(request, 'index.html', {})

@login_required(login_url='/accounts/login/')
def request_song(request):
    if request.method == 'POST':
        try:
            if song.objects.get(song_url=f"https://www.youtube.com/watch?v={video_id(request.POST['YouTube URL'])}"):
                return JsonResponse({"message":"ALREADY IN QUEUE"})
        except ObjectDoesNotExist:
            if video_id(request.POST["YouTube URL"]):
                url = f"https://www.youtube.com/watch?v={video_id(request.POST['YouTube URL'])}"
                data = scrape_title(url)
                if data==None:
                    return JsonResponse({"message": "INVALID URL"})
                try:
                    if songs_blacklist.objects.get(song_url=url) or songs_blacklist.objects.get(song_title=data[0]):
                        return JsonResponse({"message": "SONG IS BLACKLISTED"})
                except songs_blacklist.DoesNotExist:
                    Song = song()
                    Song.song_url = url
                    Song.song_title = data[0]
                    Song.song_duration = data[1]
                    Song.song_thumbnail = data[2]
                    Song.save()
                    async_to_sync(channel_layer.group_send)(
            "ZS12",
            {
                'type': 'new_song',
                'id': str(Song.id),
                'song_url': url,
                'song_thumbnail':data[2],
                'song_title': data[0],
                'song_duration': data[1],
                'position': str(len(song.objects.all())-1)
            }
        )
                    return JsonResponse({"message": "SONG REQUESTED", "url":url})
            else:
                return JsonResponse({"message": "INVALID URL"})
    try:
        songs= song.objects.all()
        current_time = datetime.now()
        sec=0
        songs_play_times=[]
        for x in songs:
            if x==songs[0]:
                songs_play_times.append(current_time.strftime('%H:%M:%S'))
            time1= x.song_duration
            sec+= get_sec(time1)
            estimated_time=current_time+timedelta(seconds=sec)
            songs_play_times.append(estimated_time.strftime('%H:%M:%S'))
        elements={
            "songs": zip(songs,songs_play_times),
        }
        return render(request, 'request_song.html', elements)
    except: 
        return render(request, 'request_song.html')


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def dashboard(request):
    try:
        songs= song.objects.all()
        current_time = datetime.now()
        sec=0
        songs_play_times=[]
        for x in songs:
            if x==songs[0]:
                songs_play_times.append(current_time.strftime('%H:%M:%S'))
            time1= x.song_duration
            sec+= get_sec(time1)
            estimated_time=current_time+timedelta(seconds=sec)
            songs_play_times.append(estimated_time.strftime('%H:%M:%S'))
        dict={"songs":zip(songs,songs_play_times),
            "current_song_url": video_id(songs[0].song_url),
            "current_song_title": songs[0].song_title,
            "current_song_id": songs[0].id,
            "current_song_skip_requests": songs[0].skip_requests,
            "song_id":video_id(songs[0].song_url),
                    }
        return render(request, 'dashboard.html', dict)
    except:
        return render(request, 'dashboard.html')

@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def songs_blacklist_page(request):
    dict={"songs":songs_blacklist.objects.all()}
    return render(request, "songs_blacklist.html", dict)

@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def songs_history(request):
    try:
        songs= songs_play_history.objects.all()
        dict={"songs":songs,
        }
        return render(request, 'history.html', dict)
    except:
        return render(request, 'history.html')

@login_required(login_url='/accounts/login/')
def account(request):
    form = PasswordChangeForm(request.user)
    return render(request, 'account.html',{'form': form})

@login_required(login_url='/accounts/login/')
def change_username(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST["data"]).exists():
            return JsonResponse({"message":"USERNAME IS TAKEN. TRY ANOTHER ONE!"})
        user = User.objects.get(username = request.user.username)
        user.username = request.POST["data"]
        user.save()
        return JsonResponse({"message":"USERNAME CHANGED!"})
    
@login_required(login_url='/accounts/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return JsonResponse({"message":"PASSWORD CHANGED!"})
        else:
            errors=[]
            for field in form:
                for error in field.errors:
                    errors.append(error)
            return JsonResponse({"message":errors})

@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def next_song(request):
    try:
        skip_votes=db["skip_votes"]
        songs= song.objects.all()
        Song=songs_play_history()
        Song.song_url = songs[0].song_url
        Song.song_title = songs[0].song_title
        Song.song_duration = songs[0].song_duration
        Song.song_thumbnail = songs[0].song_thumbnail
        Song.save()
        songs[0].delete()
        skip_votes.delete_many({})
        current_song=songs[0]
        response={"current_song":{"title":current_song.song_title,
                                  "url":current_song.song_url,
                                  "id":current_song.id}}
        return redirect(reverse("songrequestapp:dashboard"))
    except IndexError:
        return render(request, 'dashboard.html')


@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def song_delete(request, id):
    song_that_is_ready_to_be_deleted = get_object_or_404(song, id=id)
    if request.method == 'POST':
        song_that_is_ready_to_be_deleted.delete()

    return HttpResponseRedirect('/dashboard')

@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def clear_queue(request):
    if request.method == "POST":
        song.objects.all().delete()
        return JsonResponse({"message":"QUEUE CLEARED"})

@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def song_delete_from_history(request, id):
    song_that_is_ready_to_be_deleted = get_object_or_404(songs_play_history, id=id)
    if request.method == 'POST':
        song_that_is_ready_to_be_deleted.delete()

    return HttpResponseRedirect('/dashboard/history')

@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def add_song_to_blacklist(request, id): 
    Song = get_object_or_404(song, id=id)
    try:
        if songs_blacklist.objects.get(song_url=Song.song_url):
            Song.delete()
            return JsonResponse({"message":"SONG IS ALREADY IN BLACKLIST"})
    except songs_blacklist.DoesNotExist:
        song_to_add= songs_blacklist()
        song_to_add.song_url = Song.song_url
        song_to_add.song_title = Song.song_title
        song_to_add.song_duration = Song.song_duration
        song_to_add.song_thumbnail = Song.song_thumbnail
        song_to_add.save()
        Song.delete()
        return HttpResponseRedirect('/dashboard')


@user_passes_test(lambda u: u.groups.filter(name='Moderation').exists())
def remove_from_blacklist(request, id): 
    if request.method == "POST":
        song_to_del=songs_blacklist.objects.get(id=id)
        song_to_del.delete()
        return JsonResponse({"message":"DELETED"})

@login_required(login_url='/accounts/login/')
def skip_vote(request, id): 
    if request.method == "POST":
        skip_votes=db["skip_votes"]
        if skip_votes.find_one({"username": request.user.username}) != None:
            return JsonResponse({"message":"ALREADY VOTED"})
        user={"username": request.user.username}
        # skip_votes.insert_one(user)
        Song = get_object_or_404(song, id=id)
        Song.skip_requests +=1
        Song.save()
        async_to_sync(channel_layer.group_send)(
    'ZS12',
    {
        'type': 'skip_vote',
        'message': "skip_vote"
    }
) 
        return JsonResponse({"message":"VOTED"})
    elif request.method == "GET":
        songs = song.objects.all()
        return JsonResponse({"message": songs[0].skip_requests})
    
    
def bug_report(request):
    if request.method=="POST":
        try:
            bugs=db["bug_reports"]
            user="UNDEFINED"
            if request.user.is_authenticated:
                user= request.user.email
            bug={"user_email": user,
                "description":request.POST["description"]}
            bugs.insert_one(bug)
            return JsonResponse({"message":"BUG REPORTED. THANKS!"})
        except:
            return JsonResponse({"message":"SOMETHING GONE WRONG. PLEASE TRY AGAIN."})
        
