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
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    # usuarios
    path("usuarios/", views.lista_usuarios, name="lista_usuarios"),
    path("usuarios/baja/<int:pk>/", views.baja_usuario, name="baja_usuario"),
    path("usuarios/alta/<int:pk>/", views.alta_usuario, name="alta_usuario"),
    path("crear-usuario/", views.crear_usuario, name="crear_usuario"),

]

