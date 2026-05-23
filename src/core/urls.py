from django.contrib import admin
from django.urls import path
from . import views 
from . import views_movimentacao
from core import views_atualizar_estoque

app_name = "core"   

urlpatterns = [
    # 1. Rota do Painel de Administração do Django
    path("admin/", admin.site.urls),
    
    # 2. Rota Principal: Ao abrir localhost:3333/ ele chama o login
    path("", views.tela_login, name="tela_login"),
    
    # 3. Rota alternativa: Também abre o login se digitar localhost:3333/login/
    path("login/", views.tela_login, name="tela_login"),
    
    # Rota do Menu Líder
    path("menu-lider/", views.menu_lider, name="menu_lider"),
    
    # Rotas que estão nos botões do seu Menu HTML
    
    path('movimentacao_estoque/', views_movimentacao.movimentacao_estoque, name='movimentacao_estoque'),
    path("produtos/", views.tela_cadastro_produto, name="tela_cadastro_produto"),
    path("categorias/", views.gerenciar_categorias, name="gerenciar_categorias"),
    path("unidades/", views.gerenciar_unidades, name="gerenciar_unidades"),
    
    # Funções de suporte (Ajax, Salvar, Excluir)
    path("salvar-produto/", views.salvar_produto, name="salvar_produto"),
    path("buscar-produto-ajax/", views.buscar_produto_ajax, name="buscar_produto_ajax"),
    path("excluir-produto/<int:id>/", views.excluir_produto, name="excluir_produto"),

    # funções de suporte a movimento_estoque
    path('atualizar-estoque/<int:id_produto>/', views_atualizar_estoque.atualizar_estoque, name='atualizar_estoque'),
    path('editar-lote/<int:id_lote>/', views_atualizar_estoque.editar_lote, name='editar_lote'),
    path('adicionar-lote/<int:id_produto>/', views_atualizar_estoque.adicionar_lote, name='adicionar_lote'),
path('informar-estoque/<int:id_produto>/<str:tipo>/', views_atualizar_estoque.informar_estoque, name='informar_estoque'),

# Adicione no seu urlpatterns
path('verificar-produto/', views.verificar_e_redirecionar, name='verificar_produto'),
]
