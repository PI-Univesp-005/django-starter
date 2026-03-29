# Instalando o Docker no Windows

No Windows, o Docker roda através do **Docker Desktop** — um aplicativo que inclui o Docker Engine, o Docker Compose e um painel gráfico. Ele usa o **WSL 2** (Windows Subsystem for Linux 2) como backend, que é mais rápido, usa menos memória e é o padrão para instalações modernas.

---

## Requisitos do sistema

- Windows 10 versão 21H2 ou mais recente, ou Windows 11 (qualquer edição)
- Processador 64-bit com virtualização de hardware habilitada na BIOS (ativada por padrão na maioria dos computadores modernos)
- Pelo menos 4 GB de RAM (8 GB ou mais é fortemente recomendado)

---

## Passo 1 — Habilitar o WSL 2

Abra o **PowerShell como Administrador** (clique com o botão direito no menu Iniciar → "Windows PowerShell (Admin)") e execute:

```powershell
wsl --install
```

Isso instala o WSL 2 e o Ubuntu por padrão. Reinicie o computador quando solicitado.

Para verificar que está na versão 2:

```powershell
wsl --set-default-version 2
wsl --list --verbose
```

A coluna `VERSION` deve mostrar `2` ao lado da sua distribuição Linux.

---

## Passo 2 — Baixar e instalar o Docker Desktop

Acesse a página oficial e baixe o instalador para Windows:

**[https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/)**

Execute o arquivo `Docker Desktop Installer.exe`. Na instalação, certifique-se de que **"Use WSL 2 instead of Hyper-V"** está marcado (deve estar por padrão). Reinicie o computador se solicitado.

---

## Passo 3 — Verificar a instalação

Abra o PowerShell ou o Prompt de Comando e execute:

```powershell
docker --version
docker compose version
docker run hello-world
```

Se o último comando imprimir "Hello from Docker!", tudo está funcionando.

---

## Atenção: quebras de linha em scripts shell

Se o Git estiver configurado para converter quebras de linha (padrão no Windows), o script `entrypoint.sh` pode receber quebras de linha no estilo Windows (CRLF), causando erros dentro do container Linux como `\r: command not found`.

Este projeto inclui um arquivo `.gitattributes` que força quebras de linha Unix (LF) para scripts shell, independentemente da configuração do Git de cada contribuidor. Nenhuma ação manual é necessária.

---

## Documentação oficial

**[https://docs.docker.com/desktop/install/windows-install/](https://docs.docker.com/desktop/install/windows-install/)**

---

← Voltar ao [README](README.pt.md)
