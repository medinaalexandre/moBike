from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entregas', views.entregas, name='entregas'),
    path('home/excluir/<pk>', views.EntregaAtivaDeleteView.as_view(), name="deleta_entregaativa"),
    path('entregas/delegarEntrega/<pk>', views.EntregaAtivaDelegaView.as_view(), name="delega_entregaativa"),
    path('entregas/delegarEntrega/<pk>', views.listaCiclistas, name="listaciclistas"),
    path('ciclistas', views.ciclistas, name='ciclistas'),
]