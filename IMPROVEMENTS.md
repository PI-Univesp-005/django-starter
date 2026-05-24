# 📋 Relatório de Melhorias e Fragilidades - FreshStock

**Data:** 24 de maio de 2026  
**Versão:** 1.0.0  
**Status:** Em Desenvolvimento (MVP)

---

## 📌 Resumo Executivo

Este relatório identifica fragilidades, pontos de melhoria e boas práticas técnicas que devem ser implementadas na aplicação **FreshStock** para garantir qualidade, segurança, performance e manutenibilidade do código.

---

## 🔴 Fragilidades Críticas

### 1. **Falta de Validação de Dados em Formulários**
- **Problema:** Views recebem dados POST direto sem validação adequada
- **Risco:** Possíveis erros em tempo de execução (ValueError em conversões)
- **Solução:** Implementar Django Forms com validação integrada
- **Prioridade:** 🔴 ALTA
- **Exemplo problemático:**
  ```python
  quantidade = int(request.POST.get('quantidade', 0))  # Pode quebrar se valor não for numérico
  ```

### 2. **Duplicação de Decorador `@login_required`**
- **Problema:** Em `zerar_estoque()` há dois decoradores `@login_required` idênticos
- **Risco:** Comportamento inesperado
- **Solução:** Remover um dos decoradores
- **Prioridade:** 🟡 BAIXA
- **Arquivo:** `src/core/views.py` linha ~259

### 3. **Ausência de Permissões Granulares**
- **Problema:** Apenas `login_required` é usado; não há controle de perfil consistente
- **Risco:** Usuários comuns podem acessar endpoints restritos se vulnerabilidade for explorada
- **Solução:** Implementar decorador customizado `@permission_required` ou usar Django Permissions
- **Prioridade:** 🔴 ALTA
- **Exemplo:**
  ```python
  @login_required  # Insuficiente
  def correcao(request):
      if request.user.perfil != 'gerente':  # Verificação manual (frágil)
          return redirect('menu')
  ```

### 4. **Sem Histórico de Movimentações**
- **Problema:** Não há registro de quem fez entrada/saída, quando e por quê
- **Risco:** Impossível auditoria e rastreabilidade
- **Solução:** Criar modelo `Movimentacao` para registrar todas as transações
- **Prioridade:** 🔴 CRÍTICA
- **Campos necessários:**
  - Tipo (entrada/saída/correção)
  - Quantidade
  - Data/Hora
  - Usuário responsável
  - Motivo (opcional)
  - Lote relacionado

### 5. **Race Conditions em Operações Concorrentes**
- **Problema:** Operações de incremento/decremento não são atômicas
- **Risco:** Em alta concorrência, quantidades podem ficar inconsistentes
- **Solução:** Usar `F()` expressions do Django ou transações `atomic()`
- **Prioridade:** 🔴 ALTA
- **Exemplo problemático:**
  ```python
  lote.quantidade += quantidade  # Não é atômico
  lote.save()
  ```
- **Solução:**
  ```python
  from django.db.models import F
  Lote.objects.filter(pk=lote.pk).update(quantidade=F('quantidade') + quantidade)
  ```

### 6. **Falta de Testes Unitários**
- **Problema:** Zero testes automatizados
- **Risco:** Regressões não detectadas, confiança baixa em mudanças
- **Solução:** Implementar testes com pytest + pytest-django
- **Prioridade:** 🔴 ALTA
- **Cobertura mínima necessária:** 70%

### 7. **Ausência de Logging**
- **Problema:** Sem logs de eventos importantes (erros, operações críticas)
- **Risco:** Difícil debugar em produção
- **Solução:** Configurar Python logging com níveis apropriados
- **Prioridade:** 🔴 ALTA
- **Exemplo:**
  ```python
  import logging
  logger = logging.getLogger(__name__)
  logger.info(f"User {request.user} deleted product {pk}")
  ```

### 8. **Redundância no Campo `quantidade_total` do Produto**
- **Problema:** Campo denormalizado que duplica soma das quantidades dos lotes
- **Risco:** Inconsistência se sinal falhar; consome espaço desnecessário
- **Solução:** Opção 1 - Usar apenas sinal (atual é OK) OU Opção 2 - Calcular dinamicamente via agregação
- **Prioridade:** 🟡 MÉDIA

### 9. **Sem Tratamento Robusto de Erros**
- **Problema:** Exceções não esperadas causam 500 erros
- **Risco:** Experiência de usuário ruim em produção
- **Solução:** Adicionar try/catch adequado e mensagens de erro genéricas
- **Prioridade:** 🟡 MÉDIA

### 10. **Migrations Problemáticas**
- **Problema:** `0002_remove_lote_quantidade_produto_quantidade_total.py` remove campo importante, depois `0003` o readiciona
- **Risco:** Confusão histórica, possível falha em restore
- **Solução:** Fazer squash de migrations e limpar histórico
- **Prioridade:** 🟡 MÉDIA
- **Comando:**
  ```bash
  python manage.py squashmigrations core 0003
  ```

---

## 🟡 Pontos de Melhoria Média Prioridade

### 11. **Sem Paginação na Lista de Produtos**
- **Problema:** Todas as linhas carregadas por padrão
- **Risco:** Performance degradada com 10k+ produtos
- **Solução:** Implementar `Paginator` do Django
- **Prioridade:** 🟡 MÉDIA
- **Sugestão:** 50 itens/página

### 12. **Views Muito Grandes (Fat Views)**
- **Problema:** Lógica de negócio misturada com views
- **Risco:** Código difícil de testar e manter
- **Solução:** Refatorar para métodos de modelo e managers
- **Prioridade:** 🟡 MÉDIA
- **Exemplo:**
  ```python
  # Ao invés de:
  for produto in produtos:
      lote_urgente = produto.lotes.order_by('data_validade').first()
      dias = (lote_urgente.data_validade - hoje).days
  
  # Usar:
  class ProdutoManager(models.Manager):
      def com_lote_urgente(self):
          # Query otimizada com select_related
  ```

### 13. **Sem Documentação de API (Docstrings)**
- **Problema:** Views/Models sem docstrings
- **Risco:** Difícil onboarding de novos desenvolvedores
- **Solução:** Adicionar docstrings em todas as funções
- **Prioridade:** 🟡 MÉDIA
- **Padrão:**
  ```python
  def estoque_detalhe(request, pk):
      """
      Exibe detalhes do estoque de um produto específico.
      
      Args:
          request: HttpRequest object
          pk: Product ID
          
      Returns:
          Rendered template with product and batch details
          
      Permissions: login_required
      """
  ```

### 14. **Filtros de Listagem Sem Otimização de Query**
- **Problema:** Query N+1 em loops
- **Risco:** Performance ruim com muitos produtos
- **Solução:** Usar `select_related()` e `prefetch_related()`
- **Prioridade:** 🟡 MÉDIA
- **Exemplo:**
  ```python
  # Antes (N+1):
  for item in lotes_info:
      item.lote.produto.nome  # Faz query adicional
  
  # Depois (Otimizado):
  lotes = Lote.objects.select_related('produto')
  ```

### 15. **Sem Índices de Banco de Dados**
- **Problema:** Queries sem índices em campos frequentemente filtrados
- **Risco:** Performance degrada exponencialmente
- **Solução:** Adicionar índices em campos de busca
- **Prioridade:** 🟡 MÉDIA
- **Campos recomendados:**
  ```python
  class Produto(models.Model):
      nome = models.CharField(max_length=150, db_index=True)
      codigo_barras = models.CharField(max_length=50, db_index=True)
  
  class Lote(models.Model):
      data_validade = models.DateField(db_index=True)
      status = models.CharField(max_length=20, db_index=True)
  ```

### 16. **Validação de Quantidade Negativa Incompleta**
- **Problema:** Nem todas as views validam quantidade negativa
- **Risco:** Dados inconsistentes
- **Solução:** Centralizar validação em forms ou model methods
- **Prioridade:** 🟡 MÉDIA

### 17. **Sem Cache para Consultas Frequentes**
- **Problema:** Mesmas queries executadas múltiplas vezes
- **Risco:** Performance ruim
- **Solução:** Implementar cache com Redis
- **Prioridade:** 🟡 MÉDIA
- **Exemplo:**
  ```python
  from django.views.decorators.cache import cache_page
  
  @cache_page(60 * 15)  # Cache por 15 minutos
  @login_required
  def estoque_lista(request):
      pass
  ```

---

## 🟢 Melhorias Recomendadas (Nice to Have)

### 18. **Usar Django Forms**
- **Benefício:** Validação automática, CSRF protection, reutilização
- **Prioridade:** 🟢 MÉDIA
- **Exemplo:**
  ```python
  class LoteForm(forms.ModelForm):
      class Meta:
          model = Lote
          fields = ['numero_lote', 'data_validade', 'quantidade']
  ```

### 19. **Migrar para Class-Based Views (CBV)**
- **Benefício:** Menos código, melhor reutilização
- **Prioridade:** 🟢 MÉDIA
- **Exemplo:**
  ```python
  from django.views import View
  
  class EstoqueDetalheView(LoginRequiredMixin, View):
      template_name = 'estoque_detalhe.html'
  ```

### 20. **Implementar Soft Delete**
- **Benefício:** Rastreabilidade, possibilidade de recuperação
- **Prioridade:** 🟢 BAIXA
- **Solução:** Adicionar campo `deleted_at` ao invés de deletar

### 21. **Adicionar Timestamps aos Modelos**
- **Benefício:** Auditoria, rastreamento de mudanças
- **Prioridade:** 🟢 BAIXA
- **Exemplo:**
  ```python
  class TimeStampedModel(models.Model):
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
      
      class Meta:
          abstract = True
  ```

### 22. **Setup de CI/CD**
- **Benefício:** Testes automatizados, deploy seguro
- **Prioridade:** 🟢 MÉDIA
- **Ferramentas:** GitHub Actions, GitLab CI, ou Jenkins

### 23. **Documentação com Django REST Framework**
- **Benefício:** Se API REST for necessária
- **Prioridade:** 🟢 BAIXA

### 24. **Internacionalização (i18n)**
- **Benefício:** Suporte a múltiplos idiomas
- **Prioridade:** 🟢 BAIXA

---

## 📊 Sumário de Prioridades

| Prioridade | Quantidade | Exemplos |
|-----------|-----------|---------|
| 🔴 CRÍTICA | 4 | Histórico, Race Conditions, Logging, Testes |
| 🔴 ALTA | 6 | Validação, Permissões, Erros, Migrations |
| 🟡 MÉDIA | 11 | Paginação, Índices, Cache, Docstrings |
| 🟢 BAIXA | 3 | Forms, CBV, Soft Delete |

---

## 🛠️ Roadmap de Implementação

### Fase 1 - Segurança (Sprint 1)
- [ ] Implementar decorador `@permission_required`
- [ ] Validar todas as entradas com Django Forms
- [ ] Adicionar logging

### Fase 2 - Confiabilidade (Sprint 2)
- [ ] Implementar testes unitários (70% cobertura)
- [ ] Fix Race Conditions com `F()` expressions
- [ ] Criação de modelo `Movimentacao` para auditoria

### Fase 3 - Performance (Sprint 3)
- [ ] Adicionar índices de banco de dados
- [ ] Paginação na lista de produtos
- [ ] Otimizar queries com select_related

### Fase 4 - Manutenibilidade (Sprint 4)
- [ ] Refatorar views em métodos de modelo
- [ ] Adicionar docstrings completas
- [ ] Squash de migrations
- [ ] Setup de CI/CD

---

## 📝 Exemplos de Código

### Exemplo 1: Validação com Django Forms
```python
# forms.py
from django import forms
from .models import Lote

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['numero_lote', 'data_validade', 'quantidade']
        
    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade < 0:
            raise forms.ValidationError("Quantidade não pode ser negativa.")
        return quantidade

# views.py
def adicionar_lote(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.produto = produto
            lote.save()
            messages.success(request, 'Lote adicionado com sucesso!')
            return redirect('estoque_detalhe', pk=pk)
    else:
        form = LoteForm()
    return render(request, 'adicionar_lote.html', {'form': form})
```

### Exemplo 2: Operação Atômica
```python
from django.db.models import F
from django.db import transaction

@transaction.atomic
def saida_estoque(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    lote = get_object_or_404(Lote, pk=lote_id, produto=produto)
    quantidade = int(request.POST.get('quantidade'))
    
    if lote.quantidade < quantidade:
        raise ValueError("Quantidade insuficiente")
    
    # Operação atômica
    Lote.objects.filter(pk=lote.pk).update(
        quantidade=F('quantidade') - quantidade
    )
    
    # Registrar movimentação
    Movimentacao.objects.create(
        lote=lote,
        tipo='saida',
        quantidade=quantidade,
        usuario=request.user,
    )
```

### Exemplo 3: Decorador de Permissão Customizado
```python
from functools import wraps
from django.http import redirect
from django.contrib.auth.decorators import login_required

def permission_required(perfil):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.perfil != perfil:
                messages.error(request, "Permissão insuficiente.")
                return redirect('menu')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Uso:
@permission_required('gerente')
def correcao(request):
    pass
```

---

## 📚 Recursos e Referências

- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django Transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Best Practices by Real Python](https://realpython.com/django-best-practices/)
- [12 Factor App](https://12factor.net/)

---

**Documento criado em:** 24 de maio de 2026  
**Próxima revisão:** Quando 50% das melhorias forem implementadas
