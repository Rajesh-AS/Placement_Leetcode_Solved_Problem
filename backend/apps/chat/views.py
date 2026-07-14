"""
Views for chat functionality — conversations, messages, and real-time support.
"""
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, MessageCreateSerializer
from apps.users.permissions import IsNotSuspended

User = get_user_model()


class ConversationListView(generics.ListAPIView):
    """List all conversations for the authenticated user."""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotSuspended]

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')


class ConversationMessagesView(generics.ListAPIView):
    """List messages in a conversation."""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotSuspended]
    pagination_class = None  # Return all messages in conversation

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        # Verify user is a participant
        try:
            conversation = Conversation.objects.get(
                id=conversation_id, participants=self.request.user
            )
        except Conversation.DoesNotExist:
            return Message.objects.none()

        # Mark unread messages as read
        Message.objects.filter(
            conversation=conversation, is_read=False
        ).exclude(sender=self.request.user).update(is_read=True)

        return Message.objects.filter(
            conversation=conversation
        ).select_related('sender')


class SendMessageView(APIView):
    """Send a message in an existing or new conversation."""
    permission_classes = [permissions.IsAuthenticated, IsNotSuspended]

    def post(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        conversation = None

        if data.get('conversation_id'):
            try:
                conversation = Conversation.objects.get(
                    id=data['conversation_id'], participants=request.user
                )
            except Conversation.DoesNotExist:
                return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Start or find existing conversation with recipient
            recipient_id = data['recipient_id']
            try:
                recipient = User.objects.get(id=recipient_id)
            except User.DoesNotExist:
                return Response({'error': 'Recipient not found.'}, status=status.HTTP_404_NOT_FOUND)

            property_id = data.get('property_id')

            # Check for existing conversation between these users about this property
            existing = Conversation.objects.filter(
                participants=request.user
            ).filter(
                participants=recipient
            )
            if property_id:
                existing = existing.filter(property_id=property_id)

            conversation = existing.first()
            if not conversation:
                from apps.properties.models import Property
                prop = None
                if property_id:
                    try:
                        prop = Property.objects.get(id=property_id)
                    except Property.DoesNotExist:
                        pass

                conversation = Conversation.objects.create(property=prop)
                conversation.participants.add(request.user, recipient)

        # Create the message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=data.get('content', ''),
            image=data.get('image', ''),
        )

        # Update conversation timestamp
        conversation.save()  # triggers auto_now on updated_at

        # Create notification for recipient
        from apps.notifications.models import Notification
        for participant in conversation.participants.exclude(id=request.user.id):
            Notification.objects.create(
                user=participant,
                notification_type='chat',
                title='New Message',
                message=f'{request.user.get_full_name() or request.user.username}: {message.content[:100] or "[Image]"}',
                related_object_id=conversation.id,
            )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


class MarkMessagesReadView(APIView):
    """Mark all messages in a conversation as read."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        try:
            conversation = Conversation.objects.get(
                id=conversation_id, participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)

        updated = Message.objects.filter(
            conversation=conversation, is_read=False
        ).exclude(sender=request.user).update(is_read=True)

        return Response({'marked_read': updated})


class UnreadCountView(APIView):
    """Get total unread message count for the authenticated user."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()
        return Response({'unread_count': count})
