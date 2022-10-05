from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.CharField(max_length=1000)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} --- {self.content}'