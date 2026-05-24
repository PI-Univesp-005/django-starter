# Estoque + Validade

Para encontrar o documentando antigo com os guias e resumos de como rodar e configurar o ambiente, [**clique aqui**](docs/indice_guias.md). Esse espaço ficará para documentar atualiações sobre a aplicação.
____

## Registro de mudanças <sub>(_changelog_)</sub>
<sup>Comentários sobre commits para adicionar contexto às mudanças.</sup>

### <sup style="font-size:9pt;">`(ddd9721: 'chore' em 22/05)`</sup> Usuários criados via fixtures

Deste commit em diante, ao rodar pela primeira vez o projeto, já existirão os seguintes usuários na aplicação Django:

* **Gerente**
  * Usuário: `gerente_teste`
  * Senha: `Senha_1234`
* **Líder**
  * Usuário: `funcionario_lider_teste`
  * Senha: `Senha_1234`
* **Funcionário**
  * Usuário: `funcionario_teste`
  * Senha: `Senha_1234`

_PS: Fixtures (dados pré carregados no banco) toda vez que são rodadas sobrescrevem os registros. Por isso coloquei para rodar só quando os volumes do banco forem derrubados (banco completamente zerado). Assim se em um teste local for necessário editar esses usuários, essas mudanças persistirão e não serão resetadas para o valor dos exemplos em `fixtures/initial_data.json` até que os dados do banco sejam apagados._

___