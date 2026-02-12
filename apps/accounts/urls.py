"""
from django.urls import path
from .views import (
    login_view,
    logout_view,
    lista_usuarios,
    crear_usuario,
    toggle_usuario,
)

urlpatterns = [
    # Login
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Usuarios
    path("usuarios/", lista_usuarios, name="lista_usuarios"),
    path("usuarios/crear/", crear_usuario, name="crear_usuario"),
    path("usuarios/toggle/<int:user_id>/", toggle_usuario, name="toggle_usuario"
    ),
]
"""
from django.urls import path
from .views import login_view, logout_view, dashboard

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/", dashboard, name="dashboard"),
]

