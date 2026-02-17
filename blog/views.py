from django.shortcuts import render, get_object_or_404
from .models import Noticia

def home(request):
    noticias = Noticia.objects.all().order_by('-data_publicacao')
    return render(request, 'home.html', {'noticias': noticias})

def detalhe_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    return render(request, 'noticia_detalhe.html', {'noticia': noticia})

# NOVA FUNÇÃO: FILTRO
def filtrar_categoria(request, nome):
    # O filtro é feito pelo campo 'categoria' do banco (ex: categoria='SAUDE')
    noticias_filtradas = Noticia.objects.filter(categoria=nome).order_by('-data_publicacao')
    
    # Reutilizamos o home.html para mostrar a lista filtrada
    return render(request, 'home.html', {'noticias': noticias_filtradas})