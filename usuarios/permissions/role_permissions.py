from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Permite acceso solo a usuarios con rol Admin
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == "Admin"


class IsBarberoRole(BasePermission):
    """
    Permite acceso solo a usuarios con rol Barbero
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == "Barbero"


class IsClienteRole(BasePermission):
    """
    Permite acceso solo a usuarios con rol Cliente
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == "Cliente"
    

class IsOwnerOrAdmin(BasePermission):
    """
    Permite acceso si el usuario es dueño del recurso
    o si es Admin
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.rol == "Admin"
            or obj.id == request.user.id
        )