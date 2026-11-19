from django.urls import path
from . import views

urlpatterns = [
    path('torneo/<int:torneo_id>/inscribirse/', views.inscribirse, name='inscribirse'),
    path('mis-torneos/', views.mis_inscripciones, name='mis_inscripciones'),
    path('<int:pk>/cancelar/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
]