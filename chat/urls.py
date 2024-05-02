from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('chat/<int:id>', views.chat, name="chat"),
    path('create_room/', views.create_room, name="create_room"),
    path('create_user/', views.create_user, name="create_user"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.sair, name='logout'),
]
