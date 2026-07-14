"""
Serializers for booking management.
"""
from rest_framework import serializers
from .models import Booking, Payment


class BookingSerializer(serializers.ModelSerializer):
    """Full booking serializer with related data."""

    user_name = serializers.SerializerMethodField()
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_phone = serializers.CharField(source='user.phone', read_only=True)
    property_name = serializers.CharField(source='property.name', read_only=True)
    property_city = serializers.CharField(source='property.city', read_only=True)
    property_image = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    room_type = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'property', 'room', 'visit_date', 'visit_time',
            'message', 'status', 'status_display', 'owner_notes',
            'rescheduled_date', 'rescheduled_time', 'reschedule_reason',
            'user_name', 'user_email', 'user_phone', 'property_name',
            'property_city', 'property_image', 'owner_name', 'room_type',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'owner_notes', 'rescheduled_date',
            'rescheduled_time', 'reschedule_reason', 'created_at', 'updated_at'
        ]

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username

    def get_owner_name(self, obj):
        return obj.property.owner.get_full_name() or obj.property.owner.username

    def get_property_image(self, obj):
        return obj.property.primary_image

    def get_room_type(self, obj):
        return obj.room.get_room_type_display() if obj.room else None


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a booking."""

    class Meta:
        model = Booking
        fields = ['property', 'room', 'visit_date', 'visit_time', 'message']

    def validate(self, data):
        from django.utils import timezone
        import datetime
        visit_datetime = datetime.datetime.combine(data['visit_date'], data['visit_time'])
        if visit_datetime < datetime.datetime.now():
            raise serializers.ValidationError("Visit date/time must be in the future.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookingStatusUpdateSerializer(serializers.Serializer):
    """Serializer for owner/admin to update booking status."""

    action = serializers.ChoiceField(choices=['approve', 'reject', 'cancel', 'complete', 'reschedule'])
    owner_notes = serializers.CharField(required=False, allow_blank=True)
    rescheduled_date = serializers.DateField(required=False)
    rescheduled_time = serializers.TimeField(required=False)
    reschedule_reason = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if data['action'] == 'reschedule':
            if not data.get('rescheduled_date') or not data.get('rescheduled_time'):
                raise serializers.ValidationError("Rescheduled date and time are required.")
        return data

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
