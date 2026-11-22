from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from inscripciones.models import Inscripcion
from torneos.models import Torneo
from .forms import ResultadoForm
from .models import Resultado, Ranking
from torneos.models import Juego, Torneo
from django.db.models import Sum
from django.contrib.auth import get_user_model


def _inscripciones_disponibles(torneo, resultado=None):
    """Jugadores del torneo que participaron y aun no tienen resultado."""
    disponibles = Inscripcion.objects.filter(
        torneo=torneo, estado='activa', asistencia__participo=True, resultado__isnull=True)
    if resultado is not None:
        # al editar, el jugador actual tambien debe aparecer
        disponibles = Inscripcion.objects.filter(pk=resultado.inscripcion_id) | disponibles
    return disponibles.select_related('usuario')


@login_required
def resultado_indice(request):
    torneos = Torneo.objects.select_related('juego')
    return render(request, 'resultados/indice.html', {'torneos': torneos, 'titulo': 'Resultados'})


@login_required
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


@login_required
def ranking_lista(request):
    juegos = list(Juego.objects.all())
    # juego elegido en la pagina (?juego=ID); si no hay, el primero que tenga ranking
    elegido = None
    if request.GET.get('juego', '').isdigit():
        elegido = next((j for j in juegos if j.pk == int(request.GET['juego'])), None)
    if elegido is None:
        con_ranking = Ranking.objects.values_list('juego_id', flat=True).distinct()
        elegido = next((j for j in juegos if j.pk in con_ranking), juegos[0] if juegos else None)
    jugadores = list(Ranking.objects.filter(juego=elegido).select_related('usuario')) if elegido else []
    # empate: mismo puntaje = misma posicion, sin desempate inventado 
    for r in jugadores:
        r.posicion = 1 + sum(1 for otro in jugadores if otro.puntos_acumulados > r.puntos_acumulados)
    return render(request, 'resultados/ranking.html', {
        'jugadores': jugadores, 'juegos': juegos, 'elegido': elegido,
        'titulo': 'Ranking de jugadores'})

def _contexto_historial(usuario):
    participaciones = (Inscripcion.objects
                       .filter(usuario=usuario, asistencia__participo=True)
                       .select_related('torneo__juego', 'resultado')
                       .order_by('-torneo__fecha', '-torneo__hora'))
    total = Resultado.objects.filter(inscripcion__usuario=usuario).aggregate(total=Sum('puntos'))['total'] or 0
    return {'jugador': usuario, 'participaciones': participaciones, 'total_puntos': total}


@login_required
def historial_mio(request):
    contexto = _contexto_historial(request.user)
    contexto.update({'titulo': 'Mi historial', 'es_propio': True})
    return render(request, 'resultados/historial.html', contexto)

@staff_member_required
def historial_jugador(request, usuario_id):
    jugador = get_object_or_404(get_user_model(), pk=usuario_id)
    contexto = _contexto_historial(jugador)
    contexto.update({'titulo': 'Historial del jugador', 'es_propio': False})
    return render(request, 'resultados/historial.html', contexto)