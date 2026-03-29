# Instalando o Docker no macOS

No macOS, a forma recomendada de usar o Docker é através do **Docker Desktop** — um aplicativo nativo que inclui o Docker Engine, o Docker Compose e um painel gráfico em um único instalador. Ele resolve a dependência do Linux de forma transparente, rodando uma máquina virtual leve em segundo plano.

---

## Requisitos do sistema

- macOS 12 (Monterey) ou mais recente
- Processador Apple Silicon (M1/M2/M3/M4) ou Intel — há instaladores separados para cada arquitetura

Se você não sabe qual chip o seu Mac tem, clique no menu Apple (canto superior esquerdo) → "Sobre Este Mac" e procure por "Chip" (Apple Silicon) ou "Processador" (Intel).

---

## Instalação

**Passo 1 — Baixar o instalador**

Acesse a página oficial e baixe o instalador para o seu chip:

**[https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)**

**Passo 2 — Instalar**

Abra o arquivo `.dmg` baixado, arraste o ícone do Docker para a pasta Aplicativos e inicie o Docker a partir de lá (ou use Spotlight: `Cmd+Espaço` → digite "Docker").

A primeira inicialização pode levar um minuto enquanto o Docker configura sua VM Linux interna.

**Passo 3 — Verificar a instalação**

Abra o Terminal (`Cmd+Espaço` → "Terminal") e execute:

```bash
docker --version
docker compose version
docker run hello-world
```

Se o último comando imprimir "Hello from Docker!", tudo está funcionando.

---

## Alternativa: instalar via Homebrew

Se você usa o [Homebrew](https://brew.sh), pode instalar o Docker Desktop pela linha de comando:

```bash
brew install --cask docker
```

Após a instalação, abra o Docker Desktop pelo menos uma vez para concluir a configuração inicial.

---

## Documentação oficial

**[https://docs.docker.com/desktop/install/mac-install/](https://docs.docker.com/desktop/install/mac-install/)**

---

← Voltar ao [README](README.pt.md)
