from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class ModeloVehiculo(models.Model):
    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE,
        related_name="modelos"
    )

    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ("marca", "nombre")
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.marca.nombre} - {self.nombre}"

class Vehiculo(models.Model):

    TIPO_CHOICES = [
        ('liviano', 'Liviano'),
        ('mediano', 'Mediano'),
        ('pesado', 'Pesado'),
        ('maquinaria', 'Maquinaria'),
        ('moto', 'Moto'),
    ]

    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.CASCADE,
        related_name="vehiculos"
    )

    placa = models.CharField(max_length=20)

    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name="vehiculos"
    )

    modelo = models.ForeignKey(
        ModeloVehiculo,
        on_delete=models.PROTECT,
        related_name="vehiculos"
    )

    anio = models.PositiveIntegerField(blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    vin = models.CharField(max_length=50, blank=True, null=True)
    motor = models.CharField(max_length=100, blank=True, null=True)
    kilometraje = models.PositiveIntegerField(blank=True, null=True)

    observaciones = models.TextField(blank=True, null=True)

    activo = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("placa",)
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.placa} - {self.marca.nombre} {self.modelo.nombre}"
