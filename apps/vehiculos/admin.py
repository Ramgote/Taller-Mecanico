from django.contrib import admin
from .models import Marca, ModeloVehiculo, Vehiculo


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)


@admin.register(ModeloVehiculo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'activo')
    search_fields = ('nombre',)
    list_filter = ('marca', 'activo')


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('placa', 'cliente', 'marca', 'modelo', 'activo')
    search_fields = ('placa',)
    list_filter = ('marca', 'activo')
