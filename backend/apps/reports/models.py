"""Report models for reporting fake listings, reviews, or users."""
from django.db import models
from django.conf import settings

class Report(models.Model):
    """A report submitted by a user against a property, review, or another user."""

    class ReportType(models.TextChoices):
        PROPERTY = 'property', 'Property/Listing'
        REVIEW = 'review', 'Review'
        USER = 'user', 'User'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Review'
        REVIEWED = 'reviewed', 'Under Investigation'
        RESOLVED = 'resolved', 'Resolved'
        DISMISSED = 'dismissed', 'Dismissed'

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_submitted'
    )
    report_type = models.CharField(max_length=20, choices=ReportType.choices)
    target_id = models.PositiveIntegerField(help_text="ID of the reported property, review, or user")
    reason = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reports'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.report_type.title()} Report #{self.id} by {self.reporter.username}"
