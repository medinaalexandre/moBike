from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entregas', views.entregas, name='entregas'),
    path('home/excluir/<pk>', views.EntregaAtivaDeleteView.as_view(), name="deleta_entregaativa"),
]