from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Juego
from .forms import JuegoForm


def juego_lista(request):
    juegos = Juego.objects.all()
    return render(request, 'torneos/juego/lista.html', {'juegos': juegos})


def juego_crear(request):
    form = JuegoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Juego creado correctamente.')
        return redirect('juego_lista')
    return render(request, 'torneos/juego/form.html', {'form': form, 'titulo': 'Nuevo juego'})


def juego_editar(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    form = JuegoForm(request.POST or None, instance=juego)
    if form.is_valid():
        form.save()
        messages.success(request, 'Juego actualizado correctamente.')
        return redirect('juego_lista')
    return render(request, 'torneos/juego/form.html', {'form': form, 'titulo': 'Editar juego'})


def juego_eliminar(request, pk):
    juego = get_object_or_404(Juego, pk=pk)
    if request.method == 'POST':
        juego.delete()
        messages.success(request, 'Juego eliminado correctamente.')
        return redirect('juego_lista')
    return render(request, 'torneos/juego/eliminar.html', {'juego': juego})