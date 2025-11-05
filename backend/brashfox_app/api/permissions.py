from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    Admins can also edit.
    Read permissions are allowed to any request.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admins can edit anything
        if request.user and request.user.is_staff:
            return True

        # Write permissions are only allowed to the author of the object.
        return obj.author == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    For models with 'user' field instead of 'author'.
    Read permissions are allowed to any request.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow owners and admins to edit objects.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admins can edit anything
        if request.user and request.user.is_staff:
            return True

        # Check if object has 'author' or 'user' field
        owner_field = getattr(obj, 'author', None) or getattr(obj, 'user', None)
        return owner_field == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    Read permissions are allowed to any request.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admins
        return request.user and request.user.is_staff
