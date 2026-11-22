from django.urls import path
from . import views

urlpatterns = [
    path('', views.recompensa_lista, name='recompensa_lista'),
    path('canjes/', views.canje_lista, name='canje_lista'),
    path('participacion/', views.participacion_lista, name='participacion_lista'),
    path('canjear/<int:pk>/', views.canje_crear, name='canje_crear'),
    path('nueva/', views.recompensa_crear, name='recompensa_crear'),
    path('<int:pk>/editar/', views.recompensa_editar, name='recompensa_editar'),
    path('<int:pk>/eliminar/', views.recompensa_eliminar, name='recompensa_eliminar'),
]