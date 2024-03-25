FROM node:14-alpine

# Instalando apache
RUN apk update && \
    apk add apache2 && \
    rm -rf /var/cache/apk/*
EXPOSE 80
# Criando diretórios e copiando arquivos relacionados ao Node.js
RUN mkdir -p /var/www/localhost/htdocs/img
RUN mkdir -p /var/www/localhost/htdocs/img/JS_Game_files
RUN rm /var/www/localhost/htdocs/index.html
WORKDIR /var/www/localhost/htdocs
COPY app.js index.html style.css package.json ./

# Copiando arquivos de imagem
WORKDIR /var/www/localhost/htdocs/img
COPY img/bg.png img/code.png img/ia.png img/Ruido.png ./

# Copiando arquivos do jogo JS
WORKDIR /var/www/localhost/htdocs/img/JSGame_files
COPY img/JS_Game_files/app.js img/JS_Game_files/style.css ./

# Voltando ao diretório raiz do aplicativo
WORKDIR /var/www/localhost/htdocs

# Comando para iniciar o Apache quando o contêiner for executado
CMD ["httpd", "-D", "FOREGROUND"]
