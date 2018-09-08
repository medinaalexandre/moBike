from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('entregas', views.entregas, name='entregas'),
    path('entregas', views.excluirEntregaAtiva, name='excluirEntregaAtiva'),
]