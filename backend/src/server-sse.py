import mcp.types as types
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn

from config import LOTERIA_CONFIG
from loterias import GeradorJogos
from resultados import get_resultado, obter_ultimo_concurso
loteria = GeradorJogos(LOTERIA_CONFIG)

mcp = FastMCP("Loterias")


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
async def resultado_megasena(concurso: int) -> list[types.TextContent]:
    """Obtém o resultado de um concurso da Mega-Sena.

    Args:
        concurso: Número do concurso desejado.
    Returns:
        Resultado do concurso, incluindo dezenas sorteadas.
    """
    resultado = get_resultado("mega-sena", concurso)
    return [types.TextContent(type="text", text=str(resultado))]

@mcp.tool()
async def resultado_lotofacil(concurso: int) -> list[types.TextContent]:
    """Obtém o resultado de um concurso da Lotofácil.

    Args:
        concurso: Número do concurso desejado.
    Returns:
        Resultado do concurso, incluindo dezenas sorteadas.
    """
    resultado = get_resultado("lotofacil", concurso)
    return [types.TextContent(type="text", text=str(resultado))]

@mcp.tool()
async def obter_ultimo_concurso_loteria(loteria: str) -> list[types.TextContent]:
    """Obtém informações do último concurso de uma loteria específica.

    Args:
        loteria: Nome da loteria (ex: 'mega-sena', 'lotofacil', 'quina', etc).
    Returns:
        Dicionário com número do concurso, data de apuração, dezenas sorteadas e se houve ganhadores.
    """
    resultado = obter_ultimo_concurso(loteria)
    return [types.TextContent(type="text", text=str(resultado))]

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


if __name__ == "__main__":
    mcp_server = mcp._mcp_server 

    starlette_app = create_starlette_app(mcp_server, debug=False)

    uvicorn.run(starlette_app, host="0.0.0.0", port=8950)