from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
class Cliente(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    telefono_alt = models.CharField(max_length=30, blank=True, null=True)
    nit_ci = models.CharField(max_length=50, blank=True, null=True)

    activo = models.BooleanField(default=True) 
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

"""    
class Cliente(models.Model):

    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    telefono_alt = models.CharField(max_length=30, blank=True, null=True)
    nit_ci = models.CharField(max_length=50, blank=True, null=True)

    activo = models.BooleanField(default=True)

    creado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clientes_creados"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.nombre
