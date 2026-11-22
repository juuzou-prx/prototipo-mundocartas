from django import forms
from .models import Recompensa


class RecompensaForm(forms.ModelForm):
    class Meta:
        model = Recompensa
        fields = ['nombre', 'descripcion', 'costo_puntos', 'activa']
        labels = {
            'costo_puntos': 'Costo en puntos',
            'activa': 'Activa',
        }
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}