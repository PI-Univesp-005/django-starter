# FreshStock 🥬

[![Python](https://img.shields.io/badge/python-3.10%2B-green)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.0%2B-darkgreen)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-MVP-yellow)](https://github.com)

<img src="src/core/templates/core/assets/img/logo_brand.png" style="width:40%;margin-left:30%">

<br>

Sistema de controle de estoque com rastreamento de validade de produtos, distribuída em lotes. Relatório com agregado geral da situação do estoque, identificando oportunidades para promoções antes da perda do item.

<sub>Desenvolvido como projeto integrador para o programa de Graduação em Engenharia de Software, Ciência de Dados ou TI da **UNIVESP**.</sub>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Características](#-características)
- [Arquitetura](#-arquitetura)
- [Requisitos do Sistema](#-requisitos-do-sistema)
- [Instalação Rápida](#-instalação-rápida)
- [Uso](#-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Modelos de Dados](#-modelos-de-dados)
- [Rotas Disponíveis](#-rotas-disponíveis)
- [Usuários Padrão](#-usuários-padrão)
- [Fragilidades Conhecidas](#-fragilidades-conhecidas)
- [Roadmap](#-roadmap)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Visão Geral

**FreshStock** é um sistema web de controle de estoque especializado em produtos perecíveis. Permite que gerenciadores de lojas e distribuidoras de alimentos rastreiem:

- ✅ **Quantidade em estoque** por lote e data de validade
- ✅ **Datas de vencimento** com alertas por faixa de dias
- ✅ **Status de lotes** (em estoque, promoção, vencido)
- ✅ **Margens de promoção** configuráveis por produto
- ✅ **Controle por perfil** (gerente, líder, funcionário)
- ✅ **Correção de inventário** (apenas gerentes)
- ✅ **Entrada e saída de estoque** rastreáveis

---

## ✨ Características

### Funcionalidades Principais

| Funcionalidade | Descrição | Perfil Acesso |
|---|---|---|
| 📊 Dashboard | Visualizar resumo de estoque | Todos |
| 📦 Gerenciar Produtos | CRUD de produtos | Gerente |
| 📅 Controlar Lotes | Registrar lotes com data de validade | Gerente/Líder |
| 📈 Entrada de Estoque | Adicionar produtos ao estoque | Gerente/Líder |
| 📉 Saída de Estoque | Remover produtos do estoque | Gerente/Líder |
| 🔧 Correção de Inventário | Ajustar quantidades manualmente | Gerente |
| 📋 Relatórios | Visualizar estoque por status/validade | Gerente |
| 🎯 Filtros Inteligentes | Filtrar por urgência/promoção/vencimento | Todos |
| 🌐 Responsivo | Interface móvel-first | Todos |

### Características Técnicas

- **Backend:** Django 5.0+ com Python 3.10+
- **Banco de Dados:** PostgreSQL, MySQL ou SQLite (comutável via Docker)
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Containerização:** Docker + Docker Compose
- **Autenticação:** Nativa do Django com perfis customizados
- **Segurança:** CSRF Protection, SQL Injection Prevention, XSS Protection

---

## 🏗️ Arquitetura

### Diagrama de Entidades (ERD)

```
┌─────────────────────────────────────────────────────────────────┐
│                      USUARIO (Django Auth)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ - id (PK)                                               │   │
│  │ - username, email, password (hashed)                    │   │
│  │ - perfil [gerente|funcionario_lider|funcionario]      │   │
│  │ - is_active                                             │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         FILIAL                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ - id (PK)                                               │   │
│  │ - nome                                                  │   │
│  │ - endereco                                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         1:N                                     │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      PRODUTO                            │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │ - id (PK)                                       │    │   │
│  │  │ - nome, codigo_barras, emoji (🥬)              │    │   │
│  │  │ - descricao, dias_margem_promocao (=30)        │    │   │
│  │  │ - quantidade_total (SUM dos lotes via Signal)  │    │   │
│  │  │ - filial_id (FK → FILIAL)                      │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         1:N                                     │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                       LOTE                              │   │
│  │  ┌─────────────────────────────────────────────────┐    │   │
│  │  │ - id (PK)                                       │    │   │
│  │  │ - numero_lote (opcional)                        │    │   │
│  │  │ - data_validade, quantidade                     │    │   │
│  │  │ - status [estoque|promocao|vencido]            │    │   │
│  │  │ - produto_id (FK → PRODUTO)                    │    │   │
│  │  │ [Signal: post_save/post_delete]                │    │   │
│  │  │  └─► Recalcula produto.quantidade_total        │    │   │
│  │  └─────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Fluxo de Dados

```
┌─────────────┐       ┌────────────┐       ┌──────────────┐
│  Frontend   │◄─────►│  Views     │◄─────►│   Models     │
│  (Templates)│       │  (Business)│       │  (Database)  │
└─────────────┘       └────────────┘       └──────────────┘
      │                     │                     │
      └─────────────────────┴─────────────────────┘
                 (HTTP Requests/Responses)
```

---

## 📋 Requisitos do Sistema

### Hardware Mínimo
- **CPU:** 2 cores
- **RAM:** 2 GB
- **Disco:** 10 GB

### Softwares Necessários

| Software | Versão | Propósito |
|---|---|---|
| Docker | 20.10+ | Containerização |
| Docker Compose | 1.29+ | Orquestração |
| Python | 3.10+ | (já dentro do container) |
| Git | 2.0+ | Versionamento |

### Banco de Dados (Opcional)
- **SQLite:** Padrão (sem config, ideal para desenvolvimento)
- **PostgreSQL:** Recomendado para produção
- **MySQL:** Alternativa (5.7+)

---

## 🚀 Instalação Rápida

### 1. Clonar o Repositório

```bash
git clone https://github.com/PI-Univesp-005/django-starter.git
cd django-starter
```

### 2. Configurar Variáveis de Ambiente

```bash
cp .env.example .env
```

### 3. Iniciar com Docker

```bash
# Desenvolvimento com SQLite (padrão)
./compose up --build
```
<sup>Para utilizar outros bancos, siga as instruções em [`.env.example`](.env.example)

### 4. Acessar a Aplicação

```
🌐 URL Principal: http://localhost:3333
📧 Painel Admin: http://localhost:3333/admin
```

---

## 📖 Uso

### Login Inicial

Usuários padrão (carregados automaticamente):

| Perfil | Usuário | Senha | Funcionalidades |
|---|---|---|---|
| **Gerente** | `gerente_teste` | `Senha_1234` | Acesso total + correção de inventário |
| **Líder** | `funcionario_lider_teste` | `Senha_1234` | Entrada/Saída + Gestão de lotes |
| **Funcionário** | `funcionario_teste` | `Senha_1234` | Visualização apenas |

### Workflow Básico

#### 1️⃣ Cadastrar Produto
Menu → Cadastro Produto → Preencher dados

#### 2️⃣ Adicionar Lote
Selecionar Produto → Estoque → Adicionar Lote

#### 3️⃣ Registrar Entrada
Estoque → Movimentar → Entrada → Selecionar Lote

#### 4️⃣ Registrar Saída
Estoque → Movimentar → Saída → Selecionar Lote

#### 5️⃣ Filtrar por Urgência
Estoque → Filtros (Margem / Amanhã / Buscar)

---

## 📂 Estrutura do Projeto

```
freshstock/
├── docker-compose.yml          # Orquestração de containers
├── Dockerfile                  # Build da aplicação
├── docker/                     # Configs específicas de DB
├── manage                      # Executável
├── compose                     # Wrapper
├── requirements.txt            # Dependências Python
├── docs/                       # Documentação
├── fixtures/                   # Dados pré-carregados
├── scripts/                    # Utilitários
│
└── src/
    ├── config/                 # Configuração Django
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    └── core/                   # App principal
        ├── models.py           # 🔑 Modelos (Usuario, Filial, Produto, Lote)
        ├── views.py            # 🔑 Lógica de negócio (18 views)
        ├── urls.py             # Roteamento
        ├── admin.py            # Admin site
        ├── migrations/         # Histórico de schema
        │
        └── templates/core/     # 🔑 Interface HTML
            ├── base.html       # Template base (CSS inline)
            ├── login.html
            ├── estoque_*.html
            ├── entrada_estoque.html
            ├── saida_estoque.html
            ├── correcao*.html
            └── assets/img/

README.md                       # Este arquivo
IMPROVEMENTS.md                 # Fragilidades & melhorias
LICENSE                         # MIT License
```

---

## 🗄️ Modelos de Dados

### Usuario (Customizado)
Estende `AbstractUser` do Django.
```
perfil: [gerente | funcionario_lider | funcionario]
```

### Filial
Agrupa produtos por localização.
```
nome, endereco
```

### Produto
Representa um item com estoque agregado.
```
nome, codigo_barras, emoji, descricao
quantidade_total (agregado via Signal de Lote)
dias_margem_promocao (padrão: 30 dias)
filial (1:N)
```

### Lote
Unidade mínima de rastreamento com validade.
```
numero_lote (opcional), data_validade, quantidade
status: [estoque | promocao | colocar_promocao | vencido]
produto (FK)

Signal: ao salvar/deletar, recalcula Produto.quantidade_total
```

---

## 🛣️ Rotas Disponíveis

### Autenticação
- `GET/POST /` - Login
- `GET /logout` - Logout

### Dashboard
- `GET /menu` - Menu principal

### Estoque
- `GET /estoque/` - Listar produtos
- `GET/POST /estoque/<id>/` - Detalhes do produto
- `GET/POST /estoque/<id>/entrada/` - Entrada de estoque
- `GET/POST /estoque/<id>/saida/` - Saída de estoque
- `GET/POST /estoque/<id>/zerar/` - Zerar estoque

### Lotes
- `POST /lote/<id>/add/` - Adicionar lote
- `GET/PUT/POST /lote/<id>/editar/` - Editar lote (PUT para HTTP correto, POST fallback)
- `DELETE/POST /lote/<id>/deletar/` - Deletar lote (DELETE para HTTP correto, POST fallback)
- `PUT/POST /lote/<id>/status/` - Atualizar status (PUT para HTTP correto, POST fallback)

### Produtos
- `GET/PUT/POST /produto/cadastro/` - Cadastrar/editar produto (PUT para HTTP correto, POST fallback)
- `DELETE/POST /produto/<id>/deletar/` - Deletar produto (DELETE para HTTP correto, POST fallback)

### Correção (Gerente apenas)
- `GET /correcao/` - Lista de produtos
- `GET /correcao/lotes/` - Listar todos os lotes
- `GET/PUT/POST /correcao/lote/<id>/` - Editar lote (correção) (PUT para HTTP correto, POST fallback)

### Relatórios
- `GET /relatorio/` - Relatório de estoque

---

## ⚠️ Fragilidades Conhecidas

Para análise completa, consulte **[IMPROVEMENTS.md](IMPROVEMENTS.md)**.

### Principais (Prioridade Alta)

- ❌ Sem histórico de movimentações (auditoria nula)
- ❌ Sem proteção contra race conditions em concorrência
- ❌ Permissões apenas básicas (`login_required`)
- ❌ Sem logging estruturado
- ❌ Zero testes automatizados
- ❌ Sem paginação (performance em 10k+ itens)

### Recomendações Imediatas

1. ✅ Implementar modelo `Movimentacao` para auditoria
2. ✅ Usar `F()` expressions + `@transaction.atomic`
3. ✅ Adicionar testes com pytest
4. ✅ Configurar logging Python
5. ✅ Paginação com 50 itens/página

---

## 🗺️ Roadmap

### v1.1 (Q3 2026) - Segurança & Auditoria
- Modelo de histórico de movimentações
- Logging estruturado
- Testes automatizados (70%)
- Race condition fixes

### v1.2 (Q4 2026) - Performance
- Paginação
- Índices de BD
- Cache com Redis
- Query optimization

### v2.0 (Q1 2027+) - Expansão
- API REST (DRF)
- Mobile app (React Native/Flutter)
- Scanner de código de barras
- ML para previsão de demanda

---

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'feat: descrição'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

**Padrão de commits:** `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

---

## 📝 Licença

Este projeto está licenciado sob a **MIT License** - veja [LICENSE](LICENSE) para detalhes.

---

## 📚 Docs: 
- [docs/indice_guias.md](docs/indice_guias.md)

---

## 📚 Changelog

### v1.0 (24/05/2026) - MVP Inicial

✅ Autenticação com perfis  
✅ Gestão de estoque por lote  
✅ Rastreamento de validade  
✅ Interface responsiva  
✅ Fixtures com 3 usuários padrão  
✅ Docker para fácil deploy  

---

<div align="center">

**Desenvolvido com ❤️ para melhorar a gestão de estoques de alimentos**

[⬆ Voltar ao Topo](#freshstock-)

</div>
___