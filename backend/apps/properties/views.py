"""
Views for property CRUD, search, and management.
"""
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Property, Room, PropertyImage, PropertyVideo, Amenity
from .serializers import (
    PropertyListSerializer, PropertyDetailSerializer,
    PropertyCreateSerializer, AmenitySerializer,
    PropertyImageSerializer, RoomSerializer
)
from .filters import PropertyFilter
from apps.users.permissions import IsOwner, IsAdmin, IsOwnerOrAdmin, IsNotSuspended


# ===================================================
# Public Property Views
# ===================================================

class PropertyListView(generics.ListAPIView):
    """
    List and search properties with advanced filtering.
    Public endpoint — no auth required.
    """
    serializer_class = PropertyListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['name', 'description', 'city', 'area', 'address']
    ordering_fields = ['rent_min', 'avg_rating', 'created_at', 'total_reviews']
    ordering = ['-is_featured', '-created_at']

    def get_queryset(self):
        return Property.objects.filter(
            is_active=True
        ).select_related('owner').prefetch_related('images', 'rooms')


class PropertyDetailView(generics.RetrieveAPIView):
    """
    Get full property details. Public endpoint.
    Increments view count on each request.
    """
    serializer_class = PropertyDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Property.objects.filter(
            is_active=True
        ).select_related('owner').prefetch_related(
            'images', 'videos', 'rooms', 'amenities'
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        Property.objects.filter(pk=instance.pk).update(
            total_views=instance.total_views + 1
        )
        # Track recently viewed for authenticated users
        if request.user.is_authenticated:
            from apps.users.models import RecentlyViewed
            RecentlyViewed.objects.update_or_create(
                user=request.user,
                property=instance,
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeaturedPropertiesView(generics.ListAPIView):
    """List featured properties for homepage."""
    serializer_class = PropertyListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Property.objects.filter(
            is_active=True, is_featured=True
        ).select_related('owner').prefetch_related('images', 'rooms')[:12]


class PopularPropertiesView(generics.ListAPIView):
    """List popular properties (highest rated + most viewed)."""
    serializer_class = PropertyListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Property.objects.filter(
            is_active=True, avg_rating__gte=3.5
        ).order_by('-total_views', '-avg_rating').select_related(
            'owner'
        ).prefetch_related('images', 'rooms')[:12]


class NearbyPropertiesView(APIView):
    """Find properties near given coordinates."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = float(request.query_params.get('radius', 5))  # km

        if not lat or not lng:
            return Response(
                {'error': 'lat and lng parameters are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        lat, lng = float(lat), float(lng)
        # Approximate degree distance (~111km per degree)
        degree_range = radius / 111.0

        properties = Property.objects.filter(
            is_active=True,
            latitude__range=(lat - degree_range, lat + degree_range),
            longitude__range=(lng - degree_range, lng + degree_range),
        ).select_related('owner').prefetch_related('images', 'rooms')

        serializer = PropertyListSerializer(properties, many=True)
        return Response(serializer.data)


class AutoSuggestView(APIView):
    """Auto-suggest cities, areas, and property names for search."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if len(query) < 2:
            return Response({'suggestions': []})

        from django.db.models import Q

        # Get matching cities
        cities = Property.objects.filter(
            city__icontains=query, is_active=True
        ).values_list('city', flat=True).distinct()[:5]

        # Get matching areas
        areas = Property.objects.filter(
            area__icontains=query, is_active=True
        ).values_list('area', flat=True).distinct()[:5]

        # Get matching property names
        names = Property.objects.filter(
            name__icontains=query, is_active=True
        ).values_list('name', flat=True)[:5]

        # Get matching colleges
        colleges = set()
        props_with_colleges = Property.objects.filter(
            is_active=True
        ).exclude(nearby_colleges=[]).values_list('nearby_colleges', flat=True)[:50]
        for college_list in props_with_colleges:
            if isinstance(college_list, list):
                for c in college_list:
                    if query.lower() in c.lower():
                        colleges.add(c)
                        if len(colleges) >= 5:
                            break

        suggestions = (
            [{'type': 'city', 'value': c} for c in cities] +
            [{'type': 'area', 'value': a} for a in areas] +
            [{'type': 'property', 'value': n} for n in names] +
            [{'type': 'college', 'value': c} for c in list(colleges)[:5]]
        )
        return Response({'suggestions': suggestions[:15]})


class AmenityListView(generics.ListAPIView):
    """List all available amenities."""
    serializer_class = AmenitySerializer
    permission_classes = [permissions.AllowAny]
    queryset = Amenity.objects.all()
    pagination_class = None


# ===================================================
# Owner Property Management Views
# ===================================================

class OwnerPropertyListView(generics.ListAPIView):
    """List properties owned by the authenticated owner."""
    serializer_class = PropertyListSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Property.objects.filter(
            owner=self.request.user
        ).select_related('owner').prefetch_related('images', 'rooms')


class OwnerPropertyCreateView(generics.CreateAPIView):
    """Create a new property listing."""
    serializer_class = PropertyCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        prop = serializer.save()
        # Update owner's property count
        if hasattr(self.request.user, 'owner_profile'):
            profile = self.request.user.owner_profile
            profile.total_properties = self.request.user.properties.count()
            profile.save(update_fields=['total_properties'])
        # Create notification for admin to verify
        from apps.notifications.models import Notification
        from django.contrib.auth import get_user_model
        User = get_user_model()
        for admin in User.objects.filter(role='admin'):
            Notification.objects.create(
                user=admin,
                notification_type='listing',
                title='New Property Listing',
                message=f'{self.request.user.get_full_name()} added "{prop.name}" in {prop.city}. Please verify.',
                related_object_id=prop.id,
            )


class OwnerPropertyUpdateView(generics.UpdateAPIView):
    """Update an existing property."""
    serializer_class = PropertyCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)


class OwnerPropertyDeleteView(generics.DestroyAPIView):
    """Soft-delete a property (set is_active=False)."""
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=['is_active'])
        return Response({'message': 'Property deactivated.'}, status=status.HTTP_200_OK)


class PropertyImageUploadView(APIView):
    """Upload images for a property."""
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, property_id):
        try:
            prop = Property.objects.get(id=property_id, owner=request.user)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        files = request.FILES.getlist('images')
        if not files:
            return Response({'error': 'No files provided.'}, status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        for i, file in enumerate(files):
            try:
                import cloudinary.uploader
                result = cloudinary.uploader.upload(
                    file, folder=f'stayfinder/properties/{property_id}/',
                    transformation=[{'width': 1200, 'height': 800, 'crop': 'fill', 'quality': 'auto'}]
                )
                url = result['secure_url']
            except (ImportError, Exception):
                from django.core.files.storage import default_storage
                path = default_storage.save(f'properties/{property_id}/{file.name}', file)
                url = f'/media/{path}'

            img = PropertyImage.objects.create(
                property=prop,
                image_url=url,
                is_primary=(i == 0 and not prop.images.filter(is_primary=True).exists()),
                order=prop.images.count() + i,
            )
            created_images.append(PropertyImageSerializer(img).data)

        return Response({'images': created_images}, status=status.HTTP_201_CREATED)


# ===================================================
# Admin Property Management Views
# ===================================================

class AdminPropertyListView(generics.ListAPIView):
    """List all properties for admin review."""
    serializer_class = PropertyListSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        queryset = Property.objects.all().select_related('owner')
        is_verified = self.request.query_params.get('is_verified')
        if is_verified is not None:
            queryset = queryset.filter(is_verified=is_verified.lower() == 'true')
        return queryset


class AdminPropertyActionView(APIView):
    """Admin actions on properties: verify, reject, feature, unfeature."""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            prop = Property.objects.get(pk=pk)
        except Property.DoesNotExist:
            return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'verify':
            prop.is_verified = True
            prop.save(update_fields=['is_verified'])
            # Notify owner
            from apps.notifications.models import Notification
            Notification.objects.create(
                user=prop.owner,
                notification_type='listing',
                title='Property Verified',
                message=f'Your property "{prop.name}" has been verified and is now live.',
                related_object_id=prop.id,
            )
            return Response({'message': 'Property verified.'})
        elif action == 'reject':
            reason = request.data.get('reason', 'Does not meet our guidelines.')
            prop.is_active = False
            prop.save(update_fields=['is_active'])
            from apps.notifications.models import Notification
            Notification.objects.create(
                user=prop.owner,
                notification_type='listing',
                title='Property Rejected',
                message=f'Your property "{prop.name}" was rejected. Reason: {reason}',
                related_object_id=prop.id,
            )
            return Response({'message': 'Property rejected.'})
        elif action == 'feature':
            prop.is_featured = True
            prop.save(update_fields=['is_featured'])
            return Response({'message': 'Property featured.'})
        elif action == 'unfeature':
            prop.is_featured = False
            prop.save(update_fields=['is_featured'])
            return Response({'message': 'Property unfeatured.'})
        else:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)


# ===================================================
# Smart Search View (replaces ai_engine)
# ===================================================

class SmartSearchView(APIView):
    """
    Natural language search that parses queries like:
    'girls hostel near PSG under 5000 with wifi'
    into structured filters and returns matching properties.
    """
    permission_classes = [permissions.AllowAny]

    # Keyword → filter mappings
    GENDER_KEYWORDS = {
        'girls': 'girls', 'girl': 'girls', 'ladies': 'girls', 'women': 'girls', 'female': 'girls',
        'boys': 'boys', 'boy': 'boys', 'men': 'boys', 'male': 'boys', 'gents': 'boys',
        'coliving': 'coliving', 'co-living': 'coliving', 'mixed': 'coliving', 'unisex': 'coliving',
    }

    TYPE_KEYWORDS = {
        'hostel': 'hostel', 'hostels': 'hostel',
        'pg': 'pg', 'paying guest': 'pg',
        'coliving': 'coliving', 'co-living': 'coliving',
        'flat': 'flat', 'apartment': 'flat',
    }

    COLLEGE_KEYWORDS = {
        'psg tech': 'PSG College of Technology',
        'psg college': 'PSG College of Arts & Science',
        'psg': 'PSG College of Technology',
        'rathinam': 'Rathinam College',
        'sri krishna': 'Sri Krishna College',
        'kumaraguru': 'Kumaraguru College',
        'karunya': 'Karunya University',
        'sns': 'SNS College',
        'ngp': 'NGP College',
        'hindusthan': 'Hindusthan College',
        'cit': 'CIT',
        'government arts': 'Government Arts College',
        'arts college': 'Government Arts College',
        'amrita': 'Amrita University',
    }

    AREA_KEYWORDS = [
        'ukkadam', 'gandhipuram', 'rs puram', 'peelamedu', 'hope college',
        'singanallur', 'saravanampatti', 'ganapathy', 'saibaba colony',
        'kuniyamuthur', 'podanur', 'sundarapuram', 'kalapatti', 'perur',
        'kovaipudur', 'sulur', 'mettupalayam', 'pollachi', 'kinathukadavu', 'madukkarai',
    ]

    AMENITY_KEYWORDS = [
        'wifi', 'ac', 'food', 'laundry', 'parking', 'cctv', 'power backup',
        'ro water', 'study hall', 'gym', 'hot water', 'geyser', 'tv',
    ]

    def get(self, request):
        import re
        query = request.query_params.get('q', '').strip().lower()
        if not query:
            return Response({'results': [], 'parsed_filters': {}})

        parsed = {}
        queryset = Property.objects.filter(is_active=True)

        # Parse gender
        for keyword, value in self.GENDER_KEYWORDS.items():
            if keyword in query:
                parsed['gender'] = value
                queryset = queryset.filter(gender=value)
                break

        # Parse property type
        for keyword, value in self.TYPE_KEYWORDS.items():
            if keyword in query:
                parsed['property_type'] = value
                queryset = queryset.filter(property_type=value)
                break

        # Parse budget (e.g., "under 5000", "below 8000", "within 6000")
        budget_match = re.search(r'(?:under|below|within|max|upto|up to|less than)\s*(?:rs\.?|₹)?\s*(\d{3,6})', query)
        if budget_match:
            max_rent = int(budget_match.group(1))
            parsed['max_budget'] = max_rent
            queryset = queryset.filter(rent_min__lte=max_rent)

        # Parse min budget
        min_match = re.search(r'(?:above|over|min|from|starting)\s*(?:rs\.?|₹)?\s*(\d{3,6})', query)
        if min_match:
            min_rent = int(min_match.group(1))
            parsed['min_budget'] = min_rent
            queryset = queryset.filter(rent_max__gte=min_rent)

        # Parse college
        for keyword, college in self.COLLEGE_KEYWORDS.items():
            if keyword in query:
                parsed['college'] = college
                queryset = queryset.filter(nearby_colleges__icontains=college)
                break

        # Parse area
        for area in self.AREA_KEYWORDS:
            if area in query:
                parsed['area'] = area.title()
                queryset = queryset.filter(area__icontains=area)
                break

        # Parse amenities
        found_amenities = []
        for amenity in self.AMENITY_KEYWORDS:
            if amenity in query:
                found_amenities.append(amenity)
                queryset = queryset.filter(amenities_list__icontains=amenity)
        if found_amenities:
            parsed['amenities'] = found_amenities

        # Parse food preference
        if 'veg' in query and 'non' not in query:
            parsed['food_type'] = 'Veg'
            queryset = queryset.filter(food_included=True, food_type__icontains='veg')
        elif 'non-veg' in query or 'non veg' in query:
            parsed['food_type'] = 'Non-Veg'
            queryset = queryset.filter(food_included=True)
        elif 'food' in query and 'food' not in found_amenities:
            parsed['food_included'] = True
            queryset = queryset.filter(food_included=True)

        # Order by rating and featured status
        queryset = queryset.select_related('owner').prefetch_related(
            'images', 'rooms'
        ).order_by('-is_featured', '-avg_rating', '-created_at')[:50]

        serializer = PropertyListSerializer(queryset, many=True)

        return Response({
            'results': serializer.data,
            'parsed_filters': parsed,
            'total': len(serializer.data),
        })

