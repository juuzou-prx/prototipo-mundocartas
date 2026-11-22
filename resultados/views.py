from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from inscripciones.models import Inscripcion
from torneos.models import Torneo
from .forms import ResultadoForm
from .models import Resultado


def _inscripciones_disponibles(torneo, resultado=None):
    """Jugadores del torneo que participaron y aun no tienen resultado."""
    disponibles = Inscripcion.objects.filter(
        torneo=torneo, estado='activa', asistencia__participo=True, resultado__isnull=True)
    if resultado is not None:
        # al editar, el jugador actual tambien debe aparecer
        disponibles = Inscripcion.objects.filter(pk=resultado.inscripcion_id) | disponibles
    return disponibles.select_related('usuario')


def resultado_indice(request):
    torneos = Torneo.objects.select_related('juego')
    return render(request, 'resultados/indice.html', {'torneos': torneos, 'titulo': 'Resultados'})


def resultado_lista(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    resultados = Resultado.objects.filter(
        inscripcion__torneo=torneo).select_related('inscripcion__usuario')
    return render(request, 'resultados/lista.html', {
        'torneo': torneo,
        'resultados': resultados,
        'titulo': 'Resultados del torneo',
    })


@staff_member_required
def resultado_crear(request, torneo_id):
    torneo = get_object_or_404(Torneo, pk=torneo_id)
    form = ResultadoForm(request.POST or None)
    form.fields['inscripcion'].queryset = _inscripciones_disponibles(torneo)
    if form.is_valid():
        form.save()
        messages.success(request, 'Resultado registrado correctamente.')
        return redirect('resultado_lista', torneo_id=torneo.pk)
    return render(request, 'resultados/form.html', {
        'form': form, 'torneo': torneo, 'titulo': 'Registrar resultado'})


@staff_member_required
def resultado_editar(request, pk):
    resultado = get_object_or_404(Resultado, pk=pk)
    torneo = resultado.inscripcion.torneo
    form = ResultadoForm(request.POST or None, instance=resultado)
    form.fields['inscripcion'].queryset = _inscripciones_disponibles(torneo, resultado)
    if form.is_valid():
        form.save()
        messages.success(request, 'Resultado actualizado correctamente.')
        return redirect('resultado_lista', torneo_id=torneo.pk)
    return render(request, 'resultados/form.html', {
        'form': form, 'torneo': torneo, 'titulo': 'Editar resultado'})


@staff_member_required
def resultado_eliminar(request, pk):
    resultado = get_object_or_404(Resultado, pk=pk)
    torneo = resultado.inscripcion.torneo
    if request.method == 'POST':
        resultado.delete()
        messages.success(request, 'Resultado eliminado correctamente.')
        return redirect('resultado_lista', torneo_id=torneo.pk)
    return render(request, 'resultados/eliminar.html', {
        'resultado': resultado, 'torneo': torneo, 'titulo': 'Eliminar resultado'})