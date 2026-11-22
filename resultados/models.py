from django.core.exceptions import ValidationError
from django.db import models
from inscripciones.models import Inscripcion


class Resultado(models.Model):
    inscripcion = models.OneToOneField(Inscripcion, on_delete=models.CASCADE, related_name='resultado')
    posicion = models.PositiveIntegerField()
    puntos = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['posicion']

    def clean(self):
        if not self.inscripcion_id:
            return
        # solo pueden tener resultado quienes participaron
        asistencia = getattr(self.inscripcion, 'asistencia', None)
        if asistencia is None or not asistencia.participo:
            raise ValidationError('Solo se puede registrar resultado a jugadores que participaron.')
        # no repetir posicion dentro del mismo torneo
        repetida = Resultado.objects.filter(
            inscripcion__torneo=self.inscripcion.torneo, posicion=self.posicion
        ).exclude(pk=self.pk)
        if repetida.exists():
            raise ValidationError('Ya existe otro jugador con esa posición en este torneo.')

    def __str__(self):
        return f'{self.inscripcion} - puesto {self.posicion}'