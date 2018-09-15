from django.contrib import admin
from .models import Entrega, EntregaAtiva, Ciclista

admin.site.register(Entrega)
admin.site.register(EntregaAtiva)
admin.site.register(Ciclista)