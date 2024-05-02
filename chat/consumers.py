import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from datetime import datetime
from .models import Message
class ChatConsumer(WebsocketConsumer):
    def connect(self):
      self.room_uri = self.scope['url_route']['kwargs']['id']
      self.room_group_name = 'chat_%s' % self.room_uri
      print(self.room_uri)
      
      async_to_sync(self.channel_layer.group_add)(
          self.room_group_name,
          self.channel_name
      )

      self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']



        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  
        message_data = {'message': message, 'timestamp': timestamp}

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_data': message_data
            }
        )

    def chat_message(self, event):
        message_data = event['message_data']
        message = Message.objects.create(room_id=int(self.room_uri), mensagem=message_data['message'])
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message_data': message_data
        }))
