from django.shortcuts import redirect

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