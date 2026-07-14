"""
Custom permission classes for role-based access control.
"""
from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    """Only allow students."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'student'
            and not request.user.is_suspended
        )


class IsOwner(BasePermission):
    """Only allow property owners."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'owner'
            and not request.user.is_suspended
        )


class IsAdmin(BasePermission):
    """Only allow administrators."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsOwnerOrAdmin(BasePermission):
    """Allow property owners or administrators."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('owner', 'admin')
            and not request.user.is_suspended
        )


class IsStudentOrOwner(BasePermission):
    """Allow students or property owners."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('student', 'owner')
            and not request.user.is_suspended
        )


class IsPropertyOwner(BasePermission):
    """Check if user owns the specific property being accessed."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsNotSuspended(BasePermission):
    """Ensure the user is not suspended."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and not request.user.is_suspended
        )
