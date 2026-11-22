from django.urls import path
from . import views

urlpatterns = [
    path('', views.resultado_indice, name='resultado_indice'),
    path('ranking/', views.ranking_lista, name='ranking_lista'),
    path('torneo/<int:torneo_id>/', views.resultado_lista, name='resultado_lista'),
    path('torneo/<int:torneo_id>/nuevo/', views.resultado_crear, name='resultado_crear'),
    path('<int:pk>/editar/', views.resultado_editar, name='resultado_editar'),
    path('<int:pk>/eliminar/', views.resultado_eliminar, name='resultado_eliminar'),
    path('historial/', views.historial_mio, name='historial_mio'),
]