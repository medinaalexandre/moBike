from django import forms
from .models import EntregaAtiva, Ciclista

class EntregaAtivaForm(forms.ModelForm):
    class Meta:
        model = EntregaAtiva
        fields = ('ciclista', 'end_coleta', 'end_entrega', 'desc',)
        labels = {'ciclista':'Ciclista', 'end_coleta':'Endereço de coleta', 'end_entrega':'Endereço de entrega', 'desc':'Descrição'}

class CiclistaForm(forms.ModelForm):
    class Meta:
        model = Ciclista
        fields = ('nome',)

class ModoCiclistaForm(forms.ModelForm):
    class Meta:
        model = Ciclista
        fields = ('nome',)