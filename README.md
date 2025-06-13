# Análise de Dados de Pokémon

Este projeto foi desenvolvido como parte de um desafio técnico, focando na integração com o Model Context Protocol (MCP), automação com n8n e interação via Telegram. Ele utiliza a PokeAPI para extrair dados de Pokémon, realizar análises e gerar relatórios detalhados.

## Sobre o Projeto

O projeto foi desenvolvido com foco em três componentes principais:

1. **Model Context Protocol (MCP)**: Permite uma comunicação estruturada e eficiente entre diferentes componentes do sistema.
2. **n8n**: Plataforma de automação que gerencia os fluxos de trabalho e integrações.
3. **Telegram Bot**: Interface de usuário para interação com o sistema.

## Tecnologias Utilizadas

- Python 3.11
- FastAPI
- Docker
- Model Context Protocol (MCP)
- n8n para automação
- Telegram Bot API

## Estrutura do Projeto

```
.
├── backend/           # API e lógica principal
├── n8n/              # Fluxos de trabalho e automações
├── venv/             # Ambiente virtual Python
├── docker-compose.yml
├── Dockerfile
├── deploy.sh         # Script de deploy
└── README.md
```

## Componentes Principais

### 1. n8n
O n8n é o coração da automação do projeto, gerenciando:
- Fluxos de trabalho para processamento de dados
- Integração com o Telegram
- Comunicação com o MCP
- Geração e envio de relatórios

### 2. Model Context Protocol (MCP)
O MCP é responsável por:
- Estruturação da comunicação entre componentes
- Padronização das requisições e respostas
- Integração com o agente de análise

### 3. Telegram Bot
Interface principal do usuário que permite:
- Envio de comandos em linguagem natural
- Recebimento de análises e relatórios
- Visualização de gráficos e estatísticas

## Instalação

### Pré-requisitos

- Python 3.11 ou superior
- Docker e Docker Compose
- Node.js (para o MCP Inspector)
- Conta no Telegram
- Acesso à internet para usar a PokeAPI

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone [URL_DO_REPOSITÓRIO]
   cd pokemon
   ```

2. **Configure o ambiente Python**
   ```bash
   # Crie e ative o ambiente virtual
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   .\venv\Scripts\activate  # Windows

   # Instale as dependências
   pip install -r backend/requirements.txt
   ```

3. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   ```
3. Inicie os serviços usando Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Uso

1. **Via Telegram**:
   - Inicie uma conversa com o bot
   - Envie comandos como:
     - "Gere um relatório dos 10 Pokémon mais fortes"
     - "Mostre a distribuição de tipos"
     - "Quais são os Pokémon com mais experiência?"

2. **Via n8n**:
   - Acesse a interface do n8n em `http://localhost:5678`
   - Gerencie os fluxos de trabalho
   - Monitore as automações

3. **Via MCP**:
   - Utilize o MCP Inspector para testar as integrações
   - Configure o servidor MCP conforme necessário

## Solução de Problemas

1. **Serviços não iniciam**:
   - Verifique os logs: `docker-compose logs`
   - Confirme se as portas necessárias estão disponíveis

2. **n8n não responde**:
   - Verifique se o container está rodando
   - Confirme as credenciais de acesso

3. **Bot do Telegram não funciona**:
   - Verifique se o token do bot está configurado
   - Confirme se o webhook está ativo

4. **MCP com problemas**:
   - Verifique a conexão com o servidor
   - Confirme as configurações do SSE

## Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Envie um pull request

## Licença

Este projeto está sob a licença MIT.

### MCP Inspector

O MCP Inspector é uma ferramenta visual para testar e depurar servidores MCP. Para usar:

1. **Instalação**:
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

2. **Iniciar o Inspector**:
   ```bash
   mcp-inspector
   ```

3. **Configurar o Servidor**:
   - Abra o Inspector em `http://localhost:6274`
   - No painel lateral, configure o servidor MCP:
     - URL: `http://localhost:8000/sse`
     - Tipo de Transporte: SSE

4. **Testar as Ferramentas**:
   - No painel de ferramentas, você verá as três ferramentas disponíveis:
     - `extrair_dados_pokemon`
     - `gerar_analise`
     - `gerar_relatorio_csv`
   - Selecione uma ferramenta e configure seus parâmetros
   - Clique em "Execute" para testar

5. **Visualizar Resultados**:
   - As respostas serão exibidas em formato JSON
   - Você pode ver o histórico de requisições
   - Os erros são exibidos de forma clara

6. **Configurações Avançadas**:
   - Timeout: 10000ms (padrão)
   - Reset de timeout em progresso: true
   - Timeout máximo total: 60000ms

Para mais detalhes sobre o MCP Inspector, consulte a [documentação oficial](https://github.com/modelcontextprotocol/inspector).

### Automação com n8n

O projeto inclui dois fluxos de trabalho em n8n:

1. **Fluxo de Recebimento e Envio de Mensagens** (`n8n/telegram-flow.json`)
   - Gerencia a comunicação via Telegram
   - Processa mensagens recebidas
   - Envia relatórios e arquivos gerados

2. **Agente MCP** (`n8n/agent-flow.json`)
   - Implementa um agente especializado em análise de dados de Pokémon
   - Utiliza o MCP para processar requisições
   - Gera respostas estruturadas

### Bot do Telegram

O projeto inclui um bot do Telegram (`@apiPokemon_bot`) que serve como interface em linguagem natural. Para usar:

1. Inicie uma conversa com `@apiPokemon_bot`
2. Envie mensagens como:
   - "Gere um relatório dos 10 Pokémon mais fortes"
   - "Mostre a distribuição de tipos"
   - "Quais são os Pokémon com mais experiência?"

O bot processará sua solicitação e enviará:
- Uma mensagem com a análise
- Arquivos CSV com dados detalhados
- Um gráfico de distribuição de tipos

## Ferramentas Disponíveis

### 1. extrair_dados_pokemon
**Descrição**: Extrai dados básicos dos Pokémon da PokeAPI.

**Parâmetros**:
- `limit` (opcional): Número máximo de Pokémon a serem extraídos (padrão: 100)

**Retorno**:
```json
{
  "success": true,
  "data": [
    {
      "name": "bulbasaur",
      "types": ["grass", "poison"],
      "stats": {
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "special-attack": 65,
        "special-defense": 65,
        "speed": 45
      },
      "base_experience": 64
    }
  ]
}
```

### 2. gerar_analise
**Descrição**: Realiza uma análise completa dos dados dos Pokémon.

**Parâmetros**:
- `limit` (opcional): Número máximo de Pokémon a serem analisados (padrão: 100)

**Retorno**:
```json
{
  "success": true,
  "analise": {
    "categorias": {
      "fortes": ["mewtwo", "rayquaza"],
      "medios": ["charizard", "blastoise"],
      "fracos": ["caterpie", "weedle"]
    },
    "estatisticas_tipos": {
      "fire": 12,
      "water": 15,
      "grass": 14
    },
    "top_experiencia": [
      {"name": "mewtwo", "base_experience": 340},
      {"name": "rayquaza", "base_experience": 340}
    ]
  }
}
```

### 3. gerar_relatorio_csv
**Descrição**: Gera relatórios detalhados em CSV e um gráfico de distribuição de tipos.

**Parâmetros**:
- `limit` (opcional): Número máximo de Pokémon a serem analisados (padrão: 100)

**Retorno**:
```json
{
  "success": true,
  "arquivos": {
    "tipos": "relatorios/analise_tipos.csv",
    "top": "relatorios/top_experiencia.csv",
    "grafico": "relatorios/distribuicao_tipos.png"
  }
}
```

**Arquivos Gerados**:
- `analise_tipos.csv`: Estatísticas por tipo de Pokémon
- `top_experiencia.csv`: Ranking dos Pokémon por experiência base
- `distribuicao_tipos.png`: Gráfico de distribuição de tipos

