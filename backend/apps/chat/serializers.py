"""
Serializers for chat conversations and messages.
"""
from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    sender_avatar = serializers.CharField(source='sender.profile_picture', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'sender_name', 'sender_avatar',
            'content', 'image', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'created_at']

    def get_sender_name(self, obj):
        return obj.sender.get_full_name() or obj.sender.username


class ConversationSerializer(serializers.ModelSerializer):
    participants_info = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    property_name = serializers.SerializerMethodField()
    property_image = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'participants_info', 'property', 'property_name',
            'property_image', 'last_message', 'unread_count',
            'created_at', 'updated_at'
        ]

    def get_participants_info(self, obj):
        return [
            {
                'id': p.id,
                'name': p.get_full_name() or p.username,
                'avatar': p.profile_picture,
                'role': p.role,
                'is_online': (
                    p.last_active and
                    (
                        __import__('django.utils.timezone', fromlist=['now']).now() -
                        p.last_active
                    ).seconds < 300  # 5 min threshold
                ),
            }
            for p in obj.participants.all()
        ]

    def get_last_message(self, obj):
        msg = obj.get_last_message()
        if msg:
            return {
                'content': msg.content or '[Image]',
                'sender': msg.sender.id,
                'created_at': msg.created_at,
                'is_read': msg.is_read,
            }
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0

    def get_property_name(self, obj):
        return obj.property.name if obj.property else None

    def get_property_image(self, obj):
        return obj.property.primary_image if obj.property else None


class MessageCreateSerializer(serializers.Serializer):
    """Create a message: either in existing conversation or start a new one."""
    conversation_id = serializers.IntegerField(required=False)
    recipient_id = serializers.IntegerField(required=False)
    property_id = serializers.IntegerField(required=False)
    content = serializers.CharField(required=False, allow_blank=True)
    image = serializers.URLField(required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('conversation_id') and not data.get('recipient_id'):
            raise serializers.ValidationError("Either conversation_id or recipient_id is required.")
        if not data.get('content') and not data.get('image'):
            raise serializers.ValidationError("Message must have content or an image.")
        return data
