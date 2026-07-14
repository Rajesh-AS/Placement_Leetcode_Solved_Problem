"""
Serializers for property listings, rooms, images, and amenities.
"""
from rest_framework import serializers
from .models import Property, Room, PropertyImage, PropertyVideo, Amenity


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name', 'icon', 'category']


class RoomSerializer(serializers.ModelSerializer):
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)

    class Meta:
        model = Room
        fields = [
            'id', 'room_type', 'room_type_display', 'rent', 'deposit',
            'total_beds', 'available_beds', 'has_attached_bathroom',
            'has_ac', 'has_balcony', 'description'
        ]


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image_url', 'caption', 'is_primary', 'order']


class PropertyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyVideo
        fields = ['id', 'video_url', 'caption']


class PropertyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for property list/search results."""

    owner_name = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    room_types = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'property_type', 'property_type_display',
            'gender', 'gender_display', 'city', 'area', 'address',
            'latitude', 'longitude', 'rent_min', 'rent_max', 'deposit',
            'available_beds', 'amenities_list', 'food_included',
            'is_verified', 'is_featured', 'avg_rating', 'total_reviews',
            'primary_image', 'owner_name', 'room_types', 'created_at'
        ]

    def get_owner_name(self, obj):
        return obj.owner.get_full_name() or obj.owner.username

    def get_primary_image(self, obj):
        return obj.primary_image

    def get_room_types(self, obj):
        return list(obj.rooms.values_list('room_type', flat=True).distinct())


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Full detail serializer with rooms, images, reviews, and owner info."""

    owner_name = serializers.SerializerMethodField()
    owner_phone = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    owner_avatar = serializers.CharField(source='owner.profile_picture', read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    videos = PropertyVideoSerializer(many=True, read_only=True)
    amenity_details = AmenitySerializer(source='amenities', many=True, read_only=True)
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'name', 'description', 'property_type', 'property_type_display',
            'gender', 'gender_display', 'address', 'city', 'area', 'state',
            'pincode', 'latitude', 'longitude', 'nearby_colleges',
            'nearby_bus_stops', 'nearby_railway_station', 'rent_min', 'rent_max',
            'deposit', 'total_beds', 'available_beds', 'amenities_list',
            'amenity_details', 'house_rules', 'food_included', 'food_type',
            'contact_phone', 'contact_email', 'is_verified', 'is_featured',
            'is_active', 'avg_rating', 'total_reviews', 'total_views',
            'rooms', 'images', 'videos', 'owner_id', 'owner_name',
            'owner_phone', 'owner_avatar', 'created_at', 'updated_at'
        ]

    def get_owner_name(self, obj):
        return obj.owner.get_full_name() or obj.owner.username

    def get_owner_phone(self, obj):
        return obj.contact_phone or obj.owner.phone


class PropertyCreateSerializer(serializers.ModelSerializer):
    """Serializer for property creation/update by owners."""

    rooms = RoomSerializer(many=True, required=False)

    class Meta:
        model = Property
        fields = [
            'name', 'description', 'property_type', 'gender', 'address',
            'city', 'area', 'state', 'pincode', 'latitude', 'longitude',
            'nearby_colleges', 'nearby_bus_stops', 'nearby_railway_station',
            'rent_min', 'rent_max', 'deposit', 'total_beds', 'available_beds',
            'amenities_list', 'house_rules', 'food_included', 'food_type',
            'contact_phone', 'contact_email', 'rooms'
        ]

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms', [])
        property_obj = Property.objects.create(
            owner=self.context['request'].user,
            **validated_data
        )
        for room_data in rooms_data:
            Room.objects.create(property=property_obj, **room_data)
        return property_obj

    def update(self, instance, validated_data):
        rooms_data = validated_data.pop('rooms', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if rooms_data is not None:
            # Replace rooms entirely on update
            instance.rooms.all().delete()
            for room_data in rooms_data:
                Room.objects.create(property=instance, **room_data)
        return instance
