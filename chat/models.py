from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Room(models.Model):
  nome = models.CharField(max_length=250)


  def __str__(self):
    return self.nome


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    mensagem = models.TextField()

    def __str__(self):
      return f"user:{self.user.username} room:{self.room.nome} mensagem:{self.mensagem}"

