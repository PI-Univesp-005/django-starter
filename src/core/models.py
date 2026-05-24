from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

class Usuario(AbstractUser):
    PERFIL_CHOICES = [
        ('gerente', 'Gerente'),
        ('funcionario_lider', 'Funcionário Líder'),
        ('funcionario', 'Funcionário'),
    ]
    perfil = models.CharField(
        max_length=20,
        choices=PERFIL_CHOICES,
        default='funcionario',
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f'{self.username} ({self.get_perfil_display()})'


class Filial(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Filial'
        verbose_name_plural = 'Filiais'

    def __str__(self):
        return self.nome


class Produto(models.Model):
    EMOJI_PADRAO = '📦'

    nome = models.CharField(max_length=150)
    codigo_barras = models.CharField(max_length=50, blank=True)
    emoji = models.CharField(max_length=10, default=EMOJI_PADRAO)
    descricao = models.TextField(blank=True)
    dias_margem_promocao = models.IntegerField(default=30)
    quantidade_total = models.PositiveIntegerField(default=0)
    filial = models.ForeignKey(
        Filial,
        on_delete=models.CASCADE,
        related_name='produtos',
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f'{self.emoji} {self.nome}'


class Lote(models.Model):
    STATUS_CHOICES = [
        ('estoque', 'Em estoque'),
        ('promocao', 'Em promoção'),
        ('colocar_promocao', 'Colocar em promoção'),
        ('vencido', 'Vencido'),
    ]

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='lotes',
    )
    numero_lote = models.CharField(max_length=50, blank=True)
    data_validade = models.DateField()
    quantidade = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='estoque',
    )

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        ordering = ['data_validade']

    def __str__(self):
        return f'Lote {self.numero_lote or "s/n"} — {self.produto.nome} (val: {self.data_validade})'


@receiver(post_save, sender=Lote)
@receiver(post_delete, sender=Lote)
def atualizar_quantidade_total_produto(sender, instance, **kwargs):
    produto = instance.produto
    total = produto.lotes.aggregate(soma=Sum('quantidade'))['soma'] or 0
    if produto.quantidade_total != total:
        produto.quantidade_total = total
        produto.save(update_fields=['quantidade_total'])