from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Produto, Lote, Filial


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
        lotes = produto.lotes.exclude(status='vencido').order_by('data_validade')
        lote_urgente = lotes.first()
        dias = None
        if lote_urgente:
            dias = (lote_urgente.data_validade - hoje).days

        if filtro == 'margem' and (dias is None or dias > produto.dias_margem_promocao):
            continue
        if filtro == 'amanha' and (dias is None or dias != 1):
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


# ─── ESTOQUE DETALHE ──────────────────────────────────────────────
@login_required
def estoque_detalhe(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    hoje = timezone.now().date()
    lotes = produto.lotes.order_by('data_validade')

    lotes_info = []
    for lote in lotes:
        dias = (lote.data_validade - hoje).days
        lotes_info.append({'lote': lote, 'dias': dias})

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
        Lote.objects.create(
            produto=produto,
            numero_lote=numero_lote,
            data_validade=data_validade,
        )
        messages.success(request, 'Lote adicionado com sucesso!')
    return redirect('estoque_detalhe', pk=pk)


# ─── EDITAR LOTE ──────────────────────────────────────────────────
@login_required
def editar_lote(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    if request.method == 'POST':
        lote.numero_lote = request.POST.get('numero_lote', '')
        lote.data_validade = request.POST.get('data_validade')
        lote.save()
        messages.success(request, 'Lote atualizado!')
        return redirect('estoque_detalhe', pk=lote.produto.pk)
    hoje = timezone.now().date()
    dias = (lote.data_validade - hoje).days
    return render(request, 'core/editar_lote.html', {
        'lote': lote,
        'dias': dias,
    })


# ─── ATUALIZAR STATUS LOTE ────────────────────────────────────────
@login_required
def atualizar_status_lote(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    if request.method == 'POST':
        lote.status = request.POST.get('status')
        lote.save()
    return redirect('estoque_detalhe', pk=lote.produto.pk)


# ─── DELETAR LOTE ─────────────────────────────────────────────────
@login_required
def deletar_lote(request, pk):
    lote = get_object_or_404(Lote, pk=pk)
    produto_pk = lote.produto.pk
    if request.method == 'POST':
        lote.delete()
        messages.success(request, 'Lote removido!')
    return redirect('estoque_detalhe', pk=produto_pk)


# ─── ENTRADA DE ESTOQUE ───────────────────────────────────────────
@login_required
def entrada_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 0))
        if quantidade > 0:
            produto.quantidade_total += quantidade
            produto.save()
            messages.success(request, f'Entrada de {quantidade} UN registrada!')
        return redirect('estoque_detalhe', pk=pk)
    return render(request, 'core/entrada_estoque.html', {'produto': produto})


# ─── SAÍDA DE ESTOQUE ─────────────────────────────────────────────
@login_required
def saida_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))
        if quantidade > 0 and quantidade <= produto.quantidade_total:
            produto.quantidade_total -= quantidade
            produto.save()
            messages.success(request, f'Saída de {quantidade} UN registrada!')
        else:
            messages.error(request, 'Quantidade inválida.')
    # return redirect('estoque_detalhe', pk=pk)
    return render(request, 'core/saida_estoque.html', {'produto': produto})


# ─── ZERAR ESTOQUE ────────────────────────────────────────────────
@login_required
def zerar_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    lotes = produto.lotes.all()
    if request.method == 'POST':
        excluir_lotes = request.POST.get('excluir_lotes') == 'sim'
        produto.quantidade_total = 0
        produto.save()
        if excluir_lotes:
            lotes.delete()
        messages.success(request, 'Estoque zerado!')
        return redirect('estoque_detalhe', pk=pk)
    return render(request, 'core/zerar_estoque.html', {
        'produto': produto,
        'lotes': lotes,
    })


# ─── CADASTRO PRODUTO ─────────────────────────────────────────────
@login_required
def cadastro_produto(request, pk=None):
    produto = get_object_or_404(Produto, pk=pk) if pk else None
    if request.method == 'POST':
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
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, 'Produto excluído!')
        return redirect('estoque_lista')
    return redirect('cadastro_produto', {'produto': produto})


# ─── CORREÇÃO DE ESTOQUE ──────────────────────────────────────────
@login_required
def correcao(request):
    if request.user.perfil != 'gerente':
        return redirect('menu')
    produtos = Produto.objects.all()
    return render(request, 'core/correcao.html', {'produtos': produtos})


@login_required
def correcao_produto(request, pk):
    if request.user.perfil != 'gerente':
        return redirect('menu')
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        nova_quantidade = int(request.POST.get('quantidade', 0))
        produto.quantidade_total = nova_quantidade
        produto.save()
        messages.success(request, 'Quantidade corrigida!')
        return redirect('correcao')
    return render(request, 'core/correcao_produto.html', {'produto': produto})


# ─── RELATÓRIO ────────────────────────────────────────────────────
@login_required
def relatorio(request):
    if request.user.perfil != 'gerente':
        return redirect('menu')
    hoje = timezone.now().date()
    amanha = hoje + timezone.timedelta(days=1)

    total_produtos = Produto.objects.count()
    total_promocao = Lote.objects.filter(status='promocao').count()
    total_amanha = Lote.objects.filter(data_validade=amanha).count()
    total_colocar_promocao = Lote.objects.filter(status='colocar_promocao').count()

    lotes_proximos = []
    for lote in Lote.objects.exclude(status='vencido').order_by('data_validade')[:20]:
        dias = (lote.data_validade - hoje).days
        lotes_proximos.append({'lote': lote, 'dias': dias})

    lotes_colocar = Lote.objects.filter(status='colocar_promocao')

    return render(request, 'core/relatorio.html', {
        'total_produtos': total_produtos,
        'total_promocao': total_promocao,
        'total_amanha': total_amanha,
        'total_colocar_promocao': total_colocar_promocao,
        'lotes_proximos': lotes_proximos,
        'lotes_colocar': lotes_colocar,
    })