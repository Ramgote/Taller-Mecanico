from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Marca, ModeloVehiculo, Vehiculo
from .forms import MarcaForm, ModeloVehiculoForm, VehiculoForm
from apps.accounts.decorators import rol_requerido


@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def lista_marcas(request):
    marcas = Marca.objects.filter(activo=True)
    paginator = Paginator(marcas, 10)
    page = request.GET.get("page")
    marcas = paginator.get_page(page)

    return render(request, "vehiculos/marca_lista.html", {
        "marcas": marcas
    })


@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def crear_marca(request):
    """
    form = MarcaForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Marca creada correctamente")
            return redirect("lista_marcas")
        else:
                # ESTO TE MOSTRARÁ EN CONSOLA POR QUÉ FALLA
                print(form.errors) 
                messages.error(request, "Error al validar el formulario. Revisa los datos.")

    return render(request, "vehiculos/marca_form.html", {
        "form": form,
        "titulo": "Crear Marca",
        "boton": "Guardar"
    })
    """

    if request.method == "POST":
        form = VehiculoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Vehículo registrado correctamente")
            return redirect("lista_vehiculos")

        else:
            print(form.errors)  # DEBUG

    else:
        form = VehiculoForm()

    return render(request, "vehiculos/vehiculo_form.html", {
        "form": form,
        "titulo": "Registrar Vehículo",
        "boton": "Guardar"
    })

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def editar_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    form = MarcaForm(request.POST or None, instance=marca)

    if form.is_valid():
        form.save()
        messages.success(request, "Marca actualizada")
        return redirect("lista_marcas")

    return render(request, "vehiculos/marca_form.html", {
        "form": form,
        "titulo": "Editar Marca",
        "boton": "Actualizar"
    })


@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def baja_marca(request, pk):
    marca = get_object_or_404(Marca, pk=pk)
    marca.activo = False
    marca.save()
    messages.warning(request, "Marca desactivada")
    return redirect("lista_marcas")

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def lista_modelos(request):
    modelos = ModeloVehiculo.objects.filter(activo=True)
    paginator = Paginator(modelos, 10)
    page = request.GET.get("page")
    modelos = paginator.get_page(page)

    return render(request, "vehiculos/modelo_lista.html", {
        "modelos": modelos
    })


@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def crear_modelo(request):
    form = ModeloVehiculoForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Modelo creado")
        return redirect("lista_modelos")

    return render(request, "vehiculos/modelo_form.html", {
        "form": form,
        "titulo": "Crear Modelo",
        "boton": "Guardar"
    })

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def lista_vehiculos(request):

    vehiculos = Vehiculo.objects.filter(activo=True)
    paginator = Paginator(vehiculos, 5)
    page = request.GET.get("page")
    vehiculos = paginator.get_page(page)

    return render(request, "vehiculos/vehiculo_lista.html", {
        "vehiculos": vehiculos
    })

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def crear_vehiculo(request):

    form = VehiculoForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Vehículo registrado correctamente")
        return redirect("lista_vehiculos")

    return render(request, "vehiculos/vehiculo_form.html", {
        "form": form,
        "titulo": "Registrar Vehículo",
        "boton": "Guardar"
    })

@rol_requerido(["SUPERADMIN", "RESPONSABLE"])
def editar_vehiculo(request, pk):

    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    form = VehiculoForm(request.POST or None, instance=vehiculo)

    if form.is_valid():
        form.save()
        messages.success(request, "Vehículo actualizado")
        return redirect("lista_vehiculos")

    return render(request, "vehiculos/vehiculo_form.html", {
        "form": form,
        "titulo": "Editar Vehículo",
        "boton": "Actualizar"
    })

from django.views.decorators.http import require_POST
from django.http import JsonResponse

@require_POST
def crear_marca_ajax(request):
    nombre = request.POST.get('nombre')

    if not nombre:
        return JsonResponse({'error': 'Nombre requerido'}, status=400)

    marca, created = Marca.objects.get_or_create(nombre=nombre.strip())

    return JsonResponse({
        'id': marca.id,
        'nombre': marca.nombre
    })


@require_POST
def crear_modelo_ajax(request):
    nombre = request.POST.get('nombre')
    marca_id = request.POST.get('marca_id')

    if not nombre or not marca_id:
        return JsonResponse({'error': 'Datos incompletos'}, status=400)

    modelo = ModeloVehiculo.objects.create(
        nombre=nombre.strip(),
        marca_id=marca_id
    )

    return JsonResponse({
        'id': modelo.id,
        'nombre': modelo.nombre
    })

from django.http import JsonResponse
from .models import ModeloVehiculo

def obtener_modelos_por_marca(request):
    marca_id = request.GET.get("marca_id")

    if not marca_id:
        return JsonResponse({"modelos": []})

    modelos = ModeloVehiculo.objects.filter(marca_id=marca_id).values("id", "nombre")

    return JsonResponse({
        "modelos": list(modelos)
    })