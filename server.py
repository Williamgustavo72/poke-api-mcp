import anyio
import click
import mcp.types as types
from mcp.server.lowlevel import Server
from app import GeradorLoteria, TipoLoteria
from loteria_api import get_resultado

# Instancia o gerador de loteria
loteria = GeradorLoteria()

def gerar_jogos_megasena_tool(args: dict):
    quantidade_jogos = args.get("quantidade_jogos")
    jogos = loteria.gerar_jogos(TipoLoteria.MEGASENA, quantidade_jogos)
    return [types.TextContent(type="text", text=str(jogos))]

def gerar_jogos_lotofacil_tool(args: dict):
    quantidade_jogos = args.get("quantidade_jogos")
    jogos = loteria.gerar_jogos(TipoLoteria.LOTOFACIL, quantidade_jogos)
    return [types.TextContent(type="text", text=str(jogos))]

def resultado_megasena_tool(args: dict):
    concurso = args.get("concurso")
    resultado = get_resultado("mega-sena", concurso)
    return [types.TextContent(type="text", text=str(resultado))]

def resultado_lotofacil_tool(args: dict):
    concurso = args.get("concurso")
    resultado = get_resultado("lotofacil", concurso)
    return [types.TextContent(type="text", text=str(resultado))]

@click.command()
@click.option("--port", default=8050, help="Porta para escutar SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Tipo de transporte",
)
def main(port: int, transport: str) -> int:
    """
    Servidor MCP para geração de jogos de Mega-Sena e Lotofácil.
    """
    app = Server("mcp-loterias")

    @app.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "gera_jogos_megasena":
            return gerar_jogos_megasena_tool(arguments)
        elif name == "gera_jogos_lotofacil":
            return gerar_jogos_lotofacil_tool(arguments)
        elif name == "resultado_megasena":
            return resultado_megasena_tool(arguments)
        elif name == "resultado_lotofacil":
            return resultado_lotofacil_tool(arguments)
        else:
            raise ValueError(f"Ferramenta desconhecida: {name}")

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="gera_jogos_megasena",
                description="Gera jogos para a Mega-Sena.",
                inputSchema={
                    "type": "object",
                    "required": ["quantidade_jogos"],
                    "properties": {
                        "quantidade_jogos": {
                            "type": "integer",
                            "description": "Quantidade de jogos a gerar da Megasena"
                        }
                    },
                },
            ),
            types.Tool(
                name="gera_jogos_lotofacil",
                description="Gera jogos para a Lotofácil.",
                inputSchema={
                    "type": "object",
                    "required": ["quantidade_jogos"],
                    "properties": {
                        "quantidade_jogos": {
                            "type": "integer",
                            "description": "Quantidade de jogos a gerar da Lotofácil"
                        }
                    },
                },
            ),
            types.Tool(
                name="resultado_megasena",
                description="Retorna o resultado de um concurso da Mega-Sena.",
                inputSchema={
                    "type": "object",
                    "required": ["concurso"],
                    "properties": {
                        "concurso": {
                            "type": "integer",
                            "description": "Número do concurso da Mega-Sena"
                        }
                    },
                },
            ),
            types.Tool(
                name="resultado_lotofacil",
                description="Retorna o resultado de um concurso da Lotofácil.",
                inputSchema={
                    "type": "object",
                    "required": ["concurso"],
                    "properties": {
                        "concurso": {
                            "type": "integer",
                            "description": "Número do concurso da Lotofácil"
                        }
                    },
                },
            ),
        ]

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.responses import Response
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )
            return Response()

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse, methods=["GET"]),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0

if __name__ == "__main__":
    main() 