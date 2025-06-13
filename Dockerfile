# Usa a imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY backend/requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY backend/ .

# Expõe a porta que a aplicação usa
EXPOSE 8000

# Comando para executar a aplicação
CMD ["python", "src/server.py"] 