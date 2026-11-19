from django.urls import path
from . import views

urlpatterns = [
    path('torneo/<int:torneo_id>/inscribirse/', views.inscribirse, name='inscribirse'),
]