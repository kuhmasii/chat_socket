import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chatapp.models import ChatRoom, Chat

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = f'chat_{self.room_name}'
		self.user_id = self.scope['user'].id

		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']

		# getting chatroom from db
		chat_room = await database_sync_to_async(
			ChatRoom.objects.get)(name=self.room_name)

		# creating a chat instance
		chat = Chat(
			user=self.scope['user'],
			room=chat_room,
			content=message
		)
		
		await database_sync_to_async(chat.save)()

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'user_id': self.user_id,
			})

	async def chat_message(self, event):
		message = event['message']
		user_id = event['user_id']

		await self.send(text_data=json.dumps({
			'message': message,
			'user_id':user_id,
		}))