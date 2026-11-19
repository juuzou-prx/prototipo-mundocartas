from django.conf import settings
from django.db import models
from torneos.models import Torneo


class Inscripcion(models.Model):
    ESTADOS = [
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inscripciones')
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')

    class Meta:
        unique_together = ['usuario', 'torneo']

    def __str__(self):
        return f'{self.usuario} - {self.torneo}'

class Pago(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    inscripcion = models.OneToOneField(Inscripcion, on_delete=models.CASCADE, related_name='pago')
    monto = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_pago = models.DateTimeField(null=True, blank=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='pagos_registrados')

    def __str__(self):
        return f'Pago de {self.inscripcion} ({self.estado})'