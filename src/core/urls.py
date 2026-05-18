from django.contrib import admin
from django.urls import path
from core import views 

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
    path("movimentacao/", views.movimentacao_estoque, name="movimentacao_estoque"),
    path("produtos/", views.tela_cadastro_produto, name="tela_cadastro_produto"),
    path("categorias/", views.gerenciar_categorias, name="gerenciar_categorias"),
    path("unidades/", views.gerenciar_unidades, name="gerenciar_unidades"),
    
    # Funções de suporte (Ajax, Salvar, Excluir)
    path("salvar-produto/", views.salvar_produto, name="salvar_produto"),
    path("buscar-produto-ajax/", views.buscar_produto_ajax, name="buscar_produto_ajax"),
    path("excluir-produto/<int:id>/", views.excluir_produto, name="excluir_produto"),
]