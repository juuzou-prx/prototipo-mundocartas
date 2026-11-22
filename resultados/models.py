from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count, Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
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


class Ranking(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ranking')
    puntos_acumulados = models.PositiveIntegerField(default=0)
    torneos_jugados = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-puntos_acumulados', 'usuario__username']

    @classmethod
    def recalcular(cls):
        """Suma los puntos de todos los resultados y actualiza el ranking (HU23)."""
        totales = (Resultado.objects.order_by()
                   .values('inscripcion__usuario')
                   .annotate(puntos=Sum('puntos'), torneos=Count('id')))
        con_resultados = []
        for t in totales:
            cls.objects.update_or_create(
                usuario_id=t['inscripcion__usuario'],
                defaults={'puntos_acumulados': t['puntos'], 'torneos_jugados': t['torneos']},
            )
            con_resultados.append(t['inscripcion__usuario'])
        # quien ya no tiene resultados vuelve a cero
        cls.objects.exclude(usuario_id__in=con_resultados).update(puntos_acumulados=0, torneos_jugados=0)

    def __str__(self):
        return f'{self.usuario} - {self.puntos_acumulados} pts'


# el ranking se actualiza solo cada vez que se guarda o elimina un resultado
@receiver([post_save, post_delete], sender=Resultado)
def actualizar_ranking(sender, **kwargs):
    Ranking.recalcular()