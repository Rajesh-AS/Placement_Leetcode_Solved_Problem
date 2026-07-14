"""
User models for StayFinder.
Custom User model with role-based access (Student, Owner, Admin).
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Custom user model with role-based access control."""

    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        OWNER = 'owner', 'Property Owner'
        ADMIN = 'admin', 'Administrator'

    class Gender(models.TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'
        OTHER = 'other', 'Other'

    # Role & Auth
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT, db_index=True)
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    # Profile
    phone = models.CharField(
        max_length=15, blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True, db_index=True)
    college = models.CharField(max_length=200, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Track last activity for online status
    last_active = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role', 'is_suspended']),
            models.Index(fields=['city']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_owner(self):
        return self.role == self.Role.OWNER

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN


class OwnerProfile(models.Model):
    """Extended profile for property owners with business details."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    business_name = models.CharField(max_length=200, blank=True)
    business_address = models.TextField(blank=True)
    id_proof = models.URLField(max_length=500, blank=True, help_text='Cloudinary URL for ID proof document')
    is_verified_owner = models.BooleanField(default=False)
    total_properties = models.PositiveIntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'owner_profiles'

    def __str__(self):
        return f"Owner: {self.user.get_full_name() or self.user.username}"


class SearchHistory(models.Model):
    """Tracks user search history for AI recommendations."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=500)
    city = models.CharField(max_length=100, blank=True)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    room_type = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} searched: {self.query}"


class RecentlyViewed(models.Model):
    """Tracks recently viewed properties per user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recently_viewed'
        ordering = ['-viewed_at']
        unique_together = ['user', 'property']

    def __str__(self):
        return f"{self.user.username} viewed {self.property.name}"
