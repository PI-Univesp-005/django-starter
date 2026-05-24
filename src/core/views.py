from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Produto, Lote, Filial
from django.db.models import Sum, Q



# ─── LOGIN / LOGOUT ───────────────────────────────────────────────
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# ─── MENU ─────────────────────────────────────────────────────────
@login_required
def menu(request):
    return render(request, 'core/menu.html')


# ─── ESTOQUE LISTA ────────────────────────────────────────────────
@login_required
def estoque_lista(request):
    produtos = Produto.objects.all()
    q = request.GET.get('q', '')
    if q:
        produtos = produtos.filter(nome__icontains=q)

    filtro = request.GET.get('filtro', '')
    hoje = timezone.now().date()

    produtos_lista = []
    for produto in produtos:
        # Lote mais urgente (menor data de validade) – usado para exibição
        lote_urgente = produto.lotes.order_by('data_validade').first()
        dias = None
        if lote_urgente:
            dias = (lote_urgente.data_validade - hoje).days

        # ---------- FILTRO MARGEM (corrigido) ----------
        if filtro == 'margem':
            if dias is None or dias < 2 or dias > produto.dias_margem_promocao:
                continue
        # Filtro Amanhã/Vencidos (permanece igual)
        elif filtro == 'amanha':
            if not (produto.lotes.filter(data_validade__lte=hoje).exists() or produto.lotes.filter(data_validade=hoje + timezone.timedelta(days=1)).exists()):
                continue

        produtos_lista.append({
            'produto': produto,
            'quantidade_total': produto.quantidade_total,
            'lote_urgente': lote_urgente,
            'dias_urgente': dias,
        })

    return render(request, 'core/estoque_lista.html', {
        'produtos_lista': produtos_lista,
        'filtro': filtro,
        'q': q,
    })
# @login_required
# def estoque_lista(request):
#     produtos = Produto.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         produtos = produtos.filter(nome__icontains=q)

#     filtro = request.GET.get('filtro', '')
#     hoje = timezone.now().date()

#     produtos_lista = []
#     for produto in produtos:
#         # Lote mais urgente (menor data_validade) – inclui vencidos
#         lote_urgente = produto.lotes.order_by('data_validade').first()
#         dias = None
#         if lote_urgente:
#             dias = (lote_urgente.data_validade - hoje).days

#         # Para o filtro Margem: verifica se existe lote não vencido dentro da margem
#         if filtro == 'margem':
#             lotes_nao_vencidos = produto.lotes.exclude(data_validade__lt=hoje).exclude(status='vencido')
#             dentro_margem = False
#             for l in lotes_nao_vencidos:
#                 d = (l.data_validade - hoje).days
#                 if 0 <= d <= produto.dias_margem_promocao:
#                     dentro_margem = True
#                     break
#             if not dentro_margem:
#                 continue

#         # Filtro Amanhã/Vencidos: produto com lote vencido ou vencendo amanhã
#         elif filtro == 'amanha':
#             if not (produto.lotes.filter(data_validade__lte=hoje).exists() or produto.lotes.filter(data_validade=hoje + timezone.timedelta(days=1)).exists()):
#                 continue

#         produtos_lista.append({
#             'produto': produto,
#             'quantidade_total': produto.quantidade_total,
#             'lote_urgente': lote_urgente,
#             'dias_urgente': dias,
#         })

#     return render(request, 'core/estoque_lista.html', {
#         'produtos_lista': produtos_lista,
#         'filtro': filtro,
#         'q': q,
#     })


# ─── ESTOQUE DETALHE ──────────────────────────────────────────────
@login_required
def estoque_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    hoje = timezone.now().date()
    lotes = produto.lotes.order_by('data_validade')

    lotes_info = []
    for lote in lotes:
        dias = (lote.data_validade - hoje).days
        lotes_info.append({'lote': lote, 'dias': dias, 'quantidade': lote.quantidade})

    return render(request, 'core/estoque_detalhe.html', {
        'produto': produto,
        'quantidade_total': produto.quantidade_total,
        'lotes_info': lotes_info,
    })


# ─── ADICIONAR LOTE ───────────────────────────────────────────────
@login_required
def adicionar_lote(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        numero_lote = request.POST.get('numero_lote', '')
        data_validade = request.POST.get('data_validade')
        quantidade = int(request.POST.get('quantidade', 0))
        lote = Lote.objects.create(
            produto=produto,
            numero_lote=numero_lote,
            data_validade=data_validade,
            quantidade=quantidade,
        )

        messages.success(request, 'Lote adicionado com sucesso!')
    return redirect('estoque_detalhe', pk=pk)

# ─── EDITAR LOTE ──────────────────────────────────────────────────
@login_required
@require_http_methods(["GET", "PUT", "POST"])
def editar_lote(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    if request.method in ['PUT', 'POST']:
        lote.numero_lote = request.POST.get('numero_lote', '')
        lote.data_validade = request.POST.get('data_validade')
        lote.quantidade = int(request.POST.get('quantidade', 0))
        lote.save()
        messages.success(request, 'Lote atualizado!')
        
        if request.method == 'PUT':
            return JsonResponse({'success': True, 'message': 'Lote atualizado com sucesso!'})
        return redirect('estoque_detalhe', pk=lote.produto.pk)
    
    hoje = timezone.now().date()
    dias = (lote.data_validade - hoje).days
    return render(request, 'core/editar_lote.html', {
        'lote': lote,
        'dias': dias,
    })


# ─── ATUALIZAR STATUS LOTE ────────────────────────────────────────
@login_required
@require_http_methods(["PUT", "POST"])
def atualizar_status_lote(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    if request.method in ['PUT', 'POST']:
        lote.status = request.POST.get('status')
        lote.save()
        messages.success(request, 'Status atualizado!')
        
        if request.method == 'PUT':
            return JsonResponse({'success': True, 'message': 'Status atualizado com sucesso!'})
    
    return redirect('estoque_detalhe', pk=lote.produto.pk)


# ─── DELETAR LOTE ─────────────────────────────────────────────────
@login_required
@require_http_methods(["DELETE", "POST"])
def deletar_lote(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    produto_pk = lote.produto.pk
    lote.delete()
    messages.success(request, 'Lote removido!')
    
    if request.method == 'DELETE':
        return JsonResponse({'success': True, 'message': 'Lote removido com sucesso!'})
    
    return redirect('estoque_detalhe', pk=produto_pk)


# ─── ENTRADA DE ESTOQUE ───────────────────────────────────────────
@login_required
def entrada_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    lotes = produto.lotes.all().order_by('data_validade')  # todos os lotes

    if request.method == 'POST':
        lote_id = request.POST.get('lote_id')
        quantidade = int(request.POST.get('quantidade', 0))
        if quantidade <= 0:
            messages.error(request, 'Quantidade deve ser positiva.')
            return redirect('entrada_estoque', pk=pk)

        if lote_id == 'novo':
            # Criar novo lote com a quantidade informada
            data_validade = request.POST.get('data_validade')
            numero_lote = request.POST.get('numero_lote', '')
            if not data_validade:
                messages.error(request, 'Data de validade obrigatória para novo lote.')
                return redirect('entrada_estoque', pk=pk)
            Lote.objects.create(
                produto=produto,
                numero_lote=numero_lote,
                data_validade=data_validade,
                quantidade=quantidade
            )
            messages.success(request, f'Novo lote criado com entrada de {quantidade} UN.')
        else:
            lote = get_object_or_404(Lote, pk=lote_id, produto=produto)
            lote.quantidade += quantidade
            lote.save()
            messages.success(request, f'{quantidade} UN adicionadas ao lote {lote.numero_lote or "s/n"}.')

        return redirect('estoque_detalhe', pk=pk)

    return render(request, 'core/entrada_estoque.html', {
        'produto': produto,
        'lotes': lotes,
    })

# ─── SAÍDA DE ESTOQUE ─────────────────────────────────────────────
@login_required
def saida_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    # apenas lotes com quantidade > 0 (para evitar selecionar lotes vazios)
    lotes = produto.lotes.filter(quantidade__gt=0).order_by('data_validade')

    if request.method == 'POST':
        lote_id = request.POST.get('lote_id')
        quantidade = int(request.POST.get('quantidade', 0))
        if quantidade <= 0:
            messages.error(request, 'Quantidade deve ser positiva.')
            return redirect('saida_estoque', pk=pk)

        lote = get_object_or_404(Lote, pk=lote_id, produto=produto)
        if lote.quantidade < quantidade:
            messages.error(request, f'Quantidade insuficiente no lote {lote.numero_lote or "s/n"}. Disponível: {lote.quantidade}')
            return redirect('saida_estoque', pk=pk)

        lote.quantidade -= quantidade
        lote.save()
        messages.success(request, f'{quantidade} UN removidas do lote {lote.numero_lote or "s/n"}.')

        return redirect('estoque_detalhe', pk=pk)

    return render(request, 'core/saida_estoque.html', {
        'produto': produto,
        'lotes': lotes,
    })

# ─── ZERAR ESTOQUE ────────────────────────────────────────────────
@login_required
@login_required
def zerar_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        excluir_lotes = request.POST.get('excluir_lotes') == 'sim'
        if excluir_lotes:
            produto.lotes.all().delete()
        else:
            # Zerar quantidade de cada lote individualmente
            for lote in produto.lotes.all():
                lote.quantidade = 0
                lote.save()
        messages.success(request, 'Estoque zerado!')
        return redirect('estoque_detalhe', pk=pk)
    return render(request, 'core/zerar_estoque.html', {
        'produto': produto,
        'lotes': produto.lotes.all(),
    })

# ─── CADASTRO PRODUTO ─────────────────────────────────────────────
@login_required
@require_http_methods(["GET", "POST", "PUT"])
def cadastro_produto(request, pk=None):
    produto = get_object_or_404(Produto, pk=pk) if pk else None
    if request.method in ['POST', 'PUT']:
        nome = request.POST.get('nome')
        codigo_barras = request.POST.get('codigo_barras', '')
        emoji = request.POST.get('emoji', '📦')
        dias_margem = int(request.POST.get('dias_margem_promocao', 30))
        if produto:
            produto.nome = nome
            produto.codigo_barras = codigo_barras
            produto.emoji = emoji
            produto.dias_margem_promocao = dias_margem
            produto.save()
            messages.success(request, 'Produto atualizado!')
            
            if request.method == 'PUT':
                return JsonResponse({'success': True, 'message': 'Produto atualizado com sucesso!'})
        else:
            filial = Filial.objects.first()
            Produto.objects.create(
                nome=nome,
                codigo_barras=codigo_barras,
                emoji=emoji,
                dias_margem_promocao=dias_margem,
                filial=filial,
            )
            messages.success(request, 'Produto cadastrado!')
        return redirect('estoque_lista')
    return render(request, 'core/cadastro_produto.html', {'produto': produto})


# ─── DELETAR PRODUTO ──────────────────────────────────────────────
@login_required
@require_http_methods(["DELETE", "POST"])
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    produto.delete()
    messages.success(request, 'Produto excluído!')
    
    if request.method == 'DELETE':
        return JsonResponse({'success': True, 'message': 'Produto excluído com sucesso!'})
    
    return redirect('estoque_lista')


# ─── CORREÇÃO DE ESTOQUE ──────────────────────────────────────────
@login_required
def correcao(request):
    if request.user.perfil != 'gerente':
        return redirect('menu')
    produtos = Produto.objects.all()
    return render(request, 'core/correcao.html', {'produtos': produtos})

@login_required
def correcao_lotes(request):
    if request.user.perfil != 'gerente':
        return redirect('menu')
    
    # Buscar todos os lotes, ordenados por produto e validade
    lotes = Lote.objects.select_related('produto').order_by('produto__nome', 'data_validade')
    
    # Filtro opcional por produto
    produto_id = request.GET.get('produto')
    if produto_id:
        lotes = lotes.filter(produto_id=produto_id)
    
    produtos = Produto.objects.all()  # para o filtro
    
    return render(request, 'core/correcao_lotes.html', {
        'lotes': lotes,
        'produtos': produtos,
        'produto_selecionado': int(produto_id) if produto_id else None,
    })

@login_required
@require_http_methods(["GET", "PUT", "POST"])
def correcao_editar_lote(request, pk):
    if request.user.perfil != 'gerente':
        return redirect('menu')
    
    lote = get_object_or_404(Lote, pk=pk)
    
    if request.method in ['PUT', 'POST']:
        nova_quantidade = int(request.POST.get('quantidade', 0))
        novo_status = request.POST.get('status')
        
        if nova_quantidade < 0:
            messages.error(request, 'Quantidade não pode ser negativa.')
        else:
            lote.quantidade = nova_quantidade
            lote.status = novo_status
            lote.save()
            messages.success(request, f'Lote {lote.numero_lote or "s/n"} atualizado com sucesso.')
            
            if request.method == 'PUT':
                return JsonResponse({'success': True, 'message': f'Lote {lote.numero_lote or "s/n"} atualizado!'})
        
        return redirect('correcao')
    
    return render(request, 'core/correcao_editar_lote.html', {
        'lote': lote,
    })
# ─── RELATÓRIO ────────────────────────────────────────────────────
@login_required
def relatorio(request):
    if request.user.perfil != 'gerente':
        return redirect('menu')
    
    hoje = timezone.now().date()
    amanha = hoje + timezone.timedelta(days=1)
    
    # Totais brutos
    total_itens = Lote.objects.aggregate(soma=Sum('quantidade'))['soma'] or 0
    total_em_promocao = Lote.objects.filter(status='promocao').aggregate(soma=Sum('quantidade'))['soma'] or 0
    total_vencidos = Lote.objects.filter(data_validade__lt=hoje).aggregate(soma=Sum('quantidade'))['soma'] or 0
    total_amanha = Lote.objects.filter(data_validade=amanha).aggregate(soma=Sum('quantidade'))['soma'] or 0
    
    # Oportunidade (lotes não vencidos, não em promoção, dentro da margem)
    qs_oportunidade = Lote.objects.exclude(data_validade__lt=hoje).exclude(status='promocao')
    lotes_oportunidade = []
    soma_oportunidade = 0
    for lote in qs_oportunidade:
        dias = (lote.data_validade - hoje).days
        if 0 <= dias <= lote.produto.dias_margem_promocao:
            lotes_oportunidade.append({
                'lote': lote,
                'dias': dias,
                'produto': lote.produto,
                'quantidade': lote.quantidade
            })
            soma_oportunidade += lote.quantidade
    
    # Próximos (2 a 15 dias) que NÃO estão na oportunidade (para não duplicar)
    ids_oportunidade = [l['lote'].id for l in lotes_oportunidade]
    qs_proximos = Lote.objects.exclude(data_validade__lt=hoje).exclude(id__in=ids_oportunidade).exclude(data_validade=amanha)
    lotes_proximos = []
    soma_proximos = 0
    for lote in qs_proximos:
        dias = (lote.data_validade - hoje).days
        if 2 <= dias <= 15:
            lotes_proximos.append({
                'lote': lote,
                'dias': dias,
                'quantidade': lote.quantidade
            })
            soma_proximos += lote.quantidade
        if len(lotes_proximos) >= 20:
            break
    
    # Estoque normal = o que sobra
    ja_classificado = total_em_promocao + total_vencidos + total_amanha + soma_oportunidade + soma_proximos
    total_normal = total_itens - ja_classificado
    if total_normal < 0:
        total_normal = 0
    
    return render(request, 'core/relatorio.html', {
        'total_itens': total_itens,
        'total_em_promocao': total_em_promocao,
        'total_amanha': total_amanha,
        'total_oportunidade': soma_oportunidade,
        'total_vencidos': total_vencidos,
        'total_normal': total_normal,
        'lotes_proximos': lotes_proximos,
        'lotes_oportunidade': lotes_oportunidade,
    })

# @login_required
# def relatorio(request):
#     if request.user.perfil != 'gerente':
#         return redirect('menu')
    
#     hoje = timezone.now().date()
#     amanha = hoje + timezone.timedelta(days=1)
    
#     # Totais (soma de quantidades)
#     total_itens = Lote.objects.aggregate(soma=Sum('quantidade'))['soma'] or 0
#     total_em_promocao = Lote.objects.filter(status='promocao').aggregate(soma=Sum('quantidade'))['soma'] or 0
#     total_amanha = Lote.objects.filter(data_validade=amanha).aggregate(soma=Sum('quantidade'))['soma'] or 0
#     total_vencidos = Lote.objects.filter(data_validade__lt=hoje).aggregate(soma=Sum('quantidade'))['soma'] or 0
    
#     # Oportunidade (dias dentro da margem, exclui vencidos e já em promoção)
#     lotes_oportunidade = []
#     soma_oportunidade = 0
#     qs_oportunidade = Lote.objects.exclude(data_validade__lt=hoje).exclude(status='promocao')
#     for lote in qs_oportunidade:
#         dias = (lote.data_validade - hoje).days
#         if 0 <= dias <= lote.produto.dias_margem_promocao:
#             lotes_oportunidade.append({
#                 'lote': lote,
#                 'dias': dias,
#                 'produto': lote.produto,
#                 'quantidade': lote.quantidade
#             })
#             soma_oportunidade += lote.quantidade
    
#     # Próximos a vencer (1 a 15 dias) - inclui amanhã, exclui vencidos, independente de oportunidade
#     lotes_proximos = []
#     soma_proximos = 0
#     qs_proximos = Lote.objects.exclude(data_validade__lt=hoje)  # todos não vencidos
#     for lote in qs_proximos:
#         dias = (lote.data_validade - hoje).days
#         if 1 <= dias <= 15:
#             lotes_proximos.append({
#                 'lote': lote,
#                 'dias': dias,
#                 'quantidade': lote.quantidade
#             })
#             soma_proximos += lote.quantidade
#         if len(lotes_proximos) >= 20:
#             break
    
#     # Estoque normal (o que sobra)
#     classificados = total_em_promocao + total_amanha + total_vencidos + soma_oportunidade + soma_proximos
#     total_normal = total_itens - classificados
#     if total_normal < 0:
#         total_normal = 0
    
#     return render(request, 'core/relatorio.html', {
#         'total_itens': total_itens,
#         'total_em_promocao': total_em_promocao,
#         'total_amanha': total_amanha,
#         'total_oportunidade': soma_oportunidade,
#         'total_vencidos': total_vencidos,
#         'total_normal': total_normal,
#         'lotes_proximos': lotes_proximos,
#         'lotes_oportunidade': lotes_oportunidade,
#     })