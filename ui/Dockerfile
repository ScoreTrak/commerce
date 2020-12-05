FROM node:lts-alpine AS node-stage

WORKDIR /opt/app
RUN chown node:node /opt/app
USER node

COPY package.json yarn.lock ./
RUN yarn install

COPY babel.config.js .browserslistrc .eslintrc.js jest.config.js vue.config.js ./
COPY public public
COPY tests tests
COPY src src

CMD ["yarn", "serve"]


FROM node-stage AS builder-stage

RUN yarn run build


FROM nginx:mainline-alpine AS nginx-stage

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder-stage /opt/app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
