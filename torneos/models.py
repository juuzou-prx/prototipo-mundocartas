from django.db import models

class Juego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='juegos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Torneo(models.Model):
    ESTADOS = [
        ('programado', 'Programado'),
        ('cancelado', 'Cancelado'),
        ('finalizado', 'Finalizado'),
    ]

    nombre = models.CharField(max_length=150)
    juego = models.ForeignKey(Juego, on_delete=models.PROTECT, related_name='torneos')
    fecha = models.DateField()
    hora = models.TimeField()
    cupo_maximo = models.PositiveIntegerField()
    costo = models.PositiveIntegerField(default=0)
    reglas = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='programado')

    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return self.nombre