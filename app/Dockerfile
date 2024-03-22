FROM node:14-alpine
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/img
RUN mkdir -p /usr/src/app/img/JS\ Game_files
WORKDIR /usr/src/app
COPY app.js index.html style.css ./
WORKDIR /usr/src/app/img
COPY bg.png code.png ia.png JS\ Game.html Ruido.png ./
WORKDIR /usr/src/app/img/JS\ Game_files
COPY app.js style.css ./
RUN npm install --production
EXPOSE 3000
CMD ["npm", "start"]