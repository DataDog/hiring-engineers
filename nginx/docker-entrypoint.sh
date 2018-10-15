#!/bin/sh

ConfigureNginx () {
  echo "Configure Nginx Started"
  # Configure NGINX properties
  if [ -n "${NGINX_HOST}" ];then
    if [ -n "${NGINX_PORT}" ]; then
      if [ -n "${APP_HOST}" ]; then
        if [ -n "${APP_PORT}" ]; then
          echo $NGINX_HOST
          envsubst '$$NGINX_HOST$$NGINX_PORT$$APP_HOST$$APP_PORT' < /etc/nginx/conf.d/mysite.template > /etc/nginx/conf.d/default.conf 
          envsubst '$$NGINX_HOST' < /etc/nginx/conf.d/status.template > /etc/nginx/conf.d/status.conf
          cat  /etc/nginx/conf.d/default.conf
          cat  /etc/nginx/conf.d/status.conf
        else
          /bin/echo "ERROR: application port is missing, please define APP_PORT environment variable."
        fi
      else
        /bin/echo "ERROR: application hostname is missing, please define APP_HOST environment variable."
      fi
    else
      /bin/echo "ERROR: nginx port is missing, please define NGINX_PORT environment variable."
    fi
  else
    /bin/echo "ERROR: nginx hostname is missing, please define NGINX_HOST environment variable."
  fi
}

ConfigureNginx

if [ "$1" = 'nginx' ]; then
  nginx -g 'daemon off;'
fi

exec "$@"
