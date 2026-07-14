"""Notification model for centralized notification system."""
from django.db import models
from django.conf import settings


class Notification(models.Model):
    """Centralized notification for all system events."""

    class NotificationType(models.TextChoices):
        BOOKING = 'booking', 'Booking Update'
        CHAT = 'chat', 'New Message'
        REVIEW = 'review', 'New Review'
        WISHLIST = 'wishlist', 'Wishlist Update'
        LISTING = 'listing', 'Listing Update'
        SYSTEM = 'system', 'System Notification'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications'
    )
    notification_type = models.CharField(max_length=20, choices=NotificationType.choices, db_index=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    related_object_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read', '-created_at']),
        ]

    def __str__(self):
        return f"{self.title} → {self.user.username}"
