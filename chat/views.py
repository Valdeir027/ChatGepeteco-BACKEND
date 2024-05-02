from django.shortcuts import render
from .models import Message, Room
import json as simplejson
from django.http import JsonResponse


# Create your views here.
def index(request):
  rooms = Room.objects.all()
  return render(request, "chat/index.html", context={"rooms": rooms})


def chat(request, id):
  room = Room.objects.get(id=id)
  messages = Message.objects.filter(room=room)

  return render(request,
                "chat/chat.html",
                context={
                    "room": room,
                    "messages": messages
                })


def create_room(request):
  if request.method == 'POST':
    dados = simplejson.loads(request.body)
    if dados:
      nome = dados['nome']
      room = Room.objects.create(nome=nome)

      return JsonResponse({'room': room.id})

  return render(request, "chat/create_room.html")
