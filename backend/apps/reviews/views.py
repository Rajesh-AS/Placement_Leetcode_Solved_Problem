"""Views for reviews."""
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Review
from .serializers import ReviewSerializer
from apps.users.permissions import IsStudent, IsAdmin


class PropertyReviewsView(generics.ListAPIView):
    """List reviews for a property."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Review.objects.filter(
            property_id=self.kwargs['property_id'],
            is_approved=True
        ).select_related('user').prefetch_related('images')


class CreateReviewView(generics.CreateAPIView):
    """Student creates a review for a property."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def create(self, request, *args, **kwargs):
        property_id = request.data.get('property')
        if Review.objects.filter(user=request.user, property_id=property_id).exists():
            return Response(
                {'error': 'You have already reviewed this property.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)


class UserReviewsView(generics.ListAPIView):
    """List reviews by the authenticated user."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('user').prefetch_related('images')


class AdminReviewListView(generics.ListAPIView):
    """Admin: list all reviews for moderation."""
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    filterset_fields = ['is_approved', 'rating']
    search_fields = ['comment', 'user__username', 'property__name']

    def get_queryset(self):
        return Review.objects.all().select_related('user', 'property').prefetch_related('images')


class AdminReviewActionView(APIView):
    """Admin: approve or remove reviews."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'approve':
            review.is_approved = True
            review.save(update_fields=['is_approved'])
            return Response({'message': 'Review approved.'})
        elif action == 'remove':
            review.delete()
            return Response({'message': 'Review removed.'})

        return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
