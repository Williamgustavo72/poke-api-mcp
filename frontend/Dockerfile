# ---- Estágio 1: Imagem Base ----
# Usar imagem oficial do Nginx baseada no Alpine Linux (leve e segura)
# Usar tag específica como 'stable-alpine' é melhor que 'latest' para consistência
FROM nginx:stable-alpine

# ---- Copiando os Arquivos do Site ----
# Limpa o diretório padrão do Nginx para garantir que só os seus arquivos estejam lá
RUN rm -rf /usr/share/nginx/html/*

# Copia TODO o conteúdo do diretório atual (o contexto de build, ou seja, 'pasta_raiz')
# para o diretório raiz do servidor Nginx dentro do container.
# Isso vai copiar 'index.html', 'favicon.ico' e a pasta 'assets' com todo seu conteúdo.
COPY . /usr/share/nginx/html/

# ---- Expondo a Porta ----
# Informa que o container vai escutar na porta 80 (HTTP padrão)
EXPOSE 8090

# ---- Comando de Execução ----
# O comando padrão da imagem base 'nginx:stable-alpine' já é iniciar o Nginx
# em primeiro plano ('nginx -g "daemon off;"'), então não precisamos especificar um CMD.