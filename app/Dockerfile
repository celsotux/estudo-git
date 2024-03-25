FROM node:14-alpine
RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/img
RUN mkdir -p /usr/src/app/img/JSGame_files
WORKDIR /usr/src/app
COPY app-server.js client.js index.html style.css package.json ./
WORKDIR /usr/src/app/img
COPY img/bg.png img/code.png img/ia.png img/Ruido.png ./img/
WORKDIR /usr/src/app/img/JSGame_files
COPY img/JSGame_files/app.js img/JSGame_files/style.css ./img/JSGame_files/
WORKDIR /usr/src/app
RUN npm install --production
EXPOSE 3000
CMD ["npm", "start"]
