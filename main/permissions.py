from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from main.models import Roles


class IsPublic(permissions.BasePermission):
    """
    Permiso personalizado que permite el acceso solo a usuarios con rol ...
    """

    def has_permission(self, request, view):
        return True


class IsProfesor(permissions.BasePermission):
    """
    Permiso personalizado que permite el acceso solo a usuarios con rol ...
    """

    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado y tiene el rol adecuado
        if not request.user.is_authenticated:
            raise PermissionDenied("Usuario no autenticado")

        if (
            not getattr(request.user, "tipo_usuario", None).codigo_rol
            == Roles.PROFESOR.value
        ):
            raise PermissionDenied("Recurso requiere privilegios de profesor.")

        return True
