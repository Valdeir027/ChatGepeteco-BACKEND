from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Message, Room
import json as simplejson
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils import timezone
import json
# Create your views here.

@login_required
def index(request):
  rooms = Room.objects.all()
  return render(request, "chat/home.html", context={"rooms": rooms})


@login_required
def create_room(request):
  if request.method == 'POST':
    dados = simplejson.loads(request.body)
    if dados:
      nome = dados['nome']
      room = Room.objects.create(nome=nome)

      return JsonResponse({'room': room.id})

  return render(request, "chat/create_room.html")


def create_user(request):
  if request.method == 'POST':
    dados = simplejson.loads(request.body)
    if dados:

      user = User.objects.create_user(username=dados['username'],
                                      email=dados['email'],
                                      password=dados['password'])
      if user:
        user = authenticate(username=dados['username'],
                            password=dados['password'])
        if user is not None:
          login(request, user)
          return JsonResponse({
              'status': 'success',
              'message': 'Usuário cadastrado com sucesso.'
          })

  return render(request, "chat/create_user.html")


def user_login(request):
  if request.method == 'POST':
    dados = simplejson.loads(request.body)
    username = dados["username"]
    password = dados["password"]
    user = authenticate(request, username=username, password=password)
    print("user:", user,"username:", username, "password:", password)
    if user is not None:
      
      login(request, user)
      return JsonResponse({
          'status': 'success',
          'message': 'Usuário autenticado com sucesso.'
      })
    else:
      return JsonResponse(
          {
              'status': 'error',
              'message': 'Credenciais inválidas.'
          }, status=400)
  else:
    return render(request, "chat/login.html")


class RoomDetailView(DetailView):
    model = Room
    template_name = 'chat/chat-list-message.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
    

def send_message(request, pk):
    data = json.loads(request.body)
    room = Room.objects.get(id = pk)
    new_message = Message.objects.create(user = request.user, text = data['message'])

    room.messages.add(new_message)
    print(pk, data)

    return render(request, 'chat/message.html',{
        'message': new_message,
    })

def create_room(request,):
    data = json.loads(request.body)
    room = Room.objects.create(user = request.user, title = data['title'])

    return render(request, 'chat/room.html',{
        'room': room, 
    })



@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/login')