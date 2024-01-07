FROM nginx:1.21.6-alpine

COPY config/default.conf /etc/nginx/conf.d/default.conf
COPY config/nginx.conf /etc/nginx/nginx.conf

EXPOSE 9200
USER 101:101
