from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):

    ROLES = (
        ('SUPERADMIN', 'Super Administrador'),
        ('RESPONSABLE', 'Responsable'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"
