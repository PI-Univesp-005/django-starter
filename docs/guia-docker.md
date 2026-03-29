# Docker — Guia Rápido de Operação

Um guia de referência para operar este projeto no dia a dia. Os comandos estão organizados por intenção, não por sintaxe — a ideia é que você encontre o que precisa pelo que quer fazer, não pelo comando que já conhece.

Para instalar, siga cada documentação feita por OS:
- 🐧 [Linux](docs/linux-docker-install.md)
- 🪟 [Windows](docs/windows-docker-install.md)
- 🍎 [MacOS](docs/macOS-docker-install.md)

---

## Regra de ouro deste projeto

Sempre que usar um profile para subir, use o mesmo profile para descer. O Docker Compose só gerencia os serviços que enxerga, sem o profile, os containers e volumes daquele serviço são invisíveis para o comando `down`.

```bash
# ✅ correto — o mesmo profile em ambos
docker compose --profile postgres up
docker compose --profile postgres down -v

# ❌ errado — o volume do postgres sobrevive silenciosamente
docker compose --profile postgres up
docker compose down -v
```

---

## Subindo e descendo serviços

Para SQLite, nenhum profile é necessário. O flag `--build` reconstrói a imagem se o `Dockerfile` ou `requirements.txt` mudaram. É seguro usá-lo sempre, pois o Docker usa o cache quando nada mudou.

```bash
# SQLite (padrão)
docker compose up --build
docker compose down -v

# PostgreSQL
docker compose --profile postgres up --build
docker compose --profile postgres down -v

# MySQL
docker compose --profile mysql up --build
docker compose --profile mysql down -v
```

O flag `-v` apaga todos os volumes nomeados associados aos serviços visíveis naquela invocação. Use-o sempre que trocar de banco ou quando uma migration mudou e o banco precisa ser recriado do zero. Omita-o quando quiser apenas parar os containers preservando os dados.

Para rodar em background (modo detached), adicione `-d`. Os logs deixam de aparecer no terminal, mas continuam acessíveis via `docker compose logs`:

```bash
docker compose --profile postgres up --build -d
```

---

## Acompanhando logs

Sem nenhuma flag, `logs` imprime todo o histórico e sai. As flags mais úteis são `-f` (follow — fica escutando novos logs em tempo real, equivalente ao `tail -f`) e `--tail` (limita quantas linhas do passado são mostradas antes de começar o follow).

```bash
# todos os serviços, tempo real
docker compose logs -f

# só o serviço web, últimas 50 linhas, tempo real
docker compose logs -f --tail 50 web

# só o postgres, sem follow — útil para inspecionar o init.sql
docker compose --profile postgres logs db
```

Para timestamps em cada linha, adicione `-t`:

```bash
docker compose logs -f -t web
```

---

## Abrindo um shell dentro de um container

`exec` roda um comando dentro de um container que já está em execução. O comando mais útil é `bash`, que abre um shell interativo — a partir daí você está dentro do container como se fosse uma máquina Linux normal.

```bash
# shell no container web
docker compose exec web bash

# shell no container postgres (útil para rodar psql diretamente)
docker compose --profile postgres exec postgres bash

# shell no container mysql
docker compose --profile mysql exec mysql bash
```

Dentro do container do postgres, você pode abrir o cliente SQL diretamente:

```bash
psql -U django_user -d django_db
```

E dentro do mysql:

```bash
mysql -u django_user -p django_db
```

Para rodar um comando único sem abrir um shell interativo, passe o comando diretamente:

```bash
# rodar as migrations manualmente de dentro do container
docker compose exec web python scripts/manage.py migrate

# abrir o Django shell (REPL Python com o ORM carregado)
docker compose exec web python scripts/manage.py shell

# checar migrations pendentes sem aplicar
docker compose exec web python scripts/manage.py migrate --check
```

---

## Inspecionando o estado do ambiente

Estes comandos respondem à pergunta "o que está rodando agora?".

```bash
# containers em execução (ps = process status)
docker compose ps

# todos os containers do sistema, incluindo os parados
docker ps -a

# volumes nomeados existentes no sistema
docker volume ls

# inspecionar um volume específico (mostra onde está no disco, tamanho, etc.)
docker volume inspect django-proj_postgres_data

# redes Docker existentes
docker network ls

# inspecionar a rede deste projeto (mostra quais containers estão conectados)
docker network inspect django-proj_default
```

Os nomes de volumes e redes seguem o padrão `<nome-do-diretório-do-projeto>_<nome-definido-no-compose>`. Se seu diretório se chama `django-proj`, o volume `postgres_data` vira `django-proj_postgres_data`.

---

## Limpeza

Docker acumula imagens, containers parados e volumes órfãos ao longo do tempo. Os comandos abaixo são seguros para rodar periodicamente.

```bash
# remove containers parados, redes não usadas, imagens sem tag e cache de build
# é o comando de limpeza geral mais seguro — não apaga volumes
docker system prune

# a versão mais agressiva — inclui volumes não associados a nenhum container
# CUIDADO: apaga dados persistidos em volumes órfãos
docker system prune --volumes

# remover um volume específico manualmente (o container precisa estar parado)
docker volume rm django-proj_postgres_data

# remover todos os volumes do projeto de uma vez
docker compose --profile postgres down -v
```

---

## Reconstruindo sem cache

Quando uma dependência do sistema muda no `Dockerfile` (como adicionar uma nova biblioteca ao `apt-get`), o Docker pode usar uma camada cacheada e não reinstalar nada. Para forçar uma reconstrução completa a partir do zero:

```bash
docker compose --profile postgres up --build --no-cache
```

Use com moderação — `--no-cache` baixa e reinstala tudo, o que pode levar vários minutos.

---

## Copiando arquivos entre o container e o host

O comando `cp` do Compose funciona nos dois sentidos. É a forma correta de extrair o arquivo SQLite do container, por exemplo:

```bash
# container → host (extrair o banco SQLite)
docker compose cp web:/app/db_sqlite/db.sqlite3 ./docker/sqlite/db.sqlite3

# host → container (injetar um arquivo de fixture, por exemplo)
docker compose cp ./fixture.json web:/app/src/fixture.json
```

---

## Parando containers de forma segura

`stop` envia um sinal `SIGTERM` para o processo principal (PID 1) do container e aguarda até 10 segundos para ele encerrar graciosamente antes de forçar com `SIGKILL`. É a forma correta de parar — equivalente ao `Ctrl+C` quando os logs estão abertos no terminal.

```bash
# parar todos os serviços visíveis (sem remover containers ou volumes)
docker compose stop

# parar só o web
docker compose stop web

# forçar a parada imediata sem esperar (use só se stop não responder)
docker compose kill web
```

`kill` deve ser o último recurso — ele não dá chance ao processo de fechar conexões de banco de dados ou terminar operações em andamento.

---

## Referência de flags mais usadas

| Flag | Contexto | Efeito |
|---|---|---|
| `--build` | `up` | Reconstrói as imagens antes de subir |
| `--no-cache` | `up --build` | Ignora o cache do Docker na reconstrução |
| `-d` | `up` | Roda em background (detached) |
| `-v` | `down` | Remove volumes nomeados junto com os containers |
| `-f` | `logs` | Segue os logs em tempo real |
| `--tail N` | `logs` | Mostra só as últimas N linhas antes de seguir |
| `-t` | `logs` | Adiciona timestamps em cada linha |
| `--profile X` | qualquer | Inclui os serviços do profile X na operação |

---

← Voltar ao [README](../README.md)