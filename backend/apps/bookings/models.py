"""
Booking models for scheduling visits to properties.
"""
from django.db import models
from django.conf import settings


class Booking(models.Model):
    """Visit booking between a student and a property."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'
        RESCHEDULED = 'rescheduled', 'Rescheduled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='bookings'
    )
    property = models.ForeignKey(
        'properties.Property', on_delete=models.CASCADE,
        related_name='bookings'
    )
    room = models.ForeignKey(
        'properties.Room', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='bookings'
    )

    # Visit details
    visit_date = models.DateField()
    visit_time = models.TimeField()
    message = models.TextField(blank=True, help_text='Message to owner')

    # Status
    status = models.CharField(
        max_length=15, choices=Status.choices,
        default=Status.PENDING, db_index=True
    )
    owner_notes = models.TextField(blank=True)

    # Reschedule fields
    rescheduled_date = models.DateField(null=True, blank=True)
    rescheduled_time = models.TimeField(null=True, blank=True)
    reschedule_reason = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['property', 'status']),
            models.Index(fields=['visit_date']),
        ]

    def __str__(self):
        return f"Booking #{self.id} — {self.user.username} → {self.property.name} ({self.status})"

class Payment(models.Model):
    """Mock payment record for a booking (Advance fee/rent)."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='INR')
    
    # Razorpay/Gateway specific fields
    transaction_id = models.CharField(max_length=100, blank=True)
    order_id = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.id} — {self.amount} {self.currency} ({self.status})"
