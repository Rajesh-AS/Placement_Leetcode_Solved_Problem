"""
Filters for property search with multi-criteria support.
"""
from django_filters import rest_framework as filters
from .models import Property


class PropertyFilter(filters.FilterSet):
    """
    Advanced property filter supporting all search criteria:
    city, area, college, budget, gender, room type, distance, amenities, rating, availability.
    """

    # Location filters
    city = filters.CharFilter(field_name='city', lookup_expr='icontains')
    area = filters.CharFilter(field_name='area', lookup_expr='icontains')
    college = filters.CharFilter(method='filter_nearby_college')

    # Budget filters
    min_rent = filters.NumberFilter(field_name='rent_min', lookup_expr='gte')
    max_rent = filters.NumberFilter(field_name='rent_max', lookup_expr='lte')

    # Type filters
    property_type = filters.ChoiceFilter(choices=Property.PropertyType.choices)
    gender = filters.ChoiceFilter(choices=Property.GenderPreference.choices)
    room_type = filters.CharFilter(method='filter_room_type')

    # Feature filters
    food_included = filters.BooleanFilter()
    is_verified = filters.BooleanFilter()
    is_featured = filters.BooleanFilter()

    # Rating filter
    min_rating = filters.NumberFilter(field_name='avg_rating', lookup_expr='gte')

    # Availability
    available = filters.BooleanFilter(method='filter_available')

    # Amenities filter (comma-separated)
    amenities = filters.CharFilter(method='filter_amenities')

    # Search query (name, description, address)
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = Property
        fields = [
            'city', 'area', 'property_type', 'gender', 'food_included',
            'is_verified', 'is_featured'
        ]

    def filter_nearby_college(self, queryset, name, value):
        """Filter properties near a specific college."""
        return queryset.filter(nearby_colleges__icontains=value)

    def filter_room_type(self, queryset, name, value):
        """Filter by room type availability."""
        return queryset.filter(rooms__room_type=value, rooms__available_beds__gt=0).distinct()

    def filter_available(self, queryset, name, value):
        """Filter properties with available beds."""
        if value:
            return queryset.filter(available_beds__gt=0)
        return queryset

    def filter_amenities(self, queryset, name, value):
        """Filter by amenities (comma-separated names)."""
        amenity_names = [a.strip().lower() for a in value.split(',')]
        for amenity in amenity_names:
            queryset = queryset.filter(amenities_list__icontains=amenity)
        return queryset

    def filter_search(self, queryset, name, value):
        """General text search across name, description, address, city, area."""
        from django.db.models import Q
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(address__icontains=value) |
            Q(city__icontains=value) |
            Q(area__icontains=value)
        )
