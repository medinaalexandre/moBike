from django.shortcuts import render
from .models import EntregaAtiva, Ciclista, Entrega
from .forms import EntregaAtivaForm, CiclistaForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
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

def listaCiclistas(request):
    entregasativa = EntregaAtiva.objects.all()
    render(request, 'entregas/delegarentrega/<pk>', {'entregasativa':entregasativa})

class EntregaAtivaDelegaView(UpdateView):
    template_name = "home/delegarentrega.html"
    model = EntregaAtiva
    fields = '__all__'
    context_object_name = 'entregaativa'
    success_url = reverse_lazy("entregas")


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
            entrega.save()
            return redirect('home')
    else:
        form = EntregaAtivaForm()
    return render(request, 'home/home.html', {'entregasAtivas': entregasAtivas, 'form': form})

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
