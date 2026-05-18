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