"""Wishlist model for saving properties."""
from django.db import models
from django.conf import settings


class Wishlist(models.Model):
    """A user's saved property."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists'
    )
    property = models.ForeignKey(
        'properties.Property', on_delete=models.CASCADE, related_name='wishlisted_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlists'
        ordering = ['-created_at']
        unique_together = ['user', 'property']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} saved {self.property.name}"
