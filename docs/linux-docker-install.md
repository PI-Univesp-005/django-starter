# Instalando o Docker no Linux

Este guia cobre Ubuntu e Debian, as distribuições Linux mais comuns entre desenvolvedores. Para outras distribuições, consulte a referência oficial no final da página.

---

## Por que usar o repositório oficial do Docker?

A maioria das distribuições Linux oferece uma versão do Docker no repositório padrão (`apt install docker.io`). Essa versão quase sempre é antiga — às vezes por anos. O Docker avança rapidamente, e recursos como profiles do Compose exigem uma versão relativamente recente. Por isso, este guia instala a partir do repositório oficial do Docker, que sempre tem a versão estável mais recente.

---

## Instalação

Abra um terminal e execute os blocos abaixo em ordem.

**Passo 1 — Remover versões antigas**

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

**Passo 2 — Instalar pré-requisitos**

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release
```

**Passo 3 — Adicionar a chave GPG oficial do Docker**

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

> Se você usa **Debian** (não Ubuntu), substitua `ubuntu` por `debian` na URL acima e no próximo comando.

**Passo 4 — Adicionar o repositório Docker ao apt**

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Passo 5 — Instalar o Docker Engine e o plugin Compose**

```bash
sudo apt-get update
sudo apt-get install -y \
    docker-ce docker-ce-cli containerd.io \
    docker-buildx-plugin docker-compose-plugin
```

**Passo 6 — Adicionar seu usuário ao grupo `docker`**

Sem este passo, todo comando `docker` exige `sudo`. A mudança entra em vigor após você sair e entrar novamente na sessão (ou rodar `newgrp docker` na sessão atual):

```bash
sudo usermod -aG docker $USER
```

**Passo 7 — Verificar a instalação**

```bash
docker --version
docker compose version
docker run hello-world
```

Se o último comando imprimir "Hello from Docker!", tudo está funcionando.

---

## Documentação oficial

**[https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)**

---

← Voltar ao [README](README.pt.md)
