from django.urls import path
from . import views


urlpatterns = [
    # Login / Logout
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Menu
    path('menu/', views.menu, name='menu'),

    # Estoque
    path('estoque/', views.estoque_lista, name='estoque_lista'),
    path('estoque/<int:pk>/', views.estoque_detalhe, name='estoque_detalhe'),

    # Lotes
    path('estoque/<int:pk>/adicionar-lote/', views.adicionar_lote, name='adicionar_lote'),
    path('lote/<int:pk>/editar/', views.editar_lote, name='editar_lote'),
    path('lote/<int:pk>/status/', views.atualizar_status_lote, name='atualizar_status_lote'),
    path('lote/<int:pk>/deletar/', views.deletar_lote, name='deletar_lote'),

    # Movimentação
    path('estoque/<int:pk>/entrada/', views.entrada_estoque, name='entrada_estoque'),
    path('estoque/<int:pk>/saida/', views.saida_estoque, name='saida_estoque'),
    path('estoque/<int:pk>/zerar/', views.zerar_estoque, name='zerar_estoque'),

    # Cadastro
    path('cadastro/', views.cadastro_produto, name='cadastro_produto'),
    path('cadastro/<int:pk>/', views.cadastro_produto, name='cadastro_produto_editar'),
    path('cadastro/<int:pk>/deletar/', views.deletar_produto, name='deletar_produto'),

    # Correção
    path('correcao/', views.correcao_lotes, name='correcao'),
    path('correcao/lote/<int:pk>/', views.correcao_editar_lote, name='correcao_editar_lote'),
    # Relatório
    path('relatorio/', views.relatorio, name='relatorio'),
]