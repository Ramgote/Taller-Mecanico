from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cliente
from .forms import ClienteForm


@login_required
def lista_clientes(request):
    clientes = Cliente.objects.filter(
        usuario=request.user,
        activo=True
    ).order_by("-id")
    
    return render(request, "clientes/lista.html", {"clientes": clientes})


@login_required
def crear_cliente(request):
    form = ClienteForm(request.POST or None)

    if form.is_valid():
        cliente = form.save(commit=False) 
        cliente.usuario = request.user
        cliente.save()
        messages.success(request, "Cliente creado correctamente")
        return redirect("lista_clientes")

    return render(request, "clientes/form.html", {"form": form})


@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        messages.success(request, "Cliente actualizado")
        return redirect("lista_clientes")

    return render(request, "clientes/form.html", {"form": form})

@login_required
def baja_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    cliente.activo = False
    cliente.save()

    messages.warning(request, "Cliente dado de baja")
    return redirect("lista_clientes")

@login_required
def alta_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    cliente.activo = True
    cliente.save()

    messages.success(request, "Cliente reactivado")
    return redirect("lista_clientes")
