import mcp.types as types
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn
import asyncio

from config import LOTERIA_CONFIG
from loterias import GeradorJogos
from resultados import get_resultado, obter_ultimo_concurso
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("HOST")
port = int(os.getenv("PORT"))
transport = os.getenv("TRANSPORT")

loteria = GeradorJogos(LOTERIA_CONFIG)

mcp = FastMCP("loterias",
              description="Serviço para geração de jogos de loterias e consulta de resultados.",
              host=host,
              port=port,
              debug=False)


@mcp.tool()
async def gerar_jogos_megasena(quantidade_jogos: int) -> list[types.TextContent]:
    """Gera jogos aleatórios para a Mega-Sena.

    Args:
        quantidade_jogos: Quantidade de jogos a serem gerados.
    Returns:
        Lista de jogos gerados, cada um como uma string.
    """
    jogos = loteria.gerar_jogos('mega-sena', quantidade_jogos)
    return [types.TextContent(type="text", text=str(jogos))]

@mcp.tool()
async def gerar_jogos_lotofacil(quantidade_jogos: int) -> list[types.TextContent]:
    """Gera jogos aleatórios para a Lotofácil.

    Args:
        quantidade_jogos: Quantidade de jogos a serem gerados.
    Returns:
        Lista de jogos gerados, cada um como uma string.
    """
    jogos = loteria.gerar_jogos('lotofacil', quantidade_jogos)
    return [types.TextContent(type="text", text=str(jogos))]

@mcp.tool()
async def gerar_jogos_quina(quantidade_jogos: int) -> list[types.TextContent]:
    """Gera jogos aleatórios para a Quina.

    Args:
        quantidade_jogos: Quantidade de jogos a serem gerados.
    Returns:
        Lista de jogos gerados, cada um como uma string.
    """
    jogos = loteria.gerar_jogos('quina', quantidade_jogos)
    return [types.TextContent(type="text", text=str(jogos))]

@mcp.tool()
async def gerar_jogos_lotomania(quantidade_jogos: int) -> list[types.TextContent]:
    """Gera jogos aleatórios para a Lotomania.

    Args:
        quantidade_jogos: Quantidade de jogos a serem gerados.
    Returns:
        Lista de jogos gerados, cada um como uma string.
    """
    jogos = loteria.gerar_jogos('lotomania', quantidade_jogos)
    return [types.TextContent(type="text", text=str(jogos))]


async def main():
    
    if transport == "sse":
        # Run the MCP server with sse transport
        await mcp.run_sse_async()
    else:
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())