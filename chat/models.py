from django.db import models

# Create your models here.
class Room(models.Model):
  nome = models.CharField(max_length=250)


  def __str__(self):
    return self.nome


class Message(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    mensagem = models.TextField()

