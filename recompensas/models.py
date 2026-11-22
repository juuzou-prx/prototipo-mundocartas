from django.core.validators import MinValueValidator
from django.db import models


class Recompensa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    costo_puntos = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['costo_puntos', 'nombre']

    def __str__(self):
        return f'{self.nombre} ({self.costo_puntos} pts)'