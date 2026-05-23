from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Produto, Mercadorias

def atualizar_estoque(request, id_produto):
    hoje = timezone.now().date()
    produto = Produto.objects.get(id=id_produto)
    qtd_total = produto.QTD_ESTOQUE
    mostrar_inativos = request.GET.get('mostrar_inativos', 'false') == 'true'

    lotes_cadastrados = Mercadorias.objects.filter(ID_PRODUTO_id=produto.id)
    
    lotes_processados = []
    for lote in lotes_cadastrados:
        inativo = lote.ID_SITUACAO in [5, 6]
        if inativo and not mostrar_inativos: continue
        
        lotes_processados.append({
            'dados': lote,
            'inativo': inativo
        })
        
    lotes_processados.sort(key=lambda x: (x['inativo'], x['dados'].DT_VALIDADE or hoje))
        
    context = {
        'produto': produto,
        'qtd_total': qtd_total,
        'lotes': lotes_processados,
        'mostrar_inativos': mostrar_inativos
    }
    return render(request, 'atualizar_estoque.html', context)

def editar_lote(request, id_lote):
    if request.method == 'POST':
        lote = Mercadorias.objects.get(ID_MERCADORIA=id_lote)
        lote.ID_SITUACAO = request.POST.get('status')
        lote.LOTE = request.POST.get('lote')
        lote.QTD_LOTE = request.POST.get('qtd')
        lote.DT_VALIDADE = request.POST.get('validade')
        lote.save()
    return redirect('core:atualizar_estoque', id_produto=lote.ID_PRODUTO.id)

def adicionar_lote(request, id_produto):
    if request.method == 'POST':
        Mercadorias.objects.create(
            ID_PRODUTO_id=id_produto,
            LOTE=request.POST.get('lote'),
            QTD_LOTE=request.POST.get('qtd'),
            DT_VALIDADE=request.POST.get('validade'),
            ID_SITUACAO=1 # Status padrão: Estoque
        )
    return redirect('core:atualizar_estoque', id_produto=id_produto)

def informar_estoque(request, id_produto, tipo):
    produto = Produto.objects.get(id=id_produto)
    if request.method == 'POST':
        qtd = int(request.POST.get('qtd', 0))
        
        # Altere para usar o nome em MAIÚSCULAS conforme seu models.py
        if tipo == 'entrada': 
            produto.QTD_ESTOQUE += qtd
        elif tipo == 'saida': 
            produto.QTD_ESTOQUE -= qtd
        elif tipo == 'zerar': 
            produto.QTD_ESTOQUE = 0
            
        produto.save()
        return redirect('core:atualizar_estoque', id_produto=id_produto)
    
    return render(request, 'confirmar_movimentacao.html', {'produto': produto, 'tipo': tipo})