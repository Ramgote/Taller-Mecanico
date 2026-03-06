from django.urls import path
from . import views
from .views import crear_cliente_ajax
# from .views import ListaClientesView

urlpatterns = [
    path("", views.lista_clientes, name="lista_clientes"),
    # path("", ListaClientesView.as_view(), name="lista_clientes"),
    path("nuevo/", views.crear_cliente, name="crear_cliente"),
    path("editar/<int:pk>/", views.editar_cliente, name="editar_cliente"),
    path("baja/<int:id>/", views.baja_cliente, name="baja_cliente"),
    path("alta/<int:id>/", views.alta_cliente, name="alta_cliente"),
    path('crear-ajax/', crear_cliente_ajax, name='crear_cliente_ajax'),
]
