from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from torneos.models import Torneo
from .models import Inscripcion


@login_required
def inscribirse(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    if request.method == 'POST':
        if torneo.estado != 'programado':
            messages.error(request, 'Este torneo no admite inscripciones.')
        elif torneo.inscripciones.filter(estado='activa').count() >= torneo.cupo_maximo:
            messages.error(request, 'El cupo de este torneo está lleno.')
        else:
            insc, creada = Inscripcion.objects.get_or_create(usuario=request.user, torneo=torneo)
            if creada:
                messages.success(request, 'Te inscribiste correctamente.')
            elif insc.estado == 'cancelada':
                insc.estado = 'activa'
                insc.save()
                messages.success(request, 'Te inscribiste correctamente.')
            else:
                messages.info(request, 'Ya estás inscrito en este torneo.')
    return redirect('torneo_detalle', pk=torneo.pk)