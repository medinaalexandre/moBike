from django.shortcuts import render, get_object_or_404
from .models import EntregaAtiva, Ciclista, Entrega, UserGeoLocation
from .forms import EntregaAtivaForm, CiclistaForm, ModoCiclistaForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import datetime
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView

# Create your views here.
class EntregaAtivaDeleteView(DeleteView):
    template_name="home/exclui.html"
    model = EntregaAtiva
    fields = '__all__'
    context_object_name = 'entregaativa'
    success_url = reverse_lazy("entregas")

    def get_object(self, queryset=None):
        ciclista = None

        id = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)

        if id is not None:
            # Busca o funcionario apartir do id
            ciclista = EntregaAtiva.objects.filter(id=id).first()

        elif slug is not None:

            campo_slug = self.get_slug_field()

            # Busca o funcionario apartir do slug
            ciclista = EntregaAtiva.objects.filter(**{campo_slug: slug}).first()

        # Retorna o objeto encontrado
        return ciclista


class CiclistaDeleteView(DeleteView):
    template_name="home/excluirCiclista.html"
    model = EntregaAtiva
    fields = '__all__'
    context_object_name = 'ciclista'
    success_url = reverse_lazy("ciclistas")

    def get_object(self, queryset=None):
        ciclista = None

        id = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)

        if id is not None:
            # Busca o ciclista apartir do id
            ciclista = Ciclista.objects.filter(id=id).first()

        elif slug is not None:

            campo_slug = self.get_slug_field()

            # Busca o ciclista apartir do slug
            ciclista = Ciclista.objects.filter(**{campo_slug: slug}).first()

        # Retorna o objeto encontrado
        return ciclista


def listaCiclistas(request):
    entregasativa = EntregaAtiva.objects.all()
    render(request, 'entregas/delegarentrega/<pk>', {'entregasativa':entregasativa})

class EntregaAtivaDelegaView(UpdateView):
    template_name = "home/delegarentrega.html"
    model = EntregaAtiva
    fields = ('ciclista','status', )
    # TODO
    # 'status e 'data_inicio tem que preencher automatico, implementar isso
    # sepa tem que criar +1 view para atualizar, com request, ai pega o objeto e atualiza
    context_object_name = 'entregaativa'
    success_url = reverse_lazy("entregas")


class CiclistaEditarView(UpdateView):
    template_name = "home/editarciclista.html"
    model = Ciclista
    fields = ('nome', 'status', )
    context_object_name = 'ciclista'
    success_url = reverse_lazy("ciclistas")


def CompletaEntrega(request,pk):
    entrega = EntregaAtiva.objects.get(pk=pk)
    # criando Entrega
    entregaConcluida = Entrega()
    # pegando os dados da EntregaAtiva
    entregaConcluida.ciclista = entrega.ciclista
    entregaConcluida.end_coleta = entrega.end_coleta
    entregaConcluida.end_entrega = entrega.end_entrega
    entregaConcluida.data = entrega.data
    # salva no bd
    print('Entrega criada')
    entregaConcluida.save()
    # deleta entregaAtiva
    print('EntregaAtiva excluida')
    entrega.delete()

    return redirect('entregas')


def entregas(request):
    entregasDisponiveis = EntregaAtiva.objects.filter(status='D').order_by('data')
    entregasEmAndamento = EntregaAtiva.objects.filter(status='E').order_by('data')
    ultimasDez = Entrega.objects.order_by('-id')[:10]

    return render(request, 'home/entregas.html', {'entregasDisponiveis': entregasDisponiveis, 'entregasEmAndamento': entregasEmAndamento,'ultimasDez':ultimasDez,})

def home(request):
    entregasAtivas = EntregaAtiva.objects.all()
    if request.method == "POST":
        form = EntregaAtivaForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit = False)
            rota = EntregaAtiva.verRota(EntregaAtiva, entrega.end_coleta, entrega.end_entrega)
            entrega.lat_coleta = rota['routes'][0]['legs'][0]['start_location']['lat']
            entrega.lng_coleta = rota['routes'][0]['legs'][0]['start_location']['lng']
            entrega.lat_entrega = rota['routes'][0]['legs'][0]['end_location']['lat']
            entrega.lng_entrega = rota['routes'][0]['legs'][0]['end_location']['lng']
            entrega.distancia = rota['routes'][0]['legs'][0]['distance']['text']
            entrega.tempo_estimado = rota['routes'][0]['legs'][0]['duration']['text']
            if entrega.ciclista is None:
                entrega.status = 'D'
            else:
                entrega.status = 'E'
                entrega.data_inicio = datetime.now()
            entrega.save()
            return redirect('home')
    else:
        form = EntregaAtivaForm()
    return render(request, 'home/home.html', {'entregasAtivas': entregasAtivas, 'form': form})

def entrega_detalhe(request,pk):
    entrega = get_object_or_404(EntregaAtiva,pk=pk)
    return render(request,'home/entrega.html',{'entrega':entrega})


def salvaXY(request):
    if request.method == 'GET':
        latitude = float(request.GET.get('latitude'))
        longitude = float(request.GET.get('longitude'))
        print(latitude)
        print(longitude)
        u = UserGeoLocation()
        #u.ciclista = Ciclista.objects.get(pk = pk)
        u.latitude = latitude
        u.longitude = longitude
        u.save()
        print('salvado')
        return HttpResponse('result')


def ciclistas(request):
    ciclistas = Ciclista.objects.all()
    if request.method == "POST":
        form = CiclistaForm(request.POST)
        if form.is_valid():
            ciclista = form.save(commit=False)
            ciclista.save()
            return redirect('ciclistas')
    else:
        form = CiclistaForm()
    return render(request, 'home/ciclistas.html', {'form': form, 'ciclistas': ciclistas})

def userPos(request):
    return render(request, 'home/userLocationMap.html')

def modoCiclista(request):
    ciclistas = Ciclista.objects.all()
    return render(request,'home/modociclista.html', {'ciclistas':ciclistas})

def modoCiclistaPk(request,pk):
    ciclista = get_object_or_404(Ciclista, pk=pk)
    entregas = Entrega.objects.filter(ciclista = pk)
    entregaatual = EntregaAtiva.objects.filter(ciclista = pk).first()
    print(entregas)
    print(entregaatual)
    return render(request,'home/modociclistapk.html', {'ciclista':ciclista, 'entregas':entregas, 'entregaatual':entregaatual})