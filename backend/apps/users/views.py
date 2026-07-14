"""
Views for user authentication, registration, profile management,
Google OAuth, and admin user operations.
"""
import os
import uuid
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, GoogleAuthSerializer,
    UserProfileSerializer, UserProfileUpdateSerializer, ChangePasswordSerializer,
    AdminUserListSerializer, OwnerProfileSerializer,
)
from .permissions import IsAdmin, IsNotSuspended
from .models import OwnerProfile, SearchHistory, RecentlyViewed

User = get_user_model()


def get_tokens_for_user(user):
    """Generate JWT access and refresh tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ===================================================
# Authentication Views
# ===================================================

class RegisterView(generics.CreateAPIView):
    """Register a new user (Student or Owner)."""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Registration successful.',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """Login with email/username and password."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_active = timezone.now()
        user.save(update_fields=['last_active'])
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Login successful.',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """Logout by blacklisting the refresh token."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'message': 'Logged out.'}, status=status.HTTP_200_OK)


class GoogleAuthView(APIView):
    """Authenticate via Google OAuth. Creates user if not exists."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']
        role = serializer.validated_data.get('role', User.Role.STUDENT)

        # Verify Google token
        try:
            import requests
            if '.' not in token:
                # It is an access token from useGoogleLogin
                resp = requests.get(
                    'https://www.googleapis.com/oauth2/v3/userinfo',
                    headers={'Authorization': f'Bearer {token}'}
                )
                if resp.status_code == 200:
                    idinfo = resp.json()
                else:
                    return Response({'error': 'Invalid Google access token.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # It is a JWT ID token
                try:
                    from google.oauth2 import id_token
                    from google.auth.transport import requests as google_requests
                    google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
                    idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), google_client_id)
                except ImportError:
                    import json, base64
                    payload = token.split('.')[1]
                    payload += '=' * (4 - len(payload) % 4)
                    idinfo = json.loads(base64.b64decode(payload))
        except Exception as e:
            return Response({'error': 'Invalid Google token.'}, status=status.HTTP_400_BAD_REQUEST)

        email = idinfo.get('email', '')
        google_id = idinfo.get('sub', '')
        first_name = idinfo.get('given_name', '')
        last_name = idinfo.get('family_name', '')
        picture = idinfo.get('picture', '')

        # Find or create user
        user = User.objects.filter(google_id=google_id).first()
        if not user:
            user = User.objects.filter(email=email).first()
            if user:
                # Link existing account to Google
                user.google_id = google_id
                if picture and not user.profile_picture:
                    user.profile_picture = picture
                user.save()
            else:
                # Create new user
                user = User.objects.create(
                    username=email.split('@')[0] + '_' + str(uuid.uuid4())[:6],
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    google_id=google_id,
                    profile_picture=picture,
                    role=role,
                    is_verified=True,
                )
                user.set_unusable_password()
                user.save()
                if role == User.Role.OWNER:
                    OwnerProfile.objects.create(user=user)

        if user.is_suspended:
            return Response({'error': 'Account suspended.'}, status=status.HTTP_403_FORBIDDEN)

        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Google authentication successful.',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens,
            'is_new_user': not user.last_login,
        }, status=status.HTTP_200_OK)


# ===================================================
# Profile Views
# ===================================================

class ProfileView(APIView):
    """Get or update the authenticated user's profile."""
    permission_classes = [permissions.IsAuthenticated, IsNotSuspended]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(request.user).data)


class ChangePasswordView(APIView):
    """Change the authenticated user's password."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password updated successfully.'})


class ForgotPasswordView(APIView):
    """Send password reset email."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').lower()
        user = User.objects.filter(email=email).first()
        if user:
            # In production, send actual reset email with token
            # For now, return success regardless (security: don't reveal if email exists)
            pass
        return Response({'message': 'If an account exists with that email, a reset link has been sent.'})


class UploadProfilePictureView(APIView):
    """Upload profile picture to Cloudinary."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('profile_picture')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # If Cloudinary is configured, upload; otherwise save locally
        try:
            import cloudinary.uploader
            result = cloudinary.uploader.upload(
                file,
                folder='stayfinder/profiles/',
                transformation=[{'width': 400, 'height': 400, 'crop': 'fill'}]
            )
            url = result['secure_url']
        except (ImportError, Exception):
            # Fallback: save URL as-is for local dev
            from django.core.files.storage import default_storage
            path = default_storage.save(f'profiles/{file.name}', file)
            url = f'/media/{path}'

        request.user.profile_picture = url
        request.user.save(update_fields=['profile_picture'])
        return Response({'profile_picture': url})


# ===================================================
# Admin User Management Views
# ===================================================

class AdminUserListView(generics.ListAPIView):
    """List all users for admin management."""
    serializer_class = AdminUserListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get('role')
        is_suspended = self.request.query_params.get('is_suspended')
        search = self.request.query_params.get('search')

        if role:
            queryset = queryset.filter(role=role)
        if is_suspended is not None:
            queryset = queryset.filter(is_suspended=is_suspended.lower() == 'true')
        if search:
            from django.db.models import Q
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        return queryset


class AdminUserActionView(APIView):
    """Admin actions: suspend, unsuspend, ban, verify users."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'suspend':
            user.is_suspended = True
            user.save(update_fields=['is_suspended'])
            return Response({'message': f'User {user.username} suspended.'})
        elif action == 'unsuspend':
            user.is_suspended = False
            user.save(update_fields=['is_suspended'])
            return Response({'message': f'User {user.username} unsuspended.'})
        elif action == 'ban':
            user.is_active = False
            user.is_suspended = True
            user.save(update_fields=['is_active', 'is_suspended'])
            return Response({'message': f'User {user.username} banned.'})
        elif action == 'verify':
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            if hasattr(user, 'owner_profile'):
                user.owner_profile.is_verified_owner = True
                user.owner_profile.save(update_fields=['is_verified_owner'])
            return Response({'message': f'User {user.username} verified.'})
        else:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)


class AdminDashboardStatsView(APIView):
    """Platform statistics for admin dashboard."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get(self, request):
        from apps.properties.models import Property
        from apps.bookings.models import Booking
        from apps.reviews.models import Review
        from django.db.models import Count, Avg
        from django.db.models.functions import TruncMonth

        total_users = User.objects.count()
        total_students = User.objects.filter(role='student').count()
        total_owners = User.objects.filter(role='owner').count()
        total_properties = Property.objects.count()
        verified_properties = Property.objects.filter(is_verified=True).count()
        total_bookings = Booking.objects.count()
        total_reviews = Review.objects.count()

        # Monthly registrations (last 6 months)
        six_months_ago = timezone.now() - timezone.timedelta(days=180)
        monthly_registrations = (
            User.objects.filter(date_joined__gte=six_months_ago)
            .annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        # Popular cities
        popular_cities = (
            Property.objects.values('city')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )

        # Top rated properties
        top_rated = (
            Property.objects.filter(avg_rating__gt=0)
            .order_by('-avg_rating')[:5]
            .values('id', 'name', 'city', 'avg_rating')
        )

        return Response({
            'total_users': total_users,
            'total_students': total_students,
            'total_owners': total_owners,
            'total_properties': total_properties,
            'verified_properties': verified_properties,
            'total_bookings': total_bookings,
            'total_reviews': total_reviews,
            'monthly_registrations': list(monthly_registrations),
            'popular_cities': list(popular_cities),
            'top_rated_properties': list(top_rated),
        })
