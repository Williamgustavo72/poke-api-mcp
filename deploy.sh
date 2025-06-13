#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Função para imprimir mensagens
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Criar diretórios necessários
print_message "Criando diretórios necessários..."
mkdir -p logs
mkdir -p frontend/build
mkdir -p nginx/ssl

# Construir imagens
print_message "Construindo imagens Docker..."
docker-compose build

# Parar containers existentes
print_message "Parando containers existentes..."
docker-compose down

# Iniciar containers
print_message "Iniciando containers..."
docker-compose up -d

# Verificar status dos containers
print_message "Verificando status dos containers..."
if docker-compose ps | grep -q "Up"; then
    print_message "Todos os containers estão rodando!"
else
    print_error "Alguns containers não iniciaram corretamente. Verifique os logs com 'docker-compose logs'."
    exit 1
fi

# Verificar logs
print_message "Verificando logs dos containers..."
docker-compose logs --tail=50

print_message "Deploy concluído com sucesso!"
print_message "A aplicação está disponível em:"
print_message "  - Frontend: http://localhost"
print_message "  - Backend API: http://localhost/api"
print_message "  - Health Check: http://localhost/api/health"

# Instruções para monitoramento
print_message "\nPara monitorar os containers:"
print_message "  - docker-compose ps"
print_message "  - docker-compose logs -f"
print_message "  - docker stats" 