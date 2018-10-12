FROM nginx:mainline-alpine

##Set docker build args 
ARG NGINX_HOST
ARG NGINX_PORT
ARG APP_HOST
ARG APP_PORT

##Associate args with container os envs
ENV NGINX_HOST=$NGINX_HOST \
    NGINX_PORT=$NGINX_PORT \
    APP_HOST=$APP_HOST \
    APP_PORT=$APP_PORT

##Copy Static Files
RUN set -x && mkdir -p /usr/share/nginx/static
COPY ../project/testweb/static /usr/share/nginx/static

##Copy custom config templates
COPY nginx/mysite.template /etc/nginx/conf.d/mysite.template

##Transform templates into real ones with envs
RUN set -x && \
    echo ${NGINX_HOST} && \
    echo ${APP_HOST} && \
    envsubst '$$NGINX_HOST$$NGINX_PORT$$APP_HOST$$APP_PORT' < /etc/nginx/conf.d/mysite.template > /etc/nginx/conf.d/default.conf && \
    cat /etc/nginx/conf.d/default.conf

##Copy Nginx root conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

STOPSIGNAL SIGTERM

### Start Nginx
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx"]
