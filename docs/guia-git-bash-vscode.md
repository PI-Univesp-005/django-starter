### Configuração do Git Bash no VS Code (Windows)

Ao instalar Git no Windows, o git bash é instalado junto. Sugiro usá-lo integrado ao terminal padrão do VSCode para que possa rodar os comandos `compose` e `manage` sem grandes problemas. 

Para definir o **Git Bash** como seu terminal padrão, siga estes passos:

1. **Abra a Paleta de Comandos**: Pressione `Ctrl + Shift + P`.
2. **Selecione o Perfil**: Digite `Terminal: Select Default Profile` e tecle `Enter`.
3. **Escolha o Git Bash**: Selecione **Git Bash** na lista suspensa.

---

### Configuração Manual (via settings.json)

Caso o Git Bash não apareça na lista automática, adicione este trecho ao seu arquivo de configurações:

```json
{
    "terminal.integrated.profiles.windows": {
        "Git Bash": {
            "path": "C:\\Program Files\\Git\\bin\\bash.exe",
            "icon": "terminal-bash"
        }
    },
    "terminal.integrated.defaultProfile.windows": "Git Bash"
}
```

Esses passos resumidos acima não foram testados, então, para mais detalhes e ajuda em caso de problemas, segue essa [**referência oficial**](https://code.visualstudio.com/docs/terminal/shell-integration). 
