from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('entregas', views.entregas, name='entregas'),
    path('home/excluir/<pk>', views.EntregaAtivaDeleteView.as_view(), name="deleta_entregaativa"),
    path('entregas/delegarEntrega/<pk>', views.EntregaAtivaDelegaView.as_view(), name="delega_entregaativa"),
    path('entregas/delegarEntrega/<pk>', views.listaCiclistas, name="listaciclistas"),
    path('entregas/completarEntrega/<pk>', views.CompletaEntrega, name="completa_entregaativa"),
    path('ciclistas', views.ciclistas, name='ciclistas'),
    path('userPos', views.userPos, name='userPos'),
    path('home/excluirCiclista/<pk>', views.CiclistaDeleteView.as_view(), name="deleta_ciclista"),
    path('home/xy', views.salvaXY, name="salvaXY"),
    path('home/entrega/<pk>', views.entrega_detalhe, name='entrega_detalhe'),
    path('home/editarciclista/<pk>', views.CiclistaEditarView.as_view(), name="editar_ciclista"),
    path('modociclista', views.modoCiclista, name='modociclista'),
    path('modociclista/<pk>', views.modoCiclistaPk, name='modociclistaPk'),
]

