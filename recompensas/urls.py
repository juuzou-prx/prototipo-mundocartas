from django.urls import path
from . import views

urlpatterns = [
    path('', views.recompensa_lista, name='recompensa_lista'),
    path('nueva/', views.recompensa_crear, name='recompensa_crear'),
    path('<int:pk>/editar/', views.recompensa_editar, name='recompensa_editar'),
    path('<int:pk>/eliminar/', views.recompensa_eliminar, name='recompensa_eliminar'),
]