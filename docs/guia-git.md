# Git para Iniciantes

Se você nunca usou Git antes, este guia é para você. Ele explica o que é o Git, por que ele existe e mostra cada ação necessária para contribuir com um projeto, de três formas: linha de comando no Linux/macOS, linha de comando no Windows e interface gráfica.

---

## Índice

1. [O que é Git e por que ele existe?](#1-o-que-é-git-e-por-que-ele-existe)
2. [Conceitos essenciais em linguagem simples](#2-conceitos-essenciais-em-linguagem-simples)
3. [O fluxo mínimo de contribuição](#3-o-fluxo-mínimo-de-contribuição)
4. [Tabela de comandos](#4-tabela-de-comandos)

---

## 1. O que é Git e por que ele existe?

Imagine que você está escrevendo um documento longo com três colegas e cada um envia versões por e-mail: `relatorio_v1.docx`, `relatorio_v2_FINAL.docx`, `relatorio_v2_FINAL_de_verdade.docx`. Em uma semana você tem uma dúzia de arquivos, ninguém sabe qual é o mais recente e duas pessoas editaram o mesmo parágrafo de formas conflitantes.

**Git resolve esse problema para código** (e, na verdade, para qualquer arquivo de texto).

Git é um **sistema de controle de versão**: uma ferramenta que rastreia cada mudança já feita em um conjunto de arquivos. Toda vez que você salva um snapshot significativo (chamado de *commit*), o Git registra quem fez a mudança, quando e por quê (através da sua mensagem de commit). Você pode consultar o histórico completo do projeto, ver exatamente o que mudou entre dois pontos no tempo e, o mais importante: **desfazer erros** revertendo para um snapshot (ponto da história) anterior.

O Git também permite que várias pessoas trabalhem no mesmo código simultaneamente sem sobrescrever o trabalho umas das outras. Cada pessoa trabalha na sua própria *branch* (ramo) isolada, e o Git oferece ferramentas para *mesclar* (merge) branches, tratando automaticamente a maioria dos casos em que duas pessoas editaram partes diferentes do código.

**GitHub, GitLab e Bitbucket** são sites que hospedam repositórios Git online. O Git em si é a ferramenta no seu computador, essas plataformas são onde ficam as cópias remotas do repositório e onde os times colaboram por meio de pull requests e revisão de código (sem necessidade de mais detalhes por enquanto). Este projeto assume o GitHub, mas os comandos Git são idênticos em todas as plataformas.

---

## 2. Conceitos essenciais em linguagem simples

**Repositório (repo):** A pasta que contém o seu projeto, mais a pasta oculta `.git` onde o Git armazena o histórico completo. Quando você "clona um repo", está baixando todo esse pacote.

**Commit:** Um snapshot salvo do projeto em um momento específico. Cada commit tem um ID único, uma mensagem que você escreve descrevendo o que mudou e um ponteiro para o commit anterior. O histórico de um projeto é uma cadeia de commits.

**Branch:** Uma linha de desenvolvimento independente. A branch padrão normalmente se chama `main`. Quando você cria uma nova branch, obtém sua própria cópia privada do código para experimentar. As mudanças na sua branch não afetam a `main` (nem a branch de ninguém mais) até você deliberadamente mesclá-las.

**Área de staging (índice):** Uma sala de espera entre seus arquivos de trabalho e um commit. Quando você faz `git add` em um arquivo, move as mudanças para a área de staging. Quando faz `git commit`, o Git salva tudo que está atualmente em staging. Esse processo em duas etapas permite que você revise exatamente o que vai no commit antes de salvá-lo.

**Remote:** Uma cópia do repositório hospedada em outro lugar: tipicamente no GitHub. O remote normalmente se chama `origin` por convenção. `git push` envia seus commits para o remote; `git pull` baixa commits do remote para a sua máquina.

**Pull Request (PR):** Um recurso de plataformas de hospedagem (GitHub, GitLab, etc.), não do Git em si. Um PR é uma proposta para mesclar sua branch em outra (normalmente a `main`). É o mecanismo padrão de revisão de código: seus colegas veem exatamente o que mudou, deixam comentários, solicitam edições e, eventualmente, aprovam e mesclam seu trabalho.

---

## 3. O fluxo mínimo de contribuição

Os sete passos abaixo cobrem tudo que você precisa para contribuir com este projeto. Cada um é mostrado de três formas:

- **CLI — Linux / macOS** (terminal POSIX)
- **CLI — Windows** (Git Bash, PowerShell ou Prompt de Comando 🤢)
- **Interface gráfica**: painel integrado do VSCode, com notas sobre o GitHub Desktop como alternativa

---

### Passo 1 — Clone: obtenha uma cópia do projeto

Clonar baixa o repositório inteiro: todos os arquivos e seu histórico completo, do GitHub para o seu computador. Você faz isso apenas uma vez por projeto.

#### CLI — Linux / macOS

```bash
cd ~/projetos        # ou onde você preferir guardar seus projetos
git clone git@github.com:PI-Univesp-005/django-starter.git
cd django-starter
```

#### CLI — Windows (PowerShell)

```sh
cd C:\Users\SeuNome\projetos
git clone git@github.com:PI-Univesp-005/django-starter.git
cd django-starter
```

#### Interface gráfica — VSCode

Pressione `Ctrl+Shift+P` (Windows/Linux) ou `Cmd+Shift+P` (macOS) para abrir a Paleta de Comandos, digite **"Git: Clone"** e pressione Enter. Cole a URL do repositório e escolha uma pasta local. O VSCode perguntará se você quer abrir o repositório clonado, clique em **"Open"**.

#### Interface gráfica — GitHub Desktop

Clique em **File → Clone Repository**, vá para a aba **URL**, cole a URL do repositório, escolha um caminho local e clique em **Clone**.

---

### Passo 2 — Branch: crie seu próprio espaço de trabalho

Antes de fazer qualquer mudança, crie uma branch. Isso mantém seu trabalho completamente separado da `main` até que esteja pronto e revisado. Use nomes curtos e descritivos com hífens.

#### CLI — Linux / macOS e Windows (idênticos)

```bash
# Certifique-se de estar na versão mais recente da main primeiro:
git checkout main
git pull origin main

# Crie e mude imediatamente para uma nova branch:
git checkout -b seu-nome/descrição-da-funcionalidade
```

#### Interface gráfica — VSCode

Clique no nome da branch no **canto inferior esquerdo** da janela. No menu que aparece no topo, selecione **"Create new branch from..."**, digite o nome da branch, pressione Enter e escolha `main` como ponto de partida.

#### Interface gráfica — GitHub Desktop

Clique no dropdown **"Current Branch"** no topo, clique em **"New Branch"**, digite um nome e clique em **"Create Branch"**.

---

### Passo 3 — Add: prepare suas mudanças para o commit

Após editar arquivos, você diz ao Git quais mudanças deseja incluir no próximo commit. Isso se chama **staging**.

#### CLI — Linux / macOS e Windows (idênticos)

```bash
# Veja quais arquivos mudaram:
git status

# Prepare um arquivo específico:
git add src/core/views.py

# Prepare tudo que mudou (use com cuidado — revise o git status antes):
git add .
```

#### Interface gráfica — VSCode

Clique no **ícone de Controle de Código-Fonte** na barra lateral esquerda (ou pressione `Ctrl+Shift+G` / `Cmd+Shift+G`). Você verá uma lista de arquivos alterados em **"Changes"**. Passe o mouse sobre um arquivo e clique no ícone **`+`** para preparar um arquivo específico, ou passe o mouse sobre o cabeçalho **"Changes"** e clique no **`+`** para preparar tudo. Os arquivos preparados se movem para **"Staged Changes"**.

#### Interface gráfica — GitHub Desktop

O painel esquerdo mostra todos os arquivos alterados com caixas de seleção. Marque os arquivos que deseja incluir no próximo commit. Você pode clicar em um arquivo para revisar suas mudanças exatas antes de prepará-lo.

---

### Passo 4 — Commit: salve um snapshot

Um commit salva permanentemente suas mudanças em staging no histórico do repositório local. A mensagem de commit é importante, ela conta aos seus colegas (e ao seu eu futuro) *por que* a mudança foi feita, não só o que mudou. Escreva no modo imperativo, como se completasse a frase "Se aplicado, este commit vai…": por exemplo, "Adicionar endpoint de login do usuário".

#### CLI — Linux / macOS e Windows (idênticos)

```bash
git commit -m "Adicionar endpoint de login do usuário"
```

#### Interface gráfica — VSCode

No painel de Controle de Código-Fonte, digite sua mensagem no campo de texto no topo (que diz "Message (press Ctrl+Enter to commit)") e pressione `Ctrl+Enter` (Windows/Linux) ou `Cmd+Enter` (macOS).

#### Interface gráfica — GitHub Desktop

No canto inferior esquerdo, preencha o campo **Summary** com sua mensagem e clique no botão azul **"Commit to `nome-da-sua-branch`"**.

---

### Passo 5 — Push: envie sua branch

Enviar (push) manda seus commits locais para o repositório remoto no GitHub. Até você fazer o push, seus commits existem apenas no seu computador — ninguém mais pode vê-los.

#### CLI — Linux / macOS e Windows (idênticos)

```bash
# Na primeira vez que você faz push de uma nova branch:
git push -u origin seu-nome/descrição-da-funcionalidade

# Nos pushes subsequentes na mesma branch:
git push
```

#### Interface gráfica — VSCode

Após o commit, o painel mostra um botão **"Publish Branch"** (se a branch nunca foi enviada) ou **"Sync Changes"** com uma seta de upload (se já foi). Clique nele.

#### Interface gráfica — GitHub Desktop

Após o commit, a barra superior mostra **"Publish branch"** (primeiro push) ou **"Push origin"** (pushes subsequentes). Clique nele.

---

### Passo 6 — Pull Request: proponha suas mudanças

Um Pull Request (PR) é como você pede para sua branch ser mesclada na `main`. Isso acontece no site do GitHub, não nas ferramentas Git locais.

Após fazer o push da sua branch, o GitHub muitas vezes mostra um banner amarelo sugerindo abrir um PR e você pode usar esse atalho ou seguir os passos abaixo.

1. Vá ao repositório no GitHub.
2. Clique na aba **"Pull requests"**.
3. Clique em **"New pull request"**.
4. Defina **base:** `main` ← **compare:** `seu-nome/descrição-da-funcionalidade`.
5. Revise as mudanças — certifique-se de que mostra apenas o que você pretendia alterar.
6. Escreva um título claro e uma descrição explicando *o que* mudou e *por quê*. Se o PR fecha uma issue, escreva `Closes #42` na descrição.
7. Clique em **"Create pull request"**.

> **Atalho no VSCode:** A extensão [GitHub Pull Requests](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github) permite criar e revisar PRs diretamente no VSCode sem abrir o navegador.
>
> **Atalho no GitHub Desktop:** Após o push, o GitHub Desktop mostra um botão **"Create Pull Request"** que abre a página correta do GitHub no seu navegador com a branch já selecionada.

---

### Passo 7 — Pull: traga as mudanças dos outros

Enquanto você trabalhava na sua branch, seus colegas podem ter mesclado as próprias mudanças na `main`. Antes de começar um novo trabalho, e ritualmente, você deve baixar as mudanças mais recentes.

#### CLI — Linux / macOS e Windows (idênticos)

```bash
# Mude para a main e baixe a versão mais recente:
git checkout main
git pull origin main

# Se você está no meio de um trabalho numa branch de funcionalidade e quer
# trazer as mudanças mais recentes da main para ela, use rebase:
git checkout seu-nome/descrição-da-funcionalidade
git rebase main
```

#### Interface gráfica — VSCode

Mude para `main` clicando no nome da branch no canto inferior esquerdo. No painel de Controle de Código-Fonte, clique em **"Sync Changes"** (seta circular), ou acesse **"..."** → **"Pull"**. Para atualizar sua branch de funcionalidade, mude de volta para ela e use **"..."** → **"Branch"** → **"Rebase Branch onto..."** → selecione `main`.

#### Interface gráfica — GitHub Desktop

Mude para `main` usando o dropdown **"Current Branch"**. Clique em **"Fetch origin"** (verifica novos commits) e depois em **"Pull origin"** (baixa os commits). Mude de volta para sua branch de funcionalidade e clique em **Branch → Rebase Current Branch** → selecione `main`.

---

## 4. Tabela de comandos

| Ação | Linux / macOS | Windows (PowerShell) |
|---|---|---|
| Clonar um repo | `git clone <url>` | `git clone <url>` |
| Ver status | `git status` | `git status` |
| Criar e mudar para branch | `git checkout -b <nome>` | `git checkout -b <nome>` |
| Mudar para branch existente | `git checkout <nome>` | `git checkout <nome>` |
| Preparar um arquivo | `git add <arquivo>` | `git add <arquivo>` |
| Preparar tudo | `git add .` | `git add .` |
| Commitar mudanças preparadas | `git commit -m "mensagem"` | `git commit -m "mensagem"` |
| Push da branch (primeira vez) | `git push -u origin <branch>` | `git push -u origin <branch>` |
| Push (vezes seguintes) | `git push` | `git push` |
| Baixar mudanças do remote | `git pull origin main` | `git pull origin main` |
| Ver histórico de commits | `git log --oneline` | `git log --oneline` |
| Descartar mudanças não preparadas | `git restore <arquivo>` | `git restore <arquivo>` |
| Tirar arquivo do staging | `git restore --staged <arquivo>` | `git restore --staged <arquivo>` |

---

## Leitura adicional

- [Documentação oficial do Git](https://git-scm.com/doc) — referência definitiva, incluindo um livro gratuito online
- [Guias Git do GitHub](https://github.com/git-guides) — tutoriais curtos e acessíveis para cada comando
- [Documentação do Controle de Código-Fonte do VSCode](https://code.visualstudio.com/docs/sourcecontrol/overview)
- [Documentação do GitHub Desktop](https://docs.github.com/en/desktop)

---

← Voltar ao [README](../README.md)
