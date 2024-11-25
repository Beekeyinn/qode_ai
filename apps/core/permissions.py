from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and obj.user == request.user
        ) or request.method in SAFE_METHODS

    def has_permission(self, request, view):
        return super().has_permission(request, view)
