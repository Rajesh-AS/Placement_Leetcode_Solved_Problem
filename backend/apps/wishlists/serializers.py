"""Serializers for wishlists."""
from rest_framework import serializers
from .models import Wishlist
from apps.properties.serializers import PropertyListSerializer


class WishlistSerializer(serializers.ModelSerializer):
    property_details = PropertyListSerializer(source='property', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'property', 'property_details', 'created_at']
        read_only_fields = ['id', 'created_at']
