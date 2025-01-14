import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        sender = User.objects.get(id=data['sender_id'])
        receiver = User.objects.get(id=data['receiver_id'])
        message = Message.objects.create(sender=sender, receiver=receiver, content=data['message'])
        self.send(json.dumps({
            'sender': sender.username,
            'message': message.content,
            'timpestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }))