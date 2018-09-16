from django.db import models
from django.utils import timezone
import urllib.request
import json

class Ciclista(models.Model):
    nome = models.CharField(blank = False, max_length = 100)
    STATUSES = (
        (u'D', u'Disponivel'),
        (u'E', u'Em entrega'),
        (u'O', u'Offline'),
    )
    status = models.CharField(null=True, choices=STATUSES, max_length=2, default='D')

    def __str__(self):
        return self.nome

class Entrega(models.Model):
    ciclista = models.ForeignKey("Ciclista", on_delete=models.CASCADE)
    end_coleta = models.CharField(max_length = 200) # trocar depois para o tipo1 que a API retornar
    end_entrega = models.CharField(max_length = 200)  # trocar depois para o tipo que a API retornar

    def criar(self, end_coleta, end_entrega):
        self.end_coleta = end_coleta
        self.end_entrega = end_entrega
        self.save()

    def __str__(self):
        return self.end_entrega

class EntregaAtiva(models.Model):
    ciclista = models.ForeignKey("Ciclista", on_delete=models.CASCADE, blank = True, default = None, null = True)
    end_coleta = models.CharField(max_length = 100)  #endereço escrito como usuario inseriu
    lat_coleta = models.FloatField(null = True)  # latitute, no formato da api
    lng_coleta = models.FloatField(null = True)  # longitude, no formato da api
    end_entrega = models.CharField(max_length = 100)
    lat_entrega = models.FloatField(null = True)
    lng_entrega = models.FloatField(null = True)
    desc = models.TextField(null = True, max_length = 200)
    data = models.DateTimeField(default=timezone.now)
    STATUSES = (
        (u'D', u'Disponivel'),
        (u'E', u'Em andamento'),
    )
    status = models.CharField(null=True, choices=STATUSES, max_length=2, default = 'D')

    def verRota(self, coleta, entrega):
        endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
        api_key = 'AIzaSyBDmhhr_81wgfC0l_80i4nMxiDyZmlxwgI'
        origin = coleta.replace(' ','+')
        destination = entrega.replace(' ','+')
        travel_mode = 'bicycling'

        nav_request = 'origin={}&destination={}&mode={}&key={}'.format(origin, destination, travel_mode, api_key)
        request = endpoint + nav_request
        response = urllib.request.urlopen(request).read()
        directions = json.loads(response)
        print(request)
        print(directions)

        return directions

    def __str__(self):
        return self.desc