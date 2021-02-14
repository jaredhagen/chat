FROM node:14.15.5-alpine

WORKDIR /usr/src/app

EXPOSE 3000

COPY package.json yarn.lock ./
RUN yarn install

COPY . .

CMD ["yarn", "start"]