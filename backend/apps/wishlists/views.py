"""Views for wishlists."""
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError

from .models import Wishlist
from .serializers import WishlistSerializer
from apps.users.permissions import IsStudent


class WishlistListView(generics.ListAPIView):
    """List all saved properties for a student."""
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Wishlist.objects.filter(
            user=self.request.user
        ).select_related('property', 'property__owner').prefetch_related('property__images')


class ToggleWishlistView(APIView):
    """Add or remove a property from wishlist."""
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request, property_id):
        from apps.properties.models import Property
        try:
            prop = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, property=prop
        )

        if not created:
            # If it already existed, remove it (toggle)
            wishlist_item.delete()
            return Response({'message': 'Removed from wishlist.', 'is_saved': False})

        return Response({'message': 'Added to wishlist.', 'is_saved': True}, status=status.HTTP_201_CREATED)


class CheckWishlistView(APIView):
    """Check if a specific property is in the user's wishlist."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, property_id):
        is_saved = Wishlist.objects.filter(user=request.user, property_id=property_id).exists()
        return Response({'is_saved': is_saved})
