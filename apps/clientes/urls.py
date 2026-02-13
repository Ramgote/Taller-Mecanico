from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_clientes, name="lista_clientes"),
    path("nuevo/", views.crear_cliente, name="crear_cliente"),
    path("editar/<int:pk>/", views.editar_cliente, name="editar_cliente"),
    path("baja/<int:pk>/", views.baja_cliente, name="baja_cliente"),
    path("alta/<int:pk>/", views.alta_cliente, name="alta_cliente"),
]
