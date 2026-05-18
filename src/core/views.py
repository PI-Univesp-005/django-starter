from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Produto, Categoria, Subcategoria, UnidadeMedida


# TELA DE LOGIN
def tela_login(request):
    return render(request, "login.html")

# TELA DO MENU LÍDER (A que você enviou o HTML)
def menu_lider(request):
    return render(request, "menu_lider.html")

# FUNÇÕES QUE O SEU MENU PEDE (Criei para não dar erro no Docker)
def movimentacao_estoque(request):
    # Por enquanto apenas abre a tela (você precisará criar o html movimentacao.html)
    return render(request, "movimentacao.html")

def gerenciar_categorias(request):
    return render(request, "categorias.html")

def gerenciar_unidades(request):
    return render(request, "unidades.html")

# Mantenha suas funções de salvar_produto, buscar_produto_ajax e excluir_produto abaixo...

def menu_funcionario_lider(request):
    # O Django vai procurar um arquivo chamado menu_lider.html
    # Certifique-se de que o nome do seu arquivo HTML é exatamente este:
    return render(request, "menu_lider.html")

# TELA DE CADASTRO: Carrega o produto (se houver busca) e as listas para sugestão
def tela_cadastro_produto(request):
    codigo_buscado = request.GET.get('busca_codigo')
    produto_encontrado = None

    if codigo_buscado:
        produto_encontrado = Produto.objects.filter(COD_BARRAS=codigo_buscado).first()
    
    contexto = {
        'produto': produto_encontrado,
        'categorias': Categoria.objects.all().order_by('nome'),
        'subcategorias': Subcategoria.objects.all().order_by('nome'),
        'unidades': UnidadeMedida.objects.all().order_by('sigla'),
    }
    return render(request, "produtos.html", contexto)

# SALVAR: Cria categorias/unidades novas automaticamente se não existirem
def salvar_produto(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')
        cat_nome = request.POST.get('categoria')
        sub_nome = request.POST.get('subcategoria')
        uni_nome = request.POST.get('unidade')
        margem = request.POST.get('margem')

        # Sincronização com tabelas auxiliares (get_or_create)
        if cat_nome:
            Categoria.objects.get_or_create(nome=cat_nome)
        if sub_nome:
            Subcategoria.objects.get_or_create(nome=sub_nome)
        if uni_nome:
            UnidadeMedida.objects.get_or_create(sigla=uni_nome)

        # Salva ou Atualiza o Produto
        produto, criado = Produto.objects.update_or_create(
            COD_BARRAS=codigo,
            defaults={
                'NOME_PRODUTO': nome,
                'CATEGORIA': cat_nome,
                'SUBCATEGORIA': sub_nome,
                'UNIDADE_MEDIDA': uni_nome,
                'MARGEM_PROMO': margem,
            }
        )

        if criado:
            messages.success(request, f"✅ Produto '{nome}' cadastrado com sucesso!")
        else:
            messages.success(request, f"💾 Alterações em '{nome}' salvas com sucesso!")

        return redirect('core:tela_cadastro_produto')

# BUSCA AJAX: Para preenchimento automático ao bipar
def buscar_produto_ajax(request):
    codigo = request.GET.get('busca_codigo')
    produto = Produto.objects.filter(COD_BARRAS=codigo).values().first()
    
    if produto:
        return JsonResponse({
            'encontrado': True, 
            'dados': {
                'id': produto.get('id') or produto.get('ID'),
                'nome': produto.get('NOME_PRODUTO'),
                'margem': produto.get('MARGEM_PROMO'),
                'cat': produto.get('CATEGORIA'),
                'sub': produto.get('SUBCATEGORIA'),
                'unidade': produto.get('UNIDADE_MEDIDA'),
            }
        })
    return JsonResponse({'encontrado': False})

# EXCLUSÃO: Remove o produto pelo ID
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    nome_excluido = produto.NOME_PRODUTO
    produto.delete()
    messages.warning(request, f"Excluído: O produto '{nome_excluido}' foi removido.")
    return redirect('core:tela_cadastro_produto')

# Verifique se o nome é EXATAMENTE tela_login (tudo minúsculo)
def tela_login(request):
    # Aqui você renderiza o seu HTML de login
    return render(request, "login.html")