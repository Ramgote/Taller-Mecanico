from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Cliente
from .forms import ClienteForm
from django.urls import reverse
from apps.accounts.decorators import rol_requerido
from apps.clientes.utils import clientes_visibles_para
from django.db.models import Q
from django.core.paginator import Paginator

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def lista_clientes(request):

    query = request.GET.get("q", "")
    estado = request.GET.get("estado", "activos")

    clientes = clientes_visibles_para(request.user)

    if estado == "inactivos":
        clientes = clientes.filter(activo=False)
    else:
        clientes = clientes.filter(activo=True)

    # BUSCADOR
    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(telefono__icontains=query)
        )

    paginator = Paginator(clientes.order_by("-id"), 5)
    page_number = request.GET.get("page")
    clientes = paginator.get_page(page_number)

    return render(request, "clientes/clientes_lista.html", {
        "clientes": clientes,
        "query": query,
        "estado": estado
    })

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def crear_cliente(request):
    # Esto es para cuando le demos al superadmin la posibilidad de crea clientes
    # form = ClienteForm(request.POST or None, instance=cliente, user=request.user)
    form = ClienteForm(request.POST or None)
    responsables = User.objects.filter(
                perfil__rol="RESPONSABLE",
                is_active=True
            )

    if form.is_valid():

        cliente = form.save(commit=False)

        # RESPONSABLE → se asigna solo
        if request.user.perfil.rol == "RESPONSABLE":
            cliente.usuario = request.user

        # SUPERADMIN → debe elegir responsable
        elif request.user.perfil.rol == "SUPERADMIN":
            responsable_id = request.POST.get("usuario")

            if not responsable_id:
                messages.error(request, "Debe elegir responsable")
                return render(request, "clientes/crear.html", {
                    "form": form,
                    "responsables": responsables,
                    "titulo": "👤 Crear Cliente",
                    "boton": "Guardar Cliente",
                    "cancelar_url": reverse("lista_clientes")
                })
            
            cliente.usuario = User.objects.get(id=responsable_id)
        cliente.activo = True
        cliente.save()

        messages.success(request, "Cliente creado correctamente")
        return redirect("lista_clientes")
    else:
        print("Error en el form : ", form.errors)
    return render(request, "clientes/crear.html", {
        "form": form,
        "responsables": responsables,
        "titulo": "👤 Crear Cliente",
        "boton": "Guardar Cliente",
        "cancelar_url": reverse("lista_clientes")
    })

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    responsables = User.objects.filter(
                perfil__rol="RESPONSABLE",
                is_active=True
            )
    
    form = ClienteForm(
        # request.POST or None,
        request.POST or None,
        instance=cliente,
        # user=request.user
    ) 

    if form.is_valid():
        # obj = form.save(commit=False)    
        # Si quieres asegurar que no cambie el estado activo:
        # obj.activo = cliente.activo 
    
        # obj.save()
        form.save()
        messages.success(request, "Cliente actualizado")
        return redirect("lista_clientes")
    else:
        print("Algo esta fallando", form.errors)

    return render(request, "clientes/editar.html", {        
            "form": form,
            "titulo": "✏️ Editar Cliente",
            "responsables": responsables,
            "responsable_id": cliente.usuario_id,
            "boton": "Actualizar Cliente",
            "cancelar_url": reverse("lista_clientes")
        })

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def baja_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.activo = False
    cliente.save()
    messages.warning(request, "Cliente dado de baja")
    return redirect("lista_clientes")

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def alta_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.activo = True
    cliente.save()
    messages.success(request, "Cliente dado de alta")
    return redirect("lista_clientes")

