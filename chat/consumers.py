import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from datetime import datetime
from .models import Message
from rest_framework.authtoken.models import Token
from .middleware import get_user_from_access_token
class ChatConsumer(WebsocketConsumer):

  def connect(self):
    self.room_uri = self.scope['url_route']['kwargs']['id']
    self.room_group_name = 'chat_%s' % self.room_uri

    async_to_sync(self.channel_layer.group_add)(self.room_group_name,
                                                self.channel_name)

    self.accept()

  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    print(text_data_json)
    try:
      user_token = text_data_json["user_token"]
    except:
      user_token = ""
    message = text_data_json['message']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if user_token =='':
      user = self.scope['user']
    else: 
        user = get_user_from_access_token(user_token)
    message_data = {
        'message': message,
        'user': user.id,
        'username': user.username,
        'timestamp': timestamp
    }
    obj_message = Message.objects.create(user=user,
                                         room_id=self.room_uri,
                                         mensagem=message)
    async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
        'type': 'chat_message',
        'message_data': message_data
    })

  def chat_message(self, event):
    message_data = event['message_data']
    try:
      user_token = event["user_token"]
    except:
      user_token = ""
    self.send(text_data=json.dumps({
        'type': 'chat',
        'message_data': message_data,
        'user_token':user_token
    }))

