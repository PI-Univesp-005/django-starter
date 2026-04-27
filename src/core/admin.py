from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Filial, Produto, Lote


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil', {'fields': ('perfil',)}),
    )
    list_display = ['username', 'email', 'perfil', 'is_staff']


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ['nome', 'endereco']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['emoji', 'nome', 'codigo_barras', 'filial', 'dias_margem_promocao']
    search_fields = ['nome', 'codigo_barras']


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ['produto', 'numero_lote', 'quantidade', 'data_validade', 'status']
    list_filter = ['status']