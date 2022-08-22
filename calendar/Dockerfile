FROM node:18-alpine3.15

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

COPY . .

EXPOSE 4000
CMD [ "npm", "run", "prod" ]