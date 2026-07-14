import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from apps.notifications.models import Notification

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'

        # Check if user is authenticated (using session/token in middleware)
        if self.scope["user"].is_anonymous:
            # We would normally reject, but for simplicity if not using token middleware
            # we accept. To secure this, you need a JWT AuthMiddlewareStack.
            pass

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get('message', '')
        sender_id = text_data_json.get('sender_id')
        
        if not sender_id or not message_content:
            return

        # Save message to database
        message = await self.save_message(sender_id, self.conversation_id, message_content)

        if message:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'sender_id': sender_id,
                    'created_at': str(message.created_at),
                    'message_id': message.id
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        created_at = event.get('created_at')
        message_id = event.get('message_id')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'created_at': created_at,
            'id': message_id
        }))

    @database_sync_to_async
    def save_message(self, sender_id, conversation_id, content):
        try:
            sender = User.objects.get(id=sender_id)
            conversation = Conversation.objects.get(id=conversation_id)
            
            # Verify sender is part of conversation
            if not conversation.participants.filter(id=sender_id).exists():
                return None
                
            msg = Message.objects.create(
                conversation=conversation,
                sender=sender,
                content=content
            )
            
            # Create notification for others
            for participant in conversation.participants.exclude(id=sender.id):
                Notification.objects.create(
                    user=participant,
                    notification_type='chat',
                    title='New Message',
                    message=f'{sender.username}: {content[:100]}',
                    related_object_id=conversation.id,
                )
                
            conversation.save() # update timestamp
            return msg
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
