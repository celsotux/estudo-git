FROM node:14-alpine

# Instalando apache
RUN apk update && \
    apk add apache2 && \
    rm -rf /var/cache/apk/*

# Alterando hostname
ENV HOSTNAME=hit-game-app
RUN echo "Hostname atual: $(hostname)" && \
    echo "HOSTNAME" > /etc/hostname && \
    echo "Novo hostname definido: $(cat /etc/hostname)"

# Expor a porta 80
EXPOSE 80

# Criar diretórios e copiar arquivos relacionados ao Node.js
RUN mkdir -p /var/www/localhost/htdocs/img
RUN mkdir -p /var/www/localhost/htdocs/img/JS_Game_files
WORKDIR /var/www/localhost/htdocs
COPY app.js index.html style.css package.json ./

# Copiar arquivos de imagem
WORKDIR /var/www/localhost/htdocs/img
COPY img/bg.png img/code.png img/ia.png img/Ruido.png ./

# Copiar arquivos do jogo JS
WORKDIR /var/www/localhost/htdocs/img/JSGame_files
COPY img/JS_Game_files/app.js img/JS_Game_files/style.css ./

# Voltar ao diretório raiz do aplicativo
WORKDIR /var/www/localhost/htdocs

# Copiar o arquivo de health check
COPY healthcheck.html /var/www/localhost/htdocs/

# Configurar o Apache para responder ao caminho /healthcheck
RUN echo "Alias /healthcheck /var/www/localhost/htdocs/healthcheck.html" >> /etc/apache2/httpd.conf

# Comando para iniciar o Apache quando o contêiner for executado
CMD ["httpd", "-D", "FOREGROUND"]
