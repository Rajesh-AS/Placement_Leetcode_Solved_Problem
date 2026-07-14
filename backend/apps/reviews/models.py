"""
Review models for property ratings and reviews.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """User review and rating for a property."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews'
    )
    property = models.ForeignKey(
        'properties.Property', on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        unique_together = ['user', 'property']  # One review per property per user
        indexes = [
            models.Index(fields=['property', '-created_at']),
            models.Index(fields=['is_approved']),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.property.name}: {self.rating}★"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update property avg_rating and total_reviews
        self._update_property_stats()

    def delete(self, *args, **kwargs):
        prop = self.property
        super().delete(*args, **kwargs)
        self._update_property_stats(prop)

    def _update_property_stats(self, prop=None):
        """Recalculate property rating stats after review changes."""
        prop = prop or self.property
        from django.db.models import Avg, Count
        stats = Review.objects.filter(
            property=prop, is_approved=True
        ).aggregate(avg=Avg('rating'), count=Count('id'))
        prop.avg_rating = stats['avg'] or 0
        prop.total_reviews = stats['count'] or 0
        prop.save(update_fields=['avg_rating', 'total_reviews'])


class ReviewImage(models.Model):
    """Images attached to a review."""

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_images'

    def __str__(self):
        return f"Image for review #{self.review.id}"
