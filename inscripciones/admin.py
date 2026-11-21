from django.contrib import admin
from .models import Inscripcion, Pago, Asistencia

admin.site.register(Inscripcion)
admin.site.register(Pago)
admin.site.register(Asistencia)