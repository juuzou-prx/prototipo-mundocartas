from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecompensaForm
from .models import Recompensa, CanjeRecompensa, resumen_puntos
from django.contrib.auth import get_user_model
from django.db.models import Count, ProtectedError, Q


@login_required
def recompensa_lista(request):
    recompensas = Recompensa.objects.all()
    if not request.user.is_staff:
        recompensas = recompensas.filter(activa=True)
    puntos = resumen_puntos(request.user)
    recompensas = list(recompensas)
    for r in recompensas:
        r.faltan = max(0, r.costo_puntos - puntos['disponibles'])
    return render(request, 'recompensas/lista.html', {
        'recompensas': recompensas, 'puntos': puntos, 'titulo': 'Recompensas'})


@login_required
@require_POST
def canje_crear(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    canje = CanjeRecompensa(usuario=request.user, recompensa=recompensa)
    try:
        canje.full_clean()
        canje.save()
        messages.success(request, f'Canjeaste "{recompensa.nombre}" por {canje.puntos_gastados} puntos.')
    except ValidationError as e:
        messages.error(request, ' '.join(e.messages))
    return redirect('recompensa_lista')


@login_required
def canje_lista(request):
    canjes = CanjeRecompensa.objects.select_related('usuario', 'recompensa')
    if not request.user.is_staff:
        canjes = canjes.filter(usuario=request.user)
    return render(request, 'recompensas/canjes.html', {
        'canjes': canjes, 'puntos': resumen_puntos(request.user), 'titulo': 'Canjes'})


@staff_member_required(login_url='iniciar_sesion')
def recompensa_crear(request):
    form = RecompensaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Recompensa creada correctamente.')
        return redirect('recompensa_lista')
    return render(request, 'recompensas/form.html', {'form': form, 'titulo': 'Nueva recompensa'})


@staff_member_required(login_url='iniciar_sesion')
def recompensa_editar(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    form = RecompensaForm(request.POST or None, instance=recompensa)
    if form.is_valid():
        form.save()
        messages.success(request, 'Recompensa actualizada correctamente.')
        return redirect('recompensa_lista')
    return render(request, 'recompensas/form.html', {'form': form, 'titulo': 'Editar recompensa'})


@staff_member_required(login_url='iniciar_sesion')
def recompensa_eliminar(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    if request.method == 'POST':
        try:
            recompensa.delete()
            messages.success(request, 'Recompensa eliminada correctamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: la recompensa ya tiene canjes. Puedes desactivarla en su lugar.')
        return redirect('recompensa_lista')
    return render(request, 'recompensas/eliminar.html', {
        'recompensa': recompensa, 'titulo': 'Eliminar recompensa'})

@staff_member_required(login_url='iniciar_sesion')
def participacion_lista(request):
    """HU30: cuantos torneos ha jugado cada jugador."""
    jugadores = (get_user_model().objects.filter(is_staff=False)
                 .annotate(
                     jugados=Count('inscripciones', filter=Q(inscripciones__asistencia__participo=True), distinct=True),
                     inscritos=Count('inscripciones', filter=Q(inscripciones__estado='activa'), distinct=True))
                 .order_by('-jugados', 'username'))
    return render(request, 'recompensas/participacion.html', {
        'jugadores': jugadores, 'titulo': 'Participación de jugadores'})