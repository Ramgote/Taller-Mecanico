from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_vehiculos, name="lista_vehiculos"),
    path("nuevo/", views.crear_vehiculo, name="crear_vehiculo"),
    path("editar/<int:pk>/", views.editar_vehiculo, name="editar_vehiculo"),

    path("marcas/", views.lista_marcas, name="lista_marcas"),
    path("marcas/nueva/", views.crear_marca, name="crear_marca"),
    path("marcas/<int:pk>/editar/", views.editar_marca, name="editar_marca"),
    path("marcas/<int:pk>/baja/", views.baja_marca, name="baja_marca"),
    
    path("modelos/", views.lista_modelos, name="lista_modelos"),
    path("modelos/nuevo/", views.crear_modelo, name="crear_modelo"),
    # path("modelos/editar/<int:pk>/", views.editar_modelo, name="editar_modelo"),
    # path("modelos/baja/<int:pk>/", views.baja_modelo, name="baja_modelo"),

    path('ajax/crear-marca/', views.crear_marca_ajax, name='crear_marca_ajax'),
    path('ajax/crear-modelo/', views.crear_modelo_ajax, name='crear_modelo_ajax'),
    path('ajax/modelos-por-marca/', views.obtener_modelos_por_marca, name='modelos_por_marca'),
]
