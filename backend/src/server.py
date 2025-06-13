import mcp.types as types
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import json
import base64
import pandas as pd
from dotenv import load_dotenv

from controllers.data_extractor import DataExtractor
from controllers.transformer import DataTransformer
from controllers.reporter import ReportGenerator

load_dotenv()

# Configurações do servidor
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))
transport = os.getenv("TRANSPORT", "sse")

# Inicializa controladores
extractor = DataExtractor()
transformer = DataTransformer()
reporter = ReportGenerator()

# Inicializa FastAPI
app = FastAPI()

# Caminho base para os relatórios
REPORTS_BASE_DIR = os.path.join("relatorios")

def _file_to_base64(file_path: str) -> str:
    """Converte um arquivo para base64."""
    try:
        with open(file_path, 'rb') as file:
            return base64.b64encode(file.read()).decode('utf-8')
    except Exception as e:
        return ""

def _csv_to_json(csv_path: str) -> list:
    """Converte um arquivo CSV para formato JSON."""
    try:
        df = pd.read_csv(csv_path)
        return df.to_dict(orient='records')
    except Exception as e:
        return []

# Endpoint HTTP para obter arquivo em base64
@app.get("/api/file/{file_path:path}")
async def get_file_base64(file_path: str):
    """Endpoint para obter arquivo em base64.
    
    Args:
        file_path: Caminho relativo do arquivo dentro da pasta relatorios
    """
    # Garante que o arquivo está dentro da pasta relatorios
    full_path = os.path.join(REPORTS_BASE_DIR, file_path)
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    # Verifica se o arquivo está dentro da pasta relatorios
    if not os.path.abspath(full_path).startswith(os.path.abspath(REPORTS_BASE_DIR)):
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    base64_data = _file_to_base64(full_path)
    if not base64_data:
        raise HTTPException(status_code=500, detail="Erro ao ler arquivo")
    
    return JSONResponse({
        "status": "success",
        "file": base64_data
    })

# Configura o MCP
mcp = FastMCP(
    "pokemon-analysis",
    description="API para análise de dados de Pokémon usando a PokeAPI. Extrai dados, gera análises estatísticas e relatórios em CSV.",
    host=host,
    port=port,
    debug=False
)

# Configura o transporte SSE
sse_transport = SseServerTransport(endpoint="/sse")

@mcp.tool()
async def extrair_dados_pokemon(limit: int = 100) -> list[types.TextContent]:
    """Extrai dados básicos dos Pokémon da PokeAPI.
    
    Retorna uma lista de Pokémon com seus atributos principais:
    - Nome
    - Tipos
    - Estatísticas (HP, Ataque, Defesa)
    - Experiência base
    
    Args:
        limit: Número máximo de Pokémon para extrair (padrão: 100)
    """
    result = await extractor.extract(limit=limit)
    return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

@mcp.tool()
async def gerar_analise(limit: int = 100) -> list[types.TextContent]:
    """Gera uma análise completa dos Pokémon.
    
    A análise inclui:
    1. Categorização por força:
       - Fraco: Experiência < 50
       - Médio: Experiência entre 50 e 100
       - Forte: Experiência > 100
    
    2. Estatísticas por tipo:
       - Média de ataque
       - Média de defesa
       - Média de HP
       - Quantidade de Pokémon
    
    3. Top 5 Pokémon por experiência base
    
    Args:
        limit: Número máximo de Pokémon para analisar (padrão: 100)
    """
    # Extrai dados
    pokemon_data = await extractor.extract(limit=limit)
    
    if pokemon_data["status"] == "error":
        return [types.TextContent(type="text", text=json.dumps(pokemon_data, ensure_ascii=False, indent=2))]
    
    # Transforma dados
    analise = await transformer.transform(pokemon_data["data"])
    
    # Gera relatório (apenas para salvar os arquivos)
    await reporter.generate(analise)
    
    result = {
        "status": "success",
        "pokemon_data": pokemon_data,
        "analise": analise
    }
    
    return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

@mcp.tool()
async def gerar_relatorio_csv(limit: int = 100) -> list[types.TextContent]:
    """Gera relatórios em CSV com análises detalhadas.
    
    Gera dois arquivos CSV:
    1. analise_tipos.csv:
       - Estatísticas médias por tipo
       - Quantidade de Pokémon por tipo
    
    2. top_experiencia.csv:
       - Top 5 Pokémon por experiência
       - Atributos detalhados
    
    Retorna apenas os nomes dos arquivos gerados.
    
    Args:
        limit: Número máximo de Pokémon para incluir (padrão: 100)
    """
    pokemon_data = await extractor.extract(limit=limit)
    
    if pokemon_data["status"] == "error":
        return [types.TextContent(type="text", text=json.dumps(pokemon_data, ensure_ascii=False, indent=2))]
    
    analise = await transformer.transform(pokemon_data["data"])
    relatorio = await reporter.generate(analise)
    
    # Extrai apenas os nomes dos arquivos dos caminhos completos
    result = {
        "status": "success",
        "arquivos": {
            "tipos": os.path.basename(relatorio["csv_path"]["tipos"]),
            "top": os.path.basename(relatorio["csv_path"]["top"]),
            "grafico": os.path.basename(relatorio["graficos_path"])
        }
    }
    
    return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]

async def main():
    if transport == "sse":
        await mcp.run_sse_async()
    else:
        await mcp.run_stdio_async()

if __name__ == "__main__":
    import asyncio
    import uvicorn
    
    # Inicia o servidor FastAPI em uma thread separada
    import threading
    def run_fastapi():
        uvicorn.run(app, host=host, port=port + 1)
    
    threading.Thread(target=run_fastapi, daemon=True).start()
    
    # Inicia o servidor MCP
    asyncio.run(main())