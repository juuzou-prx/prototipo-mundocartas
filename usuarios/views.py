from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Perfil
# Create your views here.

def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('torneo_lista')
    if request.method == 'POST':
        #validar el usuario - contraseña
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            #buscar el perfil usuario su no existe lo crea
            Perfil.objects.get_or_create(usuario=user)
            login(request, user)
            return redirect('torneo_lista')
    else:
        form = AuthenticationForm(request)
    return render(request, 'usuarios/iniciar_sesion.html', {'form':form})

def registrar_usuario(request):
    if request.method == 'POST':
        #validar el usuario - contraseña
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Perfil.objects.create(usuario=user)
            return redirect('iniciar_sesion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'usuarios/registrar_usuario.html', {'form':form})

def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')