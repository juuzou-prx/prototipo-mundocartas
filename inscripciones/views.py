from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
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


@login_required
def mis_inscripciones(request):
    inscripciones = Inscripcion.objects.filter(
        usuario=request.user, estado='activa'
    ).select_related('torneo__juego')
    return render(request, 'inscripciones/mis_inscripciones.html', {'inscripciones': inscripciones})


@login_required
def cancelar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk, usuario=request.user, estado='activa')
    if request.method == 'POST':
        inscripcion.estado = 'cancelada'
        inscripcion.save()
        messages.success(request, 'Tu inscripción fue cancelada.')
        return redirect('mis_inscripciones')
    return render(request, 'inscripciones/cancelar_inscripcion.html', {'inscripcion': inscripcion})


@staff_member_required
def lista_inscritos(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    inscripciones = torneo.inscripciones.filter(estado='activa').select_related('usuario')
    return render(request, 'inscripciones/lista_inscritos.html', {
        'torneo': torneo,
        'inscripciones': inscripciones,
    })