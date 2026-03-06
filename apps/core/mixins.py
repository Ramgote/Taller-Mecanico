from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    allowed_roles = []

    def dispatch(self, request, *args, **kwargs):

        if not hasattr(request.user, "perfil"):
            raise PermissionDenied("Usuario sin perfil")

        if request.user.perfil.rol not in self.allowed_roles:
            raise PermissionDenied("No tienes permisos para acceder aquí")

        return super().dispatch(request, *args, **kwargs)
    
class OwnerFilterMixin:
    """
    Filtra automáticamente los objetos por usuario dueño.
    """

    owner_field = "usuario"

    def get_queryset(self):
        qs = super().get_queryset()

        user = self.request.user

        if user.perfil.rol == "SUPERADMIN":
            return qs

        # Filtra automáticamente por el usuario logueado
        return qs.filter(**{self.owner_field: user})

