from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Q
from .models import Produto, Categoria, Subcategoria, Mercadorias

def movimentacao_estoque(request):
    hoje = timezone.now().date()
    
    # =========================================================================
    # DOCUMENTAÇÃO OFICIAL DOS FILTROS DA TELA
    # 1. TODOS: Mostra a lista completa de produtos (com e sem alertas).
    # 2. MARGEM DE PROMOÇÃO: Mostra apenas produtos com alertas na Situação C.
    # 3. VAI VENCER AMANHÃ: Mostra apenas produtos com o status estrito de "Vence amanhã".
    # 4. FILTRO POR CATEGORIA: Filtra a lista por uma categoria específica (ex: Legumes).
    # 5. FILTRO POR SUBCATEGORIA: Localiza os produtos por uma prateleira específica.
    # 6. BUSCA/BIP: Filtra pelo código de barras exato ou por parte do nome do produto.
    # =========================================================================
    
    # Capturando as escolhas de filtros e buscas enviadas pelo usuário no HTML
    filtro_atual = request.GET.get('filtro', 'todos')
    cat_selecionada = request.GET.get('categoria', '')
    subcat_selecionada = request.GET.get('prateleira', '')
    busca_atual = request.GET.get('busca', '') # Captura o que o usuário bipou ou digitou

    produtos_cadastrados = Produto.objects.all()

    # Nova regra da barra de busca
    if busca_atual:
        produtos_cadastrados = produtos_cadastrados.filter(
            Q(COD_BARRAS__icontains=busca_atual) | 
            Q(NOME_PRODUTO__icontains=busca_atual)
        )

    # Aplicando os filtros de Categoria e Prateleira direto na busca do Banco de Dados
    if cat_selecionada:
        produtos_cadastrados = produtos_cadastrados.filter(CATEGORIA=cat_selecionada)
    if subcat_selecionada:
        produtos_cadastrados = produtos_cadastrados.filter(SUBCATEGORIA=subcat_selecionada)

    lista_final = []
    
    for prod in produtos_cadastrados:
        # =========================================================================
        # DOCUMENTAÇÃO DA REGRA DE NEGÓCIO (CORAÇÃO DA APLICAÇÃO - STATUS DOS LOTES)
        # Para cada produto, pode ter 0 ou vários lotes relacionados na tabela mercadoria.
        # O sistema busca na tabela mercadorias aquele lote com a data mais próxima do dia atual,
        # desde que o lote ainda possua estoque disponível (QTD_LOTE > 0).
        # =========================================================================
        lote_urgente = Mercadorias.objects.filter(
            ID_PRODUTO_id=prod.id, 
            QTD_LOTE__gt=0,
            DT_VALIDADE__isnull=False
        ).order_by('DT_VALIDADE').first()
        
        # SOMA DO ESTOQUE REAL: Agrega a quantidade de todos os lotes ativos do produto
        soma_estoque = Mercadorias.objects.filter(ID_PRODUTO_id=prod.id).aggregate(total=Sum('QTD_LOTE'))['total']
        qtd_real_estoque = soma_estoque or 0
        
        exibir_alerta = False
        alerta_texto = ""
        alerta_cor = "warning" # Cor padrão: Laranja/Amarelo
        dias_para_vencer = None
        
        if lote_urgente:
            dias_para_vencer = (lote_urgente.DT_VALIDADE - hoje).days
            margem_alerta = getattr(prod, 'DIAS_ANTES_VALIDADE_ALERTA', getattr(prod, 'MARGEM_PROMO', 30))

            # ---------------------------------------------------------------------
            # SITUAÇÃO A: Ter um lote com data de validade menor que hoje.
            # Significa que o produto está VENCIDO. Exibe sinal de alerta vermelho.
            # ---------------------------------------------------------------------
            if dias_para_vencer < 0:
                exibir_alerta = True
                alerta_texto = "Vencido!"
                alerta_cor = "danger"
                
            # ---------------------------------------------------------------------
            # SITUAÇÃO B: Ter um lote com data de validade igual a de hoje.
            # Alerta o usuário que o produto VENCE HOJE. Exibe sinal laranja forte.
            # ---------------------------------------------------------------------
            elif dias_para_vencer == 0:
                exibir_alerta = True
                alerta_texto = "Vence hoje"
                alerta_cor = "warning-high"
                
            # ---------------------------------------------------------------------
            # SITUAÇÃO C: Data de validade maior que hoje (Vai vencer no futuro).
            # O sistema calcula a diferença e avisa de acordo com o campo do produto
            # DIAS_ANTES_VALIDADE_ALERTA. Se estiver dentro da margem, informa os dias
            # para o usuário decidir se quer colocar o produto em promoção.
            # ---------------------------------------------------------------------
            elif dias_para_vencer > 0 and dias_para_vencer <= margem_alerta:
                exibir_alerta = True
                if dias_para_vencer == 1:
                    alerta_texto = "Vence amanhã"
                else:
                    alerta_texto = f"{dias_para_vencer} dias"
                    
        # =========================================================================
        # APLICAÇÃO DAS REGRAS DE EXIBIÇÃO DOS FILTROS (BOTÕES DA TELA)
        # =========================================================================
        incluir_na_lista = True
        
        if filtro_atual == 'promocao':
            # Filtro 2: Só mantém na tela se o produto se enquadrar estritamente na Situação C
            if not (dias_para_vencer is not None and dias_para_vencer > 0 and dias_para_vencer <= margem_alerta):
                incluir_na_lista = False
                
        elif filtro_atual == 'amanha':
            # Filtro 3: Só mantém na tela se o texto do alerta for exatamente "Vence amanhã"
            if alerta_texto != "Vence amanhã":
                incluir_na_lista = False

        if incluir_na_lista:
            lista_final.append({
                'objeto': prod,
                'qtd_total': qtd_real_estoque, 
                'exibir_alerta': exibir_alerta,
                'alerta_texto': alerta_texto,
                'alerta_cor': alerta_cor,
            })
        
    categorias = Categoria.objects.all()
    subcategorias = Subcategoria.objects.all() 

    context = {
        'produtos': lista_final,
        'categorias': categorias,
        'subcategorias': subcategorias,
        'filtro_atual': filtro_atual,
        'cat_selecionada': cat_selecionada,
        'subcat_selecionada': subcat_selecionada,
        'busca_atual': busca_atual, # Garante que a barra de pesquisa não apague o que foi bipado
    }
    
    return render(request, 'movimentacao_estoque.html', context)