from django.shortcuts import render
from ..models import Receita

def busca(request):
    busca_receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    
    if 'busca' in request.GET:
        nome_busca = request.GET['busca']
        busca_receitas = busca_receitas.filter(nome_receita__icontains=nome_busca)
    
    dados = {
        'receitas': busca_receitas
    }

    return render(request, 'receitas/busca.html', dados)