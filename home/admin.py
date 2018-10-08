from django.contrib import admin
from .models import Entrega, EntregaAtiva, Ciclista, UserGeoLocation

admin.site.register(Entrega)
admin.site.register(EntregaAtiva)
admin.site.register(Ciclista)
admin.site.register(UserGeoLocation)
