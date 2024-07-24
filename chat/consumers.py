import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from datetime import datetime
from .models import Message, Room
from rest_framework.authtoken.models import Token
from .middleware import get_user_from_access_token


class ChatConsumer(WebsocketConsumer):

  def connect(self):
      self.accept()

      # Adiciona o WebSocket ao grupo de notificações
      async_to_sync(self.channel_layer.group_add)(
          'main',
          self.channel_name
      )
      self.groups.append('main')
    

  def disconnect(self, close_code):
        # Remove o WebSocket do grupo de notificações
        async_to_sync(self.channel_layer.group_discard)(
            'main',
            self.channel_name
        )

  def receive(self, text_data):
    text_data_json = json.loads(text_data)
    command = text_data_json.get('command', '')
    user_token = text_data_json.get("user_token")
    print(user_token) 
    if user_token is not None:
      user = get_user_from_access_token(user_token)
    else: 
        user = self.scope["user"]

    if command == 'join':
      room_name = text_data_json.get('room_name')
      if room_name:
          group_name = f'chat_{room_name}'
          # Adiciona o WebSocket ao grupo
          try:
              async_to_sync(self.channel_layer.group_add)(group_name,
                                                  self.channel_name)
              print("Conectou no grupo: ", group_name)

              self.groups.append(group_name)
              

              print(self.groups)
          except:
              print("não conectou")

    elif command == 'leave':
      room_name = text_data_json.get('room_name')
      if room_name:
          group_name = f'chat_{room_name}'
          # Remove o WebSocket do grupo
          async_to_sync(self.channel_layer.group_discard)(
              group_name,
              self.channel_name
          )
          print("removendo grupo:", group_name)
          for group in self.groups:
              if group == group_name:
                  self.groups.remove(group_name)

    elif command == 'createRoom':
      room_name = text_data_json.get('room_name')
      if room_name:
          room = Room.objects.create(user = self.scope["user"], title = room_name)

          group_name = f'chat_{room.id}'


          try:
              async_to_sync(self.channel_layer.group_send)(
                  "main",
                  {
                      'type': 'create_room',
                      'room': {
                          'id': room.id,
                          'title': room.title,
                          'created_at': room.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                          'user': {
                            'id':room.user.id,
                            'username':room.user.username
                          }
                      }
                  }
              )
              print("enviou pro grupo")
          except:
              print("não enviou nada pro servidor")

    elif command == 'getMessages':
        room_name = text_data_json.get('room_name')
        print("room_name:", room_name)
        messages = Message.objects.filter(room__id=int(room_name))
        messages_list = []

        for message in messages:
            user = message.user
            messages_list.append({
                "id":message.id,
                "text":message.text,
                "created_at":message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "user": {
                    "id":user.id,
                    "username":user.username
                }
            })
        async_to_sync(self.channel_layer.group_send)(
              'main',
              {
                  'type': 'getMessages',
                  'messages': messages_list
              }
            )

    elif command == 'getRooms':
        # Get all rooms from the database
        rooms = Room.objects.all()
        room_list = [{'id': room.id, 'title': room.title} for room in rooms]
        async_to_sync(self.channel_layer.group_send)(
              'main',
              {
                  'type': 'getRooms',
                  'rooms': room_list
              }
            )

    elif command == 'message':
      room_name = text_data_json.get('room_name')
      message = text_data_json.get('message', '')
      if room_name:
          group_name = f'chat_{room_name}'
          room = Room.objects.get(id = room_name)   

          new_message = Message.objects.create(user = user, text = message)
          room.messages.add(new_message)
          # Envia a mensagem para o grupo
          async_to_sync(self.channel_layer.group_send)(
              group_name,
              {
                  'type': 'chat_message',
                  'message': {
                      'id': new_message.id,
                      'text': new_message.text,
                      'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                      'user': {
                          'id': new_message.user.id,
                          'username': new_message.user.username
                      }
                      
                      }
                  
                  
              }
          )
          async_to_sync(self.channel_layer.group_send)(
              'main',
              {
                  'type': 'notify_users',
                  'notification': {
                      'room':{
                          'id': room.id,
                          'title': room.title,
                          'created_at': room.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                          'user': {
                              'id':room.user.id,
                              'username':room.user.username,
                          }

                      },
                      'message':{
                        'id': new_message.id,
                        'text': new_message.text,
                        'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'user': {
                            'id': new_message.user.id,
                            'username': new_message.user.username
                        }
                  }
                  }
              }
          )


  def getMessages(self, event):
    messages = event.get('messages', '')

    self.send(text_data=json.dumps({
        'messages': messages,
    }))

  def getRooms(self, event):
    rooms = event.get('rooms', '')

    self.send(text_data=json.dumps({
        'rooms': rooms,
    }))

  def chat_message(self, event):
    message = event.get('message', '')
    user = event.get('user', '')
    self.send(text_data=json.dumps({
        'message': message,
        'username': user
    }))

  def notify_users(self, event):
        # Envia notificações para todos os usuários
        message = event.get('notification', '')

        self.send(text_data=json.dumps({
            'notification': message
        }))

  def create_room(self, event):
        print(event)
        # Envia notificações para todos os usuários
        room = event.get('room', '')

        self.send(text_data=json.dumps({
            'room': room
        }))

  def login_user(self, event):
        # Envia notificações para todos os usuários
        user = event.get('user', '')

        self.send(text_data=json.dumps({
            'user': user
        }))

