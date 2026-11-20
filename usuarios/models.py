from django.conf import settings
from django.db import models


def rol_jugador_default():
    rol, _ = Rol.objects.get_or_create(nombre='Jugador')
    return rol.id


class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, default=rol_jugador_default, related_name='perfiles')
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    def __str__(self):
        return f'{self.usuario.username} - {self.rol.nombre}'