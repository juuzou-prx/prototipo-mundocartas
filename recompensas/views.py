from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RecompensaForm
from .models import Recompensa


@login_required
def recompensa_lista(request):
    recompensas = Recompensa.objects.all()
    if not request.user.is_staff:
        recompensas = recompensas.filter(activa=True)
    return render(request, 'recompensas/lista.html', {
        'recompensas': recompensas, 'titulo': 'Recompensas'})


@staff_member_required
def recompensa_crear(request):
    form = RecompensaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Recompensa creada correctamente.')
        return redirect('recompensa_lista')
    return render(request, 'recompensas/form.html', {'form': form, 'titulo': 'Nueva recompensa'})


@staff_member_required
def recompensa_editar(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    form = RecompensaForm(request.POST or None, instance=recompensa)
    if form.is_valid():
        form.save()
        messages.success(request, 'Recompensa actualizada correctamente.')
        return redirect('recompensa_lista')
    return render(request, 'recompensas/form.html', {'form': form, 'titulo': 'Editar recompensa'})


@staff_member_required
def recompensa_eliminar(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    if request.method == 'POST':
        recompensa.delete()
        messages.success(request, 'Recompensa eliminada correctamente.')
        return redirect('recompensa_lista')
    return render(request, 'recompensas/eliminar.html', {
        'recompensa': recompensa, 'titulo': 'Eliminar recompensa'})