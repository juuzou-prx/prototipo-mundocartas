from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from inscripciones.models import Inscripcion
from resultados.models import Resultado

# Para cambiar cuanto se gana, solo se modifican estos valores:
PUNTOS_POR_INSCRIPCION = 5
PUNTOS_POR_PODIO = {1: 30, 2: 20, 3: 10}   # posicion: puntos


class Recompensa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    costo_puntos = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['costo_puntos', 'nombre']

    def __str__(self):
        return f'{self.nombre} ({self.costo_puntos} pts)'


class CanjeRecompensa(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='canjes')
    recompensa = models.ForeignKey(Recompensa, on_delete=models.PROTECT, related_name='canjes')
    puntos_gastados = models.PositiveIntegerField(default=0)
    fecha_canje = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_canje']

    def clean(self):
        if not self.usuario_id or not self.recompensa_id:
            return
        if not self.recompensa.activa:
            raise ValidationError('Esta recompensa no está disponible.')
        if resumen_puntos(self.usuario)['disponibles'] < self.recompensa.costo_puntos:
            raise ValidationError('No tienes puntos suficientes para esta recompensa.')

    def save(self, *args, **kwargs):
        if not self.pk:
            # se guarda el costo del momento, por si el precio cambia despues
            self.puntos_gastados = self.recompensa.costo_puntos
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario} canjeó {self.recompensa.nombre}'


def resumen_puntos(usuario):
    """Puntos canjeables del jugador: ganados - gastados."""
    inscripciones = Inscripcion.objects.filter(usuario=usuario, estado='activa').count()
    ganados = inscripciones * PUNTOS_POR_INSCRIPCION
    for r in Resultado.objects.filter(inscripcion__usuario=usuario, posicion__in=PUNTOS_POR_PODIO):
        ganados += PUNTOS_POR_PODIO[r.posicion]
    gastados = usuario.canjes.aggregate(total=Sum('puntos_gastados'))['total'] or 0
    return {'ganados': ganados, 'gastados': gastados, 'disponibles': ganados - gastados}