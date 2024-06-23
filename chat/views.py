from django.shortcuts import render
from .models import Message, Room
import json as simplejson
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.utils import timezone

# Create your views here.

@login_required
def index(request):
  rooms = Room.objects.all()
  return render(request, "chat/index.html", context={"rooms": rooms})

@login_required
def chat(request, id):
  room = Room.objects.get(id=id)
  messages = Message.objects.filter(room=room)

  return render(request,
                "chat/chat.html",
                context={
                    "room": room,
                    "messages": messages
                })

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

@login_required
def list_users(requests):
  sessions = Session.objects.filter(expire_date__gte=timezone.now())
  usuarios_logados = []
  for session in sessions:
      data_da_sessao = session.get_decoded()
      user_id = data_da_sessao.get('_auth_user_id')
      user = User.objects.get(pk=user_id)
      usuarios_logados.append(user)
  return render(requests, "chat/list_users.html", context={"users": usuarios_logados})

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect('/login')