# Django — Arquitetura, Capacidades e Decisões deste Projeto

---

## Índice

1. [O que é Django e quais são seus objetivos](#1-o-que-é-django-e-quais-são-seus-objetivos)
2. [Funcionalidades principais](#2-funcionalidades-principais)
3. [Melhores casos de uso](#3-melhores-casos-de-uso)
4. [Arquitetura MVT](#4-arquitetura-mvt)
5. [Componentes de uma aplicação Django](#5-componentes-de-uma-aplicação-django)
6. [Por que este projeto está estruturado como está](#6-por-que-este-projeto-está-estruturado-como-está)
7. [Estrutura deste projeto – detalhes e decisões](#7-estrutura-deste-projeto--detalhes-e-decisões)
8. [Responsabilidades dos módulos](#8-responsabilidades-dos-módulos)
9. [Arquivos esperados em cada módulo e seus papéis](#9-arquivos-esperados-em-cada-módulo-e-seus-papéis)
10. [Como adicionar novos apps no Django](#10-como-adicionar-novos-apps-no-django)
11. [Boas práticas para manter a arquitetura escalável](#11-boas-práticas-para-manter-a-arquitetura-escalável)

---

## 1. O que é Django e quais são seus objetivos

Django é um framework web Python criado em 2003 e tornado open-source em 2005. Seu lema — *"the web framework for perfectionists with deadlines"* — resume bem a filosofia: entregar um conjunto completo de ferramentas prontas para uso que permita construir aplicações web robustas rapidamente, sem sacrificar qualidade ou segurança.

Os três objetivos centrais do Django são:

**Velocidade de desenvolvimento.** O framework toma decisões por você onde não há razão para escolher de outra forma — estrutura de pastas, ORM, sistema de autenticação, painel administrativo. Você escreve apenas o que é único na sua aplicação.

**Segurança por padrão.** Proteções contra os ataques mais comuns (SQL injection, XSS, CSRF, clickjacking) estão ativas sem nenhuma configuração adicional. O desenvolvedor precisa fazer esforço deliberado para desativá-las.

**Escalabilidade com convenção.** O mesmo padrão arquitetural funciona de um projeto com uma tabela no banco até plataformas com milhões de usuários (Instagram, Pinterest e Disqus foram construídos com Django). A convenção compartilhada pelo ecossistema facilita a entrada de novos desenvolvedores no projeto.

---

## 2. Funcionalidades principais

| Funcionalidade | O que faz |
|---|---|
| **ORM** | Mapeia tabelas do banco de dados para classes Python. Você escreve queries em Python, não em SQL. Suporta PostgreSQL, MySQL, SQLite, Oracle. |
| **Sistema de migrações** | Gera e aplica automaticamente as mudanças de esquema do banco conforme você altera os models. |
| **Roteamento de URLs** | Associa padrões de URL a funções de view via expressões simples ou regex. |
| **Sistema de templates** | Motor de templates com herança, filtros e tags — para quem renderiza HTML no servidor. |
| **Painel administrativo** | Interface CRUD completa gerada automaticamente a partir dos models, disponível em `/admin/`. |
| **Autenticação e permissões** | Usuários, grupos, sessões e permissões por objeto — prontos para usar ou estender. |
| **Formulários** | Validação, sanitização e renderização de formulários HTML a partir de classes Python. |
| **Cache** | Integração com Memcached, Redis e cache em memória com uma API unificada. |
| **Internacionalização** | Suporte a múltiplos idiomas e fusos horários embutido. |
| **Signals** | Sistema de eventos desacoplado: dispare e escute acontecimentos em qualquer parte da aplicação. |
| **Segurança** | CSRF, XSS, SQL injection, clickjacking e HTTPS enforcement — ativos por padrão. |

O Django também facilita a criação de migrations e usuários admin para o gerencimanto da aplicação. Esses comandos rodados através do `manage.py` ainda não estão disponíveis localmente, apenas no **container**. Eles dependem de que o venv e python estejam alinhados com o que roda na versão do docker para serem configurados e executados localmente, isto já está [listado como tarefa futura](../README.md#pontos-pendentes-todo).

---

## 3. Melhores casos de uso

Django brilha em aplicações que são **centradas em dados e orientadas a conteúdo**, onde a produtividade e a segurança importam mais do que performance bruta em I/O assíncrono.

**Django é uma excelente escolha para:**

- APIs REST e GraphQL (com Django REST Framework ou Strawberry)
- Sistemas de gerenciamento de conteúdo (CMS)
- Plataformas de e-commerce e SaaS B2B
- Painéis internos e ferramentas administrativas
- Aplicações com modelos de dados complexos e muitas relações
- Projetos que precisam de um painel de administração funcional rapidamente

**Django não é a melhor escolha para:**

- Serviços que precisam de altíssima concorrência com conexões persistentes (WebSockets em escala — prefira FastAPI + Starlette ou Node.js)
- Microsserviços muito pequenos onde o overhead do framework seria desproporcional (prefira Flask ou FastAPI)
- Aplicações em tempo real com centenas de milhares de conexões simultâneas

> **Nota:** Django suporta ASGI e views assíncronas desde a versão 3.1, o que melhora sua performance em I/O. Mas o ecossistema ainda é majoritariamente síncrono.

---

## 4. Arquitetura MVT

Django segue o padrão **MVT — Model, View, Template**. É uma variação do MVC clássico onde o Django em si faz o papel do "Controller":

```
Requisição HTTP
      │
      ▼
  URLs (urls.py)          ← roteamento: qual view trata esta URL?
      │
      ▼
  View (views.py)         ← lógica: o que fazer com a requisição?
      │
      ├──► Model (models.py) ◄──► Banco de dados
      │
      ▼
  Template (.html) ou JsonResponse
      │
      ▼
Resposta HTTP
```

| Camada | Responsabilidade |
|---|---|
| **Model** | Define a estrutura dos dados e as regras de negócio ligadas a eles. Cada model é uma classe Python que vira uma tabela no banco. |
| **View** | Recebe a requisição, orquestra a lógica (consulta o model, processa dados) e decide o que retornar. É o equivalente ao Controller do MVC. |
| **Template** | Renderiza a resposta — normalmente HTML com variáveis dinâmicas. Em APIs JSON, essa camada é substituída por serializers ou `JsonResponse`. |
| **URLs** | Tabela de roteamento que conecta padrões de endereço às views corretas. O Django chama essa peça de URLconf. |

---

## 5. Componentes de uma aplicação Django

Um **projeto** Django é o container de configuração global. Um ou mais **apps (módulos)** dentro dele são as unidades funcionais independentes. Essa separação é central na filosofia do framework.

```
meu_projeto/               ← projeto (configuração global)
├── config/
│   ├── settings.py        ← configurações globais
│   ├── urls.py            ← URLconf raiz
│   ├── wsgi.py
│   └── asgi.py
├── usuarios/              ← app (domínio: usuários)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   └── migrations/
│       └── ...
├── pedidos/               ← app (domínio: pedidos)
│   └── ...
└── manage.py
```

**Umo app deve representar um único domínio de negócio** — usuários, pedidos, produtos, pagamentos. Essa modularidade permite reutilizar apps (módulos) em projetos diferentes e facilita testes isolados.

Cado app contém tipicamente:

- **`models.py`** — definição das tabelas e suas relações
- **`views.py`** — lógica de negócio e construção das respostas
- **`urls.py`** — rotas específicas deste domínio (incluídas no URLconf raiz)
- **`admin.py`** — registro dos models no painel administrativo
- **`migrations/`** — histórico de mudanças de esquema (scheme) gerado automaticamente

---

## 6. Por que este projeto está estruturado como está

### `src/config/` como pacote do projeto

A convenção padrão do `django-admin startproject` cria o pacote de configuração com o mesmo nome do projeto (ex: `django_starter/settings.py`). Renomeá-lo para `config/` é uma prática consolidada na comunidade porque:

- O nome `config` é autoexplicativo e agnóstico ao nome do projeto
- Facilita copiar a estrutura entre projetos
- Evita confusão quando o nome do projeto muda

### Nenhum app separado (por enquanto)

A recomendação do Django é criar apps (módulos) quando há um domínio de negócio definido. **Quando criar o primeiro app:** assim que o primeiro model for definido, ou quando houver muitos endpoints relacionados ao mesmo domínio.

### `settings.py` lê tudo do ambiente

O Django recomenda separar configuração de código, chamado de [Twelve-Factor App](https://12factor.net/config). Em vez de valores hard-coded, cada configuração sensível (`SECRET_KEY`, credenciais do banco, `DEBUG`, `ALLOWED_HOSTS`) é lida com `os.environ.get()`. Isso significa:

- O mesmo código roda em desenvolvimento, staging e produção sem modificação
- Segredos nunca entram no repositório Git
- Trocar o banco de dados é uma mudança de variável de ambiente, não de código

### `SECRET_KEY` lida do ambiente

O Django usa a `SECRET_KEY` para assinar cookies de sessão, tokens CSRF e outros dados criptografados. Expô-la no código-fonte é uma vulnerabilidade de segurança grave. A prática recomendada é sempre salvá-la na variável de ambiente, nunca deixá-la no `settings.py` com um valor real.

### `DEBUG=False` em produção

Com `DEBUG=True`, o Django exibe stack traces detalhados com variáveis locais no navegador em caso de erro. Útil em desenvolvimento, perigoso em produção (expõe muitos detalhes e potencialmente segredos).

### `ALLOWED_HOSTS` como lista do ambiente

O Django rejeita requisições cujo header `Host` não esteja em `ALLOWED_HOSTS`, proteção contra ataques de HTTP Host header injection. Em desenvolvimento, `localhost` e `127.0.0.1` são suficientes. Em produção, o domínio real precisa estar na lista. Ler do ambiente evita ter que alterar o código entre deploys.

### `DEFAULT_AUTO_FIELD = BigAutoField`

Por padrão, o Django usava `AutoField` (inteiro de 32 bits, máximo de ~2,1 bilhões de registros) como chave primária automática. Desde o Django 3.2, a recomendação é usar `BigAutoField` (64 bits, máximo de ~9,2 quintilhões). Definir isso explicitamente em `settings.py` evita warnings ao rodar as migrations e garante que todos os models criados no futuro usem o campo correto.

---

## 7. Estrutura deste projeto – detalhes e decisões

Este projeto foi concebido desde o início para ser executado em contêineres Docker, com suporte nativo a SQLite (para desenvolvimento rápido e testes locais) e MySQL/PostgreSQL (como candidatos a serem considerados no futuro). A estrutura de pastas reflete essa intenção e segue as melhores práticas da comunidade Django.

### 7.1. `src/` – isolamento do código

Todo o código Python (projeto e apps - módulos) está dentro da pasta `src/`. Essa separação mantém a raiz do repositório limpa para arquivos de infraestrutura (Dockerfile, docker-compose.yml, scripts de entrada) e documentação. Além disso, facilita futuras migrações para ferramentas que esperam o código em um subdiretório (como alguns provedores de PaaS).

### 7.2. `config/` – configuração do projeto

Dentro de `src/` está o pacote `config/`, que contém a configuração global do projeto:

- **`settings.py`** — lê todas as variáveis sensíveis do ambiente, define o banco de dados conforme a variável `DB`, e mantém as opções padrão do Django. Neste arquivo também se registram os apps (módulos), middleware, templates, etc.
- **`urls.py`** — roteador principal; atualmente inclui apenas a URL `"/"` que aponta para a view `core.views.hello`.
- **`asgi.py`** e **`wsgi.py`** — pontos de entrada para servidores ASGI (assíncrono) e WSGI (síncrono). O projeto mantém ambos para não limitar futuras escolhas de deploy.

### 7.3. `core/` – primeiro app (e app compartilhada)

O diretório `core/` é o primeira **app** (módulo) Django. Ele tem um papel especial: serve como repositório de funcionalidades compartilhadas, modelos base e lógica que não pertence a um domínio específico. A decisão de começar com um app chamada `core` é comum em projetos de médio e grande porte, porque:

- Permite centralizar utilitários, mixins e modelos abstratos que serão reutilizados por outros apps (módulos).
- Evita que a pasta `config/` acumule código de negócio, mantendo a separação de responsabilidades.
- Oferece um local óbvio para o primeiro model (`HealthCheck`), evitando a criação prematura de vários apps.

A app `core` está devidamente registrada em `INSTALLED_APPS` como `'core.apps.CoreConfig'`.

### 7.4. Docker e ambientes

A infraestrutura containerizada está dividida em:

- **`Dockerfile`** – define a imagem da aplicação, instalando dependências e configurando o ambiente Python.
- **`docker-compose.yml`** – orquestra os serviços `web` (Django) e, opcionalmente, `db` (PostgreSQL) via profile `--profile postgres`.
- **`entrypoint.sh`** – script executado na inicialização do container; responsável por rodar migrações antes de iniciar o servidor. A presença de migrações automatizadas garante que o banco de dados esteja sempre atualizado.
- **`docker/postgres/`** – contém um Dockerfile personalizado e um `init.sql` que ativa extensões úteis (`pg_trgm`, `unaccent`). Esse script roda apenas na primeira inicialização do volume de dados.
- **`docker/mysql/`** – contém um Dockerfile personalizado e um `init.sql`. Esse script roda apenas na primeira inicialização do volume de dados.

Essa estrutura permite alternar entre SQLite (sem banco externo) e PostgreSQL com um simples comando `docker compose --profile postgres up`.

---

## 8. Responsabilidades dos módulos

Para manter a arquitetura limpa e previsível, cada parte do projeto tem uma responsabilidade bem definida:

### 8.1. `config/`

- **Configurar** o Django para o ambiente atual (desenvolvimento, produção, teste).
- **Definir** a lista de apps (módulos) instalados, middlewares, templates, autenticação, etc.
- **Roteamento** raiz (`urls.py`) – direciona as URLs para os apps (módulos) apropriadas.
- **Ponto de entrada** para servidores (WSGI/ASGI) e gerenciamento de ambiente.

O pacote `config` **não deve conter models, views ou lógica de negócio**. Qualquer código que não seja estritamente de configuração deve ser movido para um app (módulo) apropriado.

### 8.2. `core/`

- **Modelos abstratos** – fornecer classes base para timestamp, UUID, etc.
- **Utilitários** – funções de uso geral (ex: `paginate_queryset`, `get_client_ip`).
- **Comportamento compartilhado** – middlewares que não são específicos de um domínio.
- **Primeiros modelos concretos** – como o `HealthCheck` usado para testes de integração.
- **Views de infraestrutura** – endpoints como `/health/`, `/status/`.

A app `core` não deve conter lógica de domínio específica (usuários, pedidos, produtos). Isso será delegado a outros apps (módulos) à medida que o projeto cresce.

---

## 9. Arquivos esperados em cada módulo e seus papéis

Se guiar bem e entender o propósito de cada arquivo dentro de um projeto Django é fundamental. Abaixo, tem uma descrição dos arquivos que aparecem (ou aparecerão) neste projeto.

### 9.1. `config/`

| Arquivo | Papel |
|---------|-------|
| `settings.py` | Configurações globais: bancos de dados, apps (módulos) instalados, middleware, segurança, internacionalização, etc. |
| `urls.py` | Roteador principal. Usa `include()` para incorporar URLs de outros apps (módulos). |
| `asgi.py` | Interface com servidores ASGI (assíncronos). Usado para WebSockets e views assíncronas. |
| `wsgi.py` | Interface com servidores WSGI (síncronos). O ponto de entrada tradicional para Gunicorn, uWSGI. |
| `__init__.py` | Torna o diretório um pacote Python; pode estar vazio. |

### 9.2. `core/`

| Arquivo | Papel |
|---------|-------|
| `models.py` | Define os modelos de dados. O primeiro model é `HealthCheck`, usado para testar a conexão com o banco. |
| `views.py` | Contém a lógica das views (funções ou classes). Aqui está a `hello()` que retorna dados em JSON. |
| `urls.py` | (Opcional) Roteador específico do app. Se existir, será incluído no `urls.py` do projeto. |
| `admin.py` | Registra os models no painel administrativo do Django. |
| `apps.py` | Configura o app dentro do Django (nome, verbose name, etc.). A classe `CoreConfig` está aqui. |
| `migrations/` | Diretório onde o Django armazena as migrações geradas a partir de alterações nos models. O arquivo `001-initial_to-be-removed.py` é a primeira migração, que criou a tabela `core_healthcheck` e inseriu um registro. |
| `__init__.py` | Necessário para que o Django reconheça o app como um pacote Python. |
| `tests.py` (futuro) | Local para escrever testes unitários do app. |

### 9.3. Outros arquivos importantes

| Arquivo | Papel |
|---------|-------|
| `manage.py` | Utilitário de linha de comando do Django. Executa comandos como `runserver`, `makemigrations`, `migrate`. |
| `requirements.txt` | Lista de dependências Python. Usado pelo Dockerfile para instalar os pacotes. |
| `entrypoint.sh` | Script de inicialização do container. Executa `migrate` e depois inicia o servidor. |
| `Dockerfile` | Instruções para construir a imagem Docker da aplicação. |
| `docker-compose.yml` | Orquestra os serviços (web, db). |
| `.env` | Armazena variáveis de ambiente (não versionado). Exemplo: `DB=sqlite`, `SECRET_KEY=...`. |

---

## 10. Como adicionar novos apps no Django

Quando o projeto precisar de um novo domínio (ex: usuários, produtos, pedidos), o caminho é criar um novo app (módulo) Django. Veja o passo a passo.

### 10.1. Criar um app

Dentro do diretório `src/` (onde está o `manage.py`), execute:

```bash
python manage.py startapp nome_do_app
```

Isso criará uma pasta `nome_do_app/` com a estrutura mínima: `models.py`, `views.py`, `admin.py`, `apps.py`, `migrations/` e `__init__.py`.

### 10.2. Registrar o app

Em `config/settings.py`, adicione o nome do app (ou seu `AppConfig`) em `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # apps (módulos) do Django
    ...
    'core.apps.CoreConfig',      # já existente
    'nome_do_app',               # nome simples
    # ou 'nome_do_app.apps.NomeDaAppConfig' para configuração personalizada
]
```

### 10.3. Definir URLs

No diretório da novo app, crie um arquivo `urls.py` (se não existir). Nele, defina as rotas específicas do app:

```python
# nome_do_app/urls.py
from django.urls import path
from . import views

app_name = 'nome_do_app'  # namespace para reverse URL
urlpatterns = [
    path('', views.minha_view, name='index'),
]
```

Depois, inclua essas URLs no roteador principal (`config/urls.py`):

```python
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),              # se core tiver urls
    path('minha-rota/', include('nome_do_app.urls')),
]
```

### 10.4. Modelos e migrações

Defina os modelos em `models.py`. Execute:

```bash
python manage.py makemigrations nome_do_app   # gera migração
python manage.py migrate                      # aplica no banco
```
 
O Django criará automaticamente a pasta `migrations/` com os arquivos de migração.

### 10.5. O que cada arquivo faz

- **`models.py`** – classes que viram tabelas no banco.
- **`views.py`** – funções ou classes que recebem requisições e retornam respostas.
- **`urls.py`** – mapeia URLs para views dentro do app.
- **`admin.py`** – personaliza como os modelos aparecem no admin.
- **`apps.py`** – configuração do app (nome, verbose_name, etc.).
- **`migrations/`** – histórico de alterações no esquema.
- **`tests.py`** – testes automatizados.
- **`templates/`** (opcional) – templates HTML específicos do app.
- **`static/`** (opcional) – arquivos estáticos (CSS, JS, imagens) específicos do app.

---

## 11. Boas práticas para manter a arquitetura escalável

1. **Mantenho apps pequenos e focados**  
   Cado app deve ter uma única responsabilidade bem definida. Evite criar um app "utils" que agrupa tudo – use `core` apenas para compartilhamento genuíno.

2. **Use `core` como base, não como depósito**  
   Coloque em `core` apenas modelos abstratos, mixins, funções utilitárias e código que não tem um domínio claro. Lógica de negócio deve ficar no app correspondente.

3. **Separe views de negócio de views de infraestrutura**  
   Views como `/health/` e `/status/` podem permanecer em `core`. Views de domínio (ex: `/products/`, `/cart/`) vão nas suas respectivos apps.

4. **Nunca importe configurações diretamente**  
   Use `from django.conf import settings` sempre que precisar acessar configurações. Isso mantém a testabilidade.

5. **Utilize `django-environ` (ou `os.environ`) para configurações**  
   Evite hard-coded valores. O projeto já faz isso, continue usando variáveis de ambiente [../.env](.env) para tudo que é sensível ou varia entre ambientes.

6. **Mantenha o `entrypoint.sh` simples**  
   No Docker, o entrypoint deve rodar apenas migrações e coletar arquivos estáticos (quando em produção). Evite lógica de negócio ali.

7. **Documente a estrutura**  
   Manter um arquivo `README.md` e este documento atualizado ajuda novos desenvolvedores a entenderem as decisões arquiteturais.

8. **Teste isoladamente**  
   Cado app deve ter seus próprios testes. O Django descobre automaticamente testes em `tests.py` ou em um pacote `tests/`.

9. **Considere dividir `settings.py` em múltiplos arquivos**  
   Quando o projeto crescer, crie um diretório `config/settings/` com `base.py`, `development.py`, `production.py` e use `DJANGO_SETTINGS_MODULE` para selecionar o ambiente.

10. **Mantenha o versionamento do banco de dados via migrações**  
    Nunca altere o banco manualmente; sempre crie uma migração. O sistema de migrações garante rastreabilidade e consistência entre ambientes.

---

Com essas práticas, o projeto pode crescer de forma organizada, mantendo a clareza e a facilidade de manutenção que Django oferece desde o início.

← Voltar ao [README](../README.md)