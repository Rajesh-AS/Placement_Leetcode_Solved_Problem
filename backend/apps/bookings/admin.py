from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'visit_date', 'visit_time', 'status', 'created_at')
    list_filter = ('status', 'visit_date')
    search_fields = ('user__username', 'property__name')
    ordering = ('-created_at',)
