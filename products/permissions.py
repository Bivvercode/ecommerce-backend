"""
This module defines custom permission classes for use in
Django REST Framework views.

The `IsSuperUserOrReadOnly` permission class allows unrestricted
read-only access to all users, but restricts write, update, and
delete operations to superusers only. This ensures that sensitive
actions can only be performed by users with elevated privileges,
while still allowing general access to view the data.
"""
from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit objects.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser
