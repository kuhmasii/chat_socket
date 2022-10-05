from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . models import Chat, ChatRoom

def index(request):
	return render(request, 'index.html')

@login_required(login_url='account_login')
def room(request, room_name):

	room_name = room_name.replace(" ", "_").lower()
	chat_room = ChatRoom.objects.filter(name__iexact=room_name).first()

	if chat_room:
		chats = Chat.objects.filter(room=chat_room)
	else:
		ChatRoom.objects.create(name=room_name)
		chats = []

	context =  {'room_name':room_name, 'chats':chats}
	return render(request, 'room.html', context)