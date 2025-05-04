FROM python:3.13-slim

# Instala o uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copia arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instala as dependências no .venv
RUN uv sync --frozen --no-cache

# Copia o código da aplicação
COPY src ./src

EXPOSE 8950

WORKDIR /app/src

# Comando para rodar o servidor
CMD ["uv", "run", "server-sse.py"] 