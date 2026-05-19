from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCatOwnerOrReadOnly(BasePermission):
    """Allow write access only to the owner of the cat being traveled."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.cat.owner == request.user
