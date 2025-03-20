FROM node:20-alpine as base
RUN apk add --no-cache g++ make py3-pip libc6-compat
WORKDIR /app
COPY package*.json ./

FROM base as dev
ENV NODE_ENV=development
RUN npm install 
COPY . .
CMD npm run dev