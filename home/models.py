from django.db import models
import urllib.request
import json

class Entrega(models.Model):
    ciclista = models.CharField(max_length = 100) # models.ForeignKey('auth.User', on_delete=models.CASCADE)
    end_coleta = models.CharField(max_length = 200) # trocar depois para o tipo que a API retornar
    end_entrega = models.CharField(max_length = 200)  # trocar depois para o tipo que a API retornar
    urgencia = models.IntegerField()

    def criar(self, end_coleta, end_entrega):
        self.end_coleta = end_coleta
        self.end_entrega = end_entrega
        self.save()

    def __str__(self):
        return self.end_entrega

class EntregaAtiva(models.Model):
    ciclista = models.CharField(max_length = 100)  # models.ForeignKey('auth.User', on_delete=models.CASCADE)
    end_coleta = models.CharField(max_length = 100)  #endereço escrito como usuario inseriu
    lat_coleta = models.FloatField(null = True)  # latitute, no formato da api
    lng_coleta = models.FloatField(null = True)  # longitude, no formato da api
    end_entrega = models.CharField(max_length = 100)
    lat_entrega = models.FloatField(null = True)
    lng_entrega = models.FloatField(null = True)
    desc = models.TextField(null = True, max_length = 200)

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

    def criar(self, ciclista, end_coleta, end_entrega, desc):
        rota = self.verRota(self, end_coleta, end_entrega)
        self.ciclista = ciclista
        self.end_coleta = end_coleta
        self.lat_coleta = rota['routes'][0]['legs'][0]['start_location']['lat']
        self.lng_coleta = rota['routes'][0]['legs'][0]['start_location']['lng']
        self.end_entrega = end_entrega
        self.lat_entrega = rota['routes'][0]['legs'][0]['end_location']['lat']
        self.lng_entrega = rota['routes'][0]['legs'][0]['end_location']['lng']
        self.desc = desc
        self.save()

    def __str__(self):
        return self.id