# definição de classes para ligar com banco de dados

from django.db import models

class Produto(models.Model):
    # O Django precisa saber como a sua tabela é estruturada
    NOME_PRODUTO = models.CharField(max_length=255)
    COD_BARRAS = models.CharField(max_length=100, unique=True)
    MARGEM_PROMO = models.IntegerField(default=30)
    CATEGORIA = models.CharField(max_length=100, blank=True, null=True)
    SUBCATEGORIA = models.CharField(max_length=100, blank=True, null=True)
    FOTO_PRODUTO = models.CharField(max_length=255, blank=True, null=True)
    QTD_ESTOQUE = models.IntegerField(default=0)
    UNIDADE_MEDIDA = models.CharField(max_length=20, default='UN')

    class Meta:
        managed = False  # ISSO É IMPORTANTE: diz ao Django que a tabela já existe no MySQL
        db_table = 'produtos' # <--- COLOQUE AQUI O NOME EXATO DA TABELA NO SEU MYSQL

    def __str__(self):
        return self.NOME_PRODUTO
    
from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class Subcategoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nome

class UnidadeMedida(models.Model):
    sigla = models.CharField(max_length=10, unique=True) # Ex: UN, KG, LT
    def __str__(self): return self.sigla

class Mercadorias(models.Model):
    ID_MERCADORIA = models.AutoField(primary_key=True)
    # Criamos a ligação (Chave Estrangeira) com a tabela de Produtos:
    ID_PRODUTO = models.ForeignKey(Produto, db_column='ID_PRODUTO', on_delete=models.CASCADE, related_name='mercadorias')
    ID_FORNECEDOR = models.IntegerField(blank=True, null=True)
    ID_SITUACAO = models.IntegerField(blank=True, null=True)
    LOTE = models.CharField(max_length=50, blank=True, null=True)
    QTD_LOTE = models.IntegerField(default=0)
    DT_COMPRA = models.DateField(blank=True, null=True)
    DT_VALIDADE = models.DateField(blank=True, null=True)
    PRECO_UN_LOTE = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False      # Diz ao Django que a tabela já existe no MySQL
        db_table = 'MERCADORIAS'  # Nome exato da tabela em maiúsculo no seu Workbench

    def __str__(self):
        return f"Lote {self.LOTE} - {self.ID_PRODUTO.NOME_PRODUTO}"