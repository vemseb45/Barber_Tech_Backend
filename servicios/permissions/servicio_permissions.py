from rest_framework.permissions import BasePermission


class IsAdminServicio(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.rol == "Admin"
        )