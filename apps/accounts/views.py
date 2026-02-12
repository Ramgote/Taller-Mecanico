"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import LoginForm, CrearUsuarioForm
from .decorators import solo_superadmin


# -------- LOGIN --------

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None and user.is_active:
                login(request, user)
                return redirect("dashboard")
            else:
                form.add_error(None, "Credenciales inválidas")

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# -------- GESTIÓN DE USUARIOS --------

@login_required
@solo_superadmin
def lista_usuarios(request):
    usuarios = User.objects.all().select_related("perfil")
    return render(
        request,
        "accounts/lista.html",
        {"usuarios": usuarios}
    )


@login_required
@solo_superadmin
def crear_usuario(request):

    form = CrearUsuarioForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("lista_usuarios")

    return render(
        request,
        "accounts/crear.html",
        {"form": form}
    )


@login_required
@solo_superadmin
def toggle_usuario(request, user_id):

    user = get_object_or_404(User, id=user_id)

    if user != request.user:  # evitar desactivarse a sí mismo
        user.is_active = not user.is_active
        user.save()

    return redirect("lista_usuarios")

"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenido al sistema 👍")
            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)

            return redirect("dashboard")

        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "accounts/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")



