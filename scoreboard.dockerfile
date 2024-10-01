FROM node:22-alpine AS build
WORKDIR /app
COPY scoreboard-fe/package*.json ./
RUN npm ci
COPY scoreboard-fe ./
RUN npm run build:prod

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html/scoreboard
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
