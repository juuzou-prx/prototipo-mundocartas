from django import forms
from .models import Juego, Torneo


class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre', 'descripcion', 'imagen']

class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ['nombre', 'juego', 'fecha', 'hora', 'cupo_maximo', 'costo', 'reglas']
        widgets = {
            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'hora': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }