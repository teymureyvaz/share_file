from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Comment
from main_project.models import File
from channels.db import database_sync_to_async

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.file_id = self.scope['url_route']['kwargs']['file_id']
        self.room_group_name = 'file_id%s' % self.file_id
        print(self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    

    @database_sync_to_async
    def save_comment(self, comment):
        comment.save()
        
    @database_sync_to_async
    def get_file(self, file_id):
        return File.objects.get(id=file_id)
        
        
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        username_str = None
        user = self.scope["user"]
        username = self.scope["user"].username
        print(username)
        print(text_data)
        text_data_json = json.loads(text_data)
        print(text_data_json)
        comment = text_data_json['text']
        file_id = text_data_json['file_id']
        file_obj = await self.get_file(file_id)

        comment_obj = Comment(author=user, text=comment,file=file_obj)
        await self.save_comment(comment_obj)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'comment_text',
                'message': comment,
                'username' : username
            }
        )

    # Receive message from room group
    async def comment_text(self, event):
        text = event['message']
        username = event['username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'comment_text': text,
            'username' : username
        }))