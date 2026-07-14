"""
Chat models for real-time messaging between students and owners.
"""
from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """A conversation thread between a student and a property owner."""

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='conversations'
    )
    property = models.ForeignKey(
        'properties.Property', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']

    def __str__(self):
        usernames = ', '.join(self.participants.values_list('username', flat=True))
        return f"Conversation: {usernames}"

    def get_last_message(self):
        return self.messages.order_by('-created_at').first()


class Message(models.Model):
    """Individual message within a conversation."""

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField(blank=True)
    image = models.URLField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', '-created_at']),
        ]

    def __str__(self):
        preview = self.content[:50] if self.content else '[Image]'
        return f"{self.sender.username}: {preview}"
