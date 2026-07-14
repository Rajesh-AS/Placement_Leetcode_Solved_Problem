"""
Admin configuration for User management.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, OwnerProfile, SearchHistory, RecentlyViewed


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for the User model with role-based fields."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_verified', 'is_suspended', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_suspended', 'is_active', 'gender', 'city')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'college')
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('StayFinder Profile', {
            'fields': ('role', 'phone', 'gender', 'profile_picture', 'city', 'college', 'google_id', 'is_verified', 'is_suspended')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('StayFinder Profile', {
            'fields': ('email', 'first_name', 'last_name', 'role', 'phone')
        }),
    )

    actions = ['suspend_users', 'unsuspend_users', 'verify_users']

    @admin.action(description='Suspend selected users')
    def suspend_users(self, request, queryset):
        queryset.update(is_suspended=True)

    @admin.action(description='Unsuspend selected users')
    def unsuspend_users(self, request, queryset):
        queryset.update(is_suspended=False)

    @admin.action(description='Verify selected users')
    def verify_users(self, request, queryset):
        queryset.update(is_verified=True)


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'is_verified_owner', 'total_properties', 'total_earnings')
    list_filter = ('is_verified_owner',)
    search_fields = ('user__username', 'user__email', 'business_name')


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'city', 'created_at')
    list_filter = ('city',)
    readonly_fields = ('created_at',)


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'viewed_at')
    readonly_fields = ('viewed_at',)
