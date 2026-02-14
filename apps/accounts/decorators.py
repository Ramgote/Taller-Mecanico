from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def solo_superadmin(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.perfil.rol == "SUPERADMIN":
            return view_func(request, *args, **kwargs)

        return redirect("login")

    return wrapper


def solo_responsable(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.perfil.rol == "RESPONSABLE":
            return view_func(request, *args, **kwargs)

        return redirect("login")

    return wrapper


def rol_requerido(roles_permitidos):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            if request.user.perfil.rol not in roles_permitidos:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
