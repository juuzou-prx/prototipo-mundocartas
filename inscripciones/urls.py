from django.urls import path
from . import views

urlpatterns = [
    path('torneo/<int:torneo_id>/inscribirse/', views.inscribirse, name='inscribirse'),
    path('mis-torneos/', views.mis_inscripciones, name='mis_inscripciones'),
    path('<int:pk>/cancelar/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    path('torneo/<int:torneo_id>/inscritos/', views.lista_inscritos, name='lista_inscritos'),
    path('pagar/<int:inscripcion_id>/', views.iniciar_pago, name='iniciar_pago'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    
    path('pago/<int:pago_id>/cambiar/', views.cambiar_pago, name='cambiar_pago'),
]