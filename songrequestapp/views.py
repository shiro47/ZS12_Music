from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse
from django.urls import reverse
from songrequestapp.forms import CustomUserCreationForm
import pymongo

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