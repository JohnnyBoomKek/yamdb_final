from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        role = getattr(request.user, 'role', '')
        if role in ['admin'] or request.user.is_superuser:
            return True
        return False


class IsSuperuserPermission(permissions.BasePermission):

    def has_permission(self, request, view,):

        if request.method in permissions.SAFE_METHODS:
            return True
        role = getattr(request.user, 'role', '')
        if role in ['admin'] or request.user.is_superuser:
            return True


class IsAuthorOrAdminorReadOnlyPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        role = getattr(request.user, 'role', '')
        if role in ['admin', 'moderator'] or request.user.is_superuser:
            return True
        return request.user == obj.author
