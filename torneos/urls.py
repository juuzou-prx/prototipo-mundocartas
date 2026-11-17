from django.urls import path
from . import views

urlpatterns = [
    path('juegos/', views.juego_lista, name='juego_lista'),
    path('juegos/nuevo/', views.juego_crear, name='juego_crear'),
    path('juegos/<int:pk>/editar/', views.juego_editar, name='juego_editar'),
    path('juegos/<int:pk>/eliminar/', views.juego_eliminar, name='juego_eliminar'),
]