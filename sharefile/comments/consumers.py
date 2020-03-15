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

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    @database_sync_to_async
    def save_comment(self, comment):
        comment.save()
        return comment.id
    
    @database_sync_to_async
    def get_file_owner(self, file_id):
        return File.objects.get(id=file_id).owner_id.username

    @database_sync_to_async
    def get_file(self, file_id):
        return File.objects.get(id=file_id)
    
    @database_sync_to_async
    def get_comment(self, comment_id):
        return Comment.objects.get(id=comment_id)
        
        
    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        username_str = None
        user = self.scope["user"]
        username = self.scope["user"].username
        text_data_json = json.loads(text_data)

        #comment create
        if 'text' in text_data_json:
            comment = text_data_json['text']
            file_id = text_data_json['file_id']
            file_obj = await self.get_file(file_id)
            file_owner_username = await self.get_file_owner(file_id)
            comment_obj = Comment(author=user, text=comment,file=file_obj)

            comment_id = await self.save_comment(comment_obj)
            print(comment_id)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_text',
                    'message': comment,
                    'username' : username,
                    'file_owner_username': file_owner_username,
                    'comment_id_creation' : comment_id
                }
            )
        #comment update
        elif 'comment_id' in text_data_json:
            comment_id = text_data_json['comment_id']
            comment_text = text_data_json['comment_text']

            comment_obj = await self.get_comment(comment_id)
            comment_obj.text = comment_text;

            await self.save_comment(comment_obj)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_update',
                    'comment_id': comment_id,
                    'comment_text' : comment_text
                }
            )
        #comment delete
        else:
            comment_id = text_data_json['deleted_comment_id']
            comment_obj = await self.get_comment(comment_id)
            comment_obj.is_active = False;

            await self.save_comment(comment_obj)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'comment_delete',
                    'comment_id': comment_id
                }
            )

    async def comment_text(self, event):
        text = event['message']
        username = event['username']
        file_owner_username = event['file_owner_username']
        comment_id_creation = event['comment_id_creation']

        await self.send(text_data=json.dumps({
            'comment_text': text,
            'username' : username,
            'file_owner_username': file_owner_username,
            'comment_id_creation' : comment_id_creation
        }))

    async def comment_update(self, event):
        comment_id = event['comment_id']
        comment_text = event['comment_text']

        await self.send(text_data=json.dumps({
            'comment_text': comment_text,
            'comment_id' : comment_id
        }))

    async def comment_delete(self, event):
        comment_id = event['comment_id']
        await self.send(text_data=json.dumps({
            'comment_delete_id' : comment_id
        }))
