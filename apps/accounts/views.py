from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import Perfil
from .forms import CrearUsuarioForm
from apps.clientes.models import Cliente
from .decorators import rol_requerido
from django.db.models import Q
from django.core.paginator import Paginator

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


@login_required
def dashboard(request):
    perfil = request.user.perfil

    # if perfil.rol == "SUPERADMIN":
    if request.user.perfil.es_superadmin():
        total_clientes = Cliente.objects.filter(activo=True).count()
        total_usuarios = User.objects.filter(is_active=True).count()

    else:
        total_clientes = Cliente.objects.filter(
            usuario=request.user,
            activo=True
        ).count()

        total_usuarios = None

    contexto = {
        "total_clientes": total_clientes,
        "total_usuarios": total_usuarios,
        "rol": perfil.rol
    }

    return render(request, "accounts/dashboard.html", contexto)

@rol_requerido(["SUPERADMIN"])
def lista_usuarios(request):

    if not request.user.perfil.es_superadmin() :
        messages.error(request, "No tienes permisos")
        return redirect("dashboard")

    query = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "activos")
    perfiles = Perfil.objects.select_related("user").all()

    if estado == "inactivos":
        perfiles = perfiles.filter(activo=False)
    else:
        perfiles = perfiles.filter(activo=True)

    # BUSCADOR
    if query:
        perfiles = perfiles.filter(
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(user__first_name__icontains=query)
        )

    paginator = Paginator(perfiles, 5)
    page_number = request.GET.get("page")
    perfiles = paginator.get_page(page_number)

    return render(request, "accounts/usuarios_lista.html", {
        "perfiles": perfiles,
        "query": query,
        "estado": estado
    })

@login_required
def baja_usuario(request, pk):

    if not request.user.perfil.es_superadmin() :
        messages.error(request, "No permitido")
        return redirect("dashboard")

    perfil = get_object_or_404(Perfil, pk=pk)

    perfil.activo = False
    perfil.save()

    messages.warning(request, "Usuario dado de baja")
    return redirect("lista_usuarios")

@login_required
def alta_usuario(request, pk):

    if not request.user.perfil.es_superadmin() :
        messages.error(request, "No permitido")
        return redirect("dashboard")

    perfil = get_object_or_404(Perfil, pk=pk)

    perfil.activo = True
    perfil.save()

    messages.success(request, "Usuario dado de alta")
    return redirect("lista_usuarios")

@login_required
def crear_usuario(request):

    if not request.user.perfil.es_superadmin() :
        return redirect("dashboard")

    form = CrearUsuarioForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        
        return redirect("lista_usuarios")

    return render(request, "accounts/crear_usuario.html", {"form": form})
