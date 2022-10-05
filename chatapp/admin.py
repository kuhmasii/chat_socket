import imp
from django.contrib import admin
from .models import ChatRoom, Chat

admin.site.register(Chat)
admin.site.register(ChatRoom)