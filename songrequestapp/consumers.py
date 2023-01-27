import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import song
from django.shortcuts import get_object_or_404

class WSConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.name = "ZS12"
    
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        # when messages is received from websocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Song=song.objects.get(song_url=message)
        # async_to_sync(self.channel_layer.group_send)(
        #     self.name,
        #     {
        #         'type': 'new_song',
        #         'id': str(Song.id),
        #         'song_url': message,
        #         'song_thumbnail':Song.song_thumbnail,
        #         'song_title': Song.song_title,
        #         'song_duration': Song.song_duration,
        #         'position': str(len(song.objects.all())-1)
        #     }
        # )
        
    def disconnect(self, text_data):
        # when websocket disconnects
        print("disconnected", json.loads(text_data))


    def new_song(self, event):
        self.send(text_data=json.dumps(event))
        
    def skip_vote(self, event, type="skip_vote"):
        self.send(text_data=json.dumps(event))