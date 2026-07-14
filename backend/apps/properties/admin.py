"""
Admin configuration for Property management.
"""
from django.contrib import admin
from .models import Property, Room, PropertyImage, PropertyVideo, Amenity


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'city', 'area', 'property_type', 'gender', 'rent_min', 'rent_max', 'is_verified', 'is_active', 'avg_rating')
    list_filter = ('property_type', 'gender', 'is_verified', 'is_active', 'is_featured', 'city', 'food_included')
    search_fields = ('name', 'description', 'city', 'area', 'address', 'owner__username')
    ordering = ('-created_at',)
    inlines = [RoomInline, PropertyImageInline]
    actions = ['verify_properties', 'feature_properties']

    @admin.action(description='Verify selected properties')
    def verify_properties(self, request, queryset):
        queryset.update(is_verified=True)

    @admin.action(description='Feature selected properties')
    def feature_properties(self, request, queryset):
        queryset.update(is_featured=True)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'category')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('property', 'room_type', 'rent', 'total_beds', 'available_beds')
    list_filter = ('room_type',)
