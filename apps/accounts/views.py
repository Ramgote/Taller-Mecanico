from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import Perfil
from .forms import CrearUsuarioForm

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "accounts/login.html")


# ---------------- LOGOUT ----------------

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- DASHBOARD ----------------

@login_required
def dashboard(request):
    rol = request.user.perfil.rol

    contexto = {
        "rol": rol
    }

    return render(request, "accounts/dashboard.html", contexto)

@login_required
def lista_usuarios(request):

    if request.user.perfil.rol != "SUPERADMIN":
        messages.error(request, "No tienes permisos")
        return redirect("dashboard")

    perfiles = Perfil.objects.select_related("user")

    return render(request, "accounts/usuarios_lista.html", {
        "perfiles": perfiles
    })

@login_required
def baja_usuario(request, pk):

    if request.user.perfil.rol != "SUPERADMIN":
        messages.error(request, "No permitido")
        return redirect("dashboard")

    perfil = get_object_or_404(Perfil, pk=pk)

    perfil.activo = False
    perfil.save()

    messages.warning(request, "Usuario dado de baja")
    return redirect("lista_usuarios")

@login_required
def alta_usuario(request, pk):

    if request.user.perfil.rol != "SUPERADMIN":
        messages.error(request, "No permitido")
        return redirect("dashboard")

    perfil = get_object_or_404(Perfil, pk=pk)

    perfil.activo = True
    perfil.save()

    messages.success(request, "Usuario reactivado")
    return redirect("lista_usuarios")

@login_required
def crear_usuario(request):

    if request.user.perfil.rol != "SUPERADMIN":
        return redirect("dashboard")

    form = CrearUsuarioForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        
        return redirect("lista_usuarios")

    return render(request, "accounts/crear_usuario.html", {"form": form})
