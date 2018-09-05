from django.shortcuts import render
from .models import EntregaAtiva
from .forms import EntregaAtivaForm
from django.shortcuts import redirect

# Create your views here.

def entrega(request):
    entregasAtivas = EntregaAtiva.objects.all()
    return render(request, 'home/entregas.html', {'entregasAtivas': entregasAtivas})


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

