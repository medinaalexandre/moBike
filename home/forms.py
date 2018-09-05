from django import forms
from .models import EntregaAtiva

class EntregaAtivaForm(forms.ModelForm):
    class Meta:
        model = EntregaAtiva
        fields = ('ciclista', 'end_coleta', 'end_entrega', 'desc',)
        labels = {'ciclista':'Ciclista', 'end_coleta':'Endereço de coleta', 'end_entrega':'Endereço de entrega', 'desc':'Descrição'}