from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Count, Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from inscripciones.models import Inscripcion
from torneos.models import Juego


class Resultado(models.Model):
    inscripcion = models.OneToOneField(Inscripcion, on_delete=models.CASCADE, related_name='resultado')
    posicion = models.PositiveIntegerField()
    puntos = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['posicion']

    def clean(self):
        if not self.inscripcion_id:
            return
        # solo pueden tener resultado quienes participaron (HU20)
        asistencia = getattr(self.inscripcion, 'asistencia', None)
        if asistencia is None or not asistencia.participo:
            raise ValidationError('Solo se puede registrar resultado a jugadores que participaron.')
        # no repetir posicion dentro del mismo torneo (HU21)
        repetida = Resultado.objects.filter(
            inscripcion__torneo=self.inscripcion.torneo, posicion=self.posicion
        ).exclude(pk=self.pk)
        if repetida.exists():
            raise ValidationError('Ya existe otro jugador con esa posición en este torneo.')

    def __str__(self):
        return f'{self.inscripcion} - puesto {self.posicion}'


class Ranking(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rankings')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='rankings')
    puntos_acumulados = models.PositiveIntegerField(default=0)
    torneos_jugados = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['juego__nombre', '-puntos_acumulados', 'usuario__username']
        unique_together = ['usuario', 'juego']

    @classmethod
    def recalcular(cls):
        """Suma los puntos de los resultados por jugador y por juego (HU23)."""
        totales = (Resultado.objects.order_by()
                   .values('inscripcion__usuario', 'inscripcion__torneo__juego')
                   .annotate(puntos=Sum('puntos'), torneos=Count('id')))
        with transaction.atomic():
            # el ranking se puede reconstruir siempre desde los resultados
            cls.objects.all().delete()
            cls.objects.bulk_create([
                cls(usuario_id=t['inscripcion__usuario'],
                    juego_id=t['inscripcion__torneo__juego'],
                    puntos_acumulados=t['puntos'],
                    torneos_jugados=t['torneos'])
                for t in totales
            ])

    def __str__(self):
        return f'{self.usuario} - {self.juego} - {self.puntos_acumulados} pts'


# el ranking se actualiza solo cada vez que se guarda o elimina un resultado
@receiver([post_save, post_delete], sender=Resultado)
def actualizar_ranking(sender, **kwargs):
    Ranking.recalcular()