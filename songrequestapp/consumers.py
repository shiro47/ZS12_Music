import json
import asyncio

from channels.consumer import AsyncConsumer

from .models import song
from django.shortcuts import get_object_or_404

class WSConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept",
                         })
        await self.send({"type":"websocket.send",
                         "text":0})
        
    async def websocket_receive(self, event):
        # when messages is received from websocket
        print("receive", event)
        await self.send({"type":"websocket.send",
                         "text":0})
        print("Sended message.")
    
    async def websocket_disconnect(self, event):
        # when websocket disconnects
        print("disconnected", event)
