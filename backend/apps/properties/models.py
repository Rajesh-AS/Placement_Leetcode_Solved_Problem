"""
Property models for StayFinder.
Includes Property, Room, PropertyImage, and Amenity models.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Amenity(models.Model):
    """Predefined amenities that can be associated with properties."""

    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Lucide icon name')
    category = models.CharField(max_length=50, blank=True, help_text='e.g. Basic, Safety, Comfort')

    class Meta:
        db_table = 'amenities'
        verbose_name_plural = 'Amenities'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Property(models.Model):
    """
    Core property model for hostels and PGs.
    Contains all details about a listing including location, pricing,
    amenities, and verification status.
    """

    class PropertyType(models.TextChoices):
        HOSTEL = 'hostel', 'Hostel'
        PG = 'pg', 'Paying Guest'
        COLIVING = 'coliving', 'Co-Living'
        FLAT = 'flat', 'Flat/Apartment'

    class GenderPreference(models.TextChoices):
        BOYS = 'boys', 'Boys'
        GIRLS = 'girls', 'Girls'
        COLIVING = 'coliving', 'Co-Living (Both)'

    # Basic Info
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='properties', limit_choices_to={'role': 'owner'}
    )
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PropertyType.choices, default=PropertyType.PG)
    gender = models.CharField(max_length=20, choices=GenderPreference.choices, default=GenderPreference.COLIVING)

    # Location
    address = models.TextField()
    city = models.CharField(max_length=100, db_index=True)
    area = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    # Nearby Landmarks
    nearby_colleges = models.JSONField(default=list, blank=True, help_text='List of nearby colleges')
    nearby_bus_stops = models.JSONField(default=list, blank=True, help_text='List of nearby bus stops')
    nearby_railway_station = models.CharField(max_length=200, blank=True)

    # Pricing
    rent_min = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    rent_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    # Capacity
    total_beds = models.PositiveIntegerField(default=0)
    available_beds = models.PositiveIntegerField(default=0)

    # Amenities (M2M + JSON for custom amenities)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='properties')
    amenities_list = models.JSONField(
        default=list, blank=True,
        help_text='Quick access JSON list of amenity names'
    )

    # House Rules
    house_rules = models.JSONField(default=list, blank=True, help_text='List of house rules')

    # Food
    food_included = models.BooleanField(default=False)
    food_type = models.CharField(max_length=50, blank=True, help_text='Veg, Non-Veg, Both')

    # Contact
    contact_phone = models.CharField(max_length=15, blank=True)
    contact_email = models.EmailField(blank=True)

    # Status & Verification
    is_verified = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False)

    # Aggregated Stats (denormalized for performance)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    total_views = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'properties'
        verbose_name_plural = 'Properties'
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['city', 'area']),
            models.Index(fields=['property_type', 'gender']),
            models.Index(fields=['rent_min', 'rent_max']),
            models.Index(fields=['avg_rating']),
            models.Index(fields=['is_verified', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.name} — {self.city}"

    @property
    def primary_image(self):
        """Return the primary image URL or first image."""
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img.image_url if img else ''


class Room(models.Model):
    """Room types and pricing within a property."""

    class RoomType(models.TextChoices):
        SINGLE = 'single', 'Single Occupancy'
        DOUBLE = 'double', 'Double Sharing'
        TRIPLE = 'triple', 'Triple Sharing'
        FOUR = 'four', 'Four Sharing'
        DORMITORY = 'dormitory', 'Dormitory'

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=20, choices=RoomType.choices)
    rent = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_beds = models.PositiveIntegerField(default=1)
    available_beds = models.PositiveIntegerField(default=1)
    has_attached_bathroom = models.BooleanField(default=False)
    has_ac = models.BooleanField(default=False)
    has_balcony = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'rooms'
        ordering = ['rent']

    def __str__(self):
        return f"{self.get_room_type_display()} — ₹{self.rent}/mo ({self.property.name})"


class PropertyImage(models.Model):
    """Images associated with a property listing."""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'property_images'
        ordering = ['order', '-is_primary']

    def __str__(self):
        return f"Image for {self.property.name}"


class PropertyVideo(models.Model):
    """Videos associated with a property listing."""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField(max_length=500)
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'property_videos'

    def __str__(self):
        return f"Video for {self.property.name}"
