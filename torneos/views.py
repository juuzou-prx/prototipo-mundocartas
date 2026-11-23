from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Juego, Torneo
from .forms import JuegoForm, TorneoForm
from django.db.models import ProtectedError

@staff_member_required(login_url='iniciar_sesion')
def juego_lista(request):
    juegos = Juego.objects.all()
    return render(request, 'torneos/juego/lista.html', {'juegos': juegos})

@staff_member_required(login_url='iniciar_sesion')
def juego_crear(request):
    form = JuegoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Juego creado correctamente.')
        return redirect('juego_lista')
    return render(request, 'torneos/juego/form.html', {'form': form, 'titulo': 'Nuevo juego'})

@staff_member_required(login_url='iniciar_sesion')
def juego_editar(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    form = JuegoForm(request.POST or None, request.FILES or None, instance=juego)
    if form.is_valid():
        form.save()
        messages.success(request, 'Juego actualizado correctamente.')
        return redirect('juego_lista')
    return render(request, 'torneos/juego/form.html', {'form': form, 'titulo': 'Editar juego'})

@staff_member_required(login_url='iniciar_sesion')
def juego_eliminar(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    if request.method == 'POST':
        try:
            juego.delete()
            messages.success(request, 'Juego eliminado correctamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar este juego porque tiene torneos creados con él.')
        return redirect('juego_lista')
    return render(request, 'torneos/juego/eliminar.html', {'juego': juego})

#torneo
def torneo_lista(request):
    torneos = Torneo.objects.select_related('juego')
    return render(request, 'torneos/torneo/lista.html', {'torneos': torneos})

def torneo_detalle(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    inscritos = torneo.inscripciones.filter(estado='activa').count()
    inscrito = request.user.is_authenticated and torneo.inscripciones.filter(
        usuario=request.user, estado='activa').exists()
    return render(request, 'torneos/torneo/detalle.html', {
        'torneo': torneo,
        'inscritos': inscritos,
        'cupos': torneo.cupo_maximo - inscritos,
        'inscrito': inscrito,
    })

@staff_member_required(login_url='iniciar_sesion')
def torneo_crear(request):
    form = TorneoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Torneo creado correctamente.')
        return redirect('torneo_lista')
    return render(request, 'torneos/torneo/form.html', {'form': form, 'titulo': 'Nuevo torneo'})

@staff_member_required(login_url='iniciar_sesion')
def torneo_editar(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    form = TorneoForm(request.POST or None, instance=torneo)
    if form.is_valid():
        form.save()
        messages.success(request, 'Torneo actualizado correctamente.')
        return redirect('torneo_lista')
    return render(request, 'torneos/torneo/form.html', {'form': form, 'titulo': 'Editar torneo'})

@staff_member_required(login_url='iniciar_sesion')
def torneo_cancelar(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    if request.method == 'POST':
        torneo.estado = 'cancelado'
        torneo.save()
        messages.success(request, 'Torneo cancelado correctamente.')
        return redirect('torneo_lista')
    return render(request, 'torneos/torneo/cancelar.html', {'torneo': torneo})

@staff_member_required(login_url='iniciar_sesion')
def torneo_eliminar(request, pk):
    torneo = get_object_or_404(Torneo, pk=pk)
    if request.method == 'POST':
        if torneo.estado == 'programado' and torneo.inscripciones.filter(estado='activa').exists():
            messages.error(request, 'No puedes eliminar un torneo programado con jugadores inscritos. Cancélalo primero.')
            return redirect('torneo_detalle', pk=torneo.pk)
        torneo.delete()
        messages.success(request, 'Torneo eliminado correctamente.')
        return redirect('torneo_lista')
    return render(request, 'torneos/torneo/eliminar.html', {'torneo': torneo})